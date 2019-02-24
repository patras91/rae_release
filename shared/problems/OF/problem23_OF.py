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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9.195455367374503}

rv.GROUND_EDGES = {0: [4, 9, 10, 2, 6, 7, 11, 14], 1: [2, 12], 2: [0, 1, 3, 4, 7, 13], 3: [2, 4, 9], 4: [2, 10, 0, 3, 9], 5: [6, 8, 11], 6: [0, 14, 5, 12, 200], 7: [0, 2], 8: [9, 5, 12], 9: [4, 0, 3, 8], 10: [11, 14, 0, 4], 11: [0, 5, 10, 13, 200], 12: [1, 6, 8, 13], 13: [2, 11, 12], 14: [0, 6, 10], 200: [6, 11]}
rv.GROUND_WEIGHTS = {(0, 4): 1.6245096746248908, (0, 9): 1, (0, 10): 6.236066570253735, (0, 2): 15.643933669416278, (0, 6): 13.69528881778616, (0, 7): 10.261316550444668, (0, 11): 6.682810351238714, (0, 14): 9.93622608534622, (1, 2): 7.412575839830357, (1, 12): 10.516019562308996, (2, 3): 3.3059268475113077, (2, 4): 5.635589571573654, (2, 7): 7.124616323016696, (2, 13): 7.040701473509168, (3, 4): 10.677832579213336, (3, 9): 8.648318195988981, (4, 10): 6.310749969255708, (4, 9): 4.577479184076932, (5, 6): 7.432350829266406, (5, 8): 10.749534606445511, (5, 11): 11.038105203621921, (6, 14): 8.017535213877437, (6, 12): 1, (6, 200): 6.886010550440959, (8, 9): 7.056601185979005, (8, 12): 5.623106575164998, (10, 11): 9.897189546783482, (10, 14): 15.145489619862975, (11, 13): 1.259639575220075, (11, 200): 11.866555137161011, (12, 13): 3.298371581443316}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13']
rv.ROBOT_CAPACITY = {'r0': 8.261968394585022, 'r1': 10.070676339977304, 'r2': 9.651541321381366, 'r3': 10.546407290393963, 'r4': 7.250234911847385, 'r5': 5.583137197369501, 'r6': 11.007831282139213, 'r7': 6.52992813755365, 'r8': 7.641170510489638, 'r9': 5.186749176887492, 'r10': 6.315754099936739, 'r11': 9.527040994377646, 'r12': 12.571068133074029, 'r13': 8.14941421155437}
rv.MACHINES = ['m0', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 9.004727174678846, 'o1': 9.687137394275418, 'o2': 8.584801513176597, 'o3': 5.920828867391269, 'o4': 9.847386048338155, 'o5': 10.316535738365705, 'o6': 7.447862876546429, 'o7': 8.77338948103426, 'o8': 6.33458643719985, 'o9': 5.406065853956438, 'o10': 5.050802725740322, 'o11': 7.336238246085753, 'o12': 3.7424429345469536, 'o13': 7.347228340101273, 'o14': 9.683026366102952, 'o15': 2.9280228386588636, 'o16': 5.885278622102863, 'o17': 4.994663318701086, 'o18': 4.770642977114564}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4'], 'type2': ['o5', 'o6', 'o7'], 'type3': ['o8', 'o9', 'o10', 'o11', 'o12'], 'type4': ['o13', 'o14', 'o15', 'o16', 'o17', 'o18']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 8, 'r2': 3, 'r3': 6, 'r4': 1, 'r5': 9, 'r6': 3, 'r7': 13, 'r8': 1, 'r9': 2, 'r10': 9, 'r11': 0, 'r12': 10, 'r13': 0, 'm0': 12, 'fixer0': 1, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK,}
    state.storedLoc = {'o0': 6, 'o1': 12, 'o2': 13, 'o3': 10, 'o4': 2, 'o5': 3, 'o6': 14, 'o7': 12, 'o8': 11, 'o9': 8, 'o10': 0, 'o11': 13, 'o12': 10, 'o13': 6, 'o14': 6, 'o15': 0, 'o16': 0, 'o17': 6, 'o18': 10}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'m0'": False, "'fixer0'": False}
    state.numUses = {'m0': 6, 'fixer0': 9}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    16: [['order', 'type0', 200]],
    27: [['order', 'type0', 200]],
    12: [['order', 'type1', 200]],
    1: [['order', 'type1', 200]],
    9: [['order', 'type1', 200]],
    29: [['order', 'type2', 200]],
    4: [['order', 'type2', 200]],
    7: [['order', 'type2', 200]],
    22: [['order', 'type3', 200]],
    19: [['order', 'type4', 200]],
    20: [['order', 'type4', 200]],
    23: [['order', 'type4', 200]],
    6: [['order', 'type4', 200]],
    28: [['order', 'type4', 200]],
    14: [['order', 'type4', 200]],
}
eventsEnv = {
}