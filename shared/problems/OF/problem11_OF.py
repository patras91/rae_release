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
rv.SHIPPING_DOC = {rv.FACTORY1: 7.035753228629384}

rv.GROUND_EDGES = {0: [6, 4, 5, 10, 13], 1: [15, 2, 9, 14], 2: [1, 8, 11], 3: [16, 10], 4: [0, 10, 12, 16], 5: [0, 6, 9, 11, 200], 6: [5, 0], 7: [12], 8: [10, 2, 12], 9: [1, 5, 15, 11, 12, 13], 10: [0, 3, 4, 12, 8, 13, 15], 11: [5, 9, 15, 2], 12: [4, 8, 9, 10, 15, 7], 13: [0, 9, 10], 14: [1], 15: [1, 10, 11, 9, 12], 16: [4, 3], 200: [5]}
rv.GROUND_WEIGHTS = {(0, 6): 7.186106953952249, (0, 4): 4.804989438303182, (0, 5): 1, (0, 10): 8.999825743250984, (0, 13): 12.895744937785242, (1, 15): 6.323034915532362, (1, 2): 12.182830921424621, (1, 9): 17.54817825100048, (1, 14): 3.462383287628265, (2, 8): 14.794746811240714, (2, 11): 9.279166799533334, (3, 16): 15.54408969997662, (3, 10): 8.941042242829818, (4, 10): 11.34869023219828, (4, 12): 3.8350549116443373, (4, 16): 3.2507195518023, (5, 6): 4.219867529518325, (5, 9): 15.874063773682227, (5, 11): 1, (5, 200): 6.586668299645914, (7, 12): 8.284659748850567, (8, 10): 12.819011917353638, (8, 12): 13.214106551817059, (9, 15): 10.956572017147032, (9, 11): 11.719932545889444, (9, 12): 6.280510386774127, (9, 13): 7.634149972958873, (10, 12): 8.051254405746425, (10, 13): 13.967457053587056, (10, 15): 1, (11, 15): 3.17556233548465, (12, 15): 13.64627595633273}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9']
rv.ROBOT_CAPACITY = {'r0': 9.833280754092232, 'r1': 10.901447139956344, 'r2': 7.73105709479501, 'r3': 8.972842614628105, 'r4': 5.977188951180522, 'r5': 8.856200074912026, 'r6': 7.832678267499132, 'r7': 9.14784801098482, 'r8': 9.95281500805455, 'r9': 9.98077391416953}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29']
rv.OBJ_WEIGHT = {'o0': 7.0937562138500185, 'o1': 4.297861053180663, 'o2': 6.91765672057719, 'o3': 6.59585140565773, 'o4': 8.16686181226195, 'o5': 6.4393258503310005, 'o6': 5.660770093756941, 'o7': 6.66353050041872, 'o8': 6.151664112923878, 'o9': 9.666482565885756, 'o10': 5.490991179633231, 'o11': 5.0976699115845205, 'o12': 7.80127366350516, 'o13': 5.308571443696101, 'o14': 5.992278952801447, 'o15': 4.703545230652022, 'o16': 8.835084593443138, 'o17': 4.9916085648166515, 'o18': 3.559357920712446, 'o19': 9.491883713786677, 'o20': 8.408386922735838, 'o21': 8.338699961109597, 'o22': 7.552460588883928, 'o23': 2.74825214548928, 'o24': 5.793989285219512, 'o25': 3.1820847633786817, 'o26': 6.208356624766201, 'o27': 9.596863290622188, 'o28': 8.077210308543725, 'o29': 10.901447139956344}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16'], 'type3': ['o17', 'o18', 'o19', 'o20'], 'type4': ['o21', 'o22'], 'type5': ['o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 9, 'r2': 13, 'r3': 6, 'r4': 10, 'r5': 8, 'r6': 1, 'r7': 3, 'r8': 9, 'r9': 8, 'm0': 7, 'm1': 10, 'm2': 13, 'm3': 10, 'm4': 8, 'm5': 10, 'm6': 12, 'm7': 5, 'fixer0': 9, 'fixer1': 1, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 2, 'o2': 16, 'o3': 2, 'o4': 4, 'o5': 13, 'o6': 14, 'o7': 0, 'o8': 3, 'o9': 6, 'o10': 14, 'o11': 10, 'o12': 13, 'o13': 15, 'o14': 8, 'o15': 8, 'o16': 9, 'o17': 10, 'o18': 13, 'o19': 15, 'o20': 2, 'o21': 6, 'o22': 9, 'o23': 8, 'o24': 16, 'o25': 4, 'o26': 8, 'o27': 2, 'o28': 8, 'o29': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'m4'": False, "'m5'": False, "'m6'": False, "'m7'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 13, 'm1': 13, 'm2': 10, 'm3': 14, 'm4': 9, 'm5': 15, 'm6': 11, 'm7': 9, 'fixer0': 4, 'fixer1': 7}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    20: [['order', 'type1', 200]],
    21: [['order', 'type1', 200]],
    29: [['order', 'type1', 200]],
    30: [['order', 'type1', 200]],
    26: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    18: [['order', 'type2', 200]],
    17: [['order', 'type2', 200]],
    13: [['order', 'type2', 200]],
    36: [['order', 'type2', 200]],
    31: [['order', 'type2', 200]],
    28: [['order', 'type3', 200]],
    32: [['order', 'type4', 200]],
    7: [['order', 'type4', 200]],
    16: [['order', 'type5', 200]],
    9: [['order', 'type5', 200]],
    41: [['order', 'type5', 200]],
    4: [['order', 'type5', 200]],
    22: [['order', 'type5', 200]],
    1: [['order', 'type5', 200]],
    14: [['order', 'type5', 200]],
}
eventsEnv = {
}