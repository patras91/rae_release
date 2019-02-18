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
rv.SHIPPING_DOC = {rv.FACTORY1: 17.254038827681754}

rv.GROUND_EDGES = {0: [4, 8, 9, 16, 3, 7, 11], 1: [13, 14, 9, 12], 2: [6, 9, 11, 13, 10], 3: [0, 8], 4: [8, 0, 10], 5: [16, 15, 18], 6: [7, 9, 2, 17], 7: [0, 6, 13, 16, 17], 8: [3, 10, 12, 0, 4, 16], 9: [0, 1, 11, 2, 6, 10, 14], 10: [2, 4, 9, 18, 8], 11: [0, 17, 2, 9, 15], 12: [1, 18, 8, 14, 200], 13: [7, 17, 1, 2, 14], 14: [9, 12, 13, 1], 15: [5, 11], 16: [0, 7, 8, 5, 200], 17: [6, 7, 11, 13], 18: [5, 10, 12], 200: [12, 16]}
rv.GROUND_WEIGHTS = {(0, 4): 7.970709403805469, (0, 8): 8.777719796614168, (0, 9): 6.131744512497589, (0, 16): 12.2818451924898, (0, 3): 12.448311900432502, (0, 7): 9.103465841639215, (0, 11): 1, (1, 13): 13.058980397524413, (1, 14): 13.846215254922702, (1, 9): 2.610119914799613, (1, 12): 4.6589890456430325, (2, 6): 8.32361867683365, (2, 9): 9.594063743972084, (2, 11): 5.397559123314536, (2, 13): 7.238845173718561, (2, 10): 4.09170937819191, (3, 8): 10.419708402461422, (4, 8): 5.2982992034634755, (4, 10): 6.966519323429271, (5, 16): 13.910919552951874, (5, 15): 12.369692926600798, (5, 18): 5.10052950551278, (6, 7): 10.545403002052675, (6, 9): 11.470574456219438, (6, 17): 2.3016280368542885, (7, 13): 14.774671051070456, (7, 16): 19.980415043216517, (7, 17): 4.45481728675808, (8, 10): 1.6230920038203411, (8, 12): 7.916972269681949, (8, 16): 15.391421595963893, (9, 11): 2.575468890858807, (9, 10): 8.004151883161777, (9, 14): 4.6231840386134655, (10, 18): 11.475778322191402, (11, 17): 11.544988819919661, (11, 15): 6.8067452702684, (12, 18): 2.307162176585879, (12, 14): 5.982439743705534, (12, 200): 1, (13, 17): 9.832414805626795, (13, 14): 10.758909360621278, (16, 200): 10.390245024179125}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5']
rv.ROBOT_CAPACITY = {'r0': 6.192808687590161, 'r1': 6.265816292682304, 'r2': 9.416908653666463, 'r3': 7.444942290057123, 'r4': 6.0142119925083835, 'r5': 9.94302282322388}
rv.MACHINES = ['m0', 'fixer0', 'fixer1', 'fixer2', 'fixer3']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 7.84950663805349, 'o1': 7.429980165277244, 'o2': 6.017968874730132, 'o3': 6.531136582264118, 'o4': 7.920348123857246, 'o5': 6.8299520799668985, 'o6': 5.453918088524304, 'o7': 8.474115267999522, 'o8': 9.748850571271825, 'o9': 8.415147096830585, 'o10': 8.083306015536966, 'o11': 6.354240622509882, 'o12': 8.553178606109027, 'o13': 6.7229822435882145, 'o14': 9.445273927186335, 'o15': 7.486839367662542, 'o16': 6.972616077239974, 'o17': 7.464110330012582}
rv.OBJ_CLASS = {'type0': ['o0'], 'type1': ['o1', 'o2', 'o3', 'o4', 'o5'], 'type2': ['o6', 'o7', 'o8', 'o9', 'o10'], 'type3': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']}

def ResetState():
  state.loc = { r0: 18, r1: 18, r2: 11, r3: 18, r4: 3, r5: 5, m0: 5, fixer0: 7, fixer1: 4, fixer2: 8, fixer3: 15, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK,}
    state.storedLoc{'o0': 4, 'o1': 2, 'o2': 4, 'o3': 15, 'o4': 12, 'o5': 12, 'o6': 10, 'o7': 9, 'o8': 5, 'o9': 0, 'o10': 14, 'o11': 10, 'o12': 10, 'o13': 7, 'o14': 18, 'o15': 16, 'o16': 18, 'o17': 18}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'm0': False, 'fixer0': False, 'fixer1': False, 'fixer2': False, 'fixer3': False}
    state.numUses6
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    3: [['order', type1, 200]],
    5: [['order', type1, 200]],
    3: [['order', type1, 200]],
    1: [['order', type1, 200]],
    3: [['order', type1, 200]],
    2: [['order', type2, 200]],
}
eventsEnv = {
}