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
rv.SHIPPING_DOC = {rv.FACTORY1: 14}

rv.GROUND_EDGES = {0: [1, 4, 6, 8, 9, 15, 200], 1: [4, 16, 17, 20, 0], 2: [5, 10, 17, 20], 3: [10, 12, 17], 4: [0, 1], 5: [12, 2, 19], 6: [0, 14], 7: [15, 14, 20], 8: [0, 10, 20], 9: [0, 11], 10: [2, 8, 11, 3, 17, 19, 20], 11: [9, 13, 10, 16], 12: [3, 17, 5, 18], 13: [14, 19, 11], 14: [6, 7, 19, 13], 15: [0, 18, 20, 7], 16: [11, 1], 17: [3, 10, 19, 1, 2, 12, 18], 18: [12, 17, 15], 19: [5, 10, 20, 13, 14, 17], 20: [7, 8, 10, 19, 1, 2, 15], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 1): 8.932004509280342, (0, 4): 10.942171730945624, (0, 6): 2.6158545414351293, (0, 8): 4.0093363455363935, (0, 9): 10.345695544809379, (0, 15): 8.354559454504503, (0, 200): 6.315610771564879, (1, 4): 12.562684680221077, (1, 16): 7.427629514950457, (1, 17): 14.1295560738359, (1, 20): 6.595671806865673, (2, 5): 1, (2, 10): 8.3607808871332, (2, 17): 6.747720633681473, (2, 20): 5.089095633418955, (3, 10): 9.170337593069599, (3, 12): 3.747306830048572, (3, 17): 2.027216903302395, (5, 12): 9.93183256097113, (5, 19): 6.973738501803219, (6, 14): 1.755437977730578, (7, 15): 8.705550616937431, (7, 14): 7.108261813952407, (7, 20): 12.949923775703773, (8, 10): 9.824651084454855, (8, 20): 6.01267654492516, (9, 11): 12.779182856345942, (10, 11): 8.629491031127694, (10, 17): 9.969990519501463, (10, 19): 5.392518175352519, (10, 20): 9.1394099081771, (11, 13): 11.176686517653883, (11, 16): 8.740761309449152, (12, 17): 3.2620693277715924, (12, 18): 1, (13, 14): 6.145636957493052, (13, 19): 7.823837113253359, (14, 19): 10.724282381234874, (15, 18): 3.0638772578914306, (15, 20): 9.452662284679274, (17, 19): 4.165869487016665, (17, 18): 6.379062161032466, (19, 20): 14.266559577952101}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1,  'r15': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.02764142234542, 'r1': 8.243509767295732, 'r2': 8.509324606338232, 'r3': 13.671131207867983, 'r4': 10.050660567272631, 'r5': 8.856452859102086, 'r6': 8.327240555833061, 'r7': 5.810583831261188, 'r8': 9.22816176901063, 'r9': 11.005645527714153, 'r10': 8.346443922456798, 'r11': 11.45691262478773, 'r12': 12.583102348246346, 'r13': 6.106218851488627, 'r14': 11.0946392395775, 'r15': 5.903810798070541}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 5.992698344107038, 'o1': 7.625150571689507, 'o2': 4.0994339508017505, 'o3': 6.146105696345082, 'o4': 7.945381497030153, 'o5': 4.244837648815636, 'o6': 8.783671408748901, 'o7': 3.8104097431230386, 'o8': 3.9159497711758737, 'o9': 9.011140300174878, 'o10': 6.9533785273065, 'o11': 3.514031127192881, 'o12': 6.188730283991653, 'o13': 6.502853329642839, 'o14': 5.938405047717242, 'o15': 6.355318680932055, 'o16': 7.028784024655261}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7'], 'type2': ['o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 16, 'r2': 18, 'r3': 13, 'r4': 19, 'r5': 18, 'r6': 5, 'r7': 3, 'r8': 0, 'r9': 17, 'r10': 18, 'r11': 10, 'r12': 11, 'r13': 15, 'r14': 14, 'r15': 15, 'm0': 2, 'm1': 8, 'm2': 10, 'm3': 7, 'm4': 14, 'm5': 19, 'm6': 3, 'm7': 19, 'm8': 20, 'm9': 15, 'm10': 14, 'fixer0': 14, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 15, 'o1': 10, 'o2': 7, 'o3': 5, 'o4': 19, 'o5': 19, 'o6': 15, 'o7': 8, 'o8': 4, 'o9': 10, 'o10': 11, 'o11': 9, 'o12': 0, 'o13': 16, 'o14': 2, 'o15': 8, 'o16': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'r15': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'fixer0': False}
    state.numUses = {'m0': 14, 'm1': 7, 'm2': 7, 'm3': 8, 'm4': 7, 'm5': 8, 'm6': 8, 'm7': 5, 'm8': 10, 'm9': 11, 'm10': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    11: [['order', 'type0', 200]],
    6: [['order', 'type0', 200]],
    13: [['order', 'type0', 200]],
    15: [['order', 'type2', 200]],
    3: [['order', 'type2', 200]],
    8: [['order', 'type2', 200]],
    2: [['order', 'type2', 200]],
    9: [['order', 'type3', 200]],
}
eventsEnv = {
}