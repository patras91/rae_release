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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 17}

rv.GROUND_EDGES = {0: [10, 1, 7, 14, 15], 1: [0, 6, 13], 2: [14], 3: [10], 4: [7, 11, 16], 5: [7, 9, 17], 6: [1, 13], 7: [0, 4, 5], 8: [11, 12, 14, 17], 9: [16, 18, 5, 200], 10: [0, 16, 3, 11, 200], 11: [4, 10, 8], 12: [16, 8], 13: [1, 6, 200], 14: [0, 2, 8], 15: [0, 16], 16: [4, 9, 10, 15, 12], 17: [5, 8, 18], 18: [17, 9], 200: [9, 10, 13]}
rv.GROUND_WEIGHTS = {(0, 10): 5.954995292028361, (0, 1): 8.995356346677926, (0, 7): 9.958484875575918, (0, 14): 6.03469357578617, (0, 15): 10.01462379101466, (1, 6): 8.312959753098895, (1, 13): 10.287975772045392, (2, 14): 7.535624102036523, (3, 10): 12.46560407030279, (4, 7): 4.839093161693134, (4, 11): 4.223180706468449, (4, 16): 10.544180038534435, (5, 7): 8.826180689020426, (5, 9): 8.209677251549738, (5, 17): 5.640528916827893, (6, 13): 11.893180378879556, (8, 11): 6.12926823894675, (8, 12): 9.408506012977034, (8, 14): 8.360765985478086, (8, 17): 7.27360813409468, (9, 16): 7.752764540296633, (9, 18): 10.189167117264859, (9, 200): 10.78720033152676, (10, 16): 4.746522711331496, (10, 11): 6.744842520649267, (10, 200): 1.1686467236294513, (12, 16): 5.253137371695255, (13, 200): 7.201339682051689, (15, 16): 5.986996091739466, (17, 18): 2.20155551334632}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.968866242026152, 'r1': 7.46323600333724, 'r2': 10.406702999192591, 'r3': 9.779498525060648, 'r4': 10.736738071379852, 'r5': 9.440752728841229, 'r6': 9.652371574886054, 'r7': 4.000221468900902, 'r8': 7.5715536558536005, 'r9': 6.339285760317024, 'r10': 9.31923721849128}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1', 'fixer2']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10']
rv.OBJ_WEIGHT = {'o0': 4.9779491582855915, 'o1': 9.038096787511227, 'o2': 4.401149105319715, 'o3': 7.834020034543669, 'o4': 5.415090754975025, 'o5': 7.635010598674668, 'o6': 5.996413079837625, 'o7': 6.416898598547329, 'o8': 8.169423735717896, 'o9': 6.9138020158031095, 'o10': 6.074998005532634}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6'], 'type2': ['o7', 'o8', 'o9'], 'type3': ['o10']}

def ResetState():
    state.loc = { 'r0': 3, 'r1': 12, 'r2': 0, 'r3': 8, 'r4': 9, 'r5': 4, 'r6': 4, 'r7': 0, 'r8': 12, 'r9': 16, 'r10': 0, 'm0': 1, 'm1': 8, 'm2': 4, 'm3': 16, 'm4': 6, 'm5': 3, 'm6': 3, 'fixer0': 16, 'fixer1': 11, 'fixer2': 12, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK,}
    state.storedLoc = {'o0': 7, 'o1': 11, 'o2': 4, 'o3': 12, 'o4': 4, 'o5': 8, 'o6': 8, 'o7': 16, 'o8': 17, 'o9': 0, 'o10': 13}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 6, 'm1': 8, 'm2': 9, 'm3': 10, 'm4': 4, 'm5': 3, 'm6': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    11: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
}
eventsEnv = {
}