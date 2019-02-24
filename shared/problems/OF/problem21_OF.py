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
rv.SHIPPING_DOC = {rv.FACTORY1: 0.3407866019199872}

rv.GROUND_EDGES = {0: [3, 10, 2, 6, 8, 9], 1: [5, 10, 7, 11], 2: [0, 3, 8], 3: [2, 4, 7, 11, 0, 5], 4: [7, 3, 8, 10], 5: [3, 1, 9, 10, 200], 6: [0, 10], 7: [1, 8, 3, 4], 8: [0, 2, 4, 7], 9: [0, 5, 11], 10: [0, 4, 5, 6, 1, 11], 11: [1, 10, 3, 9], 200: [5]}
rv.GROUND_WEIGHTS = {(0, 3): 13.718261032768993, (0, 10): 11.3638203442387, (0, 2): 8.033421029957681, (0, 6): 4.696678642990205, (0, 8): 5.3044788918727, (0, 9): 6.295132446294618, (1, 5): 8.657013819885828, (1, 10): 10.14646209336626, (1, 7): 13.407396088307163, (1, 11): 9.039423404423538, (2, 3): 4.62654322757657, (2, 8): 10.802375169410231, (3, 4): 7.557806655168996, (3, 7): 12.979488172291944, (3, 11): 1.7476834854675491, (3, 5): 21.601051972048303, (4, 7): 9.592265857539562, (4, 8): 6.4963905659119305, (4, 10): 9.530925830543593, (5, 9): 1.6793811936881031, (5, 10): 1, (5, 200): 3.7626429570582607, (6, 10): 11.77890151782169, (7, 8): 12.314263593937756, (9, 11): 6.160681325802838, (10, 11): 14.740699502919684}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19']
rv.ROBOT_CAPACITY = {'r0': 3.4097049293732677, 'r1': 7.118347845441409, 'r2': 9.690868218955668, 'r3': 6.866845762497879, 'r4': 9.282404683111816, 'r5': 10.225416637612977, 'r6': 7.520457274179153, 'r7': 13.08062269211768, 'r8': 8.21556868443962, 'r9': 11.822784390931199, 'r10': 8.926494637883774, 'r11': 5.605352866377125, 'r12': 8.91892949325549, 'r13': 8.162922755312218, 'r14': 9.74992559826275, 'r15': 11.96947286840032, 'r16': 4.665135791544973, 'r17': 8.874697235248565, 'r18': 8.985726786883948, 'r19': 7.781152828627015}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16']
rv.OBJ_WEIGHT = {'o0': 8.040534279786467, 'o1': 8.44092097768696, 'o2': 8.16898256784503, 'o3': 3.201811333227981, 'o4': 6.369963022080283, 'o5': 5.98258708806213, 'o6': 8.289066979812958, 'o7': 8.652363364063095, 'o8': 8.565040513975802, 'o9': 8.461966554221576, 'o10': 5.894203472907951, 'o11': 5.22699333756101, 'o12': 6.453843467895672, 'o13': 9.119013454366952, 'o14': 5.1087348897704885, 'o15': 8.139191326873762, 'o16': 8.091726715972401}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15'], 'type4': ['o16']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 1, 'r2': 11, 'r3': 5, 'r4': 3, 'r5': 6, 'r6': 9, 'r7': 10, 'r8': 3, 'r9': 8, 'r10': 6, 'r11': 0, 'r12': 5, 'r13': 2, 'r14': 1, 'r15': 0, 'r16': 9, 'r17': 2, 'r18': 5, 'r19': 4, 'm0': 0, 'fixer0': 8, 'fixer1': 4, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 4, 'o2': 4, 'o3': 10, 'o4': 6, 'o5': 0, 'o6': 0, 'o7': 10, 'o8': 7, 'o9': 3, 'o10': 3, 'o11': 4, 'o12': 11, 'o13': 7, 'o14': 9, 'o15': 3, 'o16': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'r16': NIL, 'r17': NIL, 'r18': NIL, 'r19': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'r14'": False, "'r15'": False, "'r16'": False, "'r17'": False, "'r18'": False, "'r19'": False, "'m0'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 2, 'fixer0': 7, 'fixer1': 6}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    5: [['order', 'type1', 200]],
    17: [['order', 'type1', 200]],
    13: [['order', 'type1', 200]],
    12: [['order', 'type2', 200]],
    6: [['order', 'type2', 200]],
    1: [['order', 'type2', 200]],
    15: [['order', 'type2', 200]],
    19: [['order', 'type3', 200]],
    8: [['order', 'type3', 200]],
    2: [['order', 'type3', 200]],
    21: [['order', 'type4', 200]],
}
eventsEnv = {
}