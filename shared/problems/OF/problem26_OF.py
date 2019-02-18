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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 16.116819257146986}

rv.GROUND_EDGES = {0: [2, 15, 17, 8, 10, 12, 13, 16, 19, 200], 1: [9, 17, 5, 13, 19], 2: [9, 0, 3], 3: [2, 4, 13, 7, 18], 4: [6, 3], 5: [1, 7, 14], 6: [7, 4], 7: [3, 5, 6, 17, 18, 200], 8: [0, 18], 9: [12, 13, 1, 2], 10: [0], 11: [13, 17], 12: [0, 9], 13: [0, 1, 14, 3, 9, 11], 14: [5, 13], 15: [19, 0], 16: [0, 18], 17: [7, 11, 0, 1], 18: [3, 7, 8, 16], 19: [0, 1, 15], 200: [0, 7]}
rv.GROUND_WEIGHTS = {(0, 2): 3.797974737506064, (0, 15): 10.386412936331267, (0, 17): 6.875174893950496, (0, 8): 10.362602879935672, (0, 10): 9.999779446063304, (0, 12): 7.928251850054698, (0, 13): 14.25587068126369, (0, 16): 7.1838496004926355, (0, 19): 1, (0, 200): 14.538924955405477, (1, 9): 6.129094570686519, (1, 17): 8.331397831516634, (1, 5): 4.057690892692762, (1, 13): 9.679200972377343, (1, 19): 8.228503847026653, (2, 9): 9.348468826281726, (2, 3): 11.427476334652988, (3, 4): 5.493237847194655, (3, 13): 3.2422935178351473, (3, 7): 9.1834814049496, (3, 18): 6.7387731863754095, (4, 6): 5.278440950764233, (5, 7): 7.570826842566596, (5, 14): 3.4999378578119646, (6, 7): 4.048903556462159, (7, 17): 10.22401360577244, (7, 18): 8.312264332096527, (7, 200): 4.878954306021155, (8, 18): 1, (9, 12): 8.93490825745759, (9, 13): 10.897648643686836, (11, 13): 12.828412526265724, (11, 17): 9.718314963270508, (13, 14): 3.6809023666193994, (15, 19): 19.32412285787374, (16, 18): 4.909571899716891}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12']
rv.ROBOT_CAPACITY = {'r0': 12.075416002085923, 'r1': 6.75045984458473, 'r2': 9.496229759018465, 'r3': 10.905006845759523, 'r4': 6.8665378839431845, 'r5': 6.3483829235779385, 'r6': 5.9384306266358315, 'r7': 8.919118773327135, 'r8': 6.614570579542145, 'r9': 9.82539023595863, 'r10': 8.754958763655715, 'r11': 8.068970601907678, 'r12': 3.5188542813735406}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 6.1630183403015115, 'o1': 4.8844029644569344, 'o2': 5.171435701094427, 'o3': 6.530948805523827, 'o4': 9.306792958522719, 'o5': 6.186569400241498, 'o6': 7.655547966567659, 'o7': 9.110423868473053, 'o8': 8.221850595889935, 'o9': 6.5022669574059115, 'o10': 7.194488052419506, 'o11': 7.757646102151794, 'o12': 8.07439377280241, 'o13': 7.886990652119328, 'o14': 5.896907207750214, 'o15': 8.3748206361226}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14'], 'type4': ['o15']}

def ResetState():
  state.loc = { r0: 6, r1: 14, r2: 4, r3: 4, r4: 8, r5: 10, r6: 11, r7: 12, r8: 4, r9: 9, r10: 16, r11: 11, r12: 4, m0: 5, m1: 3, m2: 6, m3: 11, m4: 10, m5: 8, m6: 2, m7: 18, fixer0: 3, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK,}
    state.storedLoc{'o0': 3, 'o1': 9, 'o2': 11, 'o3': 5, 'o4': 13, 'o5': 10, 'o6': 18, 'o7': 8, 'o8': 6, 'o9': 2, 'o10': 0, 'o11': 6, 'o12': 3, 'o13': 8, 'o14': 18, 'o15': 18}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'fixer0': False}
    state.numUses9
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    8: [['order', type0, 200]],
    8: [['order', type0, 200]],
    8: [['order', type0, 200]],
    8: [['order', type1, 200]],
    2: [['order', type1, 200]],
    7: [['order', type2, 200]],
    4: [['order', type2, 200]],
    5: [['order', type2, 200]],
    6: [['order', type2, 200]],
    3: [['order', type2, 200]],
    7: [['order', type3, 200]],
    7: [['order', type3, 200]],
    2: [['order', type3, 200]],
    5: [['order', type4, 200]],
}
eventsEnv = {
}