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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 6}

rv.GROUND_EDGES = {0: [10, 12, 4, 5, 7, 9, 11, 200], 1: [4, 2], 2: [1, 3, 12, 4], 3: [10, 2], 4: [0, 2, 1, 10], 5: [0], 6: [8], 7: [0, 10], 8: [11, 6], 9: [0], 10: [0, 3, 4, 7, 11], 11: [0, 10, 8, 12], 12: [11, 0, 2], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 10): 8.349558336460143, (0, 12): 13.310391594741917, (0, 4): 7.575883671248545, (0, 5): 6.332249003855482, (0, 7): 1.0317388237870384, (0, 9): 7.26552964827675, (0, 11): 13.774747877319495, (0, 200): 11.648514703801101, (1, 4): 3.686024931463308, (1, 2): 8.056203149587187, (2, 3): 1.957360102623233, (2, 12): 8.939072702248819, (2, 4): 1, (3, 10): 4.288594130036586, (4, 10): 10.035662168465734, (6, 8): 8.64667582634972, (7, 10): 8.58180128356625, (8, 11): 8.427833764831927, (10, 11): 10.029777983544514, (11, 12): 14.062099370625006}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.424085885600618, 'r1': 6.2209383087523875, 'r2': 11.799459158715667, 'r3': 8.966421860248662, 'r4': 8.914005705071094, 'r5': 11.787836945282208, 'r6': 6.094898231238938, 'r7': 6.478324028311924, 'r8': 5.961779408969228, 'r9': 3.949559940398963, 'r10': 6.670854781005403, 'r11': 8.20403179418205, 'r12': 7.39952984381394, 'r13': 5.510826661935358, 'r14': 9.593703968053577}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 5.601741558933446, 'o1': 8.895104537583538, 'o2': 6.52929647516173, 'o3': 8.238048458576722, 'o4': 7.575900183973956, 'o5': 5.2153429969206915, 'o6': 5.12642213886506, 'o7': 6.46504168662737, 'o8': 5.768953163028376, 'o9': 11.1679282380008, 'o10': 4.518503068622039, 'o11': 5.405432475896783, 'o12': 5.729767276129999, 'o13': 8.072779815814135, 'o14': 8.19725838587669, 'o15': 3.3627651134484573, 'o16': 4.514078566114193, 'o17': 3.9787336532404263}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type1': ['o9', 'o10', 'o11', 'o12', 'o13', 'o14'], 'type2': ['o15', 'o16', 'o17']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 11, 'r2': 11, 'r3': 6, 'r4': 12, 'r5': 12, 'r6': 7, 'r7': 4, 'r8': 0, 'r9': 8, 'r10': 2, 'r11': 7, 'r12': 4, 'r13': 9, 'r14': 0, 'm0': 5, 'fixer0': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK,}
    state.storedLoc = {'o0': 9, 'o1': 6, 'o2': 0, 'o3': 9, 'o4': 10, 'o5': 3, 'o6': 4, 'o7': 11, 'o8': 0, 'o9': 7, 'o10': 12, 'o11': 8, 'o12': 9, 'o13': 5, 'o14': 7, 'o15': 4, 'o16': 9, 'o17': 8}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'm0': False, 'fixer0': False}
    state.numUses = {'m0': 9}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    2: [['order', 'type0', 200]],
    4: [['order', 'type0', 200]],
}
eventsEnv = {
}