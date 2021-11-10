import copy
import random
import numpy as np

"""
############
## PARAMS ##
############
"""

INITIAL_CAPITAL = 5.0
decay_rate = 0.3
# lr = 0.5
MAX_TIMESTAMP = 5
STEP_REWARDS = 0

HASH_STATE = {} # STATE_HASH : STATE_OBJECT
TRANSITION = [] # (STATE_HASH, MOVE_INDEX) : NEXT_STATE_HASH

CURRENT_ITER = [0, 0]


class project:
    def __init__(self, index, cost, benefit, name, cur_year=0, max_year=10, been_upgraded=False):
        self.index = index
        self.cost = cost
        self.benefit = benefit
        self.name = name
        self.been_upgraded = False
        self.cur_year = cur_year
        self.max_year = max_year

    def update(self):
        if self.cur_year + 1 > self.max_year:
            return False, 0
        else:
            self.cur_year += 1
            return True, self.benefit

    def proj_upgrade(self, test=True):
        if test:
            if not self.been_upgraded:
                return True, 0.3 * self.cost
            else:
                return False, 0
        else:
            if not self.been_upgraded:
                self.benefit *= 1.4
                self.been_upgraded = True
                return True, 0.3 * self.cost
            else:
                return False, 0

    def proj_termination(self):
        return (self.max_year - self.cur_year) / 10 * 0.5 * self.cost

    def investment_termination(self):  # Last year of the period, sum all benefits
        return (self.max_year - self.cur_year) * self.benefit

    def __hash__(self):
        attr = str(self.index) + str(self.cost) + str(self.benefit) + str(self.name) + str(self.been_upgraded) + str(
            self.cur_year) + str(self.max_year)
        return hash(attr)

    def __str__(self):
        return self.name


"""
##########
## DATA ##
##########
"""
