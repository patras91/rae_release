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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1.0237120419214847}

rv.GROUND_EDGES = {0: [1, 6, 7], 1: [0, 4, 5], 2: [7, 8, 4, 200], 3: [6, 7, 4], 4: [1, 2, 3, 5, 8], 5: [1, 4, 7, 200], 6: [0, 3], 7: [0, 2, 3, 5], 8: [4, 2], 200: [2, 5]}
rv.GROUND_WEIGHTS = {(0, 1): 11.021240268239637, (0, 6): 7.258943770784028, (0, 7): 10.05360243589996, (1, 4): 11.765048393493487, (1, 5): 6.478798411957192, (2, 7): 9.528049561414669, (2, 8): 11.4823048160117, (2, 4): 11.044349116999923, (2, 200): 1, (3, 6): 11.163760143176145, (3, 7): 1.8247313979918651, (3, 4): 7.104814156103553, (4, 5): 12.1344903341971, (4, 8): 7.204047265889467, (5, 7): 10.221682053050747, (5, 200): 8.74060953709523}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5']
rv.ROBOT_CAPACITY = {'r0': 4.198826466992163, 'r1': 8.613511233266705, 'r2': 4.957748267510469, 'r3': 8.707121854841454, 'r4': 9.820553303403354, 'r5': 6.27196180338117}
rv.MACHINES = ['m0', 'm1', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']
rv.OBJ_WEIGHT = {'o0': 5.137246635786331, 'o1': 7.136641000128244, 'o2': 7.127635691881151, 'o3': 7.990243068422276, 'o4': 9.278158039561855, 'o5': 6.832057820258854, 'o6': 5.753553997830064, 'o7': 3.9576535220873184, 'o8': 7.256628420966065, 'o9': 7.790998476328026, 'o10': 7.657123437295579, 'o11': 6.171739464837914, 'o12': 7.533343818881838, 'o13': 8.650034785626781, 'o14': 9.820553303403354, 'o15': 6.240623033835441, 'o16': 9.820553303403354, 'o17': 8.60803294417961, 'o18': 6.199858891129305, 'o19': 8.638604931783973, 'o20': 8.926963006758264, 'o21': 2.724903975296325, 'o22': 9.127574683705994, 'o23': 8.432336392531349, 'o24': 6.950345477175977}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16'], 'type3': ['o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23'], 'type4': ['o24']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 3, 'r2': 3, 'r3': 0, 'r4': 5, 'r5': 8, 'm0': 0, 'm1': 6, 'fixer0': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 3, 'o2': 3, 'o3': 4, 'o4': 6, 'o5': 2, 'o6': 7, 'o7': 0, 'o8': 4, 'o9': 4, 'o10': 4, 'o11': 6, 'o12': 2, 'o13': 6, 'o14': 3, 'o15': 6, 'o16': 2, 'o17': 3, 'o18': 4, 'o19': 7, 'o20': 0, 'o21': 3, 'o22': 6, 'o23': 3, 'o24': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'m0'": False, "'m1'": False, "'fixer0'": False}
    state.numUses = {'m0': 9, 'm1': 4, 'fixer0': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    7: [['order', 'type0', 200]],
    25: [['order', 'type0', 200]],
    22: [['order', 'type0', 200]],
    15: [['order', 'type0', 200]],
    26: [['order', 'type0', 200]],
    28: [['order', 'type0', 200]],
    35: [['order', 'type1', 200]],
    1: [['order', 'type1', 200]],
    31: [['order', 'type1', 200]],
    4: [['order', 'type1', 200]],
    24: [['order', 'type2', 200]],
    36: [['order', 'type2', 200]],
    19: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
    33: [['order', 'type2', 200]],
    20: [['order', 'type2', 200]],
    11: [['order', 'type3', 200]],
    34: [['order', 'type3', 200]],
    12: [['order', 'type3', 200]],
    18: [['order', 'type3', 200]],
}
eventsEnv = {
}