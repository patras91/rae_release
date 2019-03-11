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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 15}

rv.GROUND_EDGES = {0: [1, 3, 4, 8, 9, 10, 13, 15, 17, 19, 22], 1: [0, 21, 14], 2: [3, 200], 3: [0, 2, 18], 4: [0, 9, 11, 20, 200], 5: [12, 16, 23], 6: [9, 18], 7: [14, 19, 12], 8: [0, 14], 9: [0, 4, 6, 16], 10: [0], 11: [16, 20, 4], 12: [7, 22, 5, 16, 20], 13: [0, 21], 14: [1, 20, 7, 8, 200], 15: [0], 16: [5, 9, 12, 20, 11], 17: [0, 18], 18: [3, 17, 23, 6], 19: [0, 7], 20: [12, 14, 4, 11, 16, 21, 200], 21: [13, 20, 1], 22: [0, 12], 23: [5, 18], 200: [2, 4, 14, 20]}
rv.GROUND_WEIGHTS = {(0, 1): 6.414844064773416, (0, 3): 6.102557677469893, (0, 4): 3.256203981447136, (0, 8): 12.329661556748867, (0, 9): 8.08613421242437, (0, 10): 5.837968009747067, (0, 13): 8.476548034930776, (0, 15): 7.058822535798396, (0, 17): 3.5353953823025996, (0, 19): 10.47342972006754, (0, 22): 6.502468625415386, (1, 21): 12.393224558342325, (1, 14): 11.840427532436351, (2, 3): 6.874875081961545, (2, 200): 6.5220608862119915, (3, 18): 3.5767292506114527, (4, 9): 8.039990354207088, (4, 11): 1.4066667922848648, (4, 20): 7.361056809037243, (4, 200): 5.009155189622284, (5, 12): 8.012076132422798, (5, 16): 11.53037283209662, (5, 23): 1, (6, 9): 8.688937602466554, (6, 18): 8.048709734985696, (7, 14): 6.185372040811256, (7, 19): 3.7596568268589463, (7, 12): 8.851258120763223, (8, 14): 7.543006790574006, (9, 16): 7.798365174696749, (11, 16): 5.914248561280717, (11, 20): 3.3134612986532694, (12, 22): 9.150174618194978, (12, 16): 8.235777330472256, (12, 20): 10.806378856455627, (13, 21): 4.440707888200348, (14, 20): 4.43931269085067, (14, 200): 11.105255130081108, (16, 20): 7.850769571064852, (17, 18): 11.254324478421317, (18, 23): 6.010369431055081, (20, 21): 2.6832601648445014, (20, 200): 7.843575299147377}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 4.992661157433249, 'r1': 6.570002437821468, 'r2': 8.735403100513775, 'r3': 7.298508547846695, 'r4': 7.761422803826312, 'r5': 8.614785254662607, 'r6': 7.011632281119017, 'r7': 9.05396687858553, 'r8': 9.684967386816052, 'r9': 3.3013440825850724}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 6.371835399012827, 'o1': 7.948791913800396, 'o2': 3.028021097106211, 'o3': 9.479853749764255, 'o4': 9.684967386816052, 'o5': 9.578009998776599, 'o6': 6.784756539294075, 'o7': 4.841089652358484, 'o8': 7.309319610916424, 'o9': 2.352341440025996, 'o10': 5.793590422599146, 'o11': 7.5669275435633825, 'o12': 9.684967386816052, 'o13': 4.7552131004113765, 'o14': 7.926615360750867, 'o15': 7.305438982366852, 'o16': 5.821085627019316, 'o17': 8.013280370338872}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10'], 'type3': ['o11', 'o12'], 'type4': ['o13', 'o14', 'o15', 'o16', 'o17']}

def ResetState():
    state.loc = { 'r0': 17, 'r1': 20, 'r2': 3, 'r3': 18, 'r4': 1, 'r5': 5, 'r6': 16, 'r7': 18, 'r8': 12, 'r9': 2, 'm0': 18, 'm1': 7, 'fixer0': 17, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK,}
    state.storedLoc = {'o0': 11, 'o1': 23, 'o2': 1, 'o3': 18, 'o4': 8, 'o5': 13, 'o6': 21, 'o7': 4, 'o8': 18, 'o9': 9, 'o10': 0, 'o11': 10, 'o12': 0, 'o13': 13, 'o14': 4, 'o15': 11, 'o16': 22, 'o17': 15}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'm1': False, 'fixer0': False}
    state.numUses = {'m0': 10, 'm1': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    16: [['order', 'type0', 200]],
    13: [['order', 'type0', 200]],
}
eventsEnv = {
}