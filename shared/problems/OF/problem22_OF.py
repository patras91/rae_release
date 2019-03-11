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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 6}

rv.GROUND_EDGES = {0: [5, 4, 16], 1: [10, 17, 4, 6, 7], 2: [14], 3: [11, 14, 20, 7, 10], 4: [0, 1, 10, 5], 5: [4, 8, 9, 16, 0, 14], 6: [1, 14, 13, 18, 200], 7: [1, 3, 9], 8: [15, 5, 11, 19], 9: [7, 17, 5, 14, 15], 10: [3, 1, 4], 11: [8, 3, 12], 12: [11, 200], 13: [6], 14: [5, 9, 2, 3, 6], 15: [9, 17, 8], 16: [0, 5, 17], 17: [16, 20, 1, 9, 15, 19], 18: [6, 20], 19: [8, 17, 20], 20: [3, 18, 17, 19, 200], 200: [6, 12, 20]}
rv.GROUND_WEIGHTS = {(0, 5): 8.657491120767313, (0, 4): 1, (0, 16): 6.2708714297089525, (1, 10): 10.11429512486234, (1, 17): 10.092868106514771, (1, 4): 6.568887734942726, (1, 6): 5.9906754001912255, (1, 7): 13.04466468490597, (2, 14): 13.247465942258414, (3, 11): 3.5714844638472467, (3, 14): 1.1278338637502126, (3, 20): 10.670049316619975, (3, 7): 6.086817714080893, (3, 10): 4.99919802638166, (4, 10): 15.006287985476753, (4, 5): 4.942225309653361, (5, 8): 12.318988971381138, (5, 9): 5.02528486268084, (5, 16): 5.655323337053175, (5, 14): 10.328788171139177, (6, 14): 8.676976631490351, (6, 13): 18.37227227484911, (6, 18): 12.35916015014565, (6, 200): 2.5247847109887136, (7, 9): 1, (8, 15): 7.788437111014187, (8, 11): 1.2681574832019509, (8, 19): 6.5319849241232095, (9, 17): 7.177904146652438, (9, 14): 9.757125561419194, (9, 15): 6.73846955622251, (11, 12): 8.10366637315835, (12, 200): 7.0284711856373665, (15, 17): 14.731890895331567, (16, 17): 8.999048410536204, (17, 20): 12.529381412886874, (17, 19): 17.324756270104125, (18, 20): 3.5936508636982953, (19, 20): 11.216383373661563, (20, 200): 4.791965738854856}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1,  'r15': rv.FACTORY1,  'r16': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 9.117919916022956, 'r1': 8.427567304239286, 'r2': 13.17291508773955, 'r3': 7.22973523609499, 'r4': 6.094718183191631, 'r5': 8.64095356463286, 'r6': 5.4899073408959715, 'r7': 10.048551553188645, 'r8': 10.44133483393235, 'r9': 10.01643120477145, 'r10': 6.416407017086486, 'r11': 5.268495132774661, 'r12': 12.241226814666486, 'r13': 6.4096344240092815, 'r14': 12.554944078061745, 'r15': 12.061968038316532, 'r16': 8.984451080303288}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8']
rv.OBJ_WEIGHT = {'o0': 6.57281391546551, 'o1': 6.375107689902549, 'o2': 6.6764553869809244, 'o3': 10.986625946749145, 'o4': 9.64085642700662, 'o5': 4.9458222416010145, 'o6': 6.1787723034569435, 'o7': 4.291298217439012, 'o8': 10.04043910893575}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3'], 'type2': ['o4', 'o5', 'o6', 'o7', 'o8']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 19, 'r2': 5, 'r3': 5, 'r4': 7, 'r5': 13, 'r6': 12, 'r7': 14, 'r8': 15, 'r9': 6, 'r10': 3, 'r11': 9, 'r12': 15, 'r13': 6, 'r14': 16, 'r15': 14, 'r16': 8, 'm0': 15, 'fixer0': 18, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 6, 'o2': 5, 'o3': 18, 'o4': 4, 'o5': 14, 'o6': 17, 'o7': 3, 'o8': 14}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'r16': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'r15': False, 'r16': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 6}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    2: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
}
eventsEnv = {
}