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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [3, 6, 1, 4, 5], 1: [0, 2, 4, 5], 2: [1, 4], 3: [4, 5, 6, 0], 4: [0, 2, 3, 6, 200, 1], 5: [0, 1, 3, 6], 6: [5, 0, 3, 4, 200], 200: [4, 6]}
rv.GROUND_WEIGHTS = {(0, 3): 6.3987423773433925, (0, 6): 5.153874198937982, (0, 1): 6.623666103109804, (0, 4): 12.442308994393585, (0, 5): 13.577140704299318, (1, 2): 3.7255555122680173, (1, 4): 7.272828615344304, (1, 5): 5.94098127341973, (2, 4): 7.1233028166910755, (3, 4): 10.528086658493583, (3, 5): 9.484251916232514, (3, 6): 6.169300762516173, (4, 6): 13.334686321231123, (4, 200): 5.230634532209901, (5, 6): 11.048500125915124, (6, 200): 4.418334602932765}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 11.309591175471933, 'r1': 10.075509955100603, 'r2': 5.686570091657025, 'r3': 5.406705656196577, 'r4': 6.061000108318671, 'r5': 9.91786797116402, 'r6': 7.992472812419164, 'r7': 6.043907262152693, 'r8': 8.724430368516515}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 6.894443953023779, 'o1': 5.261384952109984, 'o2': 7.231351936694473, 'o3': 8.029553573735948, 'o4': 6.386891384948493, 'o5': 3.1366777158541614, 'o6': 7.1644474788408585, 'o7': 3.3470146835877563, 'o8': 6.312927529703881, 'o9': 7.311220147657218, 'o10': 6.186397634100569, 'o11': 7.516964315132552, 'o12': 8.307963307894902, 'o13': 3.4799580879571717, 'o14': 7.135765292839803, 'o15': 6.819883304438078, 'o16': 8.630159198525988, 'o17': 4.802775464956567, 'o18': 3.617284405337285}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5'], 'type2': ['o6', 'o7'], 'type3': ['o8', 'o9', 'o10'], 'type4': ['o11', 'o12', 'o13', 'o14'], 'type5': ['o15', 'o16', 'o17', 'o18']}

def ResetState():
    state.loc = { 'r0': 5, 'r1': 2, 'r2': 4, 'r3': 4, 'r4': 3, 'r5': 6, 'r6': 4, 'r7': 4, 'r8': 4, 'm0': 6, 'fixer0': 2, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK,}
    state.storedLoc = {'o0': 3, 'o1': 3, 'o2': 2, 'o3': 2, 'o4': 4, 'o5': 5, 'o6': 5, 'o7': 6, 'o8': 1, 'o9': 2, 'o10': 3, 'o11': 1, 'o12': 4, 'o13': 4, 'o14': 1, 'o15': 2, 'o16': 6, 'o17': 0, 'o18': 6}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 6}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    24: [['order', 'type0', 200]],
    10: [['order', 'type0', 200]],
}
eventsEnv = {
}