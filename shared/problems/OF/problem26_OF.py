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
rv.SHIPPING_DOC = {rv.FACTORY1: 2}

rv.GROUND_EDGES = {0: [4, 11, 8, 17, 200], 1: [5, 11], 2: [10, 14], 3: [13, 12], 4: [14, 0], 5: [11, 12, 14, 1, 10, 18], 6: [8, 14, 16], 7: [12], 8: [0, 16, 6, 12, 13, 15, 18], 9: [17], 10: [5, 14, 2, 13], 11: [14, 0, 1, 5, 18], 12: [3, 8, 5, 7, 16], 13: [8, 10, 3], 14: [6, 2, 4, 5, 10, 11, 15, 16], 15: [8, 14, 18], 16: [6, 12, 14, 8], 17: [0, 9], 18: [5, 8, 11, 15], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 4): 5.868569099446925, (0, 11): 14.035995917415296, (0, 8): 10.54908579451677, (0, 17): 8.810956154510578, (0, 200): 8.64875229691391, (1, 5): 2.998360028297795, (1, 11): 2.4001303947257657, (2, 10): 6.36713269419685, (2, 14): 11.632540535970431, (3, 13): 5.0822246880039526, (3, 12): 6.549568484661368, (4, 14): 10.092417194598452, (5, 11): 7.890217019388279, (5, 12): 4.2021874135497095, (5, 14): 8.446411936951266, (5, 10): 1.1897889639834265, (5, 18): 14.030617703165799, (6, 8): 11.174327795695682, (6, 14): 3.164654355094866, (6, 16): 12.578551617921699, (7, 12): 6.683735278987876, (8, 16): 8.275464203125601, (8, 12): 4.48553869791615, (8, 13): 10.842565198164055, (8, 15): 3.6944644222555763, (8, 18): 5.918545274690441, (9, 17): 8.161667286784281, (10, 14): 11.232523555855009, (10, 13): 2.3675489914614225, (11, 14): 13.46695228371427, (11, 18): 12.181203910545433, (12, 16): 12.866615877793304, (14, 15): 12.544116882972922, (14, 16): 4.760489661041796, (15, 18): 6.684123341513648}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.5291981473683185, 'r1': 9.49097183998704, 'r2': 4.659024453804514, 'r3': 4.626811734517391, 'r4': 9.016876430333765, 'r5': 9.355411324333728, 'r6': 9.503950562401513, 'r7': 10.056268219268627, 'r8': 10.332227189928755}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1', 'fixer2']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13']
rv.OBJ_WEIGHT = {'o0': 6.798180857458785, 'o1': 9.649611296811136, 'o2': 6.550002786206278, 'o3': 5.96302902927995, 'o4': 8.387517867873466, 'o5': 6.869723796249438, 'o6': 6.283430872962571, 'o7': 8.85330403949879, 'o8': 9.099613474821664, 'o9': 10.332227189928755, 'o10': 7.483627170987259, 'o11': 9.0459817332437, 'o12': 5.1645661451874565, 'o13': 6.6541982627243055}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9'], 'type3': ['o10'], 'type4': ['o11', 'o12', 'o13']}

def ResetState():
    state.loc = { 'r0': 14, 'r1': 18, 'r2': 8, 'r3': 3, 'r4': 8, 'r5': 5, 'r6': 12, 'r7': 5, 'r8': 7, 'm0': 11, 'm1': 6, 'm2': 16, 'm3': 6, 'm4': 6, 'm5': 15, 'm6': 7, 'fixer0': 10, 'fixer1': 9, 'fixer2': 5, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK,}
    state.storedLoc = {'o0': 10, 'o1': 5, 'o2': 7, 'o3': 10, 'o4': 13, 'o5': 8, 'o6': 1, 'o7': 10, 'o8': 14, 'o9': 3, 'o10': 16, 'o11': 3, 'o12': 8, 'o13': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 9, 'm1': 13, 'm2': 13, 'm3': 9, 'm4': 13, 'm5': 10, 'm6': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    6: [['order', 'type0', 200]],
    3: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
    16: [['order', 'type1', 200]],
    24: [['order', 'type1', 200]],
    25: [['order', 'type1', 200]],
    23: [['order', 'type1', 200]],
    5: [['order', 'type1', 200]],
    20: [['order', 'type2', 200]],
    14: [['order', 'type3', 200]],
    10: [['order', 'type4', 200]],
    1: [['order', 'type4', 200]],
}
eventsEnv = {
}