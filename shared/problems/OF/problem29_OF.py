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
rv.SHIPPING_DOC = {rv.FACTORY1: 1.0985966916695107}

rv.GROUND_EDGES = {0: [1, 9, 12, 13, 14], 1: [4, 7, 0, 17], 2: [12, 19, 8, 10, 16], 3: [4, 9, 8, 22], 4: [5, 12, 22, 1, 3], 5: [20, 21, 4, 7, 13, 15], 6: [8, 11, 18, 22], 7: [1, 5, 12, 13, 17, 22], 8: [2, 3, 6, 10, 15, 19, 18, 200], 9: [0, 3], 10: [2, 13, 8, 20], 11: [6, 12, 20, 21], 12: [0, 2, 4, 7, 11, 15], 13: [0, 5, 7, 10, 19], 14: [0], 15: [5, 12, 8], 16: [2, 22], 17: [1, 7], 18: [6, 8, 19], 19: [13, 18, 2, 8], 20: [10, 11, 5], 21: [11, 5], 22: [3, 6, 4, 7, 16], 200: [8]}
rv.GROUND_WEIGHTS = {(0, 1): 1, (0, 9): 10.38079134245391, (0, 12): 3.004791363999452, (0, 13): 2.899870338234539, (0, 14): 14.138216073494295, (1, 4): 5.436187120786922, (1, 7): 4.217158260059366, (1, 17): 6.1183815659772005, (2, 12): 11.51798604360934, (2, 19): 4.4186507492655895, (2, 8): 14.054489109287163, (2, 10): 8.453323364617725, (2, 16): 4.291839081203712, (3, 4): 5.045351237887775, (3, 9): 4.272671923036942, (3, 8): 1.880392844117738, (3, 22): 6.533468349086888, (4, 5): 9.268003499561082, (4, 12): 6.651531269782964, (4, 22): 1.0634373034192848, (5, 20): 8.50743232987475, (5, 21): 4.566457651714556, (5, 7): 9.95009428732631, (5, 13): 12.821851921474549, (5, 15): 6.15377489135947, (6, 8): 2.787861910244022, (6, 11): 7.200464651910253, (6, 18): 9.45700867699114, (6, 22): 6.16130899691625, (7, 12): 5.0134559234676495, (7, 13): 12.31739886143206, (7, 17): 5.364633974087388, (7, 22): 15.117284781749252, (8, 10): 4.4059337676386345, (8, 15): 7.551360368551462, (8, 19): 4.785348443007628, (8, 18): 7.8219035024660934, (8, 200): 7.075514592695584, (10, 13): 6.1139341948891115, (10, 20): 5.181850614765569, (11, 12): 7.082592163985755, (11, 20): 5.673793904932862, (11, 21): 9.57264644247215, (12, 15): 14.588410033315384, (13, 19): 10.069674367521399, (16, 22): 6.897282210390146, (18, 19): 2.533478045561486}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']
rv.ROBOT_CAPACITY = {'r0': 7.995736845105344, 'r1': 9.229129702784226, 'r2': 9.823743975744106, 'r3': 6.870947626002512, 'r4': 7.017096394517254, 'r5': 5.674096395079854, 'r6': 7.744350514578723}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 7.583603157834586, 'o1': 8.974273002534845, 'o2': 9.770467640570498, 'o3': 7.209624741639788, 'o4': 9.823743975744106, 'o5': 9.620619103220143, 'o6': 8.794761494929407, 'o7': 5.657916431976109, 'o8': 7.4767950656652005, 'o9': 5.702111773994065, 'o10': 4.499139930444698, 'o11': 4.845451402745355, 'o12': 9.823743975744106, 'o13': 7.3096870934431, 'o14': 4.439492738507942, 'o15': 4.2300697603502115, 'o16': 4.804761446693575}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16']}

def ResetState():
  state.loc = { r0: 0, r1: 22, r2: 13, r3: 11, r4: 7, r5: 22, r6: 16, m0: 1, fixer0: 11, fixer1: 14, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK,}
    state.storedLoc{'o0': 18, 'o1': 15, 'o2': 1, 'o3': 19, 'o4': 17, 'o5': 12, 'o6': 0, 'o7': 12, 'o8': 9, 'o9': 4, 'o10': 14, 'o11': 19, 'o12': 2, 'o13': 13, 'o14': 19, 'o15': 9, 'o16': 6}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses7
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', type0, 200]],
    7: [['order', type0, 200]],
    8: [['order', type0, 200]],
    8: [['order', type1, 200]],
    7: [['order', type1, 200]],
    1: [['order', type1, 200]],
    7: [['order', type1, 200]],
    7: [['order', type2, 200]],
    8: [['order', type2, 200]],
    4: [['order', type2, 200]],
    3: [['order', type2, 200]],
    8: [['order', type2, 200]],
    4: [['order', type3, 200]],
    8: [['order', type3, 200]],
    3: [['order', type3, 200]],
}
eventsEnv = {
}