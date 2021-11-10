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
MAX_TIMESTAMP = 5
STEP_REWARDS = 0

HASH_STATE = {} # STATE_HASH : STATE_OBJECT
TRANSITION = [] # (STATE_HASH, MOVE_INDEX) : NEXT_STATE_HASH

CURRENT_ITER = [0, 0]

MAX_PROFIT = [float('-inf')]
MAX_PROFIT_PATH = []

def entropy_update():
    if CURRENT_ITER[0] >= 0.9 * CURRENT_ITER[1]:
        return 0.2
    elif CURRENT_ITER[0] >= 0.75 * CURRENT_ITER[1]:
        return 0.35
    elif CURRENT_ITER[0] >= 0.6 * CURRENT_ITER[1]:
        return 0.50
    elif CURRENT_ITER[0] >= 0.45 * CURRENT_ITER[1]:
        return 0.65
    elif CURRENT_ITER[0] >= 0.3 * CURRENT_ITER[1]:
        return 0.8
    else:
        return 1

def lr_update():
    if CURRENT_ITER[0] >= 0.9 * CURRENT_ITER[1]:
        return 0.25
    elif CURRENT_ITER[0] >= 0.75 * CURRENT_ITER[1]:
        return 0.30
    elif CURRENT_ITER[0] >= 0.6 * CURRENT_ITER[1]:
        return 0.35
    elif CURRENT_ITER[0] >= 0.45 * CURRENT_ITER[1]:
        return 0.40
    elif CURRENT_ITER[0] >= 0.3 * CURRENT_ITER[1]:
        return 0.45
    else:
        return 0.5



"""
########################
## PROJECT DEFINITION ##
########################
"""

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



"""
#################
## HELPER FUNC ##
#################
"""

def associates_logic(ongoing_proj_list):
    total_extra_benefits = 0
    # More associated benefits here
    return total_extra_benefits

def toBinary(a, max_length):
    r = []
    for _ in range(max_length):
        r.append(a%2)
        a //= 2
    return r

def toTrinary(a, max_length):
    r = []
    for _ in range(max_length):
        r.append(a%3)
        a //= 3
    return r

def random_generate_function(p):
    return random.random() < p



"""
######################
## STATE DEFINITION ##
######################
"""

