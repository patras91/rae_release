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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 8.500470013257853}

rv.GROUND_EDGES = {0: [13, 2, 9, 11, 12, 16], 1: [16, 5, 14], 2: [0, 5], 3: [4, 11, 15], 4: [9, 13, 3, 7, 14], 5: [1, 2, 11, 13, 15, 10], 6: [10, 11, 13], 7: [4, 12, 13], 8: [17, 14], 9: [0, 4, 12, 14], 10: [5, 12, 17, 6], 11: [0, 3, 5, 6, 200], 12: [0, 9, 7, 10, 200], 13: [6, 0, 4, 5, 7], 14: [1, 4, 8, 9, 15, 17, 200], 15: [3, 5, 14], 16: [0, 1, 200], 17: [8, 14, 10], 200: [11, 12, 14, 16]}
rv.GROUND_WEIGHTS = {(0, 13): 11.736741360037406, (0, 2): 4.658925280380963, (0, 9): 7.658850959901311, (0, 11): 7.595578138675205, (0, 12): 7.250730283275391, (0, 16): 2.2532964511580884, (1, 16): 10.208454420277555, (1, 5): 1, (1, 14): 10.701170765342543, (2, 5): 7.083541275021074, (3, 4): 3.571037608405799, (3, 11): 8.01734032985061, (3, 15): 5.090048049338224, (4, 9): 6.460581339032283, (4, 13): 9.882726145996068, (4, 7): 8.714348638893295, (4, 14): 12.314506796190862, (5, 11): 8.980840184336017, (5, 13): 3.740212586580526, (5, 15): 7.2134192911016655, (5, 10): 8.414040710622514, (6, 10): 11.200944937432432, (6, 11): 9.092153839698655, (6, 13): 1.6974768337024155, (7, 12): 11.059673311272105, (7, 13): 3.097013601535018, (8, 17): 14.284530081001162, (8, 14): 8.529720804398993, (9, 12): 13.381318469782444, (9, 14): 13.865377563174157, (10, 12): 4.824052968429575, (10, 17): 5.255614084263437, (11, 200): 7.503048984986565, (12, 200): 8.427983392825503, (14, 15): 11.507621645493806, (14, 17): 2.9742262752580926, (14, 200): 10.294497135309445, (16, 200): 16.17967759583273}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']
rv.ROBOT_CAPACITY = {'r0': 7.578964366132872, 'r1': 9.798232422425484, 'r2': 6.280899512506878, 'r3': 8.36660531181772, 'r4': 8.384338131817856, 'r5': 6.612122891219918, 'r6': 2.740418937607977, 'r7': 8.04762236529057, 'r8': 7.5318052175941625}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 9.349290777660325, 'o1': 6.512941398109374, 'o2': 6.922745363915446, 'o3': 6.199533456369855, 'o4': 7.1006788290471405, 'o5': 6.568903174329047, 'o6': 5.519366719757468, 'o7': 3.977467212026878, 'o8': 8.985702695910835, 'o9': 8.505514329230337, 'o10': 5.746746745738408, 'o11': 6.644759765120842, 'o12': 6.171082340937414, 'o13': 8.045865641384657, 'o14': 6.519556696411677, 'o15': 9.798232422425484, 'o16': 7.64089625235345, 'o17': 7.939141678256888, 'o18': 6.424960331926756, 'o19': 8.52297897917184, 'o20': 9.718817570352567, 'o21': 7.418507203631109, 'o22': 6.672906306763275}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14', 'o15'], 'type3': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 2, 'r1': 0, 'r2': 13, 'r3': 0, 'r4': 12, 'r5': 12, 'r6': 9, 'r7': 2, 'r8': 0, 'm0': 4, 'm1': 11, 'm2': 11, 'm3': 9, 'fixer0': 13, 'fixer1': 8, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 11, 'o1': 15, 'o2': 9, 'o3': 6, 'o4': 14, 'o5': 1, 'o6': 3, 'o7': 7, 'o8': 13, 'o9': 9, 'o10': 16, 'o11': 5, 'o12': 1, 'o13': 10, 'o14': 13, 'o15': 3, 'o16': 9, 'o17': 2, 'o18': 15, 'o19': 7, 'o20': 11, 'o21': 16, 'o22': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 12, 'm1': 9, 'm2': 10, 'm3': 6, 'fixer0': 9, 'fixer1': 8}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    16: [['order', 'type0', 200]],
    1: [['order', 'type0', 200]],
    13: [['order', 'type0', 200]],
    5: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
    10: [['order', 'type0', 200]],
    8: [['order', 'type1', 200]],
    18: [['order', 'type1', 200]],
    4: [['order', 'type1', 200]],
    17: [['order', 'type1', 200]],
    6: [['order', 'type2', 200]],
    11: [['order', 'type3', 200]],
}
eventsEnv = {
}