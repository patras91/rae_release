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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 15}

rv.GROUND_EDGES = {0: [3, 17, 2], 1: [5, 8], 2: [0, 4, 20, 15], 3: [8, 17, 20, 0, 4, 14], 4: [3, 12, 19, 2], 5: [14, 1, 8], 6: [8, 11], 7: [19], 8: [1, 5, 12, 3, 6, 9, 10, 14], 9: [8], 10: [8, 19, 11, 16], 11: [6, 10, 17, 19, 200], 12: [14, 4, 8, 18], 13: [20], 14: [3, 8, 5, 12, 18], 15: [2], 16: [10, 20], 17: [11, 0, 3, 18, 200], 18: [12, 14, 17], 19: [10, 11, 20, 4, 7], 20: [13, 16, 2, 3, 19], 200: [11, 17]}
rv.GROUND_WEIGHTS = {(0, 3): 1.7250797406439613, (0, 17): 14.442314296551285, (0, 2): 14.744822310141283, (1, 5): 3.5811913857682702, (1, 8): 7.237952539140359, (2, 4): 6.644033249374615, (2, 20): 5.469602492834859, (2, 15): 12.561689292114814, (3, 8): 7.361284820530092, (3, 17): 6.221022698371156, (3, 20): 12.58304651805274, (3, 4): 11.601240758377827, (3, 14): 11.973169586725174, (4, 12): 6.401229985792573, (4, 19): 7.62831466413083, (5, 14): 2.367283298868598, (5, 8): 4.431001934797798, (6, 8): 8.725306488630874, (6, 11): 12.983220283356328, (7, 19): 10.244978545943994, (8, 12): 11.0511314075759, (8, 9): 2.847101005828126, (8, 10): 5.539727265022798, (8, 14): 2.376552913683777, (10, 19): 14.691152006590361, (10, 11): 14.432915181151674, (10, 16): 8.08583495573661, (11, 17): 5.367588105399202, (11, 19): 9.11983290684535, (11, 200): 9.774886130697142, (12, 14): 7.157986003627873, (12, 18): 1, (13, 20): 1, (14, 18): 12.504962301261116, (16, 20): 7.777989015077972, (17, 18): 16.41434708720228, (17, 200): 11.008585277658831, (19, 20): 13.97664070715241}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.111895674998803, 'r1': 6.925659736430749, 'r2': 6.195258829148306, 'r3': 12.632773727267592, 'r4': 4.549356455879064, 'r5': 10.186588393342296, 'r6': 5.7140309542182415, 'r7': 11.084530348774226, 'r8': 9.917500370195658, 'r9': 7.691156233994107}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6']
rv.OBJ_WEIGHT = {'o0': 10.120103626668348, 'o1': 8.399113052411156, 'o2': 6.260186979808451, 'o3': 8.221505012934443, 'o4': 9.836562147323907, 'o5': 7.098533661764028, 'o6': 4.540270173878049}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3'], 'type2': ['o4', 'o5', 'o6']}

def ResetState():
    state.loc = { 'r0': 11, 'r1': 8, 'r2': 1, 'r3': 8, 'r4': 5, 'r5': 14, 'r6': 11, 'r7': 9, 'r8': 18, 'r9': 2, 'm0': 19, 'fixer0': 20, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK,}
    state.storedLoc = {'o0': 15, 'o1': 2, 'o2': 8, 'o3': 0, 'o4': 1, 'o5': 11, 'o6': 19}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 7}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    12: [['order', 'type0', 200]],
    5: [['order', 'type1', 200]],
    9: [['order', 'type1', 200]],
    13: [['order', 'type1', 200]],
    3: [['order', 'type2', 200]],
    1: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
}
eventsEnv = {
}