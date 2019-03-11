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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [4, 3, 6], 1: [2, 4, 6, 8], 2: [1, 8, 9, 7, 200], 3: [0, 5, 6, 7, 200], 4: [8, 9, 0, 1, 5], 5: [4, 6, 8, 9, 3, 7], 6: [0, 1, 3, 5], 7: [2, 5, 3, 9], 8: [1, 2, 4, 5], 9: [5, 7, 2, 4], 200: [2, 3]}
rv.GROUND_WEIGHTS = {(0, 4): 11.016630380893066, (0, 3): 9.911992954187781, (0, 6): 7.782021368685181, (1, 2): 10.203282088352827, (1, 4): 5.580604996781457, (1, 6): 14.549532263754, (1, 8): 13.746158237696445, (2, 8): 4.858695834743381, (2, 9): 2.817230326231214, (2, 7): 10.975099647109266, (2, 200): 9.182306424177135, (3, 5): 7.910388150858101, (3, 6): 17.091056752257263, (3, 7): 7.27327385555623, (3, 200): 1, (4, 8): 9.669368110845054, (4, 9): 3.7620894900242083, (4, 5): 7.287924561290217, (5, 6): 8.992928470029934, (5, 8): 1, (5, 9): 6.265702728340308, (5, 7): 18.61889044407957, (7, 9): 4.390879356574713}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1,  'r15': rv.FACTORY1,  'r16': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.461872793719749, 'r1': 9.493766210080455, 'r2': 7.4891442968203386, 'r3': 7.782259617386458, 'r4': 11.930032053696475, 'r5': 7.657523015072865, 'r6': 7.642526038479937, 'r7': 6.825743144239262, 'r8': 11.946108552113904, 'r9': 9.546758428787134, 'r10': 9.167472742357862, 'r11': 6.397955607330745, 'r12': 7.231826818405738, 'r13': 6.964587700062408, 'r14': 9.55342253905829, 'r15': 7.644966026771239, 'r16': 7.477965810814241}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
rv.OBJ_WEIGHT = {'o0': 4.208670683341454, 'o1': 7.89064277331158, 'o2': 4.452857047994039, 'o3': 6.554517750008205, 'o4': 8.924769048000584, 'o5': 6.931702276824684, 'o6': 2.6789059530786137, 'o7': 6.623777564977624, 'o8': 5.172079430537438, 'o9': 3.783243321182992, 'o10': 4.929852689801976, 'o11': 7.223075699800377, 'o12': 5.04422301106022, 'o13': 3.3387963535471137, 'o14': 7.537301379788945}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 2, 'r2': 9, 'r3': 0, 'r4': 4, 'r5': 7, 'r6': 0, 'r7': 2, 'r8': 8, 'r9': 3, 'r10': 0, 'r11': 3, 'r12': 7, 'r13': 1, 'r14': 6, 'r15': 4, 'r16': 8, 'm0': 5, 'm1': 5, 'm2': 9, 'm3': 8, 'm4': 3, 'm5': 7, 'm6': 7, 'm7': 7, 'fixer0': 3, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 1, 'o2': 5, 'o3': 7, 'o4': 8, 'o5': 2, 'o6': 7, 'o7': 8, 'o8': 5, 'o9': 3, 'o10': 5, 'o11': 4, 'o12': 4, 'o13': 4, 'o14': 8}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'r16': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'r15': False, 'r16': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False}
    state.numUses = {'m0': 12, 'm1': 7, 'm2': 6, 'm3': 12, 'm4': 8, 'm5': 11, 'm6': 11, 'm7': 4}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    7: [['order', 'type0', 200]],
    9: [['order', 'type2', 200]],
}
eventsEnv = {
}