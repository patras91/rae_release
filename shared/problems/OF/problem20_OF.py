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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [4, 16, 1, 9, 13, 17], 1: [0, 10, 3], 2: [14, 15, 3], 3: [1, 2, 14, 200], 4: [14, 18, 0, 8, 10], 5: [9, 8, 11], 6: [10, 15], 7: [16, 10, 13], 8: [4, 5, 18, 10], 9: [0, 5, 11, 14], 10: [4, 7, 8, 16, 17, 18, 1, 6, 12], 11: [5, 9, 13, 18], 12: [10, 14], 13: [0, 7, 11, 15], 14: [3, 9, 17, 2, 4, 12], 15: [2, 13, 6, 200], 16: [10, 0, 7], 17: [0, 10, 14], 18: [11, 4, 8, 10], 200: [3, 15]}
rv.GROUND_WEIGHTS = {(0, 4): 6.0283994419903015, (0, 16): 5.918785395584372, (0, 1): 8.980886023046043, (0, 9): 2.2200289851903747, (0, 13): 4.780723067801385, (0, 17): 9.593152439825735, (1, 10): 3.79095868247268, (1, 3): 13.706440712768792, (2, 14): 7.074004474666171, (2, 15): 2.849892908564483, (2, 3): 17.590718718826793, (3, 14): 5.478359047076708, (3, 200): 1.1217501425356078, (4, 14): 7.518313060547072, (4, 18): 13.48737190842564, (4, 8): 9.077847178413888, (4, 10): 2.0042583802578795, (5, 9): 4.9572735193598785, (5, 8): 12.40150374387013, (5, 11): 13.603168198522336, (6, 10): 5.521025355634023, (6, 15): 2.439369700620449, (7, 16): 11.53779209763174, (7, 10): 4.417070577653529, (7, 13): 8.365493363512037, (8, 18): 5.311981554409556, (8, 10): 9.932146962945065, (9, 11): 6.869525890735448, (9, 14): 13.593124614610861, (10, 16): 11.209391391530081, (10, 17): 3.9814148423061075, (10, 18): 9.3118998149505, (10, 12): 1.5579785605993104, (11, 13): 7.294457090831105, (11, 18): 11.049674291646898, (12, 14): 1.1560358903355317, (13, 15): 8.188202108100059, (14, 17): 15.121074737354707, (15, 200): 7.824556920965627}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.9193410895784, 'r1': 11.234879313121123, 'r2': 7.941775486187646, 'r3': 10.813728896018173, 'r4': 9.575404483808528, 'r5': 7.319799126515921, 'r6': 7.809475937799704, 'r7': 9.859465839146534, 'r8': 6.084624664260046}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 7.854514081976849, 'o1': 3.9707446822992685, 'o2': 6.9886241179540605, 'o3': 8.797202750530328, 'o4': 8.874039609702562, 'o5': 6.2109277806151155, 'o6': 7.296782415781403, 'o7': 5.194229457810247, 'o8': 9.377117198247415, 'o9': 5.7455923433287515, 'o10': 4.488951222755606, 'o11': 7.0000505685381205, 'o12': 6.094667709616788, 'o13': 4.566730166546355, 'o14': 4.154660973362983, 'o15': 6.891999639674498, 'o16': 5.757351647540732}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12'], 'type2': ['o13', 'o14', 'o15', 'o16']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 1, 'r2': 2, 'r3': 4, 'r4': 6, 'r5': 7, 'r6': 6, 'r7': 3, 'r8': 6, 'm0': 1, 'm1': 0, 'm2': 14, 'fixer0': 10, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 6, 'o1': 1, 'o2': 3, 'o3': 12, 'o4': 6, 'o5': 18, 'o6': 8, 'o7': 14, 'o8': 1, 'o9': 1, 'o10': 4, 'o11': 16, 'o12': 2, 'o13': 2, 'o14': 15, 'o15': 2, 'o16': 2}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'm1': False, 'm2': False, 'fixer0': False}
    state.numUses = {'m0': 10, 'm1': 10, 'm2': 9}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
    19: [['order', 'type0', 200]],
    17: [['order', 'type0', 200]],
    2: [['order', 'type1', 200]],
    5: [['order', 'type1', 200]],
    6: [['order', 'type2', 200]],
    9: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
    11: [['order', 'type2', 200]],
}
eventsEnv = {
}