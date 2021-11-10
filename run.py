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
# Initialized Ongoing projects
B01 = project((0,1), 1.8, 0.21, "B01",  2)
B02 = project((0,2), 2.2, 0.25, "B02",  4)
B03 = project((0,3), 2.5, 0.28, "B03",  1)
B04 = project((0,4), 3.0, 0.33, "B04",  3)
bt0 = [B01, B02, B03, B04]

# Projects for t=1
A11 = project((1,1), 2.3, 0.28, "A11")
A12 = project((1,2), 2.1, 0.24, "A12")
A13 = project((1,3), 2.8, 0.32, "A13")
A14 = project((1,4), 2.7, 0.30, "A14")
A15 = project((1,5), 1.9, 0.22, "A15")
bt1 = [A11, A12, A13, A14, A15]

# Projects for t=2
A21 = project((2,1), 2.6, 0.28, "A21")
A22 = project((2,2), 2.4, 0.26, "A22")
A23 = project((2,3), 2.7, 0.30, "A23")
bt2 = [A21, A22, A23]

# Projects for t=3
A31 = project((3,1), 1.4, 0.16, "A31")
A32 = project((3,2), 3.8, 0.42, "A32")
A33 = project((3,3), 1.8, 0.22, "A33")
bt3 = [A31, A32, A33]

# Projects for t=4
A41 = project((4,1), 1.6, 0.18, "A41")
A42 = project((4,2), 3.1, 0.35, "A42")
A43 = project((4,3), 2.0, 0.22, "A43")
A44 = project((4,4), 2.5, 0.28, "A43")
bt4 = [A41, A42, A43, A44]

# Projects for t=5
A51 = project((5,1), 1.9, 0.21, "A51")
A52 = project((5,2), 2.1, 0.25, "A52")
A53 = project((5,3), 2.5, 0.28, "A53")
A54 = project((5,4), 3.1, 0.33, "A53")
bt5 = [A51, A52, A53, A54]

BACK_LIST = [bt1, bt2, bt3, bt4, bt5, []]