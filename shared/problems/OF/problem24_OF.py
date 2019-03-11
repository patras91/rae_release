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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 5}

rv.GROUND_EDGES = {0: [3, 19, 21, 2, 11, 13, 22, 200], 1: [4, 16, 22, 20, 21], 2: [0, 3, 12], 3: [2, 5, 0, 8, 16], 4: [11, 19, 1, 7, 21], 5: [3, 8, 10], 6: [18], 7: [4, 8], 8: [3, 10, 21, 5, 7, 13, 14, 19], 9: [12, 15, 18, 14], 10: [5, 14, 19, 8, 21], 11: [0, 4], 12: [2, 9], 13: [0, 8, 18], 14: [8, 9, 10, 15, 16], 15: [14, 9, 17, 18], 16: [3, 14, 19, 1, 17], 17: [15, 16, 18], 18: [15, 6, 9, 13, 17], 19: [8, 0, 4, 10, 16], 20: [1], 21: [1, 4, 10, 0, 8], 22: [0, 1], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 3): 5.566023450684228, (0, 19): 5.100693346539264, (0, 21): 11.788359120401177, (0, 2): 10.079125619611213, (0, 11): 14.691488431693642, (0, 13): 6.676121151072877, (0, 22): 4.86685225429069, (0, 200): 2.7129790495375534, (1, 4): 2.652120734658678, (1, 16): 5.663312440594207, (1, 22): 2.0736197947086126, (1, 20): 6.144789321268778, (1, 21): 12.157950941094992, (2, 3): 3.723648128225544, (2, 12): 5.702319974541805, (3, 5): 6.686479614840351, (3, 8): 4.08952526247395, (3, 16): 4.841558104869161, (4, 11): 1, (4, 19): 5.840131550685619, (4, 7): 10.419630303108896, (4, 21): 12.01457904875971, (5, 8): 8.19233055012802, (5, 10): 3.638821980328779, (6, 18): 2.67156520447147, (7, 8): 17.74441312040541, (8, 10): 2.80090728957574, (8, 21): 12.432167412198995, (8, 13): 11.582413330334319, (8, 14): 11.745158989918446, (8, 19): 15.382793149347851, (9, 12): 1, (9, 15): 1, (9, 18): 11.15364055019045, (9, 14): 5.899764471132892, (10, 14): 4.873709182237253, (10, 19): 6.129902955754648, (10, 21): 9.485563123752733, (13, 18): 1.939037661582856, (14, 15): 14.245223872090403, (14, 16): 5.532386952646015, (15, 17): 6.322599542730066, (15, 18): 9.5402658609104, (16, 19): 4.103325952127337, (16, 17): 11.968066241261365, (17, 18): 13.464792985767442}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.983199533880491, 'r1': 8.769632894745067, 'r2': 5.896547144519898}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13']
rv.OBJ_WEIGHT = {'o0': 7.90832308194754, 'o1': 6.06764739322594, 'o2': 4.6374857699737735, 'o3': 7.00020975478776, 'o4': 7.533418375644162, 'o5': 5.474750302610597, 'o6': 8.401598265296503, 'o7': 8.032381754000905, 'o8': 8.534203606723523, 'o9': 2.9319095637356325, 'o10': 3.828584928848274, 'o11': 7.6372220041489385, 'o12': 8.769632894745067, 'o13': 6.382007056135561}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6'], 'type2': ['o7', 'o8'], 'type3': ['o9', 'o10'], 'type4': ['o11', 'o12', 'o13']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 10, 'r2': 0, 'm0': 19, 'm1': 0, 'm2': 16, 'fixer0': 13, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK,}
    state.storedLoc = {'o0': 19, 'o1': 1, 'o2': 1, 'o3': 16, 'o4': 0, 'o5': 15, 'o6': 16, 'o7': 9, 'o8': 15, 'o9': 15, 'o10': 0, 'o11': 15, 'o12': 14, 'o13': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'm0': False, 'm1': False, 'm2': False, 'fixer0': False}
    state.numUses = {'m0': 8, 'm1': 9, 'm2': 7}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    10: [['order', 'type0', 200]],
    1: [['order', 'type0', 200]],
}
eventsEnv = {
}