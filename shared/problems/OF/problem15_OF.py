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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 11}

rv.GROUND_EDGES = {0: [8, 17, 2, 12], 1: [3, 5, 9, 14], 2: [0, 6, 12, 200], 3: [9, 1, 5], 4: [6, 13, 7, 14], 5: [1, 3, 13, 6, 7, 9], 6: [2, 5, 10, 17, 4, 8], 7: [4, 5, 10, 18], 8: [0, 6, 13, 10], 9: [1, 5, 16, 3], 10: [7, 8, 6], 11: [12, 13, 14], 12: [0, 2, 17, 11], 13: [11, 14, 4, 5, 8, 15], 14: [1, 4, 16, 17, 11, 13], 15: [13, 16, 17], 16: [15, 9, 14, 19], 17: [15, 0, 6, 12, 14], 18: [7, 19], 19: [16, 18], 200: [2]}
rv.GROUND_WEIGHTS = {(0, 8): 13.952226475877907, (0, 17): 10.61384088329622, (0, 2): 5.077430890864693, (0, 12): 3.0948091560322597, (1, 3): 13.570304512009093, (1, 5): 10.59918728906326, (1, 9): 4.001718741280488, (1, 14): 10.402653284439069, (2, 6): 6.242065068239579, (2, 12): 7.925530051270464, (2, 200): 13.54739283551035, (3, 9): 10.083593805260746, (3, 5): 13.262630665395157, (4, 6): 2.488620146467639, (4, 13): 5.2795555305051565, (4, 7): 15.072083836490389, (4, 14): 12.894775872440693, (5, 13): 13.478226097603025, (5, 6): 14.96104355489871, (5, 7): 1, (5, 9): 9.741653603984647, (6, 10): 10.078527484103976, (6, 17): 10.66963242080585, (6, 8): 3.5790046847445893, (7, 10): 14.110942554148268, (7, 18): 11.4347373721312, (8, 13): 10.39025909060719, (8, 10): 2.3455916244714325, (9, 16): 6.952857943398154, (11, 12): 7.176005553012793, (11, 13): 9.057365019705482, (11, 14): 10.916546899047677, (12, 17): 3.975730199346512, (13, 14): 1, (13, 15): 5.292875299086367, (14, 16): 8.14116907832678, (14, 17): 5.847435775341907, (15, 16): 9.051097855727942, (15, 17): 4.8176508198563885, (16, 19): 6.948288165180458, (18, 19): 1}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 2.4089786843752234, 'r1': 6.789291865087073, 'r2': 9.845107618162862, 'r3': 8.23112526335521, 'r4': 11.306452044916373}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12']
rv.OBJ_WEIGHT = {'o0': 5.119668237583159, 'o1': 6.924484540889238, 'o2': 6.599682038159671, 'o3': 9.446667182977263, 'o4': 3.6786293783443167, 'o5': 5.194391004077896, 'o6': 8.174101777802234, 'o7': 7.003324235403839, 'o8': 4.571844547555959, 'o9': 5.83240693891268, 'o10': 11.306452044916373, 'o11': 3.3684612426536744, 'o12': 4.958990546810899}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12']}

def ResetState():
    state.loc = { 'r0': 8, 'r1': 8, 'r2': 16, 'r3': 14, 'r4': 17, 'm0': 10, 'm1': 8, 'm2': 10, 'm3': 9, 'm4': 13, 'm5': 1, 'fixer0': 15, 'fixer1': 19, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 17, 'o2': 13, 'o3': 6, 'o4': 13, 'o5': 3, 'o6': 18, 'o7': 11, 'o8': 4, 'o9': 4, 'o10': 16, 'o11': 5, 'o12': 2}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 9, 'm1': 15, 'm2': 10, 'm3': 8, 'm4': 11, 'm5': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    13: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
}
eventsEnv = {
}