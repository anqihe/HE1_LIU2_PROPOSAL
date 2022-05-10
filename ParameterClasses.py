from enum import Enum
import numpy as np
import InputData as Data
from InputData import HealthStates
import SimPy.Markov as Markov

class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    COVID = 1
    POST_COVID = 2
    COVID_DEATH = 3
    NATUAL_DEATH = 4

class Therapies(Enum):
    """ mono vs. combination therapy """
    WITHOUT = 0
    WITH = 1


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy

        # initial health state
        self.initialHealthState = HealthStates.WELL


        # transition probability matrix of the selected therapy
        self.transRateMatrix = []


        if therapy == Therapies.WITHOUT:
            # calculate transition rate matrix for the mono therapy
            self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=False)
        else:
            # calculate transition probability matrix for the combination therapy
            self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=True)

        # annual treatment cost
        if self.therapy == Therapies.WITHOUT:
            self.annualTreatmentCost = 0
        elif self.therapy == Therapies.WITH:
            self.annualTreatmentCost = Data.VAX_COST

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT


