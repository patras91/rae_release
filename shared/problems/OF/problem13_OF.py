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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 17}

rv.GROUND_EDGES = {0: [5, 12, 10, 11, 15], 1: [17, 4], 2: [6, 4], 3: [14, 20, 5, 6], 4: [1, 2, 8, 14, 16, 200], 5: [3, 15, 16, 0, 6, 14], 6: [3, 5, 14, 17, 2, 9], 7: [10, 17, 9], 8: [12, 4, 14, 200], 9: [6, 7, 12, 19], 10: [0, 7], 11: [0, 13, 19], 12: [8, 0, 9, 19], 13: [11, 17], 14: [3, 5, 8, 4, 6], 15: [0, 5], 16: [4, 5, 20], 17: [13, 1, 6, 7, 18], 18: [17], 19: [9, 11, 12], 20: [16, 3], 200: [4, 8]}
rv.GROUND_WEIGHTS = {(0, 5): 5.5727748744309515, (0, 12): 12.044156286582862, (0, 10): 9.774388951710089, (0, 11): 13.62441045589853, (0, 15): 10.521736984912659, (1, 17): 10.61564180112358, (1, 4): 9.05303533478904, (2, 6): 4.201087992369262, (2, 4): 11.453368404639203, (3, 14): 5.324772163795193, (3, 20): 3.266883412004095, (3, 5): 3.075066236263524, (3, 6): 8.370970452243107, (4, 8): 7.847964626005829, (4, 14): 10.90872902898198, (4, 16): 6.140174444696951, (4, 200): 10.391387270459528, (5, 15): 11.045748037658903, (5, 16): 8.613042687633751, (5, 6): 12.39381292308041, (5, 14): 5.329396181454151, (6, 14): 1.8945388126292695, (6, 17): 3.6250259464206263, (6, 9): 17.277621216435975, (7, 10): 1, (7, 17): 3.82219592235019, (7, 9): 6.900789483899494, (8, 12): 14.907761753852025, (8, 14): 3.373491312775662, (8, 200): 5.5649206407151155, (9, 12): 6.709640502045618, (9, 19): 9.778858686996536, (11, 13): 6.062930211215536, (11, 19): 10.864107731282406, (12, 19): 12.637966477802994, (13, 17): 7.917890153299046, (16, 20): 11.487296826347988, (17, 18): 12.731062809521895}

rv.ROBOTS = { 'r0': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.584981369594157}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 7.441689394323291, 'o1': 7.080556488437959, 'o2': 8.584981369594157, 'o3': 4.909256580170111, 'o4': 8.584981369594157, 'o5': 8.584981369594157, 'o6': 6.461203309448579, 'o7': 7.62101656032336, 'o8': 7.091233342591782, 'o9': 8.584981369594157, 'o10': 5.941021565620704, 'o11': 7.747672250053664, 'o12': 3.1051036333790076, 'o13': 8.231042940830235, 'o14': 7.1137507229049985, 'o15': 6.049111659569273}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2'], 'type2': ['o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9'], 'type3': ['o10', 'o11', 'o12', 'o13', 'o14', 'o15']}

def ResetState():
    state.loc = { 'r0': 8, 'm0': 3, 'm1': 9, 'm2': 16, 'm3': 9, 'm4': 14, 'm5': 8, 'm6': 20, 'm7': 17, 'm8': 7, 'm9': 15, 'fixer0': 8, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 6, 'o2': 15, 'o3': 6, 'o4': 3, 'o5': 15, 'o6': 8, 'o7': 4, 'o8': 15, 'o9': 0, 'o10': 14, 'o11': 17, 'o12': 8, 'o13': 13, 'o14': 10, 'o15': 8}
    state.load = { 'r0': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'fixer0': False}
    state.numUses = {'m0': 9, 'm1': 9, 'm2': 13, 'm3': 10, 'm4': 6, 'm5': 7, 'm6': 12, 'm7': 9, 'm8': 8, 'm9': 9}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    10: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
}
eventsEnv = {
}