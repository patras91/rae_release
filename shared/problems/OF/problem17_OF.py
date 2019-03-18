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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1}

rv.GROUND_EDGES = {0: [6, 1, 7, 8, 200], 1: [0, 200, 2, 6, 11], 2: [1, 8, 11, 4], 3: [7, 11, 5, 8, 9], 4: [2, 7, 10], 5: [3, 11, 7], 6: [0, 1], 7: [0, 3, 5, 11, 4, 10], 8: [0, 2, 3], 9: [3, 10], 10: [4, 7, 9, 11], 11: [1, 7, 10, 2, 3, 5], 200: [0, 1]}
rv.GROUND_WEIGHTS = {(0, 6): 1.769546980750543, (0, 1): 2.8534582873980128, (0, 7): 7.200936401663946, (0, 8): 4.294224849651767, (0, 200): 4.88923303369706, (1, 200): 7.452586035331043, (1, 2): 4.4308080981548805, (1, 6): 2.113044660341548, (1, 11): 1, (2, 8): 3.412201066600553, (2, 11): 5.909767319956131, (2, 4): 5.741080499705955, (3, 7): 3.4391100075520793, (3, 11): 4.314351779701354, (3, 5): 11.49279633940458, (3, 8): 4.262969905595719, (3, 9): 7.226684404485354, (4, 7): 4.541556698682956, (4, 10): 4.027970076806305, (5, 11): 14.305501091303656, (5, 7): 8.554621225848788, (7, 11): 7.3797171452260235, (7, 10): 1, (9, 10): 6.447904512504271, (10, 11): 3.304581185137902}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.956503530509547, 'r1': 9.115140098576502, 'r2': 12.451647049734408, 'r3': 7.2720624612190115, 'r4': 7.885521121246015, 'r5': 10.52793906318248}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20']
rv.OBJ_WEIGHT = {'o0': 6.280060678592676, 'o1': 10.510466987293398, 'o2': 2.2733901449544165, 'o3': 7.508621120189845, 'o4': 9.492279700717297, 'o5': 6.741278459509594, 'o6': 9.66654165510601, 'o7': 5.627056924479076, 'o8': 5.683446595879834, 'o9': 11.102350112992703, 'o10': 5.610511091791468, 'o11': 10.208933196578073, 'o12': 7.935688157944673, 'o13': 4.663304149755541, 'o14': 8.679237866000406, 'o15': 11.597347488163752, 'o16': 5.160458924189333, 'o17': 8.388712417295872, 'o18': 7.679157183523059, 'o19': 8.621046279718971, 'o20': 8.838973792466378}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15', 'o16'], 'type4': ['o17', 'o18'], 'type5': ['o19', 'o20']}

def ResetState():
    state.loc = { 'r0': 7, 'r1': 11, 'r2': 6, 'r3': 6, 'r4': 2, 'r5': 1, 'm0': 4, 'fixer0': 0, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK,}
    state.storedLoc = {'o0': 1, 'o1': 8, 'o2': 5, 'o3': 3, 'o4': 10, 'o5': 2, 'o6': 11, 'o7': 3, 'o8': 0, 'o9': 7, 'o10': 7, 'o11': 6, 'o12': 10, 'o13': 1, 'o14': 2, 'o15': 6, 'o16': 11, 'o17': 9, 'o18': 3, 'o19': 1, 'o20': 7}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    13: [['order', 'type0', 200]],
    15: [['order', 'type0', 200]],
}
eventsEnv = {
}