__author__ = 'mason'
from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

def GetCostOfMove(r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(item):
    return max(1, np.random.beta(2, 2))

def GetCostOfWrap(m, item):
    return max(1, np.random.normal(5, .5))

def GetCostOfPickup(r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfPutdown(r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfLoad(r, m, item):
    return max(1, np.random.normal(3, .5))

DURATION.TIME = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'repair': 8,
    'wait': 1
}

DURATION.COUNTER = {
    'lookupDB': GetCostOfLookup,
    'wrap': GetCostOfWrap,
    'pickup': GetCostOfPickup,
    'putdown': GetCostOfPutdown,
    'acquireRobot': 1,
    'freeRobot': 1,
    'loadMachine': GetCostOfLoad,
    'moveRobot': GetCostOfMove,
    'repair': 8,
    'wait': 1
}

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 17.95422920413762}

rv.GROUND_EDGES = {0: [6, 10, 16, 2, 9, 15, 18, 22], 1: [9, 15, 3, 10], 2: [0, 7, 14, 16, 200], 3: [1, 7, 17, 14, 21], 4: [5, 15, 19, 17, 200], 5: [6, 16, 4, 10, 12], 6: [19, 0, 5, 11], 7: [2, 3, 16, 21], 8: [22], 9: [0, 1, 16], 10: [1, 5, 13, 0, 20], 11: [6, 19, 22], 12: [5], 13: [20, 10], 14: [2, 3, 21], 15: [0, 1, 4], 16: [2, 5, 9, 0, 7], 17: [4, 3, 19], 18: [0, 200], 19: [17, 4, 6, 11], 20: [10, 13], 21: [3, 14, 7], 22: [0, 8, 11], 200: [2, 4, 18]}
rv.GROUND_WEIGHTS = {(0, 6): 8.619597088030687, (0, 10): 4.577468031000187, (0, 16): 6.9356183632187784, (0, 2): 6.708928493147898, (0, 9): 8.6683692548937, (0, 15): 8.743891855066758, (0, 18): 12.810769120797959, (0, 22): 14.64272044942219, (1, 9): 11.848763638666158, (1, 15): 7.029426794427253, (1, 3): 8.447602539184414, (1, 10): 4.371641644783115, (2, 7): 11.782149899069825, (2, 14): 11.119166420674272, (2, 16): 6.3276332233081725, (2, 200): 15.098740286466516, (3, 7): 7.914534446874016, (3, 17): 1, (3, 14): 2.8039742105235694, (3, 21): 8.283548480469776, (4, 5): 3.3247358415195096, (4, 15): 7.62002493607919, (4, 19): 8.046874999405405, (4, 17): 7.4229402316970035, (4, 200): 9.221346976472363, (5, 6): 6.3951400943318735, (5, 16): 2.498888346631582, (5, 10): 9.701635418955332, (5, 12): 6.197343514637971, (6, 19): 10.290581722745301, (6, 11): 4.3197387551023025, (7, 16): 1, (7, 21): 7.20790515616147, (8, 22): 6.666042756288388, (9, 16): 4.4253938851546355, (10, 13): 11.420995493242868, (10, 20): 5.6530229851161735, (11, 19): 6.041048969130715, (11, 22): 12.32016904186116, (13, 20): 10.95017090365015, (14, 21): 3.40358090803442, (17, 19): 10.296355111539981, (18, 200): 10.054851301333628}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']
rv.ROBOT_CAPACITY = {'r0': 6.101389228327754, 'r1': 6.603068782247985, 'r2': 5.562772714938848, 'r3': 9.423203572136734, 'r4': 7.693044982330765, 'r5': 5.550494268901925, 'r6': 9.964884884425652}
rv.MACHINES = ['m0', 'm1', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 9.638496848655851, 'o1': 7.916297322215782, 'o2': 4.996118475832659, 'o3': 8.557423658627837, 'o4': 8.756745185667926, 'o5': 5.897312158871295, 'o6': 9.964884884425652, 'o7': 8.761773042724002, 'o8': 7.443302716806709, 'o9': 9.70782803565698, 'o10': 8.355695398328498, 'o11': 6.3859213351371835, 'o12': 4.998243148523022, 'o13': 7.29522805750638, 'o14': 7.954460514278594, 'o15': 4.398523410894613, 'o16': 8.13445307311483, 'o17': 7.464035103882169}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4'], 'type2': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16'], 'type4': ['o17']}

def ResetState():
  state.loc = { r0: 5, r1: 13, r2: 12, r3: 11, r4: 3, r5: 4, r6: 16, m0: 10, m1: 4, fixer0: 22, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK,}
    state.storedLoc{'o0': 16, 'o1': 8, 'o2': 9, 'o3': 17, 'o4': 10, 'o5': 8, 'o6': 7, 'o7': 11, 'o8': 21, 'o9': 17, 'o10': 10, 'o11': 3, 'o12': 17, 'o13': 13, 'o14': 5, 'o15': 7, 'o16': 20, 'o17': 4}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'm1': False, 'fixer0': False}
    state.numUses11
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    4: [['order', type0, 200]],
    5: [['order', type1, 200]],
    2: [['order', type2, 200]],
    1: [['order', type2, 200]],
    2: [['order', type2, 200]],
    8: [['order', type2, 200]],
    1: [['order', type2, 200]],
    8: [['order', type4, 200]],
}
eventsEnv = {
}