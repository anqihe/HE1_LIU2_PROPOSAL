import InputData as D
import SimPy.EconEval as Econ
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
import SimPy.Statistics as Stat


def print_outcomes(multi_cohort_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and prediction interval of patient survival time
    survival_mean_PI_text = multi_cohort_outcomes.statMeanSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and prediction interval text of time to AIDS
    time_of_covid_PI_text = multi_cohort_outcomes.statMeanNumCOVID\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total QALY
    utility_mean_PI_text = multi_cohort_outcomes.statMeanQALY\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_PI_text)
    print("  Estimate of mean times of COVID and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          time_of_covid_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_PI_text)
    print("  Estimate of mean discounted utility and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          utility_mean_PI_text)
    print("")


def plot_survival_curves_and_histograms(multi_cohort_outcomes_without, multi_cohort_outcomes_with):
    """ plot the survival curves and the histograms of survival times
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    sets_of_survival_curves = [
        multi_cohort_outcomes_without.survivalCurves,
        multi_cohort_outcomes_with.survivalCurves
    ]

    # graph survival curve
    Path.plot_sets_of_sample_paths(
        sets_of_sample_paths=sets_of_survival_curves,
        title='Survival Curves',
        x_label='Simulation Time Step (year)',
        y_label='Number of Patients Alive',
        legends=['Without Vaccine', 'With Vaccine'],
        transparency=0.4,
        color_codes=['green', 'blue']
    )

    # histograms of survival times
    set_of_survival_times = [
        multi_cohort_outcomes_without.meanSurvivalTimes,
        multi_cohort_outcomes_with.meanSurvivalTimes
    ]

    # graph histograms
    Hist.plot_histograms(
        data_sets=set_of_survival_times,
        title='Histograms of Average Patient Survival Time',
        x_label='Survival Time (year)',
        y_label='Counts',
        bin_width=0.25,
        #x_range=[18, 28],
        legends=['Without Vaccine', 'With Vaccine'],
        color_codes=['green', 'blue'],
        transparency=0.5
    )


def print_comparative_outcomes(multi_cohort_outcomes_without, multi_cohort_outcomes_with):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_mean_survival_time = Stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_with.meanSurvivalTimes,
        y_ref=multi_cohort_outcomes_without.meanSurvivalTimes)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean survival time and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted cost under combination therapy with respect to non vax
    increase_mean_discounted_cost = Stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_with.meanCosts,
        y_ref=multi_cohort_outcomes_without.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2,
                                                                                form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted QALY under combination therapy with respect to mono therapy
    increase_mean_discounted_qaly = Stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_cohort_outcomes_with.meanQALYs,
        y_ref=multi_cohort_outcomes_without.meanQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)


def report_CEA_CBA(multi_cohort_outcomes_without, multi_cohort_outcomes_with):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # define two strategies
    without_therapy_strategy = Econ.Strategy(
        name='Without Vaccine',
        cost_obs=multi_cohort_outcomes_without.meanCosts,
        effect_obs=multi_cohort_outcomes_without.meanQALYs,
        color='green'
    )
    with_therapy_strategy = Econ.Strategy(
        name='With Vaccine',
        cost_obs=multi_cohort_outcomes_with.meanCosts,
        effect_obs=multi_cohort_outcomes_with.meanQALYs,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[without_therapy_strategy, with_therapy_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    CEA.plot_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional Discounted QALY',
        y_label='Additional Discounted Cost',
        fig_size=(6, 5),
        add_clouds=True,
        transparency=0.2)

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # uncertainty (projection) interval
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    NBA = Econ.CBA(
        strategies=[without_therapy_strategy, with_therapy_strategy],
        wtp_range=[-10000, 10000],
        if_paired=True
        # wtp_range=[0, 50000],
        # if_paired=False
    )
    # show the net monetary benefit figure
    NBA.plot_incremental_nmbs(
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='p',
        show_legend=True,
        figure_size=(6, 5),
    )