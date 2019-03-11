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
rv.SHIPPING_DOC = {rv.FACTORY1: 6}

rv.GROUND_EDGES = {0: [1, 3, 10, 6, 7], 1: [0, 10, 11, 200], 2: [6, 3, 5, 9, 10], 3: [2, 6, 0, 4, 8, 11], 4: [3, 8, 7], 5: [2, 8, 7, 200], 6: [0, 10, 2, 3, 9], 7: [0, 4, 5, 8], 8: [3, 11, 4, 5, 7], 9: [2, 6], 10: [1, 2, 6, 0, 11], 11: [1, 3, 10, 8, 200], 200: [1, 5, 11]}
rv.GROUND_WEIGHTS = {(0, 1): 8.025721111855079, (0, 3): 5.405433444799605, (0, 10): 10.153885701958618, (0, 6): 10.331125438589469, (0, 7): 17.175440860143134, (1, 10): 1.1318178992101249, (1, 11): 16.244811156697814, (1, 200): 10.603772017980859, (2, 6): 6.869657298494056, (2, 3): 5.9286681365479375, (2, 5): 6.04104127386098, (2, 9): 6.447831914674209, (2, 10): 8.081042841149308, (3, 6): 9.948847009971095, (3, 4): 13.341563924276489, (3, 8): 7.916401736197669, (3, 11): 6.549395827751452, (4, 8): 1.1560939286162784, (4, 7): 6.923355140085963, (5, 8): 15.070157405130066, (5, 7): 6.90043353530856, (5, 200): 15.621131406127706, (6, 10): 8.502817561859738, (6, 9): 7.630598321298749, (7, 8): 2.8604587344262136, (8, 11): 6.925568452740438, (10, 11): 7.788928990780606, (11, 200): 9.948714836907536}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.713511404317364, 'r1': 13.078178820748974, 'r2': 6.360439721662063, 'r3': 6.321806962481993, 'r4': 7.170878044165121, 'r5': 7.1006886735696995, 'r6': 5.322815208817213, 'r7': 4.593034491094496, 'r8': 7.394047446453826, 'r9': 10.563290365524777}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1,  'm11': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 5.949461244241851, 'o1': 9.399266421279341, 'o2': 7.79995301990829, 'o3': 7.773636116321178, 'o4': 6.257823161149965, 'o5': 5.043245549930367, 'o6': 9.397041768173477, 'o7': 8.227839245491484, 'o8': 5.413268088595891, 'o9': 9.041040261045161, 'o10': 8.429541352393544, 'o11': 8.210986038882261, 'o12': 7.6662583108216795, 'o13': 8.127263122718688, 'o14': 8.832034916239637, 'o15': 6.942938254722057, 'o16': 6.667223960277025, 'o17': 4.182806347214686}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10'], 'type3': ['o11', 'o12', 'o13'], 'type4': ['o14', 'o15', 'o16', 'o17']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 0, 'r2': 9, 'r3': 0, 'r4': 4, 'r5': 10, 'r6': 7, 'r7': 7, 'r8': 3, 'r9': 11, 'm0': 0, 'm1': 1, 'm2': 4, 'm3': 5, 'm4': 0, 'm5': 7, 'm6': 4, 'm7': 0, 'm8': 4, 'm9': 3, 'm10': 7, 'm11': 10, 'fixer0': 10, 'fixer1': 3, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK,}
    state.storedLoc = {'o0': 9, 'o1': 1, 'o2': 7, 'o3': 7, 'o4': 0, 'o5': 4, 'o6': 2, 'o7': 6, 'o8': 5, 'o9': 11, 'o10': 3, 'o11': 10, 'o12': 1, 'o13': 8, 'o14': 7, 'o15': 0, 'o16': 0, 'o17': 7}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'm11': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 8, 'm1': 14, 'm2': 10, 'm3': 11, 'm4': 9, 'm5': 11, 'm6': 8, 'm7': 14, 'm8': 1, 'm9': 4, 'm10': 13, 'm11': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    18: [['order', 'type1', 200]],
    15: [['order', 'type1', 200]],
}
eventsEnv = {
}