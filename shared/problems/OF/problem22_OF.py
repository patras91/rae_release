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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 6}

rv.GROUND_EDGES = {0: [3, 5, 2, 6, 8], 1: [7, 4, 5], 2: [0, 4, 5, 8], 3: [8, 0, 4], 4: [1, 2, 3, 7, 9], 5: [1, 2, 8, 0, 7, 200], 6: [0, 9], 7: [5, 9, 1, 4], 8: [0, 2, 5, 3], 9: [6, 4, 7, 200], 200: [5, 9]}
rv.GROUND_WEIGHTS = {(0, 3): 11.526295256626145, (0, 5): 6.530259326268724, (0, 2): 12.275812517193293, (0, 6): 7.740927428657366, (0, 8): 9.333934252292458, (1, 7): 10.165805367111597, (1, 4): 10.266982585534082, (1, 5): 5.233988236813826, (2, 4): 5.815224206797062, (2, 5): 7.584183090831896, (2, 8): 3.9382451655807333, (3, 8): 7.39270297809603, (3, 4): 1.5136726311140256, (4, 7): 5.848388443945991, (4, 9): 10.7897151422458, (5, 8): 10.523827191830033, (5, 7): 6.369738754527011, (5, 200): 9.566581166205907, (6, 9): 13.912000170621187, (7, 9): 1, (9, 200): 8.668029257948769}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.63897316603649, 'r1': 4.10474251450759, 'r2': 10.155508802417048}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1', 'fixer2']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']
rv.OBJ_WEIGHT = {'o0': 5.420346768207287, 'o1': 0.9921746375594536, 'o2': 10.155508802417048, 'o3': 4.139493735946335, 'o4': 4.8034945877396495, 'o5': 8.126532705155926, 'o6': 5.09151334495275, 'o7': 6.875882177032544, 'o8': 8.351972325610596, 'o9': 6.165126257045541, 'o10': 6.0583389317062295, 'o11': 6.1831948289669265, 'o12': 6.37538700505924, 'o13': 10.155508802417048, 'o14': 7.690013626094929, 'o15': 5.941867533963612, 'o16': 4.629104695089522, 'o17': 10.136088029417532, 'o18': 9.858649985357385, 'o19': 6.960713979397299, 'o20': 6.3865740074319834, 'o21': 2.606728504163571, 'o22': 8.5507232567567, 'o23': 5.497573032195701, 'o24': 6.656667519955894}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14', 'o15'], 'type3': ['o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 1, 'r2': 3, 'm0': 0, 'fixer0': 3, 'fixer1': 9, 'fixer2': 3, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 5, 'o2': 7, 'o3': 1, 'o4': 2, 'o5': 3, 'o6': 8, 'o7': 9, 'o8': 9, 'o9': 8, 'o10': 5, 'o11': 9, 'o12': 5, 'o13': 9, 'o14': 5, 'o15': 7, 'o16': 6, 'o17': 6, 'o18': 6, 'o19': 8, 'o20': 5, 'o21': 5, 'o22': 7, 'o23': 5, 'o24': 9}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'm0': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 7}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    26: [['order', 'type0', 200]],
    28: [['order', 'type0', 200]],
    27: [['order', 'type0', 200]],
    2: [['order', 'type0', 200]],
    20: [['order', 'type0', 200]],
    30: [['order', 'type1', 200]],
    16: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    22: [['order', 'type1', 200]],
    18: [['order', 'type2', 200]],
    6: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
    31: [['order', 'type2', 200]],
    8: [['order', 'type3', 200]],
    11: [['order', 'type3', 200]],
    21: [['order', 'type4', 200]],
}
eventsEnv = {
}