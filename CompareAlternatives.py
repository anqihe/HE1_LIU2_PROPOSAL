# import inputdaaata as D
# import MultiCohortClasses as Cls
# import MultiCohortSupport as Support
# import ProbilisticParamClasses as P
#
# N_COHORTS = 200  # number of cohorts
# POP_SIZE = 100 # population size of each cohort
#
# # create a multi-cohort to simulate under mono therapy
# multiCohortMono = Cls.MultiCohort(
#     ids=range(N_COHORTS),
#     pop_size=POP_SIZE,
#     therapy=P.Therapies.MONO
# )
#
# multiCohortMono.simulate(sim_length=D.SIM_LENGTH)
#
# # create a multi-cohort to simulate under combo therapy
# multiCohortCombo = Cls.MultiCohort(
#     ids=range(N_COHORTS, 2*N_COHORTS),
#     pop_size=POP_SIZE,
#     therapy=P.Therapies.COMBO
# )
#
# multiCohortCombo.simulate(sim_length=D.SIM_LENGTH)
#
# # print the estimates for the mean survival time and mean time to AIDS
# Support.print_outcomes(multi_cohort_outcomes=multiCohortMono.multiCohortOutcomes,
#                        therapy_name=P.Therapies.MONO)
# Support.print_outcomes(multi_cohort_outcomes=multiCohortCombo.multiCohortOutcomes,
#                        therapy_name=P.Therapies.COMBO)
#
# # draw survival curves and histograms
# Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
#                                             multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)
#
# # print comparative outcomes
# Support.print_comparative_outcomes(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
#                                    multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)
#
# # report the CEA results
# Support.report_CEA_CBA(multi_cohort_outcomes_mono=multiCohortMono.multiCohortOutcomes,
#                        multi_cohort_outcomes_combo=multiCohortCombo.multiCohortOutcomes)


import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support


# simulating mono therapy
# create a cohort
cohort_mono = Cls.Cohort(id=0,
                         pop_size=D.POP_SIZE,
                         parameters=P.Parameters(therapy=P.Therapies.WITHOUT))
# simulate the cohort
cohort_mono.simulate(sim_length=D.SIMULATION_LENGTH)

# simulating combination therapy
# create a cohort
cohort_combo = Cls.Cohort(id=1,
                          pop_size=D.POP_SIZE,
                          parameters=P.Parameters(therapy=P.Therapies.WITH))
# simulate the cohort
cohort_combo.simulate(sim_length=D.SIMULATION_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(sim_outcomes=cohort_mono.cohortOutcomes,
                       therapy_name=P.Therapies.WITHOUT)
Support.print_outcomes(sim_outcomes=cohort_combo.cohortOutcomes,
                       therapy_name=P.Therapies.WITH)
# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_without=cohort_mono.cohortOutcomes,
                                            sim_outcomes_with=cohort_combo.cohortOutcomes)
# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_without=cohort_mono.cohortOutcomes,
                                   sim_outcomes_with=cohort_combo.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_without=cohort_mono.cohortOutcomes,
                       sim_outcomes_with=cohort_combo.cohortOutcomes)

print('At level of willingness-to-pay = 181.43$, we will recommend taking the vaccine.')