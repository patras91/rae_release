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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 12.451542252575736}

rv.GROUND_EDGES = {0: [2, 3, 6, 7, 8, 9, 200], 1: [2, 3, 9, 10], 2: [4, 6, 11, 0, 1, 13], 3: [0, 1], 4: [10, 2], 5: [11], 6: [0, 2, 10, 11, 12], 7: [0, 12, 10, 200], 8: [0], 9: [0, 1], 10: [1, 4, 7, 13, 6, 200], 11: [2, 6, 5, 200], 12: [6, 7], 13: [2, 10], 200: [0, 7, 10, 11]}
rv.GROUND_WEIGHTS = {(0, 2): 9.442504400933268, (0, 3): 3.4801221486397242, (0, 6): 10.838375876763749, (0, 7): 6.96072994812549, (0, 8): 9.122396136220257, (0, 9): 11.921256579299921, (0, 200): 8.86904083825095, (1, 2): 2.8837399160357045, (1, 3): 4.47474530923326, (1, 9): 16.31816196905367, (1, 10): 5.9376796726782315, (2, 4): 11.48623848131533, (2, 6): 8.96854873847039, (2, 11): 8.92408397468529, (2, 13): 11.845754268860716, (4, 10): 5.181455858129723, (5, 11): 3.455879919992115, (6, 10): 4.685455576834986, (6, 11): 8.110047575675686, (6, 12): 7.147893028028827, (7, 12): 12.680163016173811, (7, 10): 7.237259921442977, (7, 200): 9.883352969211678, (10, 13): 8.350668843969666, (10, 200): 5.783218505826722, (11, 200): 11.024548375352353}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3']
rv.ROBOT_CAPACITY = {'r0': 5.781719295847649, 'r1': 8.498227829285472, 'r2': 10.17036206823564, 'r3': 6.406106078228245}
rv.MACHINES = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'm13', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13']
rv.OBJ_WEIGHT = {'o0': 9.31548670579976, 'o1': 5.0219893870820025, 'o2': 6.777716150045467, 'o3': 4.239358324590274, 'o4': 9.696379712668293, 'o5': 5.709327305277249, 'o6': 5.889001613515333, 'o7': 5.056363487493273, 'o8': 5.508936749554337, 'o9': 10.17036206823564, 'o10': 7.860132093872037, 'o11': 6.216745910718647, 'o12': 6.4130596750046, 'o13': 7.034411565435194}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6', 'o7'], 'type2': ['o8', 'o9', 'o10', 'o11', 'o12', 'o13']}

def ResetState():
    state.loc = { 'r0': 12, 'r1': 3, 'r2': 9, 'r3': 8, 'm0': 4, 'm1': 11, 'm2': 8, 'm3': 8, 'm4': 8, 'm5': 7, 'm6': 0, 'm7': 1, 'm8': 3, 'm9': 2, 'm10': 10, 'm11': 3, 'm12': 12, 'm13': 4, 'fixer0': 2, 'fixer1': 0, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 1, 'o2': 13, 'o3': 2, 'o4': 11, 'o5': 3, 'o6': 5, 'o7': 6, 'o8': 5, 'o9': 7, 'o10': 5, 'o11': 5, 'o12': 6, 'o13': 2}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'m0'": False, "'m1'": False, "'m2'": False, "'m3'": False, "'m4'": False, "'m5'": False, "'m6'": False, "'m7'": False, "'m8'": False, "'m9'": False, "'m10'": False, "'m11'": False, "'m12'": False, "'m13'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 10, 'm1': 14, 'm2': 14, 'm3': 12, 'm4': 6, 'm5': 7, 'm6': 18, 'm7': 10, 'm8': 7, 'm9': 6, 'm10': 4, 'm11': 12, 'm12': 9, 'm13': 9, 'fixer0': 11, 'fixer1': 6}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    9: [['order', 'type0', 200]],
    19: [['order', 'type0', 200]],
    23: [['order', 'type0', 200]],
    18: [['order', 'type0', 200]],
    21: [['order', 'type1', 200]],
    13: [['order', 'type1', 200]],
    12: [['order', 'type1', 200]],
    11: [['order', 'type1', 200]],
    22: [['order', 'type2', 200]],
    5: [['order', 'type2', 200]],
    16: [['order', 'type2', 200]],
    10: [['order', 'type2', 200]],
}
eventsEnv = {
}