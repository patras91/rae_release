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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [1, 12, 9, 15], 1: [0, 9], 2: [16], 3: [6, 18, 7, 9], 4: [16], 5: [13, 16, 8, 200], 6: [16, 3, 18], 7: [3, 9, 11, 17], 8: [5, 12, 18], 9: [0, 1, 3, 17, 7, 18], 10: [18], 11: [7, 13, 17], 12: [17, 0, 8, 13, 14, 18], 13: [12, 5, 11, 19, 200], 14: [12, 17, 19], 15: [0], 16: [2, 17, 4, 5, 6], 17: [7, 9, 14, 18, 11, 12, 16], 18: [6, 8, 9, 12, 19, 3, 10, 17], 19: [13, 14, 18], 200: [5, 13]}
rv.GROUND_WEIGHTS = {(0, 1): 9.385904563860526, (0, 12): 4.998749460946394, (0, 9): 1.9196596728729034, (0, 15): 7.786739523563495, (1, 9): 13.10630608875772, (2, 16): 14.808690128521615, (3, 6): 5.24294394248305, (3, 18): 3.519800306249727, (3, 7): 11.936128219584823, (3, 9): 13.926624814849049, (4, 16): 8.76155477761071, (5, 13): 5.500593288750758, (5, 16): 3.5277339345567773, (5, 8): 11.762322205554021, (5, 200): 5.738385947188972, (6, 16): 9.272286831299661, (6, 18): 7.97472961099244, (7, 9): 9.175060521197313, (7, 11): 11.0694356882287, (7, 17): 8.320336287088024, (8, 12): 9.153498731994965, (8, 18): 7.830459057718584, (9, 17): 11.69921522174729, (9, 18): 13.943430127885707, (10, 18): 5.79426511313622, (11, 13): 6.164519840100614, (11, 17): 11.3747440440838, (12, 17): 11.242852996549745, (12, 13): 5.077071221237082, (12, 14): 3.3581298004833124, (12, 18): 7.922311906151895, (13, 19): 3.0806426392100636, (13, 200): 13.562014050879966, (14, 17): 1.3120749071049458, (14, 19): 5.642266700910305, (16, 17): 5.415581411600606, (17, 18): 4.475088346893681, (18, 19): 6.3470621380650964}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.397735241230677, 'r1': 8.561958554596844, 'r2': 7.446895201757199, 'r3': 8.44943186480871, 'r4': 9.808488412872645, 'r5': 11.574577132468878, 'r6': 9.5422042834407, 'r7': 8.340232301471705, 'r8': 10.583991525923382}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11']
rv.OBJ_WEIGHT = {'o0': 8.342349125694236, 'o1': 5.705250677192405, 'o2': 6.753631609541407, 'o3': 4.958132167960917, 'o4': 7.292608000552997, 'o5': 5.247211813300208, 'o6': 8.429915490904861, 'o7': 6.732242724502739, 'o8': 8.703476730752536, 'o9': 8.001574132937362, 'o10': 7.013797105247296, 'o11': 7.2964809346220765}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5'], 'type2': ['o6', 'o7', 'o8'], 'type3': ['o9', 'o10', 'o11']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 19, 'r2': 12, 'r3': 11, 'r4': 0, 'r5': 6, 'r6': 7, 'r7': 12, 'r8': 4, 'm0': 17, 'm1': 0, 'm2': 19, 'm3': 13, 'm4': 9, 'm5': 17, 'm6': 12, 'fixer0': 14, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK,}
    state.storedLoc = {'o0': 0, 'o1': 19, 'o2': 3, 'o3': 9, 'o4': 1, 'o5': 11, 'o6': 4, 'o7': 10, 'o8': 17, 'o9': 4, 'o10': 13, 'o11': 7}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False}
    state.numUses = {'m0': 12, 'm1': 8, 'm2': 9, 'm3': 6, 'm4': 12, 'm5': 11, 'm6': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    8: [['order', 'type0', 200]],
    17: [['order', 'type0', 200]],
}
eventsEnv = {
}