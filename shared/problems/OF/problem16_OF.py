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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 2}

rv.GROUND_EDGES = {0: [10, 12, 4, 14], 1: [2], 2: [9, 13, 1], 3: [13, 5, 6, 7, 11], 4: [0, 10, 12, 11, 14], 5: [3, 7, 11], 6: [3, 7, 11, 13, 14], 7: [3, 5, 12, 6, 10, 200], 8: [9, 10, 11], 9: [11, 14, 2, 8, 200], 10: [7, 0, 4, 8], 11: [3, 4, 6, 9, 5, 8], 12: [0, 4, 7], 13: [3, 2, 6], 14: [0, 4, 6, 9], 200: [7, 9]}
rv.GROUND_WEIGHTS = {(0, 10): 10.07219104509902, (0, 12): 5.405200248136975, (0, 4): 14.642935315234151, (0, 14): 12.729683959941143, (1, 2): 7.481033543387969, (2, 9): 7.399124633160598, (2, 13): 9.639702741314442, (3, 13): 7.041476150178168, (3, 5): 2.4147240136264356, (3, 6): 8.131240849082525, (3, 7): 6.119935208215244, (3, 11): 12.210042376233822, (4, 10): 3.897993999967709, (4, 12): 3.660985915373826, (4, 11): 15.052080516582379, (4, 14): 13.440222919733227, (5, 7): 7.374253494968325, (5, 11): 7.918169055997053, (6, 7): 13.521650834638319, (6, 11): 16.053286483417075, (6, 13): 11.864391071126828, (6, 14): 13.844027633818037, (7, 12): 12.759054360224487, (7, 10): 12.89604794665848, (7, 200): 14.49416016049529, (8, 9): 6.07506752353687, (8, 10): 2.6265212262981485, (8, 11): 2.7704331797212065, (9, 11): 5.805661089485488, (9, 14): 8.290171715444247, (9, 200): 8.933556113469377}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 4.9023701863260385, 'r1': 8.704636045104383, 'r2': 6.849553691059741, 'r3': 11.123699859164045, 'r4': 8.557996729983058, 'r5': 9.166911799298541, 'r6': 7.165206155597559, 'r7': 7.992255175357095, 'r8': 6.835750267701533, 'r9': 10.160947003335565, 'r10': 6.0354070269155065, 'r11': 7.175251005060632}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26']
rv.OBJ_WEIGHT = {'o0': 10.143153877871502, 'o1': 6.715765163835023, 'o2': 9.26102831634582, 'o3': 3.6840411289703376, 'o4': 7.534304169957619, 'o5': 7.553509670536988, 'o6': 8.207812394403682, 'o7': 6.482479152730883, 'o8': 7.717552716041194, 'o9': 5.282730326356399, 'o10': 7.363320431411822, 'o11': 10.046700650941881, 'o12': 5.7740091937552345, 'o13': 2.5897120065576935, 'o14': 8.944291992841404, 'o15': 6.095781573155051, 'o16': 8.596217600812349, 'o17': 6.5715271609660135, 'o18': 5.581605586922871, 'o19': 7.28728365393179, 'o20': 7.137029101612727, 'o21': 3.9483174789839475, 'o22': 5.028673350583203, 'o23': 4.8096300523088145, 'o24': 8.793412560247102, 'o25': 7.767958113645139, 'o26': 3.1074646646016224}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type3': ['o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24'], 'type4': ['o25', 'o26']}

def ResetState():
    state.loc = { 'r0': 3, 'r1': 4, 'r2': 13, 'r3': 5, 'r4': 3, 'r5': 3, 'r6': 12, 'r7': 7, 'r8': 2, 'r9': 2, 'r10': 13, 'r11': 14, 'm0': 12, 'fixer0': 7, 'fixer1': 11, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK,}
    state.storedLoc = {'o0': 7, 'o1': 12, 'o2': 7, 'o3': 0, 'o4': 8, 'o5': 3, 'o6': 3, 'o7': 14, 'o8': 6, 'o9': 7, 'o10': 6, 'o11': 11, 'o12': 5, 'o13': 4, 'o14': 3, 'o15': 10, 'o16': 6, 'o17': 7, 'o18': 12, 'o19': 9, 'o20': 8, 'o21': 1, 'o22': 7, 'o23': 12, 'o24': 7, 'o25': 6, 'o26': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 7}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    9: [['order', 'type0', 200]],
    20: [['order', 'type0', 200]],
    28: [['order', 'type1', 200]],
    39: [['order', 'type1', 200]],
    17: [['order', 'type1', 200]],
    38: [['order', 'type1', 200]],
    15: [['order', 'type1', 200]],
    4: [['order', 'type1', 200]],
    30: [['order', 'type2', 200]],
    35: [['order', 'type2', 200]],
    16: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
    11: [['order', 'type2', 200]],
    27: [['order', 'type2', 200]],
    44: [['order', 'type3', 200]],
    37: [['order', 'type3', 200]],
    22: [['order', 'type3', 200]],
    21: [['order', 'type3', 200]],
    31: [['order', 'type3', 200]],
    19: [['order', 'type3', 200]],
    36: [['order', 'type3', 200]],
    23: [['order', 'type4', 200]],
    8: [['order', 'type4', 200]],
}
eventsEnv = {
}