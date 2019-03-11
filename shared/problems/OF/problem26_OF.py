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
rv.SHIPPING_DOC = {rv.FACTORY1: 5}

rv.GROUND_EDGES = {0: [19, 4, 12], 1: [7, 17, 19], 2: [10], 3: [5, 10], 4: [0], 5: [6, 16, 23, 3], 6: [10, 5, 11, 15, 23], 7: [22, 1, 15, 20, 21, 200], 8: [12, 23], 9: [13, 19, 22], 10: [14, 21, 2, 3, 6], 11: [6], 12: [0, 8, 16, 17], 13: [9, 22], 14: [20, 23, 10], 15: [6, 7], 16: [12, 22, 5], 17: [12, 1, 18, 200], 18: [17], 19: [1, 9, 0], 20: [7, 14], 21: [7, 10], 22: [9, 13, 7, 16, 23, 200], 23: [6, 22, 5, 8, 14], 200: [7, 17, 22]}
rv.GROUND_WEIGHTS = {(0, 19): 6.28220899212421, (0, 4): 7.252644840762494, (0, 12): 5.979803486105721, (1, 7): 6.232415319579437, (1, 17): 1.558923583513467, (1, 19): 4.761835519312406, (2, 10): 9.151444840319888, (3, 5): 11.176053625404442, (3, 10): 6.16676267209305, (5, 6): 6.735748287844953, (5, 16): 12.193493510237513, (5, 23): 8.460224607201763, (6, 10): 5.695090135525666, (6, 11): 10.917810238467563, (6, 15): 6.642510751252441, (6, 23): 10.164181381334389, (7, 22): 14.244146501665305, (7, 15): 8.96788117351118, (7, 20): 8.690083884476607, (7, 21): 4.841887171664489, (7, 200): 4.391771945137414, (8, 12): 6.981190627142601, (8, 23): 15.60747233269194, (9, 13): 19.19405989041846, (9, 19): 2.4047055594330544, (9, 22): 8.304431205874462, (10, 14): 7.413142009332988, (10, 21): 13.405197097831918, (12, 16): 6.2493372365576825, (12, 17): 10.396143446393122, (13, 22): 13.324327199140063, (14, 20): 5.48914801471215, (14, 23): 5.843283088022924, (16, 22): 6.028609217801458, (17, 18): 1, (17, 200): 9.323935768739378, (22, 23): 5.3737986750391675, (22, 200): 2.0242996365726587}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.383330537389426, 'r1': 5.48715850415339}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19']
rv.OBJ_WEIGHT = {'o0': 6.160643907530134, 'o1': 5.402324938983506, 'o2': 6.383330537389426, 'o3': 2.118759325112512, 'o4': 6.383330537389426, 'o5': 4.963728366952715, 'o6': 6.383330537389426, 'o7': 6.383330537389426, 'o8': 6.383330537389426, 'o9': 6.383330537389426, 'o10': 6.383330537389426, 'o11': 2.8499589887416725, 'o12': 6.383330537389426, 'o13': 6.383330537389426, 'o14': 6.383330537389426, 'o15': 6.383330537389426, 'o16': 6.383330537389426, 'o17': 6.383330537389426, 'o18': 6.383330537389426, 'o19': 6.383330537389426}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19']}

def ResetState():
    state.loc = { 'r0': 15, 'r1': 1, 'm0': 18, 'm1': 12, 'm2': 18, 'm3': 9, 'm4': 6, 'm5': 5, 'm6': 21, 'm7': 7, 'm8': 9, 'fixer0': 10, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK,}
    state.storedLoc = {'o0': 6, 'o1': 11, 'o2': 5, 'o3': 15, 'o4': 9, 'o5': 19, 'o6': 7, 'o7': 2, 'o8': 8, 'o9': 14, 'o10': 8, 'o11': 17, 'o12': 16, 'o13': 13, 'o14': 5, 'o15': 4, 'o16': 6, 'o17': 1, 'o18': 20, 'o19': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'fixer0': False}
    state.numUses = {'m0': 11, 'm1': 7, 'm2': 7, 'm3': 11, 'm4': 3, 'm5': 13, 'm6': 9, 'm7': 8, 'm8': 10}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    20: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
}
eventsEnv = {
}