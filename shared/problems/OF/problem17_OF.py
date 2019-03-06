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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 8}

rv.GROUND_EDGES = {0: [1, 3, 5, 6, 7, 10, 12, 200], 1: [0, 7], 2: [5, 11, 4], 3: [0], 4: [2, 200], 5: [0, 2, 8, 200], 6: [0, 9, 11], 7: [0, 1, 200], 8: [5], 9: [6], 10: [0, 12, 11], 11: [6, 10, 12, 2], 12: [0, 10, 11, 200], 200: [0, 4, 5, 7, 12]}
rv.GROUND_WEIGHTS = {(0, 1): 11.69004109442996, (0, 3): 7.110049947974285, (0, 5): 2.3454206305770375, (0, 6): 10.60503752556484, (0, 7): 4.43428777045475, (0, 10): 1, (0, 12): 1, (0, 200): 8.08031603997927, (1, 7): 9.272813653438108, (2, 5): 9.494979309740833, (2, 11): 6.421247671295811, (2, 4): 10.382555354583316, (4, 200): 7.2565649185988175, (5, 8): 10.054835791433089, (5, 200): 5.568129287094251, (6, 9): 14.843281014966252, (6, 11): 8.866032051858275, (7, 200): 13.636255547549958, (10, 12): 11.792657999342136, (10, 11): 9.067324588237383, (11, 12): 8.990602772692824, (12, 200): 5.7205874800537355}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.921871224901258, 'r1': 8.134445978146685, 'r2': 6.537659492530862, 'r3': 5.5106422552064425, 'r4': 4.54556292817966, 'r5': 7.386573091181315, 'r6': 7.623909672132154, 'r7': 6.13076250166827, 'r8': 9.814983354123582}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30']
rv.OBJ_WEIGHT = {'o0': 7.69598146420042, 'o1': 7.0283988602957885, 'o2': 3.39841217741717, 'o3': 7.6034327670263115, 'o4': 0.8231373104657802, 'o5': 8.986740638503337, 'o6': 9.657393112237598, 'o7': 6.191821294604906, 'o8': 7.4490065165937365, 'o9': 7.750704374430541, 'o10': 6.986247343135306, 'o11': 5.056514758115949, 'o12': 5.345916211950361, 'o13': 5.718414126954473, 'o14': 5.572586424981095, 'o15': 8.543390266671086, 'o16': 4.401601402063136, 'o17': 8.290908181221313, 'o18': 2.4078113928546054, 'o19': 7.833341880871194, 'o20': 5.118219292485353, 'o21': 9.806750532160539, 'o22': 8.589432529800579, 'o23': 9.220228057414595, 'o24': 5.213099358702657, 'o25': 3.195427224305406, 'o26': 6.206198878223197, 'o27': 6.954338967062647, 'o28': 6.214511424286083, 'o29': 6.1912339083653904, 'o30': 4.7903218319190435}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16'], 'type3': ['o17', 'o18', 'o19', 'o20', 'o21', 'o22'], 'type4': ['o23', 'o24', 'o25'], 'type5': ['o26', 'o27', 'o28', 'o29', 'o30']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 0, 'r2': 6, 'r3': 4, 'r4': 4, 'r5': 4, 'r6': 1, 'r7': 3, 'r8': 9, 'm0': 1, 'fixer0': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK,}
    state.storedLoc = {'o0': 12, 'o1': 0, 'o2': 7, 'o3': 8, 'o4': 5, 'o5': 3, 'o6': 6, 'o7': 11, 'o8': 11, 'o9': 7, 'o10': 5, 'o11': 9, 'o12': 9, 'o13': 8, 'o14': 11, 'o15': 2, 'o16': 8, 'o17': 10, 'o18': 6, 'o19': 10, 'o20': 2, 'o21': 8, 'o22': 9, 'o23': 8, 'o24': 6, 'o25': 5, 'o26': 7, 'o27': 8, 'o28': 10, 'o29': 12, 'o30': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 10}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    20: [['order', 'type0', 200]],
    24: [['order', 'type0', 200]],
    4: [['order', 'type0', 200]],
    17: [['order', 'type0', 200]],
    9: [['order', 'type0', 200]],
    7: [['order', 'type3', 200]],
    18: [['order', 'type3', 200]],
    14: [['order', 'type3', 200]],
    29: [['order', 'type4', 200]],
    15: [['order', 'type4', 200]],
    6: [['order', 'type4', 200]],
    13: [['order', 'type5', 200]],
    27: [['order', 'type5', 200]],
    2: [['order', 'type5', 200]],
    25: [['order', 'type5', 200]],
    30: [['order', 'type5', 200]],
}
eventsEnv = {
}