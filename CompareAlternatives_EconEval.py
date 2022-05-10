import InputData as D
import MultiCohortClasses as Cls
import MultiCohortSupport as Support
import ProbilisticParamClasses as P

N_COHORTS = 200  # number of cohorts
POP_SIZE = 100 # population size of each cohort

# create a multi-cohort to simulate under mono therapy
multiCohortWITHOUT = Cls.MultiCohort(
    ids=range(N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.WITHOUT
)

multiCohortWITHOUT.simulate(sim_length=D.SIMULATION_LENGTH)

# create a multi-cohort to simulate under combo therapy
multiCohortWITH = Cls.MultiCohort(
    ids=range(N_COHORTS, 2*N_COHORTS),
    pop_size=POP_SIZE,
    therapy=P.Therapies.WITH
)

multiCohortWITH.simulate(sim_length=D.SIMULATION_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohortWITHOUT.multiCohortOutcomes,
                       therapy_name=P.Therapies.WITHOUT)
Support.print_outcomes(multi_cohort_outcomes=multiCohortWITH.multiCohortOutcomes,
                       therapy_name=P.Therapies.WITH)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_without=multiCohortWITHOUT.multiCohortOutcomes,
                                            multi_cohort_outcomes_with=multiCohortWITH.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_without=multiCohortWITHOUT.multiCohortOutcomes,
                                   multi_cohort_outcomes_with=multiCohortWITH.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_without=multiCohortWITHOUT.multiCohortOutcomes,
                       multi_cohort_outcomes_with=multiCohortWITH.multiCohortOutcomes)
