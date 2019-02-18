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
rv.SHIPPING_DOC = {rv.FACTORY1: 3.718447886283298}

rv.GROUND_EDGES = {0: [1, 4, 19], 1: [0, 11, 20], 2: [8, 19], 3: [15, 8, 9], 4: [0, 9, 15, 16, 200], 5: [8, 11, 18, 7, 9, 10], 6: [7, 8, 17, 15], 7: [5, 15, 6], 8: [3, 13, 14, 2, 5, 6, 10, 18], 9: [3, 4, 5, 10, 16, 18], 10: [5, 8, 9, 16, 20], 11: [1, 5, 20], 12: [14, 20], 13: [8, 18], 14: [19, 8, 12], 15: [4, 6, 18, 3, 7], 16: [4, 9, 10, 17], 17: [6, 16, 18], 18: [8, 9, 17, 5, 13, 15, 200], 19: [0, 2, 14], 20: [1, 10, 11, 12], 200: [4, 18]}
rv.GROUND_WEIGHTS = {(0, 1): 5.673696611983118, (0, 4): 11.455399434589411, (0, 19): 8.656104236609597, (1, 11): 6.808859409821559, (1, 20): 6.263724451637014, (2, 8): 5.546611188870162, (2, 19): 5.006141719970923, (3, 15): 4.646846338072372, (3, 8): 3.3462622960123003, (3, 9): 10.251137767279145, (4, 9): 13.864337560863884, (4, 15): 5.543556396570736, (4, 16): 8.695334471631668, (4, 200): 15.24230751317161, (5, 8): 2.108680174541848, (5, 11): 12.578321459270121, (5, 18): 13.437598669850525, (5, 7): 13.149787016254912, (5, 9): 12.875813810780894, (5, 10): 4.7015441132768006, (6, 7): 5.689673416506448, (6, 8): 10.374487220084083, (6, 17): 8.468660844450449, (6, 15): 15.986462008215733, (7, 15): 10.477316874240861, (8, 13): 7.911137514886608, (8, 14): 5.930213364785894, (8, 10): 7.2444969926015155, (8, 18): 1, (9, 10): 3.6160298117015017, (9, 16): 9.852099255162164, (9, 18): 1, (10, 16): 8.151496156330378, (10, 20): 4.462279513181148, (11, 20): 7.850679315271933, (12, 14): 1, (12, 20): 1, (13, 18): 12.819526014711428, (14, 19): 10.764464659167306, (15, 18): 13.532782893749982, (16, 17): 8.478598759000215, (17, 18): 10.038422345495803, (18, 200): 9.704472713820673}

rv.ROBOTS = ['r0']
rv.ROBOT_CAPACITY = {'r0': 7.7651792513138576}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']
rv.OBJ_WEIGHT = {'o0': 7.7651792513138576, 'o1': 7.073629561658105, 'o2': 4.3016382507583675, 'o3': 7.754802137780453, 'o4': 5.442417520848785, 'o5': 6.655308872874954, 'o6': 7.7651792513138576, 'o7': 7.7651792513138576, 'o8': 7.7651792513138576, 'o9': 7.752015108021408, 'o10': 7.7651792513138576, 'o11': 5.262049713810031, 'o12': 6.59804484334908, 'o13': 7.7651792513138576, 'o14': 5.41686840565421, 'o15': 6.999158528393682, 'o16': 5.631312246183708, 'o17': 7.7651792513138576, 'o18': 5.140031238333075, 'o19': 7.7651792513138576, 'o20': 7.7651792513138576, 'o21': 5.289648456801412, 'o22': 1.3840769609407655, 'o23': 5.2093726607135205, 'o24': 6.01025746993441}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17', 'o18'], 'type4': ['o19', 'o20', 'o21', 'o22', 'o23', 'o24']}

def ResetState():
  state.loc = { r0: 16, m0: 12, m1: 11, m2: 11, m3: 9, m4: 10, m5: 13, m6: 0, m7: 0, m8: 12, m9: 3, m10: 17, fixer0: 0, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK, o20: UNK, o21: UNK, o22: UNK, o23: UNK, o24: UNK,}
    state.storedLoc{'o0': 4, 'o1': 1, 'o2': 16, 'o3': 11, 'o4': 8, 'o5': 9, 'o6': 14, 'o7': 11, 'o8': 10, 'o9': 3, 'o10': 0, 'o11': 16, 'o12': 7, 'o13': 2, 'o14': 4, 'o15': 3, 'o16': 3, 'o17': 4, 'o18': 20, 'o19': 10, 'o20': 15, 'o21': 20, 'o22': 2, 'o23': 18, 'o24': 19}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL, o20: NIL, o21: NIL, o22: NIL, o23: NIL, o24: NIL,}
    state.busy{'r0': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'fixer0': False}
    state.numUses10
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    6: [['order', type0, 200]],
    6: [['order', type0, 200]],
    2: [['order', type0, 200]],
    5: [['order', type1, 200]],
    3: [['order', type1, 200]],
    3: [['order', type1, 200]],
    6: [['order', type2, 200]],
    8: [['order', type2, 200]],
    3: [['order', type2, 200]],
    4: [['order', type2, 200]],
    1: [['order', type2, 200]],
    8: [['order', type3, 200]],
    5: [['order', type3, 200]],
    1: [['order', type3, 200]],
    4: [['order', type3, 200]],
    5: [['order', type4, 200]],
    7: [['order', type4, 200]],
    1: [['order', type4, 200]],
    6: [['order', type4, 200]],
    1: [['order', type4, 200]],
    3: [['order', type4, 200]],
}
eventsEnv = {
}