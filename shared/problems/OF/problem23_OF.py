__author__ = 'mason'
from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

def GetCostOfMove(id, r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(id, item):
    return max(1, np.random.beta(2, 2))

def GetCostOfWrap(id, m, item):
    return max(1, np.random.normal(5, .5))

def GetCostOfPickup(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfPutdown(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfLoad(id, r, m, item):
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
    'repair': 5,
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
    'repair': 5,
    'wait': 1
}

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [6, 1, 3, 7, 18, 20], 1: [0, 5, 13, 19], 2: [20, 22, 5], 3: [0], 4: [7, 12, 6, 23, 200], 5: [2, 14, 1, 18], 6: [4, 15, 0, 13], 7: [0, 4, 13, 21], 8: [18], 9: [12, 18, 20, 10, 22], 10: [9, 13], 11: [20, 17, 21, 23], 12: [15, 4, 9], 13: [1, 6, 7, 17, 10, 16, 21], 14: [20, 5], 15: [22, 6, 12], 16: [13, 21], 17: [11, 13], 18: [0, 5, 8, 9, 21], 19: [1, 22, 23], 20: [0, 2, 9, 11, 14], 21: [7, 11, 13, 18, 16], 22: [9, 2, 15, 19], 23: [4, 11, 19], 200: [4]}
rv.GROUND_WEIGHTS = {(0, 6): 7.353131185149001, (0, 1): 9.31844015634196, (0, 3): 7.323866608243338, (0, 7): 8.72105946770584, (0, 18): 5.3602377955289455, (0, 20): 3.4272044817539182, (1, 5): 9.060232078635059, (1, 13): 4.810404167779006, (1, 19): 15.996843264216896, (2, 20): 12.771881766366505, (2, 22): 7.874729207249334, (2, 5): 3.1538077881440065, (4, 7): 3.719238867415723, (4, 12): 8.668804530279267, (4, 6): 7.705670368024646, (4, 23): 6.105882480301487, (4, 200): 6.739461808343224, (5, 14): 6.720189493169476, (5, 18): 10.19959150428705, (6, 15): 12.100866573131565, (6, 13): 8.815423729190007, (7, 13): 1.2922169446024263, (7, 21): 6.276125013451315, (8, 18): 9.130685638165014, (9, 12): 7.62669045784963, (9, 18): 9.563924600711712, (9, 20): 13.732027182275628, (9, 10): 6.199050585242396, (9, 22): 2.6441062010734724, (10, 13): 10.475050064300758, (11, 20): 4.705906641777277, (11, 17): 5.468029935386338, (11, 21): 12.238021779356075, (11, 23): 3.5805513238487876, (12, 15): 11.591043816596247, (13, 17): 5.582042621277376, (13, 16): 3.0179629260896546, (13, 21): 2.1226380172949133, (14, 20): 8.227544846955169, (15, 22): 8.010315855473914, (16, 21): 4.36651730677047, (18, 21): 9.948129697483926, (19, 22): 9.852166067691511, (19, 23): 1}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.61210809207785, 'r1': 8.809167381417078, 'r2': 7.171361885299295, 'r3': 9.140644877141725, 'r4': 5.440964213524074, 'r5': 7.957344187408873, 'r6': 6.0388547118203455, 'r7': 8.029244313513122}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 6.869885087508089, 'o1': 6.183323477988073, 'o2': 8.520342751949917, 'o3': 7.368263537001065, 'o4': 6.977245730548404, 'o5': 0.7949651879130188, 'o6': 8.098852423234266, 'o7': 9.140644877141725, 'o8': 7.42487558208129, 'o9': 5.821061700119928, 'o10': 9.140644877141725, 'o11': 2.5475002910533053, 'o12': 8.231110306941607, 'o13': 8.17378630507713, 'o14': 9.140644877141725, 'o15': 8.008528030480152, 'o16': 7.136050876788485, 'o17': 9.140644877141725, 'o18': 6.392403835428505, 'o19': 7.407916019288981, 'o20': 6.924505618479737, 'o21': 5.359657655278453}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13', 'o14', 'o15'], 'type3': ['o16', 'o17', 'o18', 'o19', 'o20'], 'type4': ['o21']}

def ResetState():
    state.loc = { 'r0': 19, 'r1': 12, 'r2': 5, 'r3': 11, 'r4': 4, 'r5': 13, 'r6': 14, 'r7': 15, 'm0': 16, 'fixer0': 3, 'fixer1': 9, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 18, 'o1': 21, 'o2': 11, 'o3': 4, 'o4': 20, 'o5': 1, 'o6': 5, 'o7': 1, 'o8': 1, 'o9': 18, 'o10': 16, 'o11': 18, 'o12': 20, 'o13': 21, 'o14': 21, 'o15': 12, 'o16': 17, 'o17': 4, 'o18': 23, 'o19': 1, 'o20': 5, 'o21': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 10}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    40: [['order', 'type0', 200]],
    32: [['order', 'type0', 200]],
}
eventsEnv = {
}