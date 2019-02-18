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
rv.SHIPPING_DOC = {rv.FACTORY1: 1.062870610375676}

rv.GROUND_EDGES = {0: [3, 5, 1, 9, 10, 11], 1: [0, 4, 5, 8, 9], 2: [3, 10], 3: [4, 9, 0, 2, 8], 4: [5, 10, 1, 3, 7, 200], 5: [12, 0, 1, 4, 9], 6: [8, 9, 7], 7: [4, 6, 11], 8: [3, 1, 6, 12], 9: [0, 3, 5, 1, 6], 10: [0, 2, 4, 11, 200], 11: [0, 7, 10], 12: [8, 5], 200: [4, 10]}
rv.GROUND_WEIGHTS = {(0, 3): 14.061092441653656, (0, 5): 10.197721189450913, (0, 1): 10.848535009400837, (0, 9): 6.80197243176349, (0, 10): 7.9594839252200025, (0, 11): 9.906829422572407, (1, 4): 9.578813211986468, (1, 5): 16.191012903303875, (1, 8): 3.8392741254993386, (1, 9): 7.249633431072491, (2, 3): 9.069746837933206, (2, 10): 1, (3, 4): 15.337997502260526, (3, 9): 10.18869020392684, (3, 8): 7.183296115291105, (4, 5): 10.125592751782037, (4, 10): 4.6787940531044985, (4, 7): 9.26905520917873, (4, 200): 8.290865027499757, (5, 12): 7.4210896348192055, (5, 9): 6.451374522668509, (6, 8): 19.06815450820124, (6, 9): 6.028946033541359, (6, 7): 6.042891185077904, (7, 11): 13.228524868330862, (8, 12): 9.349202805326168, (10, 11): 14.095248302092708, (10, 200): 16.12740986578956}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3']
rv.ROBOT_CAPACITY = {'r0': 8.375417029556443, 'r1': 10.157722099743674, 'r2': 11.640293649226162, 'r3': 6.793510983409443}
rv.MACHINES = ['m0', 'm1', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 7.89542799159434, 'o1': 7.0632578537813, 'o2': 6.5545798416925205, 'o3': 3.517867237636426, 'o4': 8.065629947719575, 'o5': 3.4318857260573163, 'o6': 4.405593620855099, 'o7': 6.827816545777696, 'o8': 3.3031063325124443, 'o9': 8.028035038343731, 'o10': 6.038758294874002, 'o11': 5.487536435288585, 'o12': 8.524686592888047, 'o13': 8.663062001766765, 'o14': 7.9489893037788235, 'o15': 5.897418750565409}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15']}

def ResetState():
  state.loc = { r0: 11, r1: 0, r2: 8, r3: 6, m0: 1, m1: 6, fixer0: 3, fixer1: 0, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK,}
    state.storedLoc{'o0': 0, 'o1': 1, 'o2': 12, 'o3': 6, 'o4': 9, 'o5': 0, 'o6': 1, 'o7': 9, 'o8': 5, 'o9': 9, 'o10': 12, 'o11': 12, 'o12': 9, 'o13': 3, 'o14': 5, 'o15': 11}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'r3': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False}
    state.numUses7
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    4: [['order', type0, 200]],
    5: [['order', type1, 200]],
    4: [['order', type1, 200]],
    6: [['order', type2, 200]],
    6: [['order', type2, 200]],
    2: [['order', type2, 200]],
    3: [['order', type2, 200]],
    6: [['order', type2, 200]],
    2: [['order', type3, 200]],
}
eventsEnv = {
}