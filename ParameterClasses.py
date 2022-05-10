from enum import Enum
import numpy as np
import test as Data
from test import HealthStates
import SimPy.Markov as Markov


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

        # annual treatment cost
        if self.therapy == Therapies.WITHOUT:
            self.annualTreatmentCost = 0
        else:
            self.annualTreatmentCost = Data.VAX_COST

        # transition probability matrix of the selected therapy
        self.transRateMatrix = []

        if self.therapy == Therapies.WITHOUT:
            # calculate transition rate matrix for the mono therapy
            self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=False)

        elif self.therapy == Therapies.WITH:
            # calculate transition probability matrix for the combination therapy
            self.transRateMatrix = Data.get_trans_rate_matrix(with_treatment=True)


        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT


