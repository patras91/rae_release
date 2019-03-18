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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 8}

rv.GROUND_EDGES = {0: [1, 9, 7, 8, 10, 12, 13, 14, 200], 1: [10, 0, 2, 3, 5, 15, 17], 2: [1, 15, 17], 3: [1, 5, 15, 17], 4: [8, 6, 16, 17], 5: [1, 3], 6: [4, 7, 9, 15], 7: [0, 6], 8: [0, 200, 4], 9: [6, 0], 10: [0, 1], 11: [13], 12: [0], 13: [0, 11], 14: [0], 15: [1, 3, 6, 2, 17], 16: [4], 17: [1, 3, 4, 15, 2], 200: [0, 8]}
rv.GROUND_WEIGHTS = {(0, 1): 8.387577195961699, (0, 9): 15.25610834197732, (0, 7): 12.477952904369888, (0, 8): 7.885512642936344, (0, 10): 3.706556192094159, (0, 12): 8.22860526006768, (0, 13): 9.63439601354993, (0, 14): 10.522977862489263, (0, 200): 6.63687816876261, (1, 10): 4.553236873631273, (1, 2): 5.726048678577822, (1, 3): 5.5071358694378585, (1, 5): 2.5860267726473634, (1, 15): 4.14792055801697, (1, 17): 12.10765392196669, (2, 15): 6.659233584892731, (2, 17): 8.454834342847041, (3, 5): 1, (3, 15): 1, (3, 17): 9.892820985223096, (4, 8): 2.5565300194448746, (4, 6): 9.627275569536762, (4, 16): 1, (4, 17): 8.54125207117182, (6, 7): 1, (6, 9): 4.206173298397544, (6, 15): 7.056128170663899, (8, 200): 1.460586769353478, (11, 13): 6.795762310990172, (15, 17): 10.675578494554369}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 11.079490067070925, 'r1': 3.8042658323904357, 'r2': 6.85687006811933, 'r3': 8.394902623580744}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 10.04966989037172, 'o1': 8.745063660118184, 'o2': 4.883220745497129, 'o3': 8.011652342298651, 'o4': 6.8123329013111, 'o5': 8.603174408740935, 'o6': 4.816102036074252, 'o7': 8.950654862249593, 'o8': 5.404142258691358, 'o9': 10.590540630207919, 'o10': 9.946365381939192, 'o11': 6.557506816321456, 'o12': 10.534790519037859, 'o13': 10.118992556146985, 'o14': 7.05928882062838, 'o15': 10.584437724276757, 'o16': 8.766407549421178, 'o17': 5.297250888000488, 'o18': 5.082036070815842, 'o19': 6.236619771569753, 'o20': 6.498201283605567, 'o21': 7.665270374871267, 'o22': 3.3699191541514577}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 7, 'r1': 14, 'r2': 3, 'r3': 10, 'm0': 6, 'm1': 9, 'm2': 3, 'm3': 8, 'm4': 6, 'm5': 15, 'm6': 12, 'm7': 11, 'm8': 12, 'm9': 5, 'm10': 13, 'fixer0': 13, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 10, 'o2': 3, 'o3': 3, 'o4': 11, 'o5': 8, 'o6': 2, 'o7': 8, 'o8': 1, 'o9': 10, 'o10': 14, 'o11': 9, 'o12': 3, 'o13': 10, 'o14': 13, 'o15': 16, 'o16': 16, 'o17': 9, 'o18': 11, 'o19': 4, 'o20': 1, 'o21': 15, 'o22': 9}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'fixer0': False}
    state.numUses = {'m0': 13, 'm1': 12, 'm2': 5, 'm3': 6, 'm4': 16, 'm5': 12, 'm6': 8, 'm7': 4, 'm8': 10, 'm9': 16, 'm10': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    19: [['order', 'type0', 200]],
    2: [['order', 'type0', 200]],
}
eventsEnv = {
}