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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 10.736588569004658}

rv.GROUND_EDGES = {0: [10, 4, 14], 1: [7, 5], 2: [6, 14, 7], 3: [7], 4: [0, 13], 5: [1, 200], 6: [11, 2, 8, 15], 7: [2, 1, 3, 9], 8: [6, 14, 200], 9: [7, 12, 15, 11], 10: [15, 0, 11], 11: [9, 10, 6], 12: [14, 9], 13: [4, 200], 14: [0, 2, 8, 12], 15: [6, 9, 10], 200: [5, 8, 13]}
rv.GROUND_WEIGHTS = {(0, 10): 4.899662169120907, (0, 4): 1, (0, 14): 1, (1, 7): 9.20019437217819, (1, 5): 11.404487061116182, (2, 6): 10.255103684923792, (2, 14): 6.224069228466911, (2, 7): 9.19049275186959, (3, 7): 7.449792364346875, (4, 13): 11.368086807384845, (5, 200): 9.78747727558171, (6, 11): 8.82358986142187, (6, 8): 2.793091053502078, (6, 15): 6.152548283302476, (7, 9): 8.758699800682878, (8, 14): 4.356341313773567, (8, 200): 11.983879903041046, (9, 12): 11.296890104655041, (9, 15): 7.235847154716275, (9, 11): 6.385978770313445, (10, 15): 10.912406900030167, (10, 11): 9.082981032991782, (12, 14): 16.09743516135992, (13, 200): 1.947651757809827}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']
rv.ROBOT_CAPACITY = {'r0': 8.917598059996052, 'r1': 6.113921719583682, 'r2': 9.643435862723194, 'r3': 6.495624905973815, 'r4': 7.246959753703099, 'r5': 5.579374283358921, 'r6': 7.771822977688098, 'r7': 7.014642095144936, 'r8': 3.651825578817469, 'r9': 8.725084081426004, 'r10': 6.470986988742304, 'r11': 9.578818345692083, 'r12': 8.460535129037696, 'r13': 10.144080390841506, 'r14': 6.932125268102849}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28']
rv.OBJ_WEIGHT = {'o0': 4.626993073213436, 'o1': 6.030302946169074, 'o2': 4.235868889707776, 'o3': 6.367783873006298, 'o4': 8.122650516639942, 'o5': 5.31046059269642, 'o6': 7.037905384732721, 'o7': 8.798608595867577, 'o8': 7.8339254177301205, 'o9': 9.851625818113016, 'o10': 4.054225800133986, 'o11': 7.461419077308221, 'o12': 10.144080390841506, 'o13': 7.239503491461234, 'o14': 6.262428208077714, 'o15': 5.900239114066981, 'o16': 4.211104285685256, 'o17': 7.469233317217028, 'o18': 3.0886679607179093, 'o19': 6.7968328747926545, 'o20': 10.144080390841506, 'o21': 9.392811020542544, 'o22': 4.655917249179993, 'o23': 7.467374184276026, 'o24': 5.306595618032294, 'o25': 4.599584691102201, 'o26': 6.665474544833583, 'o27': 5.417973542722238, 'o28': 5.429311808444514}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13'], 'type3': ['o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23'], 'type4': ['o24', 'o25', 'o26', 'o27', 'o28']}

def ResetState():
    state.loc = { 'r0': 3, 'r1': 8, 'r2': 13, 'r3': 2, 'r4': 3, 'r5': 10, 'r6': 6, 'r7': 6, 'r8': 11, 'r9': 11, 'r10': 8, 'r11': 14, 'r12': 13, 'r13': 5, 'r14': 7, 'm0': 12, 'm1': 7, 'm2': 8, 'm3': 12, 'm4': 11, 'm5': 1, 'm6': 3, 'm7': 15, 'fixer0': 12, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 8, 'o2': 1, 'o3': 14, 'o4': 14, 'o5': 9, 'o6': 9, 'o7': 4, 'o8': 1, 'o9': 7, 'o10': 2, 'o11': 11, 'o12': 12, 'o13': 5, 'o14': 7, 'o15': 15, 'o16': 0, 'o17': 12, 'o18': 13, 'o19': 6, 'o20': 13, 'o21': 6, 'o22': 5, 'o23': 14, 'o24': 9, 'o25': 7, 'o26': 9, 'o27': 13, 'o28': 11}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'r14'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'m4'": False, "'m5'": False, "'m6'": False, "'m7'": False, "'fixer0'": False}
    state.numUses = {'m0': 10, 'm1': 3, 'm2': 10, 'm3': 8, 'm4': 7, 'm5': 11, 'm6': 12, 'm7': 9, 'fixer0': 9}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    33: [['order', 'type0', 200]],
    13: [['order', 'type0', 200]],
    30: [['order', 'type1', 200]],
    23: [['order', 'type1', 200]],
    20: [['order', 'type1', 200]],
    14: [['order', 'type3', 200]],
    3: [['order', 'type3', 200]],
    4: [['order', 'type3', 200]],
    18: [['order', 'type3', 200]],
    24: [['order', 'type3', 200]],
    37: [['order', 'type3', 200]],
    17: [['order', 'type3', 200]],
    15: [['order', 'type3', 200]],
    32: [['order', 'type3', 200]],
    19: [['order', 'type4', 200]],
    6: [['order', 'type4', 200]],
    36: [['order', 'type4', 200]],
    11: [['order', 'type4', 200]],
    5: [['order', 'type4', 200]],
}
eventsEnv = {
}