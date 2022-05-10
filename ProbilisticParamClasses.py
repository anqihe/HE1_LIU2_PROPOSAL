import math

import scipy.stats as stat

import SimPy.RandomVariateGenerators as RVGs
from ParameterClasses import *  # import everything from the ParameterClass module


class Parameters:
    """ class to include parameter information to simulate the model """

    def __init__(self, therapy):

        self.therapy = therapy              # selected therapy
        self.initialHealthState = HealthStates.WELL     # initial health state
        self.annualTreatmentCost = 0        # annual treatment cost
        self.transRateMatrix = []                # transition probability matrix of the selected therapy
        self.annualStateCosts = []          # annual state costs
        self.annualStateUtilities = []      # annual state utilities
        self.discountRate = Data.DISCOUNT   # discount rate


class ParameterGenerator:
    """ class to generate parameter values from the selected probability distributions """

    def __init__(self, therapy):

        self.therapy = therapy
        self.probMatrixRVG = []     # list of dirichlet distributions for transition probabilities
        self.lnRelativeRiskRVG = None  # normal distribution for the natural log of the treatment relative risk
        self.annualStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.annualStateUtilityRVG = []  # list of beta distributions for the annual utility of states
        # self.annualTreatmentCostRVG = None   # gamma distribution for treatment cost

        # # create Dirichlet distributions for transition probabilities
        # j = 0
        # for probs in Data.TRANS_MATRIX:
        #     # note:  for a Dirichlet distribution all values of the argument 'a' should be non-zero.
        #     # setting if_ignore_0s to True allows the Dirichlet distribution to take 'a' with zero values.
        #     self.probMatrixRVG.append(RVGs.Dirichlet(
        #         a=probs, if_ignore_0s=True))
        #     j += 1
        #
        # treatment relative risk
        # rr_ci = [0.365, 0.71]   # confidence interval of the treatment relative risk
        #
        # # find the mean and st_dev of the normal distribution assumed for ln(RR)
        # # sample mean ln(RR)
        # mean_ln_rr = math.log(Data.TREATMENT_RR)
        # # sample standard deviation of ln(RR)
        # std_ln_rr = \
        #     (math.log(rr_ci[1]) - math.log(rr_ci[0])) / (2 * stat.norm.ppf(1 - 0.05 / 2))
        # # create a normal distribution for ln(RR)
        # self.lnRelativeRiskRVG = RVGs.Normal(loc=mean_ln_rr,
        #                                      scale=std_ln_rr)

        # create gamma distributions for annual state cost
        for cost in Data.ANNUAL_STATE_COST:
            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.annualStateCostRVG.append(RVGs.Constant(value=0))

            else:
                self.annualStateCostRVG.append(RVGs.Constant(value=1))
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5
                fit_output = RVGs.Gamma.fit_mm(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.annualStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                               loc=0,
                               scale=fit_output["scale"]))

        # # create a gamma distribution for annual treatment cost
        # if self.therapy == Therapies.WITHOUT:
        #     annual_cost = 0
        # else:
        #     annual_cost = Data.VAX_COST
        #
        # fit_output = RVGs.Gamma.fit_mm(mean=annual_cost, st_dev=annual_cost/5)
        # self.annualTreatmentCostRVG = RVGs.Gamma(a=fit_output["a"],
        #                                          loc=0,
        #                                          scale=fit_output["scale"])

        # create beta distributions for annual state utility
        for utility in Data.ANNUAL_STATE_UTILITY:
            # if utility is zero, add a constant 0, otherwise add a beta distribution
            if utility == 0:
                self.annualStateUtilityRVG.append(RVGs.Constant(value=0))
            elif utility == 1:
                self.annualStateUtilityRVG.append(RVGs.Constant(value=1))
            else:
                # find alpha and beta of the assumed beta distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 4
                fit_output = RVGs.Beta.fit_mm(mean=utility, st_dev=utility / 4)
                # append the distribution
                self.annualStateUtilityRVG.append(
                    RVGs.Beta(a=fit_output["a"], b=fit_output["b"]))

    def get_new_parameters(self, rng):
        """
        :param rng: random number generator
        :return: a new parameter set
        """

        # create a parameter set
        param = Parameters(therapy=self.therapy)

        # # calculate transition probabilities
        # prob_matrix = []    # probability matrix without background mortality added
        # # for all health states
        # for s in HealthStates:
        #     # if the current state is not death
        #     if s not in [HealthStates.COVID_DEATH, HealthStates.NATUAL_DEATH]:
        #         # sample from the dirichlet distribution to find the transition probabilities between hiv states
        #         # fill in the transition probabilities out of this state
        #         prob_matrix.append(self.probMatrixRVG[s.value].sample(rng))
        #
        # # sampled relative risk
        # rr = math.exp(self.lnRelativeRiskRVG.sample(rng))
        #
        # # calculate transition probabilities between hiv states
        # if self.therapy == Therapies.MONO:
        #     # calculate transition probability matrix for the mono therapy
        #     param.transRateMatrix = get_trans_rate_matrix(trans_prob_matrix=prob_matrix)
        #
        # elif self.therapy == Therapies.COMBO:
        #     # calculate transition probability matrix for the combination therapy
        #     param.transRateMatrix = get_trans_rate_matrix_combo(
        #         rate_matrix_mono=get_trans_rate_matrix(trans_prob_matrix=prob_matrix),
        #         combo_rr=rr)

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.annualStateCostRVG:
            param.annualStateCosts.append(dist.sample(rng))

        # # sample from the gamma distribution that is assumed for the treatment cost
        # param.annualTreatmentCost = self.annualTreatmentCostRVG.sample(rng)

        # sample from beta distributions that are assumed for annual state utilities
        for dist in self.annualStateUtilityRVG:
            param.annualStateUtilities.append(dist.sample(rng))

        # return the parameter set
        return param
