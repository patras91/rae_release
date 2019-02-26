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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 13.886231009570105}

rv.GROUND_EDGES = {0: [4, 17, 1, 6, 7, 12], 1: [0, 3, 4, 5, 20, 200], 2: [8], 3: [1, 11, 18], 4: [1, 7, 17, 0, 10], 5: [1], 6: [0], 7: [0, 4, 13], 8: [10, 13, 2, 9, 11, 15], 9: [8, 11, 14, 16], 10: [4, 8], 11: [3, 8, 20, 9], 12: [0, 19, 200], 13: [7, 16, 8], 14: [18, 9, 16], 15: [8, 18, 19], 16: [9, 14, 19, 13, 200], 17: [19, 0, 4], 18: [3, 15, 14, 20], 19: [12, 15, 16, 17], 20: [1, 18, 11], 200: [1, 12, 16]}
rv.GROUND_WEIGHTS = {(0, 4): 10.254460589269488, (0, 17): 6.063905112871297, (0, 1): 6.8979942264979215, (0, 6): 6.0174248699057395, (0, 7): 9.332080913247033, (0, 12): 3.7282696226439835, (1, 3): 9.126062359029529, (1, 4): 9.633114278381058, (1, 5): 9.946378054456057, (1, 20): 5.580686386323298, (1, 200): 7.202020356912618, (2, 8): 5.053844126511688, (3, 11): 9.470681944904156, (3, 18): 9.75137544761553, (4, 7): 2.771758149099247, (4, 17): 9.655706275075824, (4, 10): 2.3268583318832565, (7, 13): 14.136482577100985, (8, 10): 8.989117720985487, (8, 13): 3.1980571747837585, (8, 9): 5.135910917130106, (8, 11): 3.5222806348568394, (8, 15): 6.71757111811026, (9, 11): 9.601654657835775, (9, 14): 1, (9, 16): 3.5630655661929937, (11, 20): 15.71025389726459, (12, 19): 9.235752301076758, (12, 200): 6.41460014480035, (13, 16): 4.26548129400508, (14, 18): 2.828602308790088, (14, 16): 6.269216388480784, (15, 18): 8.52398927144862, (15, 19): 5.126425797142534, (16, 19): 9.089882201167933, (16, 200): 3.832190530330995, (17, 19): 11.488505596223204, (18, 20): 10.006450158072374}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5']
rv.ROBOT_CAPACITY = {'r0': 7.7411815625817, 'r1': 9.546770625803477, 'r2': 8.326721904063373, 'r3': 9.794769611598376, 'r4': 8.454764922546985, 'r5': 10.072239295229487}
rv.MACHINES = ['m0', 'm1', 'm2', 'fixer0', 'fixer1', 'fixer2']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 9.10979145730059, 'o1': 8.181273595997064, 'o2': 9.919341580826366, 'o3': 9.365824978834706, 'o4': 5.850061264931133, 'o5': 7.174772694781906, 'o6': 7.003473820766781, 'o7': 9.74596949701078, 'o8': 5.3507850039819544, 'o9': 5.071088216027951, 'o10': 5.92626035637237, 'o11': 2.9269679612202353, 'o12': 7.864251801584116, 'o13': 3.721112521847941, 'o14': 6.032599272696446, 'o15': 2.1542325939948963}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']}

def ResetState():
    state.loc = { 'r0': 18, 'r1': 18, 'r2': 17, 'r3': 19, 'r4': 6, 'r5': 17, 'm0': 3, 'm1': 6, 'm2': 5, 'fixer0': 16, 'fixer1': 1, 'fixer2': 14, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 7, 'o2': 10, 'o3': 3, 'o4': 10, 'o5': 4, 'o6': 10, 'o7': 19, 'o8': 11, 'o9': 14, 'o10': 17, 'o11': 17, 'o12': 18, 'o13': 19, 'o14': 6, 'o15': 1}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'fixer0'": False, "'fixer1'": False, "'fixer2'": False}
    state.numUses = {'m0': 10, 'm1': 9, 'm2': 8, 'fixer0': 6, 'fixer1': 12, 'fixer2': 6}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    23: [['order', 'type0', 200]],
    9: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
    7: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    13: [['order', 'type1', 200]],
    22: [['order', 'type1', 200]],
    5: [['order', 'type2', 200]],
    14: [['order', 'type2', 200]],
    2: [['order', 'type2', 200]],
    17: [['order', 'type2', 200]],
}
eventsEnv = {
}