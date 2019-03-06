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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 16}

rv.GROUND_EDGES = {0: [22, 3, 5, 7, 8], 1: [11, 20, 4], 2: [15, 10, 12], 3: [0, 20], 4: [1, 6, 13, 19, 20], 5: [0, 13, 12], 6: [8, 18, 19, 4, 14, 200], 7: [0, 13], 8: [0, 6, 13, 14, 15], 9: [15, 10], 10: [2, 9, 17, 18, 19], 11: [12, 1, 17], 12: [2, 5, 11, 13, 16, 17], 13: [7, 8, 12, 14, 21, 4, 5], 14: [6, 8, 13, 17], 15: [8, 9, 2, 16, 20], 16: [12, 15, 18, 21, 22], 17: [11, 12, 14, 10], 18: [6, 10, 21, 16], 19: [10, 4, 6], 20: [3, 4, 15, 1], 21: [16, 13, 18], 22: [16, 0], 200: [6]}
rv.GROUND_WEIGHTS = {(0, 22): 3.4812794487900973, (0, 3): 7.597439378900105, (0, 5): 4.081300694900696, (0, 7): 6.8261444183013165, (0, 8): 11.72097681334547, (1, 11): 7.336091484963972, (1, 20): 5.157345508032018, (1, 4): 1, (2, 15): 5.649180194192152, (2, 10): 6.993344310685535, (2, 12): 3.2392827996409936, (3, 20): 10.265764527898412, (4, 6): 13.310946736259606, (4, 13): 12.925477237735794, (4, 19): 10.67442117794103, (4, 20): 5.386805778043431, (5, 13): 10.207843910023303, (5, 12): 13.51332263691004, (6, 8): 11.807962577009253, (6, 18): 8.71203228143464, (6, 19): 5.717769108677617, (6, 14): 12.420075155269215, (6, 200): 3.2279991258179264, (7, 13): 9.869982978326577, (8, 13): 4.448585090728367, (8, 14): 13.197161504947733, (8, 15): 4.660192057648471, (9, 15): 4.779645659195369, (9, 10): 12.963512861697708, (10, 17): 5.250788377117194, (10, 18): 12.196661146851856, (10, 19): 4.885150676592463, (11, 12): 8.453607336273642, (11, 17): 9.685358038068882, (12, 13): 5.800133711539919, (12, 16): 9.808042057414761, (12, 17): 8.988274969837192, (13, 14): 7.905474826667812, (13, 21): 8.513797522857331, (14, 17): 13.684855852710891, (15, 16): 8.937140754488036, (15, 20): 7.788038203356001, (16, 18): 1, (16, 21): 9.618504539743805, (16, 22): 5.864420183908828, (18, 21): 12.108842772609414}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.675007335944336, 'r1': 4.674834020044434, 'r2': 6.687597708336289, 'r3': 8.899912715317903, 'r4': 8.561172116777632, 'r5': 10.085549081324334, 'r6': 7.089162103220093}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 6.174755879494767, 'o1': 9.132329344423152, 'o2': 9.283947898825971, 'o3': 3.920122623852794, 'o4': 10.085549081324334, 'o5': 7.283476280832668, 'o6': 4.582629325466772, 'o7': 3.3294516037305324, 'o8': 6.0732045147459, 'o9': 8.152175636138534, 'o10': 5.29092986769127, 'o11': 4.350786005807231, 'o12': 9.949485419975568, 'o13': 8.363576317288588, 'o14': 8.043454580243829, 'o15': 8.977187100898044, 'o16': 7.834704856622336, 'o17': 8.116018372283634, 'o18': 2.9260948546603753, 'o19': 9.055016031336411, 'o20': 4.70269629516272, 'o21': 7.763598257660122}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12', 'o13'], 'type3': ['o14', 'o15', 'o16', 'o17', 'o18', 'o19'], 'type4': ['o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 19, 'r1': 8, 'r2': 12, 'r3': 2, 'r4': 8, 'r5': 17, 'r6': 6, 'm0': 16, 'm1': 20, 'm2': 6, 'm3': 4, 'm4': 3, 'm5': 10, 'fixer0': 2, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 22, 'o2': 13, 'o3': 8, 'o4': 12, 'o5': 11, 'o6': 13, 'o7': 10, 'o8': 8, 'o9': 8, 'o10': 11, 'o11': 15, 'o12': 5, 'o13': 7, 'o14': 20, 'o15': 16, 'o16': 6, 'o17': 13, 'o18': 18, 'o19': 15, 'o20': 20, 'o21': 17}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False}
    state.numUses = {'m0': 13, 'm1': 8, 'm2': 13, 'm3': 7, 'm4': 10, 'm5': 12}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    11: [['order', 'type0', 200]],
    1: [['order', 'type1', 200]],
    8: [['order', 'type1', 200]],
    17: [['order', 'type1', 200]],
    4: [['order', 'type1', 200]],
    20: [['order', 'type1', 200]],
    10: [['order', 'type2', 200]],
    18: [['order', 'type3', 200]],
    6: [['order', 'type3', 200]],
    16: [['order', 'type4', 200]],
    7: [['order', 'type4', 200]],
}
eventsEnv = {
}