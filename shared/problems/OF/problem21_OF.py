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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 17}

rv.GROUND_EDGES = {0: [1, 3, 6, 9, 14, 15, 200], 1: [0, 4, 5, 20, 7], 2: [6, 8, 9, 4, 5, 13, 19, 20], 3: [0, 12], 4: [2, 6, 1, 7], 5: [2, 10, 1, 8], 6: [0, 2, 4], 7: [1, 4, 12, 14, 18, 19], 8: [5, 2, 16, 17], 9: [0, 2], 10: [5, 15, 16, 18], 11: [18, 20], 12: [3, 7, 17], 13: [2, 16], 14: [0, 7, 15, 19], 15: [0, 10, 14], 16: [8, 10, 20, 13], 17: [8, 12, 19, 20], 18: [7, 10, 11], 19: [2, 7, 14, 17], 20: [2, 17, 1, 11, 16], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 1): 15.082750891539856, (0, 3): 14.016991624692947, (0, 6): 13.048703116791774, (0, 9): 5.856521138225597, (0, 14): 4.226922464481248, (0, 15): 6.992619397468226, (0, 200): 7.677267461168244, (1, 4): 11.79459260391216, (1, 5): 7.741775962892736, (1, 20): 13.01413841053145, (1, 7): 1, (2, 6): 4.84465368935207, (2, 8): 11.079965624630956, (2, 9): 8.357084265601635, (2, 4): 13.559325996332113, (2, 5): 4.618253564549821, (2, 13): 5.498939525166784, (2, 19): 3.8688563377967142, (2, 20): 6.495053928273521, (3, 12): 12.198620152188107, (4, 6): 2.6762184963847355, (4, 7): 10.079241263803222, (5, 10): 14.20179466987047, (5, 8): 10.894883676385808, (7, 12): 6.059314858671425, (7, 14): 10.17685721205493, (7, 18): 15.894159471170033, (7, 19): 9.908499429841587, (8, 16): 11.304683842701925, (8, 17): 1, (10, 15): 5.673289941838199, (10, 16): 11.13844687060211, (10, 18): 6.748699644704787, (11, 18): 5.889946226652875, (11, 20): 8.469325231590622, (12, 17): 1.9621078371053349, (13, 16): 8.23713207656709, (14, 15): 3.828718763429566, (14, 19): 5.39737530502795, (16, 20): 3.0915063587838345, (17, 19): 13.420584501507935, (17, 20): 4.420598283893849}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.814349353919291, 'r1': 7.218165137473714, 'r2': 13.279791602625583, 'r3': 8.024516744424457, 'r4': 6.86180893885633, 'r5': 4.949549978070279, 'r6': 2.701523046086143, 'r7': 8.138236188829824, 'r8': 8.680805578303831, 'r9': 4.881084928000492, 'r10': 7.56162510729716}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 1.9922181736645523, 'o1': 4.322392695789233, 'o2': 7.436708279453436, 'o3': 9.848979643339382, 'o4': 7.595696129339827, 'o5': 3.7288549734546375, 'o6': 4.975716208637499, 'o7': 7.504447674421816, 'o8': 6.263213552255787, 'o9': 5.51813196362418, 'o10': 6.088270040110251, 'o11': 7.772206932838484, 'o12': 5.052346725657838, 'o13': 11.315044171961492, 'o14': 4.857235485076319, 'o15': 8.759906980628859, 'o16': 4.097879578861081}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7'], 'type2': ['o8'], 'type3': ['o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']}

def ResetState():
    state.loc = { 'r0': 14, 'r1': 9, 'r2': 18, 'r3': 1, 'r4': 17, 'r5': 4, 'r6': 10, 'r7': 3, 'r8': 2, 'r9': 9, 'r10': 7, 'm0': 8, 'm1': 14, 'm2': 7, 'm3': 8, 'fixer0': 19, 'fixer1': 2, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 1, 'o1': 9, 'o2': 7, 'o3': 18, 'o4': 16, 'o5': 7, 'o6': 17, 'o7': 18, 'o8': 9, 'o9': 8, 'o10': 5, 'o11': 2, 'o12': 4, 'o13': 3, 'o14': 16, 'o15': 11, 'o16': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 9, 'm1': 7, 'm2': 10, 'm3': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    5: [['order', 'type0', 200]],
    3: [['order', 'type0', 200]],
}
eventsEnv = {
}