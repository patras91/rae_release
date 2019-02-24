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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9.763932284884039}

rv.GROUND_EDGES = {0: [1, 3, 7], 1: [4, 5, 6, 7, 13, 0, 2, 200], 2: [1, 10, 13], 3: [0, 4, 8], 4: [3, 1, 8, 13], 5: [9, 13, 1, 10, 12, 14], 6: [8, 1], 7: [0, 1], 8: [3, 4, 10, 6, 9, 11], 9: [8, 10, 13, 5, 14], 10: [2, 5, 11, 14, 8, 9], 11: [8, 10], 12: [5], 13: [2, 4, 1, 5, 9, 14], 14: [5, 9, 13, 10], 200: [1]}
rv.GROUND_WEIGHTS = {(0, 1): 15.803236934849073, (0, 3): 4.15810546318945, (0, 7): 6.088776857173395, (1, 4): 10.924357747370022, (1, 5): 7.468538216691355, (1, 6): 7.170415495983177, (1, 7): 11.38979421858949, (1, 13): 5.951403167649747, (1, 2): 5.001730019722283, (1, 200): 4.032935319189109, (2, 10): 14.889395325448822, (2, 13): 3.996384679160598, (3, 4): 4.174887601213262, (3, 8): 8.390815597529375, (4, 8): 7.639929941717603, (4, 13): 11.753370369117384, (5, 9): 6.637357555446098, (5, 13): 4.832851972515362, (5, 10): 12.314737844793935, (5, 12): 6.726369272959458, (5, 14): 10.609777356063141, (6, 8): 7.6375422677853635, (8, 10): 6.004063106791931, (8, 9): 2.227422690924663, (8, 11): 11.90584611793965, (9, 10): 3.864207214571657, (9, 13): 3.8523790267664726, (9, 14): 5.776341972880902, (10, 11): 4.7441977648381695, (10, 14): 2.930422207595181, (13, 14): 3.0406972313272247}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19']
rv.ROBOT_CAPACITY = {'r0': 9.495970531774722, 'r1': 7.992708327491358, 'r2': 7.572489375287689, 'r3': 7.877352883112685, 'r4': 5.653396739012429, 'r5': 9.9373899189322, 'r6': 8.138894530183023, 'r7': 8.72632297077082, 'r8': 7.230297603908782, 'r9': 9.44569269376447, 'r10': 10.850804957203014, 'r11': 6.724382900188777, 'r12': 8.144722842523835, 'r13': 6.596477334535969, 'r14': 7.44555660127011, 'r15': 6.667699914556944, 'r16': 6.188848656392917, 'r17': 9.011749295997946, 'r18': 8.917786016906192, 'r19': 8.030099358369656}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 7.401350144520265, 'o1': 7.05728582995105, 'o2': 7.299146690087002, 'o3': 4.215692654403798, 'o4': 9.810580211287856, 'o5': 10.850804957203014, 'o6': 6.630433849608384, 'o7': 5.542766924536711, 'o8': 5.753222111910393, 'o9': 6.831778686004558, 'o10': 8.498498805758313, 'o11': 6.998480805609671, 'o12': 7.742532546014291, 'o13': 3.0929758125687843, 'o14': 6.077090221942735, 'o15': 7.837408279500107, 'o16': 5.501282875470804}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3', 'o4', 'o5'], 'type2': ['o6', 'o7', 'o8'], 'type3': ['o9', 'o10', 'o11'], 'type4': ['o12', 'o13', 'o14', 'o15', 'o16']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 10, 'r2': 12, 'r3': 3, 'r4': 1, 'r5': 2, 'r6': 13, 'r7': 5, 'r8': 14, 'r9': 4, 'r10': 5, 'r11': 6, 'r12': 13, 'r13': 5, 'r14': 8, 'r15': 4, 'r16': 9, 'r17': 10, 'r18': 11, 'r19': 2, 'm0': 4, 'fixer0': 7, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 1, 'o1': 2, 'o2': 4, 'o3': 9, 'o4': 13, 'o5': 13, 'o6': 12, 'o7': 3, 'o8': 0, 'o9': 4, 'o10': 11, 'o11': 10, 'o12': 12, 'o13': 6, 'o14': 6, 'o15': 14, 'o16': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'r16': NIL, 'r17': NIL, 'r18': NIL, 'r19': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'r14'": False, "'r15'": False, "'r16'": False, "'r17'": False, "'r18'": False, "'r19'": False, "'m0'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 11, 'fixer0': 6, 'fixer1': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    17: [['order', 'type0', 200]],
    13: [['order', 'type1', 200]],
    19: [['order', 'type1', 200]],
    7: [['order', 'type1', 200]],
    14: [['order', 'type1', 200]],
    3: [['order', 'type1', 200]],
    9: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
    8: [['order', 'type2', 200]],
    15: [['order', 'type4', 200]],
}
eventsEnv = {
}