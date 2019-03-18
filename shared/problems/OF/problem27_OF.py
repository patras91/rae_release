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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 15}

rv.GROUND_EDGES = {0: [5, 1, 10, 11, 15, 16], 1: [0, 5, 6], 2: [9, 19, 10], 3: [10, 13, 14, 19], 4: [13, 16, 5, 9], 5: [1, 4, 13, 0, 20, 200], 6: [1], 7: [19, 20], 8: [12, 200], 9: [4, 15, 2, 12, 18], 10: [0, 2, 3, 17], 11: [0], 12: [9, 13, 20, 8], 13: [21, 3, 4, 5, 12], 14: [3], 15: [0, 200, 9, 20], 16: [0, 4, 21], 17: [10], 18: [9], 19: [3, 2, 7], 20: [5, 15, 7, 12], 21: [16, 13], 200: [5, 8, 15]}
rv.GROUND_WEIGHTS = {(0, 5): 6.158640044951195, (0, 1): 5.481244128308817, (0, 10): 6.114555546715497, (0, 11): 6.553336145370623, (0, 15): 9.981751917306138, (0, 16): 7.447469333304243, (1, 5): 11.652065769837758, (1, 6): 2.7807550025702232, (2, 9): 12.046900141513992, (2, 19): 7.802528024955645, (2, 10): 11.487784001870219, (3, 10): 10.727212513400067, (3, 13): 3.3604737945758325, (3, 14): 4.422659287339135, (3, 19): 8.188728292276755, (4, 13): 3.5737183674377277, (4, 16): 1.5428661157675938, (4, 5): 7.4520850236286, (4, 9): 5.299307826342733, (5, 13): 9.174423219922746, (5, 20): 17.237291428962177, (5, 200): 5.470522331325098, (7, 19): 3.1694366619958645, (7, 20): 6.398252511909472, (8, 12): 9.430313818336483, (8, 200): 10.450531995816402, (9, 15): 9.640188108545543, (9, 12): 1, (9, 18): 5.420027564204107, (10, 17): 3.524655899763575, (12, 13): 15.42666784998751, (12, 20): 5.212071607029463, (13, 21): 9.025461796306585, (15, 200): 7.828620207996171, (15, 20): 9.364885904371052, (16, 21): 9.711742531044768}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 9.485396359574736, 'r1': 7.803371198371937, 'r2': 6.260300567955632, 'r3': 6.821030234120105, 'r4': 7.844659822089547, 'r5': 10.71186831640167, 'r6': 8.352424048552479, 'r7': 6.464583457345206, 'r8': 7.0447642059985975, 'r9': 9.090715199599375, 'r10': 10.504046019980633, 'r11': 11.137649641025348}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13']
rv.OBJ_WEIGHT = {'o0': 8.130393002145388, 'o1': 8.766328369107075, 'o2': 7.569233820424645, 'o3': 8.563317619367856, 'o4': 5.602431765004827, 'o5': 4.862671406751362, 'o6': 2.190857127581098, 'o7': 8.560301521040932, 'o8': 7.446325127800052, 'o9': 7.124140562472506, 'o10': 7.187575090192507, 'o11': 7.003306519215143, 'o12': 5.1044146115866535, 'o13': 3.2944364845604}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11'], 'type3': ['o12', 'o13']}

def ResetState():
    state.loc = { 'r0': 20, 'r1': 13, 'r2': 3, 'r3': 8, 'r4': 20, 'r5': 13, 'r6': 2, 'r7': 13, 'r8': 16, 'r9': 16, 'r10': 14, 'r11': 3, 'm0': 16, 'fixer0': 21, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK,}
    state.storedLoc = {'o0': 18, 'o1': 4, 'o2': 9, 'o3': 2, 'o4': 2, 'o5': 6, 'o6': 13, 'o7': 5, 'o8': 20, 'o9': 19, 'o10': 16, 'o11': 5, 'o12': 1, 'o13': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 4}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    7: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
}
eventsEnv = {
}