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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4.980244920518748}

rv.GROUND_EDGES = {0: [1, 4, 5, 7, 200], 1: [0, 6, 7], 2: [6, 3, 200], 3: [2, 7, 6], 4: [0, 7], 5: [0, 7, 6, 200], 6: [3, 5, 1, 2], 7: [0, 1, 3, 4, 5], 200: [0, 2, 5]}
rv.GROUND_WEIGHTS = {(0, 1): 11.342078166318302, (0, 4): 14.30074101743459, (0, 5): 11.525723594499873, (0, 7): 3.1336049814455826, (0, 200): 12.289834666621385, (1, 6): 10.298181258955127, (1, 7): 6.543351178220619, (2, 6): 11.289387889343343, (2, 3): 12.551840614833871, (2, 200): 3.581421839447981, (3, 7): 14.25106329281217, (3, 6): 10.124559120649568, (4, 7): 1, (5, 7): 8.596964497470681, (5, 6): 5.920428268666733, (5, 200): 5.887923976332556}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9']
rv.ROBOT_CAPACITY = {'r0': 9.83720803859191, 'r1': 3.7325342223704885, 'r2': 9.801941873505468, 'r3': 9.660443945610087, 'r4': 5.585029566082837, 'r5': 5.6169984009377085, 'r6': 4.133027196661649, 'r7': 9.89381422178218, 'r8': 6.47177294007402, 'r9': 9.609415098045403}
rv.MACHINES = ['m0', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 8.309075800900242, 'o1': 7.995096953848465, 'o2': 9.162156417503123, 'o3': 3.5240664869921043, 'o4': 8.930387394676394, 'o5': 4.247559624156283, 'o6': 5.260022653146142, 'o7': 7.674180812056108, 'o8': 4.3062601372190645, 'o9': 6.266538109795004, 'o10': 2.083555692305744, 'o11': 3.7129356587045734, 'o12': 7.388408199288045, 'o13': 3.4675797189263693, 'o14': 6.409760585743939, 'o15': 7.971875850558736, 'o16': 9.596298022509465, 'o17': 5.399701656089129}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17']}

def ResetState():
  state.loc = { r0: 1, r1: 5, r2: 4, r3: 4, r4: 2, r5: 7, r6: 4, r7: 7, r8: 4, r9: 3, m0: 1, fixer0: 7, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK,}
    state.storedLoc{'o0': 3, 'o1': 7, 'o2': 4, 'o3': 5, 'o4': 6, 'o5': 4, 'o6': 6, 'o7': 1, 'o8': 4, 'o9': 7, 'o10': 3, 'o11': 4, 'o12': 7, 'o13': 0, 'o14': 2, 'o15': 4, 'o16': 1, 'o17': 3}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'fixer0': False}
    state.numUses10
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    6: [['order', type0, 200]],
    2: [['order', type0, 200]],
    6: [['order', type1, 200]],
    1: [['order', type1, 200]],
    7: [['order', type1, 200]],
    5: [['order', type1, 200]],
    2: [['order', type1, 200]],
    6: [['order', type1, 200]],
    8: [['order', type1, 200]],
    2: [['order', type2, 200]],
    4: [['order', type2, 200]],
    3: [['order', type2, 200]],
    8: [['order', type3, 200]],
}
eventsEnv = {
}