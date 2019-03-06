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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9}

rv.GROUND_EDGES = {0: [5, 10, 1, 6, 8], 1: [0, 2, 10], 2: [1, 3], 3: [7, 2, 8, 9, 11], 4: [9], 5: [11, 0, 9], 6: [0, 7, 8, 200], 7: [6, 3, 10], 8: [0, 3, 6], 9: [3, 5, 11, 4], 10: [1, 7, 0], 11: [3, 9, 5], 200: [6]}
rv.GROUND_WEIGHTS = {(0, 5): 1, (0, 10): 5.344536633285017, (0, 1): 13.599277489576304, (0, 6): 9.166891946957914, (0, 8): 18.293792471643187, (1, 2): 6.54244369463435, (1, 10): 10.938167615632915, (2, 3): 13.076482499664596, (3, 7): 9.665566268391899, (3, 8): 6.07718583873136, (3, 9): 2.604303157965882, (3, 11): 10.064122463960768, (4, 9): 7.990687177037423, (5, 11): 6.072699071673304, (5, 9): 8.789101602099642, (6, 7): 1, (6, 8): 5.060468627960727, (6, 200): 9.98274531971919, (7, 10): 9.402132143355914, (9, 11): 9.452948664345392}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 6.2735009538737705, 'r1': 5.1062347358482025, 'r2': 6.452672087242858, 'r3': 9.00102901212996, 'r4': 7.497683192057469, 'r5': 6.947874514601823, 'r6': 10.346799457656925, 'r7': 7.26485071385084}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30']
rv.OBJ_WEIGHT = {'o0': 9.12183095140402, 'o1': 7.556537148663618, 'o2': 8.189975188637048, 'o3': 7.295729880493433, 'o4': 3.5331827106559097, 'o5': 7.676824067802897, 'o6': 8.824749693879243, 'o7': 6.756212558941044, 'o8': 3.7353726546286508, 'o9': 8.562029429357056, 'o10': 7.587824406453435, 'o11': 8.864070002488583, 'o12': 6.093642203063572, 'o13': 7.849724050305619, 'o14': 6.64958335190247, 'o15': 4.667230680846449, 'o16': 6.127562163022207, 'o17': 3.5365225754500815, 'o18': 6.237108444481269, 'o19': 8.29007921580102, 'o20': 6.2938974178549945, 'o21': 2.229284022837146, 'o22': 5.5882527486973546, 'o23': 7.853326921363047, 'o24': 9.368399482387789, 'o25': 5.451583683224572, 'o26': 3.4142486913191035, 'o27': 6.192955542700569, 'o28': 2.810645119901113, 'o29': 6.343333609897716, 'o30': 4.955159407527063}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18'], 'type3': ['o19', 'o20', 'o21', 'o22', 'o23'], 'type4': ['o24', 'o25'], 'type5': ['o26', 'o27', 'o28', 'o29', 'o30']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 0, 'r2': 9, 'r3': 7, 'r4': 2, 'r5': 9, 'r6': 6, 'r7': 2, 'm0': 2, 'm1': 2, 'm2': 7, 'm3': 5, 'm4': 8, 'm5': 7, 'fixer0': 8, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 7, 'o2': 11, 'o3': 11, 'o4': 3, 'o5': 11, 'o6': 11, 'o7': 3, 'o8': 6, 'o9': 6, 'o10': 6, 'o11': 6, 'o12': 4, 'o13': 7, 'o14': 1, 'o15': 2, 'o16': 1, 'o17': 2, 'o18': 9, 'o19': 8, 'o20': 8, 'o21': 10, 'o22': 11, 'o23': 5, 'o24': 1, 'o25': 2, 'o26': 0, 'o27': 11, 'o28': 5, 'o29': 5, 'o30': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False}
    state.numUses = {'m0': 9, 'm1': 13, 'm2': 8, 'm3': 9, 'm4': 11, 'm5': 5}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    21: [['order', 'type0', 200]],
    15: [['order', 'type0', 200]],
    32: [['order', 'type0', 200]],
    40: [['order', 'type0', 200]],
    33: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
    10: [['order', 'type1', 200]],
    41: [['order', 'type1', 200]],
    22: [['order', 'type1', 200]],
    39: [['order', 'type1', 200]],
    38: [['order', 'type1', 200]],
    34: [['order', 'type1', 200]],
    9: [['order', 'type2', 200]],
    35: [['order', 'type2', 200]],
    7: [['order', 'type3', 200]],
    37: [['order', 'type3', 200]],
    17: [['order', 'type3', 200]],
    2: [['order', 'type3', 200]],
    25: [['order', 'type3', 200]],
    23: [['order', 'type4', 200]],
    14: [['order', 'type4', 200]],
}
eventsEnv = {
}