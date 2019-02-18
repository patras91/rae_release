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
rv.SHIPPING_DOC = {rv.FACTORY1: 2.3028757625664182}

rv.GROUND_EDGES = {0: [2, 8, 1, 4, 6], 1: [0], 2: [4, 0, 7], 3: [10, 7, 9], 4: [0, 7, 8, 11, 2, 200], 5: [6, 11], 6: [0, 5, 7, 10], 7: [2, 3, 4, 6, 9], 8: [0, 4, 200], 9: [3, 7], 10: [3, 11, 6], 11: [10, 4, 5], 200: [4, 8]}
rv.GROUND_WEIGHTS = {(0, 2): 4.730762434251068, (0, 8): 5.993583524434232, (0, 1): 7.438147053224384, (0, 4): 16.204160740971247, (0, 6): 1, (2, 4): 6.211815390737519, (2, 7): 7.390902348209848, (3, 10): 4.434819659527007, (3, 7): 11.882820285869002, (3, 9): 12.701953798653738, (4, 7): 13.79539170987234, (4, 8): 1.5056595104395933, (4, 11): 9.963036640172517, (4, 200): 9.027613898838528, (5, 6): 11.066215366210486, (5, 11): 4.11361966476162, (6, 7): 8.888541764072597, (6, 10): 8.134484112678791, (7, 9): 10.194233114066973, (8, 200): 11.546677324566584, (10, 11): 2.0119867660906916}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12']
rv.ROBOT_CAPACITY = {'r0': 9.368237680238032, 'r1': 8.37832441870192, 'r2': 9.091763827400587, 'r3': 7.217502315641015, 'r4': 8.207056084673757, 'r5': 8.311844814822207, 'r6': 6.853428100510153, 'r7': 13.295311229550027, 'r8': 7.792750493993799, 'r9': 7.018784874842129, 'r10': 8.672850255170607, 'r11': 7.483777341960908, 'r12': 6.933030958394318}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'fixer0', 'fixer1', 'fixer2']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10']
rv.OBJ_WEIGHT = {'o0': 7.126695581542435, 'o1': 8.744926761032799, 'o2': 5.881120281675971, 'o3': 5.863513663768469, 'o4': 4.322654261860096, 'o5': 9.273581113669419, 'o6': 7.140707062469046, 'o7': 7.267173928486952, 'o8': 8.722843526018396, 'o9': 1.2736186978956985, 'o10': 8.117608015891223}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4'], 'type2': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10']}

def ResetState():
  state.loc = { r0: 9, r1: 11, r2: 2, r3: 0, r4: 2, r5: 9, r6: 1, r7: 2, r8: 9, r9: 3, r10: 8, r11: 2, r12: 5, m0: 10, m1: 9, m2: 10, m3: 1, m4: 3, m5: 8, fixer0: 0, fixer1: 9, fixer2: 8, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK,}
    state.storedLoc{'o0': 0, 'o1': 5, 'o2': 7, 'o3': 11, 'o4': 2, 'o5': 1, 'o6': 9, 'o7': 6, 'o8': 7, 'o9': 4, 'o10': 9}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses8
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    6: [['order', type0, 200]],
    6: [['order', type0, 200]],
    1: [['order', type0, 200]],
    6: [['order', type1, 200]],
    3: [['order', type1, 200]],
    7: [['order', type2, 200]],
    8: [['order', type2, 200]],
    5: [['order', type2, 200]],
    7: [['order', type2, 200]],
    3: [['order', type2, 200]],
}
eventsEnv = {
}