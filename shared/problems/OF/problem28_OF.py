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
rv.SHIPPING_DOC = {rv.FACTORY1: 13}

rv.GROUND_EDGES = {0: [10, 19, 9, 11, 16, 18, 200], 1: [14, 19, 6, 13], 2: [4, 12, 13], 3: [5, 9, 15], 4: [2, 5, 18], 5: [7, 18, 3, 4], 6: [1, 11, 14, 8, 15, 18], 7: [8, 9, 17, 19, 5], 8: [6, 11, 13, 7], 9: [0, 3, 7, 14, 15], 10: [0, 13, 14], 11: [0, 6, 8], 12: [17, 2], 13: [1, 8, 10, 16, 18, 2], 14: [9, 10, 15, 1, 6, 18], 15: [6, 9, 3, 14], 16: [0, 13, 19], 17: [12, 7], 18: [0, 6, 14, 4, 5, 13], 19: [16, 0, 1, 7], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 10): 10.15237143059376, (0, 19): 7.977183274131573, (0, 9): 9.184971271875408, (0, 11): 8.266730361969136, (0, 16): 10.147475256132518, (0, 18): 3.633254121038588, (0, 200): 9.463596470837418, (1, 14): 4.95646216077591, (1, 19): 7.17451361042666, (1, 6): 6.134586663291409, (1, 13): 4.389047037767012, (2, 4): 5.180933002652013, (2, 12): 6.097126270960549, (2, 13): 9.784911508116142, (3, 5): 8.83392153832164, (3, 9): 6.998445475202426, (3, 15): 14.653566866377112, (4, 5): 8.22098693644905, (4, 18): 3.4064446093956313, (5, 7): 5.182540031537117, (5, 18): 11.533321891914454, (6, 11): 9.847778469427396, (6, 14): 4.553832910146468, (6, 8): 8.743099110139532, (6, 15): 8.552014957203497, (6, 18): 12.954526332014275, (7, 8): 9.95566718630982, (7, 9): 10.53063718563258, (7, 17): 4.289664742651366, (7, 19): 14.845958104509737, (8, 11): 5.533558505624951, (8, 13): 6.634512746456096, (9, 14): 8.27919078242414, (9, 15): 8.477927688169705, (10, 13): 8.634488464355854, (10, 14): 10.496718054016755, (12, 17): 1, (13, 16): 16.121042454539378, (13, 18): 8.752334873602916, (14, 15): 3.222518057001052, (14, 18): 12.544225338023136, (16, 19): 2.5362983335732707}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 11.004284746159948, 'r1': 8.261899878984986, 'r2': 11.68357788626307, 'r3': 7.382338927621331, 'r4': 10.434852160801004, 'r5': 4.444705867597832, 'r6': 10.983556591291523, 'r7': 8.569596953813823, 'r8': 8.298710628655016, 'r9': 7.709330681083756, 'r10': 9.384989250601784, 'r11': 7.779831275740327, 'r12': 6.889059647955714}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1', 'fixer2', 'fixer3']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19']
rv.OBJ_WEIGHT = {'o0': 6.297260373989616, 'o1': 10.27065593136856, 'o2': 7.897515233360391, 'o3': 8.7819553201862, 'o4': 4.514760753062982, 'o5': 6.784123151917492, 'o6': 5.612567918881453, 'o7': 7.545438073576748, 'o8': 4.119129796243346, 'o9': 8.302039157570498, 'o10': 7.60372680227405, 'o11': 4.65668671302531, 'o12': 4.210957942265551, 'o13': 6.182261229003385, 'o14': 8.737347517385013, 'o15': 7.173768074765366, 'o16': 7.671750830158276, 'o17': 9.06437775011656, 'o18': 6.722845715565954, 'o19': 4.609742399368798}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12', 'o13'], 'type3': ['o14', 'o15', 'o16', 'o17', 'o18', 'o19']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 16, 'r2': 14, 'r3': 4, 'r4': 5, 'r5': 1, 'r6': 18, 'r7': 14, 'r8': 17, 'r9': 12, 'r10': 8, 'r11': 7, 'r12': 6, 'm0': 17, 'm1': 12, 'm2': 5, 'm3': 4, 'fixer0': 3, 'fixer1': 7, 'fixer2': 5, 'fixer3': 19, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK,}
    state.storedLoc = {'o0': 7, 'o1': 13, 'o2': 5, 'o3': 12, 'o4': 18, 'o5': 11, 'o6': 8, 'o7': 1, 'o8': 1, 'o9': 14, 'o10': 6, 'o11': 0, 'o12': 6, 'o13': 18, 'o14': 16, 'o15': 8, 'o16': 14, 'o17': 3, 'o18': 0, 'o19': 15}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False, 'fixer3': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'fixer0': False, 'fixer1': False, 'fixer2': False, 'fixer3': False}
    state.numUses = {'m0': 10, 'm1': 20, 'm2': 10, 'm3': 19}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    19: [['order', 'type0', 200]],
    3: [['order', 'type0', 200]],
    4: [['order', 'type0', 200]],
    30: [['order', 'type0', 200]],
    23: [['order', 'type0', 200]],
    20: [['order', 'type1', 200]],
    29: [['order', 'type1', 200]],
    6: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    5: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
    9: [['order', 'type3', 200]],
    24: [['order', 'type3', 200]],
    22: [['order', 'type3', 200]],
    7: [['order', 'type3', 200]],
    11: [['order', 'type3', 200]],
    32: [['order', 'type3', 200]],
}
eventsEnv = {
}