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
rv.SHIPPING_DOC = {rv.FACTORY1: 9}

rv.GROUND_EDGES = {0: [10, 6, 7, 9, 12, 13, 14], 1: [11, 8, 200], 2: [7], 3: [4, 10, 5], 4: [7, 8, 3, 12, 200], 5: [3, 12, 13], 6: [0], 7: [0, 2, 4, 13], 8: [1, 11, 14, 4], 9: [0, 10, 11, 13], 10: [9, 0, 3, 11, 13], 11: [9, 10, 1, 8], 12: [0, 4, 13, 5], 13: [0, 7, 9, 10, 5, 12], 14: [0, 8], 200: [1, 4]}
rv.GROUND_WEIGHTS = {(0, 10): 11.78014833245399, (0, 6): 12.152248670237583, (0, 7): 6.4948772729583935, (0, 9): 2.1976377157256515, (0, 12): 6.520251761195633, (0, 13): 9.586181639174916, (0, 14): 8.128424957283354, (1, 11): 7.082415045275027, (1, 8): 12.943911159589156, (1, 200): 8.997443012922586, (2, 7): 7.591348687715993, (3, 4): 1, (3, 10): 11.659602402264035, (3, 5): 10.995838991715726, (4, 7): 8.008332814200012, (4, 8): 2.3908568712135914, (4, 12): 7.105950467590271, (4, 200): 5.864512167118434, (5, 12): 11.547198664875168, (5, 13): 8.492130250940845, (7, 13): 8.725902446572178, (8, 11): 7.304868462426259, (8, 14): 6.3747295986288, (9, 10): 7.916972086038156, (9, 11): 10.999597011273686, (9, 13): 1, (10, 11): 6.1165478534952324, (10, 13): 7.523396695991095, (12, 13): 9.601933916529939}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.187214632044585, 'r1': 4.491129112304801, 'r2': 7.235171898910824, 'r3': 8.223957673156614, 'r4': 7.568394015266714, 'r5': 6.038596075787024, 'r6': 11.137877858514157, 'r7': 9.182619555748872, 'r8': 7.317043042436569, 'r9': 7.318988070274694, 'r10': 8.729590949517116, 'r11': 6.663596850129487, 'r12': 9.395203327483086, 'r13': 9.565164723046895}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 8.248681278190112, 'o1': 7.3052338141409034, 'o2': 5.635510960068508, 'o3': 3.423592829908957, 'o4': 8.00486331135244, 'o5': 8.249294658633888, 'o6': 9.291602749004326, 'o7': 3.476257095242959, 'o8': 6.5086135426875, 'o9': 5.9616265019627885, 'o10': 5.787804702237668, 'o11': 5.990596609357306, 'o12': 5.730654584105039, 'o13': 5.487480053926726, 'o14': 9.382063440188027, 'o15': 6.617086944791016, 'o16': 9.142231741608166, 'o17': 10.440214070242053}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9'], 'type2': ['o10', 'o11', 'o12', 'o13'], 'type3': ['o14', 'o15', 'o16', 'o17']}

def ResetState():
    state.loc = { 'r0': 13, 'r1': 4, 'r2': 9, 'r3': 13, 'r4': 9, 'r5': 6, 'r6': 4, 'r7': 3, 'r8': 10, 'r9': 2, 'r10': 13, 'r11': 7, 'r12': 1, 'r13': 1, 'm0': 3, 'fixer0': 10, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK,}
    state.storedLoc = {'o0': 13, 'o1': 7, 'o2': 13, 'o3': 13, 'o4': 13, 'o5': 11, 'o6': 3, 'o7': 12, 'o8': 12, 'o9': 5, 'o10': 6, 'o11': 3, 'o12': 10, 'o13': 7, 'o14': 9, 'o15': 5, 'o16': 14, 'o17': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    11: [['order', 'type0', 200]],
    13: [['order', 'type0', 200]],
    28: [['order', 'type0', 200]],
    20: [['order', 'type0', 200]],
    14: [['order', 'type0', 200]],
    16: [['order', 'type0', 200]],
    17: [['order', 'type1', 200]],
    27: [['order', 'type2', 200]],
    22: [['order', 'type2', 200]],
    23: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
    5: [['order', 'type3', 200]],
    6: [['order', 'type3', 200]],
    25: [['order', 'type3', 200]],
    21: [['order', 'type3', 200]],
}
eventsEnv = {
}