import numpy as np

import SimPy.EconEval as Econ
import SimPy.Markov as Markov
import SimPy.SamplePath as Path
import SimPy.Statistics as Stat
from InputData import HealthStates


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: an instance of the parameters class
        """
        self.id = id
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)  # patient state monitor

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        rng = np.random.RandomState(seed=self.id)
        # gillespie algorithm
        gillespie = Markov.Gillespie(transition_rate_matrix=self.params.transRateMatrix)

        t = 0  # simulation time
        if_stop = False

        while not if_stop:
            # find time until next event (dt), and next state
            # (note that the gillespie algorithm returns None for dt if the process
            # is in an absorbing state)

            dt, new_state_index = gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # stop if time to next event (dt) is None (i.e. we have reached an absorbing state)
            if dt is None:
                if_stop = True

            else:
                # else if next event occurs beyond simulation length
                if dt + t > sim_length:
                    # advance time to the end of the simulation and stop
                    t = sim_length
                    # the individual stays in the current state until the end of the simulation
                    new_state_index = self.stateMonitor.currentState.value
                    if_stop = True
                else:
                    # advance time to the time of next event
                    t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthStates(new_state_index))


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState   # initial health state
        self.survivalTime = None      # survival time
        self.nCOVID = 0        # numbers of  COVID
        # patient's cost and utility monitor
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """

        # update survival time
        if new_state in (HealthStates.COVID_DEATH, HealthStates.NATUAL_DEATH):
            self.survivalTime = time

        # update covid counts
        if new_state in (HealthStates.COVID, HealthStates.COVID_DEATH):
            self.nCOVID += 1

        # update cost and utility
        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState)
                                       #next_state=new_state)

        # update current health state
        self.currentState = new_state


class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        self.tLastRecorded = 0  # time when the last cost and outcomes got recorded

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, time, current_state):
        """ updates the discounted total cost and health utility
        :param time: simulation time
        :param current_state: current health state
        """

        cost = self.params.annualStateCosts[current_state.value] + self.params.annualTreatmentCost
        utility = self.params.annualStateUtilities[current_state.value]

        # discounted cost and utility (continuously compounded)
        discounted_cost = Econ.pv_continuous_payment(payment=cost,
                                                     discount_rate=self.params.discountRate,
                                                     discount_period=(self.tLastRecorded, time))
        discounted_utility = Econ.pv_continuous_payment(payment=utility,
                                                        discount_rate=self.params.discountRate,
                                                        discount_period=(self.tLastRecorded, time))

        # if next_state == HealthStates.COVID:
        #    discounted_cost += Econ.pv_single_payment(payment=5000, discount_rate=0.03, discount_period=time,
        #                                             discount_continuously=True)

        # update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        self.totalDiscountedUtility += discounted_utility

        # update the time since last recording to the current time
        self.tLastRecorded = time


class Cohort:
    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param parameters: parameters
        """
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params)
            # simulate
            patient.simulate(sim_length)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.nTotalCOVID = []           # covid times
        self.costs = []                 # patients' discounted costs
        self.utilities =[]              # patients' discounted utilities
        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)

        self.statSurvivalTime = None    # summary statistics for survival time
        self.statNumOfCOVID = None      # summary statistics for time to AIDS
        self.statCost = None            # summary statistics for discounted cost
        self.statUtility = None         # summary statistics for discounted utility

        self.meanSurvivalTime = None
        self.meanNumOfCOVID = None
        self.meanCosts = None


    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record survival time and time until AIDS
        if not (simulated_patient.stateMonitor.survivalTime is None):
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        #if simulated_patient.stateMonitor.nCOVID is not None:
        self.nTotalCOVID.append(simulated_patient.stateMonitor.nCOVID)

        # discounted cost and discounted utility
        self.costs.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
        self.utilities.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        # calculate mean number of stokes
        self.meanNumOfCOVID = sum(self.nTotalCOVID)/len(self.nTotalCOVID)
        self.meanCosts = sum(self.costs)/len(self.costs)


        # summary statistics
        self.statSurvivalTime = Stat.SummaryStat(name='Survival time', data=self.survivalTimes)
        self.statNumOfCOVID = Stat.SummaryStat(name='Times of COVID', data=self.nTotalCOVID)
        self.statCost = Stat.SummaryStat(name='Discounted cost', data=self.costs)
        self.statUtility = Stat.SummaryStat(name='Discounted utility', data=self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1] * len(self.survivalTimes)
        )




