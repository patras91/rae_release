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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [1, 2, 3, 7, 10, 14, 16], 1: [0, 4, 7, 12, 15, 200], 2: [0, 6, 9, 8], 3: [0], 4: [1, 7, 200], 5: [7, 12, 6, 9], 6: [5, 7, 2, 13], 7: [0, 1, 4, 8, 13, 14, 5, 6], 8: [2, 9, 14, 7, 15, 200], 9: [5, 11, 16, 2, 8], 10: [0], 11: [9], 12: [1, 5], 13: [6, 7], 14: [0, 7, 8, 15], 15: [1, 8, 14, 16], 16: [0, 9, 15, 200], 200: [1, 4, 8, 16]}
rv.GROUND_WEIGHTS = {(0, 1): 8.462790163017997, (0, 2): 9.81410472800401, (0, 3): 3.594483029905727, (0, 7): 7.3373279350097205, (0, 10): 7.719971774951489, (0, 14): 8.407073393044458, (0, 16): 8.226388666066399, (1, 4): 6.803164021826825, (1, 7): 11.98470923114101, (1, 12): 1.4019343000211126, (1, 15): 7.658595516072437, (1, 200): 8.275491667562504, (2, 6): 6.128298416631865, (2, 9): 2.9122464631307494, (2, 8): 4.112879071250152, (4, 7): 4.717771177882421, (4, 200): 9.166240636277417, (5, 7): 8.180334547166247, (5, 12): 10.595141202379637, (5, 6): 6.021706865658524, (5, 9): 15.379298362852293, (6, 7): 7.070885996765231, (6, 13): 9.612653762683777, (7, 8): 8.071020903799187, (7, 13): 9.982496615713549, (7, 14): 1, (8, 9): 7.674184888575679, (8, 14): 1, (8, 15): 4.50616884327996, (8, 200): 9.71252126007521, (9, 11): 16.768910489023924, (9, 16): 1, (14, 15): 12.691639509289125, (15, 16): 4.298270148135273, (16, 200): 9.389033150439825}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.85926884826157, 'r1': 9.444608291799037, 'r2': 10.879599348027275, 'r3': 10.781675778753753, 'r4': 9.438432159732143, 'r5': 5.970322112149838, 'r6': 6.893654644464376, 'r7': 6.722477006163355}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']
rv.OBJ_WEIGHT = {'o0': 9.57624510370637, 'o1': 7.16577946330248, 'o2': 7.498440012753972, 'o3': 8.91367294620096, 'o4': 6.605930790787679, 'o5': 7.793355933309081, 'o6': 3.411689080110597, 'o7': 7.023114158987552, 'o8': 2.908270139537345, 'o9': 4.759624784882262, 'o10': 4.194488663475985, 'o11': 8.300266561592405, 'o12': 6.254926412542725, 'o13': 6.8842523422541015, 'o14': 10.156420693211798, 'o15': 1.814013867964107, 'o16': 6.643024705433071, 'o17': 5.620126455657786, 'o18': 10.205271286774654, 'o19': 5.330247634326916, 'o20': 7.9545168840884966, 'o21': 7.759925835581175, 'o22': 7.35627877159371, 'o23': 6.934553945051674}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4'], 'type2': ['o5', 'o6', 'o7', 'o8', 'o9'], 'type3': ['o10', 'o11', 'o12', 'o13'], 'type4': ['o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20'], 'type5': ['o21', 'o22', 'o23']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 8, 'r2': 8, 'r3': 6, 'r4': 7, 'r5': 16, 'r6': 4, 'r7': 0, 'm0': 6, 'fixer0': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 9, 'o2': 11, 'o3': 12, 'o4': 13, 'o5': 3, 'o6': 1, 'o7': 16, 'o8': 5, 'o9': 5, 'o10': 8, 'o11': 7, 'o12': 14, 'o13': 4, 'o14': 14, 'o15': 5, 'o16': 5, 'o17': 5, 'o18': 15, 'o19': 10, 'o20': 1, 'o21': 5, 'o22': 13, 'o23': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 8}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    7: [['order', 'type0', 200]],
    9: [['order', 'type0', 200]],
    8: [['order', 'type1', 200]],
    31: [['order', 'type1', 200]],
    33: [['order', 'type1', 200]],
    26: [['order', 'type3', 200]],
    5: [['order', 'type3', 200]],
    16: [['order', 'type3', 200]],
    6: [['order', 'type3', 200]],
    10: [['order', 'type4', 200]],
    27: [['order', 'type4', 200]],
    14: [['order', 'type4', 200]],
    1: [['order', 'type4', 200]],
    2: [['order', 'type4', 200]],
    29: [['order', 'type5', 200]],
    32: [['order', 'type5', 200]],
    25: [['order', 'type5', 200]],
}
eventsEnv = {
}