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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 8.048233125398255}

rv.GROUND_EDGES = {0: [5, 10, 4, 14], 1: [9, 13], 2: [4, 5, 11, 6, 15], 3: [12, 5, 6], 4: [0, 2, 13], 5: [3, 0, 2], 6: [2, 3], 7: [8, 10, 11, 200], 8: [15, 7, 10], 9: [10, 1], 10: [8, 0, 7, 9], 11: [12, 2, 7], 12: [15, 3, 11, 13], 13: [4, 12, 1], 14: [0, 15], 15: [2, 12, 14, 8, 200], 200: [7, 15]}
rv.GROUND_WEIGHTS = {(0, 5): 12.35301771733193, (0, 10): 9.276184126807586, (0, 4): 6.778050859420929, (0, 14): 4.8567798483919535, (1, 9): 11.773386876689298, (1, 13): 7.676058762078815, (2, 4): 5.438693221688636, (2, 5): 3.3803568366229646, (2, 11): 4.97907689112856, (2, 6): 12.9471386496481, (2, 15): 15.364960285562379, (3, 12): 13.974129448213949, (3, 5): 7.570935539894789, (3, 6): 4.353461135499601, (4, 13): 6.801782192734931, (7, 8): 9.375544991438545, (7, 10): 7.6852145621322965, (7, 11): 2.36821682893013, (7, 200): 16.154458382796, (8, 15): 10.240499757033739, (8, 10): 12.582252430795585, (9, 10): 10.071519852435834, (11, 12): 9.760626526477946, (12, 15): 14.998679422280427, (12, 13): 11.033657667471918, (14, 15): 4.721371665677662, (15, 200): 14.463335884057688}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3']
rv.ROBOT_CAPACITY = {'r0': 9.218232963591436, 'r1': 8.648090155889703, 'r2': 7.889070572100205, 'r3': 7.195381796098958}
rv.MACHINES = ['m0', 'm1', 'm2', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11']
rv.OBJ_WEIGHT = {'o0': 5.178630996919536, 'o1': 8.400727790661096, 'o2': 1.3132189764461675, 'o3': 6.458392644308592, 'o4': 7.402597012932076, 'o5': 9.218232963591436, 'o6': 6.90625656005948, 'o7': 1.964913116681557, 'o8': 5.71258900791671, 'o9': 5.234579650262532, 'o10': 4.619067004678308, 'o11': 6.912887215390994}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10'], 'type3': ['o11']}

def ResetState():
  state.loc = { r0: 8, r1: 4, r2: 0, r3: 7, m0: 7, m1: 12, m2: 6, fixer0: 13, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK,}
    state.storedLoc{'o0': 6, 'o1': 14, 'o2': 15, 'o3': 15, 'o4': 10, 'o5': 11, 'o6': 15, 'o7': 1, 'o8': 6, 'o9': 13, 'o10': 6, 'o11': 1}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'm0': False, 'm1': False, 'm2': False, 'fixer0': False}
    state.numUses8
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    2: [['order', type0, 200]],
    6: [['order', type0, 200]],
    4: [['order', type0, 200]],
    3: [['order', type1, 200]],
    7: [['order', type1, 200]],
    4: [['order', type1, 200]],
    4: [['order', type1, 200]],
    1: [['order', type2, 200]],
    1: [['order', type2, 200]],
    3: [['order', type2, 200]],
    6: [['order', type2, 200]],
    6: [['order', type3, 200]],
}
eventsEnv = {
}