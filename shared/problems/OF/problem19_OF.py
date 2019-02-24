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
rv.SHIPPING_DOC = {rv.FACTORY1: 7.994400550139446}

rv.GROUND_EDGES = {0: [5, 9, 10, 1, 3, 6, 200], 1: [0], 2: [6, 8, 4, 12], 3: [0, 9], 4: [2, 7], 5: [7, 8, 11, 0], 6: [0, 2], 7: [9, 4, 5], 8: [9, 2, 5], 9: [0, 3, 7, 8, 10, 11], 10: [9, 11, 12, 0], 11: [9, 5, 10, 12], 12: [2, 11, 10], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 5): 7.0530086279095245, (0, 9): 3.4852275298963287, (0, 10): 9.35888324434713, (0, 1): 11.339724185751109, (0, 3): 13.676801151095768, (0, 6): 8.396073267417071, (0, 200): 7.585395244685884, (2, 6): 5.133356896015648, (2, 8): 17.01596223442113, (2, 4): 9.137514049718671, (2, 12): 14.021239407898827, (3, 9): 13.185661415392346, (4, 7): 6.755831033495068, (5, 7): 7.591113579562451, (5, 8): 8.618112545797302, (5, 11): 8.876682202450402, (7, 9): 4.168661798270874, (8, 9): 6.728660574354848, (9, 10): 7.199719333451641, (9, 11): 3.4057551622406557, (10, 11): 10.290320372307882, (10, 12): 5.368448623016537, (11, 12): 7.91466028250892}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13']
rv.ROBOT_CAPACITY = {'r0': 7.520361943979993, 'r1': 8.52198330305852, 'r2': 7.788267866554655, 'r3': 4.910032477492137, 'r4': 11.151658225604516, 'r5': 7.621021994153286, 'r6': 7.273699371763225, 'r7': 7.104242183919337, 'r8': 11.129247828346848, 'r9': 9.743997426604768, 'r10': 8.439210260882671, 'r11': 9.38995916239773, 'r12': 7.30588460361578, 'r13': 7.5083536972245355}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 7.5654365828355505, 'o1': 6.275193169841035, 'o2': 6.0598838951646785, 'o3': 6.2181175219685825, 'o4': 9.327435346717063, 'o5': 6.848756541226334, 'o6': 4.094042027829181, 'o7': 5.4935839294084765, 'o8': 5.691715809526982, 'o9': 6.602108931366923, 'o10': 5.518393432277602, 'o11': 9.715770730981534, 'o12': 6.394692161009488, 'o13': 5.839794209877358, 'o14': 2.8533476278534575, 'o15': 8.433006295671598, 'o16': 7.679105738430915, 'o17': 3.982825313485878, 'o18': 6.187861230234016, 'o19': 11.151658225604516, 'o20': 8.028346503577641, 'o21': 7.3656508498805655, 'o22': 6.8823393049299515}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3'], 'type2': ['o4'], 'type3': ['o5', 'o6', 'o7', 'o8', 'o9', 'o10'], 'type4': ['o11', 'o12', 'o13', 'o14', 'o15'], 'type5': ['o16', 'o17', 'o18', 'o19'], 'type6': ['o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 4, 'r2': 8, 'r3': 4, 'r4': 8, 'r5': 10, 'r6': 11, 'r7': 10, 'r8': 9, 'r9': 2, 'r10': 7, 'r11': 4, 'r12': 10, 'r13': 10, 'm0': 10, 'm1': 10, 'm2': 5, 'm3': 9, 'm4': 3, 'm5': 1, 'm6': 4, 'm7': 8, 'm8': 2, 'm9': 2, 'm10': 0, 'm11': 12, 'm12': 11, 'fixer0': 8, 'fixer1': 1, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 9, 'o2': 6, 'o3': 0, 'o4': 10, 'o5': 0, 'o6': 8, 'o7': 0, 'o8': 6, 'o9': 0, 'o10': 12, 'o11': 6, 'o12': 0, 'o13': 10, 'o14': 4, 'o15': 7, 'o16': 9, 'o17': 4, 'o18': 7, 'o19': 4, 'o20': 3, 'o21': 12, 'o22': 10}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'m4'": False, "'m5'": False, "'m6'": False, "'m7'": False, "'m8'": False, "'m9'": False, "'m10'": False, "'m11'": False, "'m12'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 11, 'm1': 5, 'm2': 15, 'm3': 13, 'm4': 6, 'm5': 11, 'm6': 12, 'm7': 9, 'm8': 7, 'm9': 15, 'm10': 10, 'm11': 13, 'm12': 12, 'fixer0': 10, 'fixer1': 5}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    27: [['order', 'type0', 200]],
    31: [['order', 'type1', 200]],
    8: [['order', 'type2', 200]],
    7: [['order', 'type3', 200]],
    32: [['order', 'type3', 200]],
    9: [['order', 'type3', 200]],
    24: [['order', 'type3', 200]],
    15: [['order', 'type4', 200]],
    10: [['order', 'type4', 200]],
    22: [['order', 'type4', 200]],
    2: [['order', 'type5', 200]],
    4: [['order', 'type5', 200]],
    25: [['order', 'type5', 200]],
    17: [['order', 'type5', 200]],
    28: [['order', 'type6', 200]],
    1: [['order', 'type6', 200]],
    20: [['order', 'type6', 200]],
}
eventsEnv = {
}