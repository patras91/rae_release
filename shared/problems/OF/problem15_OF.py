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
rv.SHIPPING_DOC = {rv.FACTORY1: 11.766388238280001}

rv.GROUND_EDGES = {0: [1], 1: [16, 17, 0, 8], 2: [11, 13, 15, 5, 12], 3: [4, 17], 4: [8, 15, 3, 14], 5: [2, 10, 14, 9, 16], 6: [11, 16, 7, 200], 7: [6, 10, 13], 8: [1, 4, 200], 9: [5, 11], 10: [11, 13, 5, 7, 14], 11: [9, 2, 6, 10], 12: [2, 16, 17, 14, 18], 13: [15, 18, 2, 7, 10], 14: [4, 5, 10, 12], 15: [2, 4, 13, 17], 16: [1, 5, 6, 12], 17: [15, 1, 3, 12, 200], 18: [12, 13], 200: [6, 8, 17]}
rv.GROUND_WEIGHTS = {(0, 1): 2.8247082195339415, (1, 16): 13.230715519057533, (1, 17): 9.463086722542995, (1, 8): 5.242838090402975, (2, 11): 11.34745655846832, (2, 13): 15.049018111713874, (2, 15): 3.780507941419798, (2, 5): 3.7729725114743635, (2, 12): 9.111629008635488, (3, 4): 11.486029751133929, (3, 17): 10.68860360139837, (4, 8): 10.553525649644108, (4, 15): 5.040810671340051, (4, 14): 3.3033132002282493, (5, 10): 11.687659323721537, (5, 14): 13.978202845956796, (5, 9): 12.041918921143829, (5, 16): 4.24459844243602, (6, 11): 2.3725753483958067, (6, 16): 7.02813790307252, (6, 7): 7.02135784475506, (6, 200): 13.700149074222656, (7, 10): 7.883590996799636, (7, 13): 7.634034371416801, (8, 200): 15.058605372396215, (9, 11): 1, (10, 11): 12.567727194031452, (10, 13): 13.066796955970764, (10, 14): 2.8000235110770157, (12, 16): 7.296271015091334, (12, 17): 5.283432359030044, (12, 14): 3.169713999258036, (12, 18): 13.197170922846041, (13, 15): 2.891269086919851, (13, 18): 13.835521408699172, (15, 17): 1.700500805679929, (17, 200): 3.4623234806929224}

rv.ROBOTS = ['r0', 'r1', 'r2']
rv.ROBOT_CAPACITY = {'r0': 3.888840005199838, 'r1': 4.883641564176113, 'r2': 6.622746374929584}
rv.MACHINES = ['m0', 'm1', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19']
rv.OBJ_WEIGHT = {'o0': 5.386075703458678, 'o1': 6.622746374929584, 'o2': 3.75939703423715, 'o3': 6.622746374929584, 'o4': 4.7268076073240515, 'o5': 6.622746374929584, 'o6': 3.593583669470115, 'o7': 6.622746374929584, 'o8': 6.509570301455969, 'o9': 5.433088261970797, 'o10': 6.622746374929584, 'o11': 6.622746374929584, 'o12': 6.622746374929584, 'o13': 6.622746374929584, 'o14': 6.622746374929584, 'o15': 5.837002587103262, 'o16': 6.622746374929584, 'o17': 5.982285193515567, 'o18': 5.488767270546775, 'o19': 6.622746374929584}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17'], 'type4': ['o18', 'o19']}

def ResetState():
  state.loc = { r0: 5, r1: 6, r2: 4, m0: 1, m1: 4, fixer0: 0, fixer1: 3, o0: UNK, o1: UNK, o2: UNK, o3: UNK, o4: UNK, o5: UNK, o6: UNK, o7: UNK, o8: UNK, o9: UNK, o10: UNK, o11: UNK, o12: UNK, o13: UNK, o14: UNK, o15: UNK, o16: UNK, o17: UNK, o18: UNK, o19: UNK,}
    state.storedLoc{'o0': 14, 'o1': 16, 'o2': 3, 'o3': 3, 'o4': 18, 'o5': 3, 'o6': 0, 'o7': 4, 'o8': 17, 'o9': 18, 'o10': 14, 'o11': 17, 'o12': 6, 'o13': 7, 'o14': 15, 'o15': 6, 'o16': 7, 'o17': 3, 'o18': 8, 'o19': 10}
  state.load = { o0: NIL, o1: NIL, o2: NIL, o3: NIL, o4: NIL, o5: NIL, o6: NIL, o7: NIL, o8: NIL, o9: NIL, o10: NIL, o11: NIL, o12: NIL, o13: NIL, o14: NIL, o15: NIL, o16: NIL, o17: NIL, o18: NIL, o19: NIL,}
    state.busy{'r0': False, 'r1': False, 'r2': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False}
    state.numUses11
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    4: [['order', type0, 200]],
    8: [['order', type0, 200]],
    8: [['order', type0, 200]],
    7: [['order', type1, 200]],
    4: [['order', type1, 200]],
    7: [['order', type1, 200]],
    7: [['order', type1, 200]],
    3: [['order', type1, 200]],
    1: [['order', type1, 200]],
    8: [['order', type1, 200]],
    8: [['order', type1, 200]],
    5: [['order', type1, 200]],
    5: [['order', type2, 200]],
    2: [['order', type2, 200]],
    2: [['order', type2, 200]],
    1: [['order', type3, 200]],
    6: [['order', type3, 200]],
    6: [['order', type3, 200]],
    3: [['order', type4, 200]],
    6: [['order', type4, 200]],
}
eventsEnv = {
}