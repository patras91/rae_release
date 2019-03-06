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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 3}

rv.GROUND_EDGES = {0: [1, 6, 12, 200], 1: [3, 6, 0], 2: [6, 7, 5], 3: [4, 6, 11, 1, 10], 4: [5, 3, 9, 10], 5: [2, 4], 6: [0, 12, 1, 2, 3], 7: [12, 2, 8], 8: [7], 9: [4, 11], 10: [3, 4, 12], 11: [9, 3, 13], 12: [0, 6, 7, 10], 13: [11], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 1): 4.565344647211164, (0, 6): 3.4028237947278512, (0, 12): 12.619607795994451, (0, 200): 2.0971571738369414, (1, 3): 3.0965295805290136, (1, 6): 9.286091319292769, (2, 6): 4.732695826982052, (2, 7): 11.925589941730278, (2, 5): 7.738706196162674, (3, 4): 13.319933624682967, (3, 6): 8.702405892082462, (3, 11): 8.29135543542487, (3, 10): 5.975298062751469, (4, 5): 5.151029847046796, (4, 9): 4.8616585951917255, (4, 10): 9.650498453698468, (6, 12): 3.578508384919582, (7, 12): 4.5464660962306445, (7, 8): 6.08840828953876, (9, 11): 1.591935397388565, (10, 12): 5.843906992663374, (11, 13): 2.9299235135458277}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.6388888578133844, 'r1': 8.632801429093837, 'r2': 7.676821589357617, 'r3': 11.11240001504867, 'r4': 9.286507500845795, 'r5': 10.569580904476272, 'r6': 7.222524475655163, 'r7': 4.741841629920609, 'r8': 5.5725644072979215, 'r9': 4.791268618480888, 'r10': 6.388568569276078, 'r11': 8.297566807383753}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10']
rv.OBJ_WEIGHT = {'o0': 4.747155376074985, 'o1': 8.92355022214323, 'o2': 10.37271997851512, 'o3': 5.455725988890051, 'o4': 4.739241837274056, 'o5': 6.017001750823908, 'o6': 8.922339489188404, 'o7': 4.325815390993322, 'o8': 5.8665475528458035, 'o9': 5.313801106178492, 'o10': 6.365540473019703}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4'], 'type2': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10']}

def ResetState():
    state.loc = { 'r0': 8, 'r1': 2, 'r2': 5, 'r3': 6, 'r4': 8, 'r5': 13, 'r6': 6, 'r7': 10, 'r8': 0, 'r9': 2, 'r10': 2, 'r11': 6, 'm0': 13, 'm1': 10, 'fixer0': 2, 'fixer1': 5, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 6, 'o2': 2, 'o3': 0, 'o4': 5, 'o5': 11, 'o6': 9, 'o7': 10, 'o8': 12, 'o9': 7, 'o10': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 11, 'm1': 6}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
    6: [['order', 'type1', 200]],
    1: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
}
eventsEnv = {
}