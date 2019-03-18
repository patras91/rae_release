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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 5}

rv.GROUND_EDGES = {0: [1, 4, 8, 9, 200], 1: [5, 6, 8, 9, 0], 2: [5, 8, 3, 4, 11, 200], 3: [2, 11, 5, 6], 4: [0, 2, 6, 5, 11, 200], 5: [3, 4, 8, 200, 1, 2, 10, 11], 6: [3, 10, 1, 4, 11], 7: [8], 8: [0, 1, 2, 5, 7], 9: [0, 1, 200], 10: [5, 6, 11, 200], 11: [2, 4, 5, 6, 10, 3], 200: [0, 2, 4, 9, 10, 5]}
rv.GROUND_WEIGHTS = {(0, 1): 7.952402047997237, (0, 4): 7.758360081617756, (0, 8): 14.941730831428151, (0, 9): 10.959486103628732, (0, 200): 11.003998394113232, (1, 5): 2.8990448496429906, (1, 6): 7.870079793413471, (1, 8): 7.265640911077123, (1, 9): 14.848669731025282, (2, 5): 10.29550421333836, (2, 8): 13.61570811984419, (2, 3): 9.97902076021434, (2, 4): 12.669304901529955, (2, 11): 14.64739390979355, (2, 200): 4.549942144530359, (3, 11): 7.392333795151888, (3, 5): 1, (3, 6): 2.96641603928607, (4, 6): 15.978020964142447, (4, 5): 10.25519279418231, (4, 11): 5.830376747807566, (4, 200): 6.948225331658348, (5, 8): 10.59458297996521, (5, 200): 12.77173460902761, (5, 10): 10.444841597549887, (5, 11): 6.861583407785289, (6, 10): 12.922113768172856, (6, 11): 7.478862076024667, (7, 8): 11.521989384068192, (9, 200): 8.305573450416798, (10, 11): 8.849860500717417, (10, 200): 6.4379522747494615}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.802131768086017, 'r1': 7.140855819299981, 'r2': 6.504989229754997, 'r3': 10.27081878346432, 'r4': 7.759363586886172, 'r5': 8.846754035871175, 'r6': 6.759340312879219, 'r7': 8.367524446568869, 'r8': 8.289053621564413, 'r9': 7.087263922833368, 'r10': 6.719161138095503, 'r11': 7.4780231805857165, 'r12': 9.29604972688221, 'r13': 9.031965647508644}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 4.2598687105280035, 'o1': 7.174892987251559, 'o2': 4.748721955654675, 'o3': 9.291853086023604, 'o4': 5.019693412173938, 'o5': 7.388454723454869, 'o6': 6.215070362519356, 'o7': 7.902653766709947, 'o8': 6.001275224542834, 'o9': 9.88398987292401, 'o10': 6.497213346564495, 'o11': 5.907237994962626, 'o12': 5.539455670735375, 'o13': 4.273134397063576, 'o14': 3.943438817801873, 'o15': 7.741740309729356, 'o16': 6.520701232504927, 'o17': 8.034794494277742, 'o18': 7.406990226536324, 'o19': 7.829201178639319, 'o20': 6.451253238638442, 'o21': 7.98677081652853, 'o22': 6.09057514606574}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12'], 'type3': ['o13', 'o14', 'o15', 'o16'], 'type4': ['o17', 'o18', 'o19', 'o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 4, 'r2': 1, 'r3': 3, 'r4': 1, 'r5': 11, 'r6': 4, 'r7': 4, 'r8': 8, 'r9': 6, 'r10': 5, 'r11': 9, 'r12': 11, 'r13': 4, 'm0': 5, 'fixer0': 6, 'fixer1': 1, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 10, 'o1': 8, 'o2': 3, 'o3': 3, 'o4': 0, 'o5': 1, 'o6': 0, 'o7': 3, 'o8': 3, 'o9': 11, 'o10': 3, 'o11': 1, 'o12': 0, 'o13': 4, 'o14': 8, 'o15': 7, 'o16': 5, 'o17': 11, 'o18': 3, 'o19': 7, 'o20': 7, 'o21': 4, 'o22': 2}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    28: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
}
eventsEnv = {
}