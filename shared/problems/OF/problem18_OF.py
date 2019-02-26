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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 3.1968202694426284}

rv.GROUND_EDGES = {0: [2, 7], 1: [3, 5, 8, 11, 6, 200], 2: [0, 3, 8], 3: [2, 5, 8, 9, 11, 1, 10], 4: [6, 8], 5: [3, 1], 6: [1, 4], 7: [0], 8: [2, 1, 3, 4], 9: [11, 3, 200], 10: [3], 11: [3, 1, 9], 200: [1, 9]}
rv.GROUND_WEIGHTS = {(0, 2): 7.308160749640605, (0, 7): 2.511497535172401, (1, 3): 13.290129299242928, (1, 5): 5.59056396192835, (1, 8): 11.20000445335291, (1, 11): 7.597923806400614, (1, 6): 8.114507234854049, (1, 200): 5.515325499584287, (2, 3): 7.382397192547968, (2, 8): 11.42076323028146, (3, 5): 4.862451507729332, (3, 8): 5.121808936247424, (3, 9): 12.369692958787319, (3, 11): 6.045965402853955, (3, 10): 10.054765824290802, (4, 6): 6.87492982919788, (4, 8): 1, (9, 11): 10.295639398298128, (9, 200): 4.766605010143325}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']
rv.ROBOT_CAPACITY = {'r0': 6.312399593008837, 'r1': 11.132272538259754, 'r2': 10.765705299429705, 'r3': 6.096714458258532, 'r4': 7.357948716655834, 'r5': 6.65942636272006, 'r6': 8.466473925781747, 'r7': 7.519259745476766, 'r8': 8.964728214969416}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30', 'o31', 'o32', 'o33', 'o34']
rv.OBJ_WEIGHT = {'o0': 10.569714746905246, 'o1': 7.2413575292655885, 'o2': 7.307911231445069, 'o3': 8.575620247485432, 'o4': 7.731539290630871, 'o5': 6.423913788633323, 'o6': 5.554953546006604, 'o7': 7.596993949593041, 'o8': 9.509357515201046, 'o9': 8.667660762750867, 'o10': 5.057263122554066, 'o11': 4.830777811693064, 'o12': 4.687657455747994, 'o13': 10.130995216021205, 'o14': 4.435900133944397, 'o15': 6.214755429417144, 'o16': 8.827238559470478, 'o17': 6.819447743721663, 'o18': 7.542733169252984, 'o19': 6.057305618853662, 'o20': 5.873800463969207, 'o21': 5.516326429750675, 'o22': 6.7987640977834065, 'o23': 9.445832923286822, 'o24': 4.178443593726364, 'o25': 9.823621637068948, 'o26': 8.649773316746039, 'o27': 6.323854404627506, 'o28': 9.33030976386369, 'o29': 3.4131444490802862, 'o30': 4.542933765879282, 'o31': 6.85546469254435, 'o32': 7.377245899591184, 'o33': 7.586881016332531, 'o34': 9.602203052077506}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14', 'o15'], 'type3': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22'], 'type4': ['o23', 'o24', 'o25', 'o26', 'o27', 'o28'], 'type5': ['o29', 'o30', 'o31', 'o32', 'o33', 'o34']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 9, 'r2': 11, 'r3': 6, 'r4': 9, 'r5': 5, 'r6': 11, 'r7': 9, 'r8': 11, 'm0': 2, 'fixer0': 6, 'fixer1': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK, 'o31': UNK, 'o32': UNK, 'o33': UNK, 'o34': UNK,}
    state.storedLoc = {'o0': 9, 'o1': 5, 'o2': 10, 'o3': 1, 'o4': 9, 'o5': 1, 'o6': 1, 'o7': 3, 'o8': 7, 'o9': 11, 'o10': 11, 'o11': 0, 'o12': 8, 'o13': 5, 'o14': 2, 'o15': 3, 'o16': 3, 'o17': 1, 'o18': 1, 'o19': 11, 'o20': 0, 'o21': 3, 'o22': 10, 'o23': 0, 'o24': 2, 'o25': 2, 'o26': 1, 'o27': 6, 'o28': 1, 'o29': 4, 'o30': 0, 'o31': 11, 'o32': 3, 'o33': 4, 'o34': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'m0'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 13, 'fixer0': 12, 'fixer1': 9}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    6: [['order', 'type0', 200]],
    26: [['order', 'type0', 200]],
    27: [['order', 'type0', 200]],
    47: [['order', 'type1', 200]],
    43: [['order', 'type1', 200]],
    46: [['order', 'type1', 200]],
    16: [['order', 'type1', 200]],
    24: [['order', 'type2', 200]],
    22: [['order', 'type2', 200]],
    15: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
    1: [['order', 'type2', 200]],
    23: [['order', 'type3', 200]],
    44: [['order', 'type3', 200]],
    29: [['order', 'type3', 200]],
    41: [['order', 'type3', 200]],
    8: [['order', 'type3', 200]],
    9: [['order', 'type3', 200]],
    20: [['order', 'type3', 200]],
    37: [['order', 'type4', 200]],
    35: [['order', 'type4', 200]],
    38: [['order', 'type5', 200]],
    2: [['order', 'type5', 200]],
    17: [['order', 'type5', 200]],
}
eventsEnv = {
}