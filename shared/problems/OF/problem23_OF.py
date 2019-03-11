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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 0}

rv.GROUND_EDGES = {0: [5, 10, 11, 2, 13, 200], 1: [3, 9, 10, 11], 2: [0, 3, 11], 3: [2, 10, 11, 1, 7, 12], 4: [5, 6, 10, 12, 7], 5: [0, 4], 6: [4, 13, 9], 7: [3, 4, 11, 8, 9], 8: [7, 9, 11], 9: [1, 6, 7, 8, 10], 10: [1, 9, 0, 3, 4], 11: [1, 2, 8, 13, 0, 3, 7], 12: [3, 4], 13: [0, 6, 11], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 5): 17.51609268632182, (0, 10): 7.884634788603514, (0, 11): 13.489499526827036, (0, 2): 10.518870053131668, (0, 13): 10.460553692754608, (0, 200): 10.371350156945663, (1, 3): 9.392162844973093, (1, 9): 6.478537734141194, (1, 10): 1, (1, 11): 6.458496474876803, (2, 3): 6.3570693398858555, (2, 11): 10.384422242849354, (3, 10): 8.206744148650152, (3, 11): 5.993951897935757, (3, 7): 18.511374648647497, (3, 12): 2.7350577054785843, (4, 5): 7.344047160943106, (4, 6): 8.564542987961344, (4, 10): 14.049939838654982, (4, 12): 12.1210317369504, (4, 7): 5.45030487373781, (6, 13): 6.705842781160037, (6, 9): 14.295415495742427, (7, 11): 1, (7, 8): 10.461721955930301, (7, 9): 11.140474247965859, (8, 9): 2.8797163606640304, (8, 11): 12.07763492056262, (9, 10): 3.7302171355395046, (11, 13): 1}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 12.075444647726997, 'r1': 9.502318374818913, 'r2': 9.13216209020689, 'r3': 5.765522234355425, 'r4': 9.133293648200109, 'r5': 7.443422742400806, 'r6': 7.840891109661572}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29']
rv.OBJ_WEIGHT = {'o0': 6.28942248972408, 'o1': 6.499954174578134, 'o2': 7.641545817274985, 'o3': 6.039462822554535, 'o4': 8.967956367577093, 'o5': 9.924858165309404, 'o6': 5.633814048063771, 'o7': 10.355588298378915, 'o8': 6.569867449888267, 'o9': 7.4071830195081585, 'o10': 6.532997017136922, 'o11': 7.363848020424267, 'o12': 8.01388154793993, 'o13': 9.633130162804232, 'o14': 4.955318633244556, 'o15': 8.612029035352245, 'o16': 4.8307795098031985, 'o17': 5.710568690292874, 'o18': 4.159110129702086, 'o19': 6.178166033317754, 'o20': 12.075444647726997, 'o21': 8.616942956050035, 'o22': 5.55565909507672, 'o23': 8.734519613387311, 'o24': 10.521792205371549, 'o25': 5.665924289356424, 'o26': 7.820987926148169, 'o27': 8.443278430257731, 'o28': 5.885267461372635, 'o29': 8.664423282568508}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21', 'o22', 'o23'], 'type5': ['o24', 'o25', 'o26', 'o27', 'o28', 'o29']}

def ResetState():
    state.loc = { 'r0': 7, 'r1': 13, 'r2': 10, 'r3': 13, 'r4': 1, 'r5': 0, 'r6': 8, 'm0': 9, 'm1': 13, 'm2': 13, 'm3': 9, 'm4': 4, 'fixer0': 11, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 10, 'o2': 4, 'o3': 10, 'o4': 13, 'o5': 5, 'o6': 6, 'o7': 13, 'o8': 1, 'o9': 3, 'o10': 6, 'o11': 3, 'o12': 7, 'o13': 9, 'o14': 9, 'o15': 6, 'o16': 8, 'o17': 11, 'o18': 9, 'o19': 3, 'o20': 2, 'o21': 9, 'o22': 1, 'o23': 12, 'o24': 8, 'o25': 10, 'o26': 5, 'o27': 2, 'o28': 9, 'o29': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'fixer0': False}
    state.numUses = {'m0': 11, 'm1': 6, 'm2': 10, 'm3': 12, 'm4': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    6: [['order', 'type0', 200]],
    19: [['order', 'type0', 200]],
}
eventsEnv = {
}