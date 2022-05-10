from enum import Enum

import numpy as np

# simulation settings
POP_SIZE = 10000         # cohort population size
SIMULATION_LENGTH = 100   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

ANNUAL_PROB_ALL_CAUSE_MORT = 0.0104
ANNUAL_PROB_COVID_MORT = 111.4 / 100000
ANNUAL_PROB_FIRST_COVID = 0.246
PROB_SURVIVE_FIRST_COVID = (24600-111.4)/24600
PROB_SURVIVE_RECURRENT_COVID = 0.95
PROB_RECURRENT_COVID = 0.04
COVID_DURATION = 2/52  # 2 week

VAX_COVID_REDUCTION = 0.85
#ANTICOAG_BLEEDING_DEATH_INCREASE = 0.05

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,     # Well
    2000,     # COVID
    0,     # post COVID
    0,          # COVID DEATH
    0,          # Natural DEATH
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,   # Well
    0.7,   # COVID # 0.8
    0.9,   # post COVID # 1
    0,      # COVID DEATH
    0,      # Natural DEATH
    ]


VAX_COST = 40
#Lamivudine_COST = 2086.0

# treatment relative risk
TREATMENT_RR = 0.15


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
    annual_prob_non_covid_mort = (ANNUAL_PROB_ALL_CAUSE_MORT - ANNUAL_PROB_COVID_MORT)
    lambda0 = -np.log(1-annual_prob_non_covid_mort)

    # Part 2: lambda 1 + lambda 2
    lambda1_plus2 = -np.log(1 - ANNUAL_PROB_FIRST_COVID)

    # Part 3
    lambda1 = lambda1_plus2*PROB_SURVIVE_FIRST_COVID
    lambda2 = lambda1_plus2*(1-PROB_SURVIVE_FIRST_COVID)

    # Part 4
    lambda3_plus4 = -np.log(1-PROB_RECURRENT_COVID)

    # Part 5
    lambda3 = lambda3_plus4*PROB_SURVIVE_RECURRENT_COVID
    lambda4 = lambda3_plus4*(1-PROB_SURVIVE_RECURRENT_COVID)

    # Part 6
    lambda5 = 1/COVID_DURATION

    # find multipliers to adjust the rates out of "Post-Stroke" depending on whether the patient
    # is receiving anticoagulation or not
    if with_treatment:
        r1 = 1-VAX_COVID_REDUCTION #0.15
        #r2 = 1+ANTICOAG_BLEEDING_DEATH_INCREASE
    else:
        r1 = 1
        #r2 = 1

    rate_matrix = [
        [0,     lambda1*r1,    0,          lambda2*r1,    lambda0],       # WELL
        [0,     0,          lambda5,    0,          0],             # covid
        [0,     lambda3*r1, 0,          lambda4*r1, lambda0],    # post covid
        [0,     0,          0,          0,          0],             # covid-DEATH
        [0,     0,          0,          0,          0]              # NATURAL-DEATH
    ]

    return rate_matrix


# print('Transition rate matrix with no treatment:')
# print(get_trans_rate_matrix(with_treatment=False))
# print('Transition rate matrix with treatment:')
# print(get_trans_rate_matrix(with_treatment=True))





# transition matrix
TRANS_COUNT_MATRIX = [
    [246796189,    65316689, 16329172,  0  ],   # Well
    [65186055, 0, 0, 130633 ],  # COVID NON HOS
    [14337013,     0,    0,    1992158 ],  # COVID  HOS

    #[0, 0, 0, 2122791, 0],  # COVID DEATH
    #[0, 0, 0, 0, 3451694]  #Natural DEATH
    ]

TRANS_PROB_MATRIX = [
    [0.7436,  0.1968, 0.0492,       0, 0.0104],   # Well
    [0.998, 0, 0, 0.002, 0],  # COVID NON HOS
    [0.878,     0,    0,    0.122, 0],  # COVID  HOS
    [0, 0, 0, 1, 0],  # COVID DEATH
    [0, 0, 0, 0, 1]  #Natural DEATH
    ]

