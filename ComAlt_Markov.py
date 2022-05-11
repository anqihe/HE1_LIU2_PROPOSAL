
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

print('At level of willingness-to-pay = $225.94, we will recommend taking the vaccine.')