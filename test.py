from enum import Enum
import numpy as np

ALPHA = 0.05
DISCOUNT = 0.03     # annual discount rate

from enum import Enum

import numpy as np

# simulation settings
POP_SIZE = 5000         # cohort population size
SIMULATION_LENGTH = 20    # length of simulation (years)

ANNUAL_PROB_ALL_CAUSE_MORT = 41.4 / 1000
ANNUAL_PROB_STROKE_MORT = 36.2 / 100000
ANNUAL_PROB_FIRST_STROKE = 15 / 1000
PROB_SURVIVE_FIRST_STROKE = 0.75
PROB_SURVIVE_RECURRENT_STROKE = 0.7
FIVE_YEAR_PROB_RECURRENT_STROKE = 0.17
STROKE_DURATION = 1/52  # 1 week

ANTICOAG_STROKE_REDUCTION = 0.8
ANTICOAG_BLEEDING_DEATH_INCREASE = 0.05



class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    COVID = 1
    POST_COVID = 2
    COVID_DEATH = 3
    NATUAL_DEATH = 4

def get_trans_rate_matrix(with_treatment):
    """
    :param with_treatment: set to True to calculate the transition rate matrix when the anticoagulation is used
    in the post-stroke state
    :return: transition rate matrix
    """

    # Part 1: find the annual probability of non-stroke death
    annual_prob_non_stroke_mort = (ANNUAL_PROB_ALL_CAUSE_MORT - ANNUAL_PROB_STROKE_MORT)
    lambda0 = -np.log(1-annual_prob_non_stroke_mort)

    # Part 2: lambda 1 + lambda 2
    lambda1_plus2 = -np.log(1 - ANNUAL_PROB_FIRST_STROKE)

    # Part 3
    lambda1 = lambda1_plus2*PROB_SURVIVE_FIRST_STROKE
    lambda2 = lambda1_plus2*(1-PROB_SURVIVE_FIRST_STROKE)

    # Part 4
    lambda3_plus4 = -1/5 * np.log(1-FIVE_YEAR_PROB_RECURRENT_STROKE)

    # Part 5
    lambda3 = lambda3_plus4*PROB_SURVIVE_RECURRENT_STROKE
    lambda4 = lambda3_plus4*(1-PROB_SURVIVE_RECURRENT_STROKE)

    # Part 6
    lambda5 = 1/STROKE_DURATION

    # find multipliers to adjust the rates out of "Post-Stroke" depending on whether the patient
    # is receiving anticoagulation or not
    if with_treatment:
        r1 = 1-ANTICOAG_STROKE_REDUCTION
        r2 = 1+ANTICOAG_BLEEDING_DEATH_INCREASE
    else:
        r1 = 1
        r2 = 1

    rate_matrix = [
        [0,     lambda1,    0,          lambda2,    lambda0],       # WELL
        [0,     0,          lambda5,    0,          0],             # STROKE
        [0,     lambda3*r1, 0,          lambda4*r1, lambda0*r2],    # POST-STROKE
        [0,     0,          0,          0,          0],             # STROKE-DEATH
        [0,     0,          0,          0,          0]              # NATURAL-DEATH
    ]

    return rate_matrix



# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,          # WEL
    0.2,        # STROKE
    0.9,          # PS
    0,     # STROKE-D
    0,      #ND
]

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,      # WELL
    0,    # STROKE
    200,      # PS
    0,   # STROKE-D
    0,      #ND
]

VAX_COST = 2000