class state:
    def __init__(self, cur_timestamp, C, ongoing_list):
        self.cur_timestamp = cur_timestamp
        self.current_cash = C
        self.back_list = BACK_LIST[self.cur_timestamp]
        self.ongoing_list = ongoing_list
        self.possible_moves = np.zeros((2 ** len(self.back_list)) * (3 ** len(self.ongoing_list)))

    def generate_moves_by_index(self, index):
        # 0: maintain, 1: pickup
        back_move_index = index % (2 ** len(self.back_list))
        # 0:maintain, 1: upgrade, 2: abort
        ongoing_move_index = index // (2 ** len(self.back_list))
        return [toBinary(back_move_index, len(self.back_list)), toTrinary(ongoing_move_index, len(self.ongoing_list))]

    def is_valid_move(self, move):
        bmove = move[0]
        omove = move[1]
        total_cost = 0

        for j in range(len(self.ongoing_list)):
            if omove[j] == 1:
                valid, cost = self.ongoing_list[j].proj_upgrade()
                if valid:
                    total_cost += cost
                    if total_cost > self.current_cash:
                        return False, 0
                else:
                    return False, 0

        for i in range(len(self.back_list)):
            if bmove[i] == 1:
                total_cost += self.back_list[i].cost
                if total_cost > self.current_cash:
                    return False, 0

        return True, total_cost

    def transist(self):
        entropy = entropy_update()
        strategy_index = 0
        if self.cur_timestamp == MAX_TIMESTAMP:  # END INVESTMENT PERIOD
            total_profit = sum([i.investment_termination() for i in self.ongoing_list])
            # STORE THE PATH TO THE MAP
            TRANSITION.append((self.__hash__(), strategy_index, total_profit))
            return False, total_profit

        strategy_index_list = []
        if random_generate_function(entropy):
            temp_index_list = np.arange((2 ** len(self.back_list)) * (3 ** len(self.ongoing_list)))
            np.random.shuffle(temp_index_list)
            strategy_index_list = temp_index_list
            # DEBUG: print("random", strategy_index_list)
        else:
            strategy_index_list = np.flip(np.argsort(self.possible_moves))
            # DEBUG: print("normal", strategy_index_list)

        move = self.generate_moves_by_index(0)
        for i in strategy_index_list:
            strategy_index = i
            move = self.generate_moves_by_index(strategy_index)
            valid, total_cost = self.is_valid_move(move)
            if valid:
                break

        if valid == False:  # No any valid moves (IN CASE SOME INVESTMENT HAS NEGATIVE PROFIT)
            TRANSITION.append((self.__hash__(), -1, -1000))  # UPDATE ALL MOVES SINCE NONE OF THEM ARE FEASIBLE
            return False, -1000  # False transition, rewards value

        total_profit = 0
        temp_ongoing_list = []
        for i in range(len(self.ongoing_list)):
            proj = self.ongoing_list[i]
            if move[1][i] == 2:
                total_profit += proj.proj_termination()
            elif move[1][i] == 1:
                proj_op = copy.deepcopy(proj)
                proj_op.proj_upgrade(test=False)
                # Upgrade year has no income
                valid, _ = proj_op.update()
                if valid:
                    temp_ongoing_list.append(proj_op)
            else:
                proj_op = copy.deepcopy(proj)
                valid, profit = proj_op.update()
                if valid:
                    total_profit += profit
                    temp_ongoing_list.append(proj_op)
        for i in range(len(self.back_list)):
            proj = self.back_list[i]
            if move[0][i] == 1:
                # Assume they must valid when first time updating
                proj_op = copy.deepcopy(proj)
                proj_op.update()
                temp_ongoing_list.append(proj_op)

        associated_benefits = associates_logic(temp_ongoing_list)
        new_state = state(self.cur_timestamp + 1,
                          self.current_cash - total_cost + total_profit + associated_benefits,
                          temp_ongoing_list)
        # STORE THE STATE TO THE MAP
        new_state_hash = new_state.__hash__()
        if new_state_hash in HASH_STATE:
            new_state = HASH_STATE[new_state_hash]
        else:
            HASH_STATE[new_state_hash] = new_state
        # STORE THE PATH TO THE MAP
        TRANSITION.append((self.__hash__(), strategy_index, new_state_hash))
        return True, new_state

    def __hash__(self):
        hash_ongoing_list = [i.__hash__() for i in self.ongoing_list]
        hash_ongoing_list.sort()
        return hash(str(self.cur_timestamp) + str(self.current_cash) + str(hash_ongoing_list))


"""
################
## Q Learning ##
################
"""

def Q_val_update():
    global TRANSITION

    if len(TRANSITION) < 1:
        return None

    # Update profit first
    cur_state_hash, action, profit = TRANSITION.pop()

    if action == -1:
        for i in range(len(HASH_STATE[cur_state_hash].possible_moves)):
            HASH_STATE[cur_state_hash].possible_moves[i] += lr_update() * (profit - INITIAL_CAPITAL - HASH_STATE[cur_state_hash].possible_moves[action])
    else:
        HASH_STATE[cur_state_hash].possible_moves[action] += lr_update() * (profit - INITIAL_CAPITAL - HASH_STATE[cur_state_hash].possible_moves[action])

    for cur_state_hash, action, next_state_hash in reversed(TRANSITION):
        HASH_STATE[cur_state_hash].possible_moves[action] += lr_update() * (STEP_REWARDS +
                                                                   decay_rate * np.max(HASH_STATE[next_state_hash].possible_moves)
                                                                   - HASH_STATE[cur_state_hash].possible_moves[action])

    if profit > MAX_PROFIT[0]:
        MAX_PROFIT[0] = profit
        global MAX_PROFIT_PATH
        MAX_PROFIT_PATH = copy.deepcopy(TRANSITION)

    TRANSITION = []
    return profit



"""
#################
## START TRIAL ##
#################
"""

