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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [6, 11, 1, 2, 12, 13], 1: [0, 7, 9, 13], 2: [0, 5, 3], 3: [2], 4: [7, 8, 9], 5: [2, 7, 8, 14], 6: [0, 200], 7: [1, 4, 5, 13], 8: [5, 12, 4, 10], 9: [1, 4], 10: [8], 11: [0], 12: [0, 8], 13: [0, 1, 7], 14: [5], 200: [6]}
rv.GROUND_WEIGHTS = {(0, 6): 8.201674748708845, (0, 11): 5.018441849829416, (0, 1): 10.33923226310804, (0, 2): 7.368569298700132, (0, 12): 6.750695259912611, (0, 13): 7.284223656158047, (1, 7): 4.003614244353505, (1, 9): 6.299269760403826, (1, 13): 4.173548088085662, (2, 5): 2.5919727086900473, (2, 3): 4.357744816614396, (4, 7): 10.560028175590418, (4, 8): 3.2625390506449508, (4, 9): 2.84706344652502, (5, 7): 1.4673208348670297, (5, 8): 8.598016983854524, (5, 14): 3.784238781762838, (6, 200): 9.059803568085854, (7, 13): 10.612073941414094, (8, 12): 3.4994103795661813, (8, 10): 9.258635932223159}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.366518837490091, 'r1': 7.928674285736238, 'r2': 5.328120685772711, 'r3': 6.052021491457906}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 3.4358141309119468, 'o1': 7.928674285736238, 'o2': 7.928674285736238, 'o3': 7.928674285736238, 'o4': 4.18848976952699, 'o5': 7.928674285736238, 'o6': 5.236426520540851, 'o7': 7.928674285736238, 'o8': 7.928674285736238, 'o9': 4.912049748974884, 'o10': 7.319080660127743, 'o11': 5.898081372257777, 'o12': 6.607565452109321, 'o13': 6.401343064949728, 'o14': 7.928674285736238, 'o15': 6.007947989995906, 'o16': 5.8799982177173495}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13'], 'type3': ['o14', 'o15', 'o16']}

def ResetState():
    state.loc = { 'r0': 13, 'r1': 7, 'r2': 11, 'r3': 12, 'm0': 9, 'fixer0': 3, 'fixer1': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 11, 'o1': 1, 'o2': 1, 'o3': 13, 'o4': 12, 'o5': 0, 'o6': 3, 'o7': 2, 'o8': 0, 'o9': 4, 'o10': 1, 'o11': 9, 'o12': 13, 'o13': 13, 'o14': 12, 'o15': 0, 'o16': 10}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 7}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    12: [['order', 'type0', 200]],
    15: [['order', 'type0', 200]],
}
eventsEnv = {
}