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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 3.062247369392921}

rv.GROUND_EDGES = {0: [1, 2, 4, 5], 1: [0], 2: [3, 4, 5, 0, 6, 200], 3: [2, 4], 4: [0, 2, 3], 5: [0, 2, 6], 6: [2, 5], 200: [2]}
rv.GROUND_WEIGHTS = {(0, 1): 12.225484897724979, (0, 2): 14.52249790516765, (0, 4): 7.134349277185606, (0, 5): 10.239810585169945, (2, 3): 4.318579204980312, (2, 4): 9.999382956554646, (2, 5): 13.567045812075127, (2, 6): 8.652388583435869, (2, 200): 10.610174760878966, (3, 4): 5.1429391039201775, (5, 6): 9.352952264929028}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']
rv.ROBOT_CAPACITY = {'r0': 7.562109149576021, 'r1': 10.183547817362761, 'r2': 6.6455727701179095, 'r3': 11.80664882896501, 'r4': 5.709832359293099, 'r5': 6.421330844979185, 'r6': 5.958666516386799}
rv.MACHINES = ['m0', 'm1', 'm2', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 7.923397080664551, 'o1': 5.180777858058828, 'o2': 5.648060012612982, 'o3': 7.548767237764681, 'o4': 6.090128012453639, 'o5': 8.188628545085805, 'o6': 4.349770981981047, 'o7': 6.580763818020844, 'o8': 4.78219377708151, 'o9': 6.5810269180432215, 'o10': 11.80664882896501, 'o11': 3.4098585928120384, 'o12': 8.532731181500635, 'o13': 4.398744609728936, 'o14': 11.80664882896501, 'o15': 7.620817672543403, 'o16': 7.829471011509058, 'o17': 6.874223400339869, 'o18': 5.862504636699303, 'o19': 5.786220174933955, 'o20': 5.85960132339654, 'o21': 6.626888084251089}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5'], 'type2': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16'], 'type4': ['o17', 'o18', 'o19', 'o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 6, 'r2': 3, 'r3': 6, 'r4': 5, 'r5': 4, 'r6': 4, 'm0': 0, 'm1': 6, 'm2': 5, 'fixer0': 2, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 0, 'o2': 5, 'o3': 1, 'o4': 4, 'o5': 4, 'o6': 1, 'o7': 2, 'o8': 6, 'o9': 1, 'o10': 6, 'o11': 4, 'o12': 1, 'o13': 6, 'o14': 1, 'o15': 6, 'o16': 6, 'o17': 4, 'o18': 6, 'o19': 1, 'o20': 5, 'o21': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'fixer0'": False}
    state.numUses = {'m0': 13, 'm1': 6, 'm2': 11, 'fixer0': 1}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    8: [['order', 'type0', 200]],
    15: [['order', 'type0', 200]],
    11: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
    10: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    3: [['order', 'type3', 200]],
    9: [['order', 'type3', 200]],
    5: [['order', 'type3', 200]],
    6: [['order', 'type3', 200]],
    17: [['order', 'type3', 200]],
    4: [['order', 'type4', 200]],
}
eventsEnv = {
}