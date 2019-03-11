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
rv.SHIPPING_DOC = {rv.FACTORY1: 3}

rv.GROUND_EDGES = {0: [9, 3, 5, 13], 1: [3], 2: [6, 12, 16], 3: [0, 8, 11, 13, 1, 18], 4: [8, 13, 15, 12], 5: [0, 18], 6: [11, 17, 18, 2, 7], 7: [6, 18, 11, 200], 8: [4, 3], 9: [0], 10: [15, 17, 12], 11: [7, 12, 16, 3, 6, 200], 12: [4, 10, 2, 11, 15, 16], 13: [0, 3, 4], 14: [15, 17], 15: [10, 12, 4, 14, 200], 16: [2, 11, 12, 18], 17: [18, 6, 10, 14], 18: [3, 5, 16, 6, 7, 17], 200: [7, 11, 15]}
rv.GROUND_WEIGHTS = {(0, 9): 5.179462266383771, (0, 3): 8.659653705505692, (0, 5): 15.623592321152007, (0, 13): 10.08657977009738, (1, 3): 11.078019988621776, (2, 6): 4.390286002067725, (2, 12): 10.343468891603425, (2, 16): 4.292604130499093, (3, 8): 12.86269269208687, (3, 11): 7.459444889533492, (3, 13): 3.041450956832098, (3, 18): 3.116021963432247, (4, 8): 5.433749740841494, (4, 13): 10.324273445236763, (4, 15): 9.802182890368499, (4, 12): 2.8409332874613877, (5, 18): 6.439268695752489, (6, 11): 9.002665478380784, (6, 17): 7.449982173702517, (6, 18): 8.879731239215138, (6, 7): 2.985367944183949, (7, 18): 3.340778102741912, (7, 11): 4.419943554971104, (7, 200): 1.3282594012144848, (10, 15): 3.029784430488223, (10, 17): 1.9781033221282707, (10, 12): 3.8930686461036776, (11, 12): 1.9299607404441437, (11, 16): 9.354450452870319, (11, 200): 9.957936938797399, (12, 15): 7.3841507696820505, (12, 16): 7.736535856121699, (14, 15): 12.50729855711256, (14, 17): 10.047695737016387, (15, 200): 5.004600850547961, (16, 18): 8.712169367876836, (17, 18): 15.276210748421716}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.562226541819154, 'r1': 7.165713805984856, 'r2': 8.253865545170681, 'r3': 9.170333916109687, 'r4': 7.6452087161086055, 'r5': 7.927683183629742, 'r6': 5.469926687719044, 'r7': 11.514094594917836, 'r8': 10.701124695798114, 'r9': 8.810063885285032, 'r10': 8.09606215604692}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 8.272804955750633, 'o1': 4.978757809209139, 'o2': 7.071275212325014, 'o3': 7.512586911520389, 'o4': 7.191579904260357, 'o5': 3.5379928575435944, 'o6': 5.934281668355101, 'o7': 5.4967681931692205, 'o8': 7.481836656809018, 'o9': 10.057694939177487, 'o10': 9.054802766848278, 'o11': 9.13947313014715, 'o12': 5.0615349701050185, 'o13': 4.419867935052061, 'o14': 1.8676921052480076, 'o15': 6.988014935984052, 'o16': 5.20351269464881, 'o17': 7.340970101791568, 'o18': 9.988225743659603, 'o19': 8.0581060164893, 'o20': 7.37668796750498, 'o21': 5.991647543539925}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10'], 'type3': ['o11', 'o12', 'o13', 'o14', 'o15', 'o16'], 'type4': ['o17', 'o18', 'o19', 'o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 9, 'r1': 17, 'r2': 5, 'r3': 15, 'r4': 18, 'r5': 3, 'r6': 18, 'r7': 16, 'r8': 2, 'r9': 9, 'r10': 8, 'm0': 1, 'm1': 0, 'fixer0': 7, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 6, 'o1': 14, 'o2': 12, 'o3': 3, 'o4': 0, 'o5': 1, 'o6': 15, 'o7': 1, 'o8': 11, 'o9': 17, 'o10': 14, 'o11': 11, 'o12': 11, 'o13': 0, 'o14': 12, 'o15': 10, 'o16': 17, 'o17': 18, 'o18': 5, 'o19': 18, 'o20': 6, 'o21': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 10, 'm1': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    28: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
}
eventsEnv = {
}