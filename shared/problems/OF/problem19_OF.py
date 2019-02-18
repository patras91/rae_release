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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1.6154844953963143}

rv.GROUND_EDGES = {0: [11, 4, 12, 13, 15, 200], 1: [11, 8, 14], 2: [6, 15, 3, 13], 3: [2, 9, 7, 8, 15], 4: [0, 7, 6, 10], 5: [11, 13, 15, 6], 6: [4, 5, 9, 10, 2], 7: [3, 10, 11, 4], 8: [1, 3, 13], 9: [12, 3, 6], 10: [4, 6, 7], 11: [1, 0, 5, 7], 12: [0, 9, 13], 13: [0, 2, 12, 5, 8], 14: [1], 15: [0, 3, 2, 5], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 11): 7.128513368782598, (0, 4): 6.691657312497856, (0, 12): 8.087650815447358, (0, 13): 1.5685145506403924, (0, 15): 3.9589458252565803, (0, 200): 1, (1, 11): 10.11865531953542, (1, 8): 10.865579854624123, (1, 14): 6.454387902667785, (2, 6): 6.914162226451115, (2, 15): 4.695112835777474, (2, 3): 4.002304755623779, (2, 13): 1, (3, 9): 15.776205863569412, (3, 7): 6.502322316741219, (3, 8): 5.9560169332892166, (3, 15): 11.675815980974468, (4, 7): 1, (4, 6): 6.775991718510122, (4, 10): 3.036264454126046, (5, 11): 9.451029025855856, (5, 13): 10.413057282505758, (5, 15): 3.2535252823500533, (5, 6): 10.780045379148147, (6, 9): 8.445530333537722, (6, 10): 11.506833533901036, (7, 10): 15.53084703352623, (7, 11): 9.385181860982604, (8, 13): 3.9304203778112763, (9, 12): 3.8945815762611335, (12, 13): 10.12833977142788}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
rv.ROBOT_CAPACITY = {'r0': 4.462300258544479, 'r1': 10.00768122243689, 'r2': 6.3872585278803236, 'r3': 8.079125176273818, 'r4': 6.129243591838298, 'r5': 7.388697536514787, 'r6': 9.884513187377875, 'r7': 9.721535578279095}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']
rv.OBJ_WEIGHT = {'o0': 9.756632025616925, 'o1': 7.335928583858721, 'o2': 8.082472973804713, 'o3': 6.600860718282842, 'o4': 5.427769045892373, 'o5': 7.709911083016857, 'o6': 7.716666449655588, 'o7': 5.988762365862065, 'o8': 7.131099527691907, 'o9': 7.285826482015119, 'o10': 4.490539883455655, 'o11': 5.26316965829753, 'o12': 8.133440493183222, 'o13': 5.837272052887618, 'o14': 7.503674297196898, 'o15': 8.596649254407716, 'o16': 7.35937651646752, 'o17': 8.840734036388122, 'o18': 7.966660645276664, 'o19': 6.777691393547597, 'o20': 5.097311177825423, 'o21': 9.451402488365874, 'o22': 9.705295984728219, 'o23': 7.025486814089069}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15'], 'type4': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']}

def ResetState():
  state.loc = { r0: 6, r1: 5, r2: 12, r3: 9, r4: 9, r5: 9, r6: 1, r7: 9, m0: 7, fixer0: 6, fixer1: 0, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK, o20: UNK, o21: UNK, o22: UNK, o23: UNK,}
    state.storedLoc{'o0': 13, 'o1': 5, 'o2': 9, 'o3': 12, 'o4': 4, 'o5': 10, 'o6': 1, 'o7': 15, 'o8': 1, 'o9': 5, 'o10': 10, 'o11': 9, 'o12': 14, 'o13': 15, 'o14': 8, 'o15': 14, 'o16': 2, 'o17': 6, 'o18': 12, 'o19': 1, 'o20': 10, 'o21': 14, 'o22': 6, 'o23': 1}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL, o20: NIL, o21: NIL, o22: NIL, o23: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses11
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    8: [['order', type0, 200]],
    6: [['order', type0, 200]],
    1: [['order', type1, 200]],
    7: [['order', type1, 200]],
    2: [['order', type1, 200]],
    4: [['order', type1, 200]],
    3: [['order', type1, 200]],
    3: [['order', type1, 200]],
    6: [['order', type1, 200]],
    3: [['order', type2, 200]],
    6: [['order', type2, 200]],
    6: [['order', type3, 200]],
    7: [['order', type3, 200]],
    4: [['order', type3, 200]],
    4: [['order', type4, 200]],
    1: [['order', type4, 200]],
    1: [['order', type4, 200]],
    7: [['order', type4, 200]],
}
eventsEnv = {
}