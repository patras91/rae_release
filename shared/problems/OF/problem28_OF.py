__author__ = 'mason'
from domain_orderFulfillment import *
from timer import DURATION
from state import state
import numpy as np

def GetCostOfMove(id, r, loc1, loc2, dist):
    return 1 + dist

def GetCostOfLookup(id, item):
    return max(1, np.random.beta(2, 2))

def GetCostOfWrap(id, m, item):
    return max(1, np.random.normal(5, .5))

def GetCostOfPickup(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfPutdown(id, r, item):
    return max(1, np.random.normal(4, 1))

def GetCostOfLoad(id, r, m, item):
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
    'repair': 5,
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
    'repair': 5,
    'wait': 1
}

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [8, 1, 4, 5], 1: [0, 12, 17], 2: [9, 12, 18], 3: [15, 13, 14], 4: [0, 7, 14], 5: [0, 7, 11, 200], 6: [14, 18, 7, 17], 7: [4, 5, 6, 14, 200, 15, 16], 8: [0, 9, 13, 17], 9: [10, 2, 8], 10: [16, 9], 11: [5, 13], 12: [1, 2, 18, 19], 13: [3, 15, 16, 8, 11, 19], 14: [3, 4, 6, 7], 15: [7, 3, 13, 16], 16: [7, 15, 10, 13, 200], 17: [1, 6, 8], 18: [2, 6, 12], 19: [13, 12], 200: [5, 16, 7]}
rv.GROUND_WEIGHTS = {(0, 8): 14.133050939711122, (0, 1): 9.720334895116123, (0, 4): 13.101940282621502, (0, 5): 8.98117971687945, (1, 12): 8.69528584307923, (1, 17): 4.1362176948031415, (2, 9): 2.248758372191917, (2, 12): 13.144777896253395, (2, 18): 5.511860744671213, (3, 15): 11.576531323303227, (3, 13): 7.61086516621345, (3, 14): 4.331339014722168, (4, 7): 7.810129694926172, (4, 14): 8.554292293428883, (5, 7): 4.183458890280213, (5, 11): 1, (5, 200): 11.737159989242215, (6, 14): 10.797588704667827, (6, 18): 6.437177012959118, (6, 7): 14.563410585226542, (6, 17): 13.784093052018022, (7, 14): 10.823933541827369, (7, 200): 8.15960298377763, (7, 15): 5.7171342296130945, (7, 16): 8.491951320885583, (8, 9): 12.852666739312763, (8, 13): 16.332039446136967, (8, 17): 10.543158948300501, (9, 10): 4.845676220515105, (10, 16): 7.443728644530777, (11, 13): 9.153889941788481, (12, 18): 5.594469183068259, (12, 19): 8.42369711723, (13, 15): 7.706092646412265, (13, 16): 12.618660731902107, (13, 19): 6.112407075969623, (15, 16): 8.783163123563872, (16, 200): 5.677164433749438}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.341612523237761, 'r1': 8.823841291242655, 'r2': 9.628910031940606, 'r3': 8.965203115071692, 'r4': 5.092134149127807, 'r5': 4.874409085688948, 'r6': 6.7689480512869045, 'r7': 10.564207173843194, 'r8': 7.643151288618503, 'r9': 6.704513920886947, 'r10': 8.330724159641784, 'r11': 8.691080485052993, 'r12': 4.899945474491379}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30']
rv.OBJ_WEIGHT = {'o0': 5.051281806773729, 'o1': 4.6404864661529714, 'o2': 6.054326202805577, 'o3': 10.564207173843194, 'o4': 6.783371489322348, 'o5': 10.564207173843194, 'o6': 9.130157087229744, 'o7': 6.663153738356589, 'o8': 7.150296996482554, 'o9': 10.297256542491844, 'o10': 7.885751990063828, 'o11': 6.423341020579042, 'o12': 8.998535289183677, 'o13': 6.0796840845242475, 'o14': 5.074977437230851, 'o15': 7.366388258640201, 'o16': 5.000042767660129, 'o17': 6.7898113799973805, 'o18': 7.438577453018147, 'o19': 6.488832872732477, 'o20': 5.828005902846621, 'o21': 4.972068096607515, 'o22': 4.76440888536745, 'o23': 8.215474204315118, 'o24': 4.915701872779451, 'o25': 6.50869582326547, 'o26': 6.249616800891649, 'o27': 3.319216625585561, 'o28': 9.670046127954041, 'o29': 9.234381247278627, 'o30': 7.736892697618068}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15'], 'type4': ['o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22'], 'type5': ['o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30']}

def ResetState():
    state.loc = { 'r0': 11, 'r1': 18, 'r2': 16, 'r3': 0, 'r4': 0, 'r5': 7, 'r6': 0, 'r7': 6, 'r8': 4, 'r9': 9, 'r10': 7, 'r11': 7, 'r12': 9, 'm0': 4, 'fixer0': 5, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK,}
    state.storedLoc = {'o0': 19, 'o1': 11, 'o2': 13, 'o3': 1, 'o4': 12, 'o5': 8, 'o6': 7, 'o7': 5, 'o8': 7, 'o9': 17, 'o10': 8, 'o11': 11, 'o12': 11, 'o13': 17, 'o14': 7, 'o15': 4, 'o16': 10, 'o17': 10, 'o18': 17, 'o19': 13, 'o20': 10, 'o21': 8, 'o22': 6, 'o23': 12, 'o24': 0, 'o25': 1, 'o26': 8, 'o27': 10, 'o28': 19, 'o29': 0, 'o30': 19}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    29: [['order', 'type0', 200]],
    31: [['order', 'type0', 200]],
}
eventsEnv = {
}