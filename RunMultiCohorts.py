import InputData as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import ProbilisticParamClasses as P
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path

N_COHORTS = 20             # number of cohorts


#WITHOUT VACCINE

# create multiple cohort
multiCohort_WITHOUT = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=P.Therapies.WITHOUT)

multiCohort_WITHOUT.simulate(sim_length=D.SIMULATION_LENGTH)

# plot the sample paths
Path.plot_sample_paths(
    sample_paths=multiCohort_WITHOUT.multiCohortOutcomes.survivalCurves,
    title='Survival Curves (without vaccine)',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Hist.plot_histogram(
    data=multiCohort_WITHOUT.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time (without vaccine)',
    x_label='Mean Survival Time (Year)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_WITHOUT.multiCohortOutcomes,
                       therapy_name=P.Therapies.WITHOUT)

# WITH VACCINE

# create multiple cohort
multiCohort_WITH = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=D.POP_SIZE,
    therapy=P.Therapies.WITH)

multiCohort_WITH.simulate(sim_length=D.SIMULATION_LENGTH)

# plot the sample paths
Path.plot_sample_paths(
    sample_paths=multiCohort_WITH.multiCohortOutcomes.survivalCurves,
    title='Survival Curves (with vaccine)',
    x_label='Time-Step (Year)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Hist.plot_histogram(
    data=multiCohort_WITH.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time (with vaccine)',
    x_label='Mean Survival Time (Year)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_WITH.multiCohortOutcomes,
                       therapy_name=P.Therapies.WITH)
