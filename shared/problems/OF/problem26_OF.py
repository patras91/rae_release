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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [3, 4, 6, 13, 2, 5, 7, 12], 1: [5, 6, 13, 15, 4, 200], 2: [0, 15], 3: [10, 14, 0, 6, 200], 4: [1, 7, 0, 14], 5: [0, 1, 8], 6: [3, 0, 1, 10, 13], 7: [0, 4, 15], 8: [5, 10, 14], 9: [10, 15], 10: [3, 6, 8, 15, 9], 11: [15], 12: [0], 13: [6, 0, 1], 14: [4, 8, 3], 15: [2, 7, 9, 1, 10, 11], 200: [1, 3]}
rv.GROUND_WEIGHTS = {(0, 3): 8.693901526457832, (0, 4): 6.083385474280429, (0, 6): 15.02302569416258, (0, 13): 9.117616509389173, (0, 2): 10.710295763087593, (0, 5): 7.593430451886199, (0, 7): 6.908865339800231, (0, 12): 2.3891063379115955, (1, 5): 4.931517620131642, (1, 6): 10.212843571654144, (1, 13): 6.955385068180437, (1, 15): 9.221468413498343, (1, 4): 1, (1, 200): 7.411739265253236, (2, 15): 3.709762345004581, (3, 10): 1, (3, 14): 7.915937657615758, (3, 6): 6.596551683877222, (3, 200): 17.847011170433653, (4, 7): 11.378999798881658, (4, 14): 9.367193396363342, (5, 8): 7.014812427590761, (6, 10): 9.215765428069167, (6, 13): 5.12713376522291, (7, 15): 9.344333998776037, (8, 10): 5.285455082478972, (8, 14): 6.548764497314852, (9, 10): 11.321326817302952, (9, 15): 8.590801058282853, (10, 15): 6.5685026247070715, (11, 15): 8.768310039383016}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.83954908418847, 'r1': 10.712019694880176, 'r2': 10.976976919147551, 'r3': 5.294994997109121, 'r4': 10.22295754159209, 'r5': 7.768539002539065, 'r6': 8.742174210471415, 'r7': 8.06637458360297, 'r8': 2.4502393100652338, 'r9': 8.051397567464262, 'r10': 8.725014839084391, 'r11': 9.893649828056903}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11']
rv.OBJ_WEIGHT = {'o0': 10.20051650685842, 'o1': 3.8265878756654654, 'o2': 8.761568635939087, 'o3': 6.538215269733823, 'o4': 7.77468675596939, 'o5': 5.510084059588531, 'o6': 9.863880910038349, 'o7': 9.93977592696191, 'o8': 7.9487978481381605, 'o9': 2.870831383534184, 'o10': 8.719094321651232, 'o11': 2.2809976417570974}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7'], 'type1': ['o8', 'o9', 'o10'], 'type2': ['o11']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 13, 'r2': 7, 'r3': 12, 'r4': 6, 'r5': 12, 'r6': 14, 'r7': 5, 'r8': 14, 'r9': 13, 'r10': 4, 'r11': 1, 'm0': 7, 'm1': 3, 'm2': 2, 'm3': 4, 'm4': 4, 'm5': 6, 'm6': 5, 'fixer0': 8, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK,}
    state.storedLoc = {'o0': 15, 'o1': 15, 'o2': 4, 'o3': 8, 'o4': 14, 'o5': 14, 'o6': 2, 'o7': 12, 'o8': 6, 'o9': 1, 'o10': 7, 'o11': 11}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 3, 'm1': 12, 'm2': 13, 'm3': 10, 'm4': 9, 'm5': 17, 'm6': 9}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    3: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
}
eventsEnv = {
}