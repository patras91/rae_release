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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 3.8159657013814297}

rv.GROUND_EDGES = {0: [6, 1, 3, 7, 8, 12, 14, 15], 1: [0, 8, 9, 16], 2: [16, 6, 13], 3: [0, 7, 11], 4: [8, 9], 5: [13, 7, 8, 10], 6: [2, 8, 11, 0, 16], 7: [0, 3, 5, 13], 8: [0, 1, 4, 5, 15, 6], 9: [1, 4], 10: [5, 12], 11: [3, 6], 12: [0, 10], 13: [2, 7, 5], 14: [0], 15: [0, 8, 16], 16: [1, 6, 15, 2, 200], 200: [16]}
rv.GROUND_WEIGHTS = {(0, 6): 11.293892106243446, (0, 1): 6.596499281798752, (0, 3): 2.931688688492744, (0, 7): 8.79458937085161, (0, 8): 7.368753847959986, (0, 12): 7.677785587850615, (0, 14): 4.505589128043539, (0, 15): 3.0512786552267013, (1, 8): 7.444540400041859, (1, 9): 8.618505010785638, (1, 16): 1.5623133743276476, (2, 16): 10.477422051338603, (2, 6): 5.780341980385936, (2, 13): 8.887487607627708, (3, 7): 6.870059806472176, (3, 11): 10.920332018183714, (4, 8): 12.155606041004846, (4, 9): 3.9088933018369527, (5, 13): 3.1680644919355263, (5, 7): 6.739306364008142, (5, 8): 6.521251455718367, (5, 10): 6.606966846362052, (6, 8): 11.204237212407364, (6, 11): 9.321626346095078, (6, 16): 8.869442776888732, (7, 13): 11.314029575474743, (8, 15): 5.154834553195916, (10, 12): 3.707666879799163, (15, 16): 3.540246711687195, (16, 200): 13.631166538389936}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10']
rv.ROBOT_CAPACITY = {'r0': 10.281296886570557, 'r1': 6.318235103690485, 'r2': 9.58867677403745, 'r3': 6.07630057211488, 'r4': 8.374679859028298, 'r5': 11.92884279858825, 'r6': 4.7254224157122735, 'r7': 10.635195171075793, 'r8': 6.649193812692838, 'r9': 7.928714207788758, 'r10': 7.984897512870441}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 5.037502073444857, 'o1': 5.412384838271533, 'o2': 5.72612660882781, 'o3': 8.650501885235975, 'o4': 8.207533446024334, 'o5': 9.365457466965324, 'o6': 8.448777315513816, 'o7': 3.423965090044843, 'o8': 9.50711560851998, 'o9': 7.268992067762231, 'o10': 3.208755044386502, 'o11': 9.188446339396174, 'o12': 7.053006138685018, 'o13': 7.862548846727578, 'o14': 7.737736948577124, 'o15': 6.113865049605994, 'o16': 6.896457526903877, 'o17': 5.758106388378217, 'o18': 5.7299336346754774}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3'], 'type2': ['o4', 'o5', 'o6'], 'type3': ['o7', 'o8', 'o9', 'o10', 'o11', 'o12'], 'type4': ['o13', 'o14', 'o15', 'o16', 'o17', 'o18']}

def ResetState():
  state.loc = { r0: 1, r1: 10, r2: 9, r3: 12, r4: 6, r5: 16, r6: 11, r7: 1, r8: 13, r9: 14, r10: 5, m0: 7, m1: 15, m2: 12, m3: 13, m4: 1, m5: 6, m6: 8, m7: 11, m8: 15, m9: 10, m10: 4, fixer0: 0, fixer1: 12, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK,}
    state.storedLoc{'o0': 16, 'o1': 16, 'o2': 9, 'o3': 13, 'o4': 13, 'o5': 15, 'o6': 5, 'o7': 9, 'o8': 16, 'o9': 14, 'o10': 13, 'o11': 3, 'o12': 7, 'o13': 4, 'o14': 12, 'o15': 1, 'o16': 13, 'o17': 6, 'o18': 6}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'fixer0': False, 'fixer1': False}
    state.numUses3
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', type0, 200]],
    7: [['order', type1, 200]],
    1: [['order', type1, 200]],
    5: [['order', type1, 200]],
    8: [['order', type2, 200]],
    3: [['order', type2, 200]],
    3: [['order', type2, 200]],
    4: [['order', type3, 200]],
    4: [['order', type3, 200]],
    8: [['order', type4, 200]],
    8: [['order', type4, 200]],
}
eventsEnv = {
}