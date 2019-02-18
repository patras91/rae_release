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
rv.SHIPPING_DOC = {rv.FACTORY1: 3.1370898194972865}

rv.GROUND_EDGES = {0: [2, 4, 1, 10, 11, 200], 1: [0, 11, 18], 2: [0, 6], 3: [5, 12, 13, 15, 6], 4: [10, 0, 15], 5: [7, 3, 6, 18], 6: [2, 3, 5, 8, 10], 7: [12, 5, 16], 8: [19, 6, 13, 14, 15, 18], 9: [17, 18], 10: [0, 4, 6, 14], 11: [0, 1, 19], 12: [13, 3, 7], 13: [8, 3, 12, 14], 14: [8, 10, 13, 16], 15: [4, 8, 3], 16: [7, 19, 14], 17: [19, 9], 18: [1, 5, 8, 9], 19: [11, 8, 16, 17], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 2): 1.6077379593220638, (0, 4): 6.398636320114307, (0, 1): 8.105509472824458, (0, 10): 14.33610974220788, (0, 11): 11.071817996852717, (0, 200): 8.481329006526554, (1, 11): 10.758281925599785, (1, 18): 3.294931341007728, (2, 6): 1.9997028574693099, (3, 5): 7.574801734943816, (3, 12): 14.231945443787172, (3, 13): 8.575771868342748, (3, 15): 6.105788739938344, (3, 6): 6.221622466248931, (4, 10): 1.7873490228362385, (4, 15): 10.297989882156545, (5, 7): 13.38409509562279, (5, 6): 4.589190161273919, (5, 18): 10.662488934361777, (6, 8): 8.893792964788448, (6, 10): 3.399295218508877, (7, 12): 10.956112519680646, (7, 16): 17.00028307496172, (8, 19): 6.934400660696071, (8, 13): 2.451517344186862, (8, 14): 9.812167955800374, (8, 15): 9.724656216894111, (8, 18): 10.836973574497271, (9, 17): 12.339551969650923, (9, 18): 11.147368078544197, (10, 14): 8.109049247167118, (11, 19): 14.061340387890416, (12, 13): 8.629035047418846, (13, 14): 12.579713713767568, (14, 16): 11.35141597660319, (16, 19): 9.404549203904006, (17, 19): 15.273475077792003}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12']
rv.ROBOT_CAPACITY = {'r0': 8.034325570969495, 'r1': 12.347590817556512, 'r2': 10.128202789095962, 'r3': 7.742286370062695, 'r4': 12.638309531668163, 'r5': 11.506279405467778, 'r6': 11.003956234396316, 'r7': 6.996678771262763, 'r8': 4.984844884039367, 'r9': 3.417518964572383, 'r10': 7.5045578458526645, 'r11': 9.545686089087111, 'r12': 6.383027431739396}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'fixer0']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']
rv.OBJ_WEIGHT = {'o0': 4.860038947079433, 'o1': 3.867707358031883, 'o2': 7.183047362050516, 'o3': 3.9102360024235616, 'o4': 7.939616675634691, 'o5': 3.829504474824975, 'o6': 2.89370423221997, 'o7': 6.047471143139306, 'o8': 7.619296546689139, 'o9': 8.551215361726276, 'o10': 6.030432511498844, 'o11': 5.014498736895727, 'o12': 5.860633282114696, 'o13': 5.262890538029251, 'o14': 4.5401138187660575, 'o15': 7.337888864099123, 'o16': 6.961819184403642, 'o17': 5.844993417526083, 'o18': 5.258117007138405, 'o19': 5.277352585440189, 'o20': 5.544756499952188, 'o21': 5.950298338247594, 'o22': 9.43607226343205, 'o23': 10.625769464565012, 'o24': 4.320460318272264, 'o25': 7.160247966827406}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5'], 'type2': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15', 'o16', 'o17', 'o18'], 'type4': ['o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']}

def ResetState():
  state.loc = { r0: 6, r1: 17, r2: 18, r3: 19, r4: 6, r5: 2, r6: 16, r7: 10, r8: 12, r9: 5, r10: 3, r11: 14, r12: 15, m0: 10, m1: 2, m2: 11, m3: 13, m4: 14, m5: 10, m6: 17, m7: 4, m8: 1, m9: 3, fixer0: 1, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK, o20: UNK, o21: UNK, o22: UNK, o23: UNK, o24: UNK, o25: UNK,}
    state.storedLoc{'o0': 12, 'o1': 7, 'o2': 12, 'o3': 7, 'o4': 15, 'o5': 3, 'o6': 10, 'o7': 10, 'o8': 10, 'o9': 1, 'o10': 1, 'o11': 1, 'o12': 8, 'o13': 9, 'o14': 7, 'o15': 14, 'o16': 15, 'o17': 18, 'o18': 6, 'o19': 7, 'o20': 4, 'o21': 5, 'o22': 8, 'o23': 3, 'o24': 0, 'o25': 3}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL, o20: NIL, o21: NIL, o22: NIL, o23: NIL, o24: NIL, o25: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'fixer0': False}
    state.numUses8
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    8: [['order', type0, 200]],
    6: [['order', type0, 200]],
    3: [['order', type1, 200]],
    8: [['order', type1, 200]],
    3: [['order', type1, 200]],
    1: [['order', type1, 200]],
    3: [['order', type2, 200]],
    4: [['order', type2, 200]],
    6: [['order', type2, 200]],
    6: [['order', type2, 200]],
    4: [['order', type2, 200]],
    8: [['order', type2, 200]],
    1: [['order', type3, 200]],
    6: [['order', type4, 200]],
    1: [['order', type4, 200]],
    4: [['order', type4, 200]],
    4: [['order', type4, 200]],
    1: [['order', type4, 200]],
    2: [['order', type4, 200]],
    5: [['order', type4, 200]],
}
eventsEnv = {
}