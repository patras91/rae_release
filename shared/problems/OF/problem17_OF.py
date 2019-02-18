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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1.991708414180747}

rv.GROUND_EDGES = {0: [8, 2, 5, 7, 10], 1: [8, 12, 13, 16, 14, 200], 2: [0, 13], 3: [9], 4: [14, 16, 10, 15, 17], 5: [0, 17, 10, 11], 6: [7, 12, 15], 7: [0, 6, 15], 8: [0, 10, 14, 17, 1, 9], 9: [8, 3, 10], 10: [0, 4, 5, 9, 14, 8, 16], 11: [5, 16], 12: [1, 6, 13, 14], 13: [2, 12, 1], 14: [1, 12, 4, 8, 10], 15: [4, 7, 6], 16: [10, 11, 1, 4], 17: [4, 5, 8], 200: [1]}
rv.GROUND_WEIGHTS = {(0, 8): 3.223202347670326, (0, 2): 5.266215500398705, (0, 5): 9.502423176718262, (0, 7): 8.028563800574497, (0, 10): 10.358739634304921, (1, 8): 3.276918268430782, (1, 12): 9.525410347826442, (1, 13): 1.4040991286885838, (1, 16): 11.441271151993993, (1, 14): 9.160139256156587, (1, 200): 6.842854891224011, (2, 13): 8.432484810627662, (3, 9): 7.568548852917539, (4, 14): 12.213581813864263, (4, 16): 6.913724610747835, (4, 10): 7.718852692849469, (4, 15): 2.9688859286068405, (4, 17): 19.586141735858106, (5, 17): 5.162853317734562, (5, 10): 4.760516562897348, (5, 11): 3.1337538628864072, (6, 7): 2.840519555479654, (6, 12): 10.656112569474518, (6, 15): 9.19662020995163, (7, 15): 7.605277796491931, (8, 10): 2.320587228275456, (8, 14): 8.996337142072406, (8, 17): 12.39138534077541, (8, 9): 11.311387689733209, (9, 10): 3.7789908135443877, (10, 14): 10.029979864515123, (10, 16): 16.576376992647358, (11, 16): 11.799173819559062, (12, 13): 3.705903340175066, (12, 14): 7.764008775368199}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']
rv.ROBOT_CAPACITY = {'r0': 5.4074969574567024, 'r1': 9.12869834434175, 'r2': 10.69600724210133, 'r3': 10.21365347134401, 'r4': 8.94071974167932, 'r5': 6.078228834652098, 'r6': 6.1110085543495165}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'fixer0', 'fixer1', 'fixer2']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 9.653890998925128, 'o1': 5.355760227693799, 'o2': 8.393158358450181, 'o3': 4.7339023499285915, 'o4': 6.0937838981019175, 'o5': 7.275187249304747, 'o6': 6.608854470831118, 'o7': 5.312437402522278, 'o8': 4.0497246660996264, 'o9': 5.649836735290256, 'o10': 7.700964353869274, 'o11': 7.393354412482304, 'o12': 8.354141297650575, 'o13': 7.722267622822293, 'o14': 8.411206143568023, 'o15': 6.701359109683658}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15']}

def ResetState():
  state.loc = { r0: 1, r1: 16, r2: 15, r3: 15, r4: 10, r5: 14, r6: 15, m0: 3, m1: 3, m2: 17, m3: 0, m4: 7, m5: 0, m6: 8, m7: 5, m8: 13, m9: 7, m10: 1, m11: 5, fixer0: 16, fixer1: 9, fixer2: 2, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK,}
    state.storedLoc{'o0': 2, 'o1': 5, 'o2': 2, 'o3': 6, 'o4': 0, 'o5': 15, 'o6': 9, 'o7': 12, 'o8': 0, 'o9': 17, 'o10': 17, 'o11': 5, 'o12': 13, 'o13': 16, 'o14': 7, 'o15': 8}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'm11': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses12
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    7: [['order', type0, 200]],
    8: [['order', type0, 200]],
    8: [['order', type0, 200]],
    6: [['order', type0, 200]],
    7: [['order', type1, 200]],
    3: [['order', type1, 200]],
    3: [['order', type3, 200]],
    3: [['order', type3, 200]],
    5: [['order', type3, 200]],
}
eventsEnv = {
}