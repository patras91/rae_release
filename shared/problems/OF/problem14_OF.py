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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1}

rv.GROUND_EDGES = {0: [1, 5, 6, 9, 10, 14, 15, 16], 1: [9, 12, 16, 200, 0, 2, 5, 17], 2: [1, 12], 3: [6, 4], 4: [3, 5, 9, 17], 5: [0, 1, 16, 4], 6: [0, 3, 7], 7: [6, 10, 16, 12, 17], 8: [11, 13, 16, 200], 9: [0, 1, 4], 10: [0, 7], 11: [14, 8], 12: [2, 7, 1, 13], 13: [12, 17, 8], 14: [0, 11], 15: [0], 16: [0, 8, 1, 5, 7, 17], 17: [1, 4, 7, 16, 13], 200: [1, 8]}
rv.GROUND_WEIGHTS = {(0, 1): 10.73032345960682, (0, 5): 8.888015813989682, (0, 6): 10.420303376660799, (0, 9): 10.940754263746637, (0, 10): 9.081945024735198, (0, 14): 18.016203939215643, (0, 15): 10.622578547016571, (0, 16): 12.982644175282616, (1, 9): 5.064280579985381, (1, 12): 11.34394688198454, (1, 16): 4.0267571523162635, (1, 200): 16.35939557512191, (1, 2): 4.665412035931995, (1, 5): 1, (1, 17): 12.098593425335391, (2, 12): 8.007559169935105, (3, 6): 11.729884017194735, (3, 4): 9.637910122011869, (4, 5): 10.145799910463477, (4, 9): 9.061472311387659, (4, 17): 7.020872924092485, (5, 16): 6.8295769122682275, (6, 7): 6.335831954780842, (7, 10): 9.408530834362065, (7, 16): 5.6076992651961, (7, 12): 9.841070319462252, (7, 17): 3.1925755799030195, (8, 11): 13.487222944597548, (8, 13): 9.830065073672582, (8, 16): 5.745724902024033, (8, 200): 10.62059622765187, (11, 14): 1.1569229582052705, (12, 13): 7.1963212714044955, (13, 17): 17.22940716417323, (16, 17): 3.618793393865059}

rv.ROBOTS = { 'r0': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.263339543627051}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 7.263339543627051, 'o1': 6.448582642170732, 'o2': 7.263339543627051, 'o3': 7.263339543627051, 'o4': 3.1973984987453443, 'o5': 7.263339543627051, 'o6': 7.263339543627051, 'o7': 6.873516234436724, 'o8': 7.263339543627051, 'o9': 7.263339543627051, 'o10': 7.263339543627051, 'o11': 5.85681617252132, 'o12': 7.263339543627051, 'o13': 4.303625014389434, 'o14': 6.713468208143435, 'o15': 4.312331626358784, 'o16': 7.263339543627051, 'o17': 7.263339543627051, 'o18': 6.710355151429338, 'o19': 7.263339543627051, 'o20': 7.263339543627051, 'o21': 4.612589907440144}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5'], 'type2': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17'], 'type4': ['o18', 'o19', 'o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 16, 'm0': 14, 'fixer0': 16, 'fixer1': 9, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 15, 'o2': 17, 'o3': 5, 'o4': 6, 'o5': 13, 'o6': 14, 'o7': 7, 'o8': 13, 'o9': 13, 'o10': 2, 'o11': 3, 'o12': 7, 'o13': 4, 'o14': 5, 'o15': 7, 'o16': 0, 'o17': 0, 'o18': 14, 'o19': 11, 'o20': 7, 'o21': 15}
    state.load = { 'r0': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    6: [['order', 'type0', 200]],
    19: [['order', 'type0', 200]],
}
eventsEnv = {
}