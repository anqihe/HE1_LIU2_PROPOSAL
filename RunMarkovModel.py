import test as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path

# selected therapy
therapy = P.Therapies.WITHOUT

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      parameters=P.Parameters(therapy=therapy))

# simulate the cohort over the specified time steps
myCohort.simulate(sim_length=D.SIMULATION_LENGTH)

# plot the sample path (survival curve)
Path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,
                       therapy_name=therapy)


# -----------------------------
# Markov model with vaccine
# -----------------------------
myCohortWith = Cls.Cohort(id=1,
                                  pop_size=D.POP_SIZE,
                                  parameters=P.Parameters(therapy=P.Therapies.WITH))

# simulate
myCohortWith.simulate(sim_length=D.SIMULATION_LENGTH)

# survival curve
Path.plot_sample_path(
    sample_path=myCohortWith.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with vaccine)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# histograms of survival times
Hist.plot_histogram(
    data=myCohortWith.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with vaccine)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# histogram of number of cvd
Hist.plot_histogram(
    data=myCohortWith.cohortOutcomes.nTotalCOVID,
    title='Number of COVID (With vaccine)',
    x_label='Number of COVID',
    y_label='Count',
    bin_width=1,
    x_range=[0, 7]
)

print('With Vaccine:')
print('     Mean survival time for the model (years):',
      myCohortWith.cohortOutcomes.meanSurvivalTime)
print('     Mean number of COVID:',
      myCohortWith.cohortOutcomes.meanNumOfCOVID)
print('Average discounted cost of patients who start in the state “Well” with vaccine:',
      myCohortWith.cohortOutcomes.meanCosts)
