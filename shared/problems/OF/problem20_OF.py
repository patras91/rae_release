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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 19}

rv.GROUND_EDGES = {0: [4, 11, 2, 8, 12, 16], 1: [17, 4, 16, 19], 2: [0, 14], 3: [13, 4, 9, 16, 20], 4: [1, 3, 15, 0, 19], 5: [6, 14, 15, 17], 6: [5, 12, 19, 200], 7: [13, 19], 8: [0, 18], 9: [3], 10: [17], 11: [0, 13], 12: [0, 6, 200], 13: [11, 3, 7, 18, 19], 14: [2, 5, 17, 19], 15: [4, 5], 16: [0, 1, 3, 17], 17: [5, 14, 1, 10, 16, 19], 18: [8, 13], 19: [1, 4, 6, 7, 13, 14, 17, 200], 20: [3], 200: [6, 12, 19]}
rv.GROUND_WEIGHTS = {(0, 4): 4.577562756389996, (0, 11): 7.3039785820020064, (0, 2): 7.946806536885008, (0, 8): 4.8365106775587074, (0, 12): 2.5147303295916483, (0, 16): 9.600867733103902, (1, 17): 10.175259210592944, (1, 4): 3.0455837870494147, (1, 16): 10.450449472985412, (1, 19): 9.674699366138828, (2, 14): 1.2421852278054715, (3, 13): 8.739092413692568, (3, 4): 14.72283923391553, (3, 9): 8.328530788775426, (3, 16): 12.985793477397452, (3, 20): 3.245711294721821, (4, 15): 15.047369833331372, (4, 19): 6.872566291145436, (5, 6): 9.767735662879916, (5, 14): 12.682693820443205, (5, 15): 7.980599372123532, (5, 17): 14.933732841091654, (6, 12): 7.012343659179841, (6, 19): 3.815186773430163, (6, 200): 8.234448594769631, (7, 13): 10.798124847418704, (7, 19): 9.729846155777858, (8, 18): 6.480867531364514, (10, 17): 14.635418322970164, (11, 13): 5.471100360131079, (12, 200): 8.50992312793454, (13, 18): 10.589867899841922, (13, 19): 16.031315417600936, (14, 17): 3.602129550213496, (14, 19): 2.4710432913443903, (16, 17): 3.0721641232702925, (17, 19): 5.738775717897374, (19, 200): 7.486966874625556}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.325359534366788, 'r1': 6.985520835448711, 'r2': 6.376086127864828, 'r3': 8.767757579226336, 'r4': 4.529729270628966, 'r5': 9.862460997833564}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15']
rv.OBJ_WEIGHT = {'o0': 8.925717112048693, 'o1': 5.916306916923551, 'o2': 7.97057582597706, 'o3': 4.885848546123166, 'o4': 6.31902267570398, 'o5': 6.07573952908454, 'o6': 8.53009520753643, 'o7': 6.6402083919146175, 'o8': 8.271121315075524, 'o9': 9.34872155617624, 'o10': 7.527650306614205, 'o11': 7.451370162145, 'o12': 5.29610888101059, 'o13': 5.721126903583544, 'o14': 6.772033793007287, 'o15': 5.760818084665499}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14', 'o15']}

def ResetState():
    state.loc = { 'r0': 19, 'r1': 10, 'r2': 1, 'r3': 13, 'r4': 7, 'r5': 4, 'm0': 1, 'm1': 14, 'm2': 3, 'm3': 14, 'm4': 14, 'm5': 16, 'm6': 8, 'm7': 5, 'm8': 7, 'm9': 8, 'fixer0': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK,}
    state.storedLoc = {'o0': 17, 'o1': 6, 'o2': 18, 'o3': 12, 'o4': 11, 'o5': 15, 'o6': 0, 'o7': 10, 'o8': 12, 'o9': 2, 'o10': 11, 'o11': 3, 'o12': 17, 'o13': 3, 'o14': 8, 'o15': 4}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'fixer0': False}
    state.numUses = {'m0': 12, 'm1': 8, 'm2': 9, 'm3': 6, 'm4': 10, 'm5': 14, 'm6': 7, 'm7': 6, 'm8': 9, 'm9': 7}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    1: [['order', 'type0', 200]],
    10: [['order', 'type0', 200]],
}
eventsEnv = {
}