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
rv.SHIPPING_DOC = {rv.FACTORY1: 3}

rv.GROUND_EDGES = {0: [2, 1, 5, 14, 200], 1: [0, 8], 2: [9, 12, 0, 10], 3: [4, 15, 200, 11], 4: [5, 6, 8, 11, 12, 3], 5: [0, 7, 10, 4], 6: [7, 10, 4, 9, 12], 7: [12, 5, 6, 8], 8: [1, 7, 4, 15], 9: [6, 12, 2], 10: [2, 13, 5, 6], 11: [3, 13, 4], 12: [2, 6, 14, 4, 7, 9, 15], 13: [14, 10, 11], 14: [0, 12, 13], 15: [8, 12, 3], 200: [0, 3]}
rv.GROUND_WEIGHTS = {(0, 2): 2.4443449373977577, (0, 1): 10.81158778970418, (0, 5): 15.293975049027248, (0, 14): 3.7644581768565537, (0, 200): 5.9553640901749425, (1, 8): 10.855560857163617, (2, 9): 2.906988226398462, (2, 12): 6.185330175087882, (2, 10): 8.63399954738644, (3, 4): 1.9897373858272598, (3, 15): 16.535453806029594, (3, 200): 9.268898163448787, (3, 11): 15.174900346336965, (4, 5): 4.878154302101432, (4, 6): 15.732728781147369, (4, 8): 9.196798503739624, (4, 11): 8.149577621106147, (4, 12): 4.409341939967321, (5, 7): 10.921610958417492, (5, 10): 3.4307889139891925, (6, 7): 7.756882954399897, (6, 10): 11.287036653021163, (6, 9): 6.760793126690096, (6, 12): 5.169394431609968, (7, 12): 11.416092876057927, (7, 8): 9.86174607536921, (8, 15): 6.925381929333458, (9, 12): 12.495771603753631, (10, 13): 7.6087378496583655, (11, 13): 7.020471605466178, (12, 14): 6.145368611024751, (12, 15): 9.853445190601224, (13, 14): 2.942754991379812}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.722251338249507, 'r1': 7.140653534230397, 'r2': 7.668705408354271, 'r3': 8.269649316779905, 'r4': 11.079157085190403, 'r5': 10.998075545360079, 'r6': 10.313960601359877, 'r7': 9.666112648253817, 'r8': 5.780680840920478}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30', 'o31', 'o32', 'o33', 'o34', 'o35', 'o36', 'o37', 'o38']
rv.OBJ_WEIGHT = {'o0': 9.953798874807237, 'o1': 7.332502984717527, 'o2': 5.25513913704272, 'o3': 5.217368748431563, 'o4': 9.83335106235117, 'o5': 6.495098258521456, 'o6': 7.618089664241138, 'o7': 8.731945810071712, 'o8': 9.2218889264762, 'o9': 5.064931243142206, 'o10': 8.585129852167846, 'o11': 3.8268437021735044, 'o12': 9.42880098390416, 'o13': 4.817098597193873, 'o14': 4.636108827212582, 'o15': 6.118604689274754, 'o16': 8.0208787640598, 'o17': 7.13699964755974, 'o18': 5.745923202050966, 'o19': 4.1829814351503565, 'o20': 7.451029322336369, 'o21': 10.84073544112712, 'o22': 9.088093270066377, 'o23': 10.484204783734311, 'o24': 9.733223767386344, 'o25': 4.62055222722765, 'o26': 4.351964303757319, 'o27': 8.734032532806975, 'o28': 5.298660735373504, 'o29': 7.605980631410813, 'o30': 7.9024889699982515, 'o31': 6.866024282568018, 'o32': 9.576330522319278, 'o33': 9.755059692770834, 'o34': 7.75597712250797, 'o35': 10.57050280914066, 'o36': 7.145120859122435, 'o37': 11.079157085190403, 'o38': 6.763428315258129}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15'], 'type4': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23'], 'type5': ['o24', 'o25', 'o26', 'o27', 'o28'], 'type6': ['o29', 'o30', 'o31', 'o32', 'o33', 'o34', 'o35'], 'type7': ['o36', 'o37', 'o38']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 5, 'r2': 7, 'r3': 2, 'r4': 15, 'r5': 13, 'r6': 3, 'r7': 0, 'r8': 10, 'm0': 9, 'fixer0': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK, 'o31': UNK, 'o32': UNK, 'o33': UNK, 'o34': UNK, 'o35': UNK, 'o36': UNK, 'o37': UNK, 'o38': UNK,}
    state.storedLoc = {'o0': 11, 'o1': 2, 'o2': 2, 'o3': 3, 'o4': 5, 'o5': 9, 'o6': 0, 'o7': 1, 'o8': 0, 'o9': 6, 'o10': 8, 'o11': 11, 'o12': 5, 'o13': 2, 'o14': 6, 'o15': 5, 'o16': 8, 'o17': 11, 'o18': 11, 'o19': 10, 'o20': 12, 'o21': 8, 'o22': 15, 'o23': 0, 'o24': 4, 'o25': 7, 'o26': 12, 'o27': 6, 'o28': 7, 'o29': 13, 'o30': 3, 'o31': 13, 'o32': 14, 'o33': 10, 'o34': 12, 'o35': 9, 'o36': 7, 'o37': 5, 'o38': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    10: [['order', 'type1', 200]],
    22: [['order', 'type1', 200]],
}
eventsEnv = {
}