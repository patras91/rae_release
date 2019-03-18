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
rv.SHIPPING_DOC = {rv.FACTORY1: 10}

rv.GROUND_EDGES = {0: [20, 21, 1, 5, 6, 7, 8, 9, 11, 15], 1: [0, 2, 7, 8, 19, 13, 14], 2: [1, 9, 21, 3, 19], 3: [2, 14, 16, 18], 4: [6], 5: [0, 12, 14, 19, 200], 6: [0, 4], 7: [0, 1, 11, 21], 8: [0, 1, 200], 9: [0, 2, 17, 20], 10: [19, 200, 17], 11: [0, 7, 13], 12: [5, 16, 200], 13: [1, 11], 14: [1, 3, 5], 15: [0], 16: [12, 3], 17: [9, 10], 18: [21, 3], 19: [2, 5, 21, 1, 10], 20: [9, 0], 21: [2, 7, 0, 18, 19], 200: [5, 8, 12, 10]}
rv.GROUND_WEIGHTS = {(0, 20): 12.92171734120996, (0, 21): 9.70652413902959, (0, 1): 1, (0, 5): 3.2415483316064, (0, 6): 4.566192916883306, (0, 7): 6.6964769499609496, (0, 8): 10.496236135158153, (0, 9): 12.355730428089277, (0, 11): 4.457188049998406, (0, 15): 9.847459647137951, (1, 2): 8.997170188137591, (1, 7): 7.0314210642828865, (1, 8): 11.232446836107092, (1, 19): 7.166421999661949, (1, 13): 4.208061531566841, (1, 14): 6.486035265770279, (2, 9): 7.184545143222398, (2, 21): 16.46555971581651, (2, 3): 5.981928404108158, (2, 19): 3.3534300387892566, (3, 14): 14.359350602788911, (3, 16): 6.22487485245872, (3, 18): 13.542144752720304, (4, 6): 1.1330489316280365, (5, 12): 13.00876112090361, (5, 14): 7.274935954124954, (5, 19): 3.3027471158862065, (5, 200): 10.275443754144998, (7, 11): 10.067396607511448, (7, 21): 6.019420306237978, (8, 200): 2.768391867394283, (9, 17): 10.803898333962616, (9, 20): 9.19618021507795, (10, 19): 10.660697175835613, (10, 200): 8.797520195938276, (10, 17): 14.78327854999058, (11, 13): 10.640716197405812, (12, 16): 8.547213992131185, (12, 200): 13.186010744284646, (18, 21): 12.260744544992406, (19, 21): 8.918699309352986}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 9.743309857300044, 'r1': 4.86133827142517, 'r2': 11.033478022018683, 'r3': 4.588401188012652, 'r4': 12.309008137198603, 'r5': 8.76568252559645, 'r6': 6.242174135474535, 'r7': 9.517668046881989, 'r8': 6.6488184466955005}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10']
rv.OBJ_WEIGHT = {'o0': 8.57170310149683, 'o1': 3.4908245006158096, 'o2': 5.959181830651324, 'o3': 9.239377961011154, 'o4': 7.382049753933965, 'o5': 8.003741685934132, 'o6': 8.453117662078622, 'o7': 7.561354083648297, 'o8': 3.20715340091754, 'o9': 4.303563026809524, 'o10': 5.339679920706445}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9'], 'type3': ['o10']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 11, 'r2': 10, 'r3': 16, 'r4': 6, 'r5': 10, 'r6': 8, 'r7': 10, 'r8': 21, 'm0': 8, 'fixer0': 5, 'fixer1': 14, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK,}
    state.storedLoc = {'o0': 7, 'o1': 3, 'o2': 17, 'o3': 0, 'o4': 7, 'o5': 13, 'o6': 11, 'o7': 16, 'o8': 15, 'o9': 9, 'o10': 15}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    8: [['order', 'type0', 200]],
    7: [['order', 'type0', 200]],
}
eventsEnv = {
}