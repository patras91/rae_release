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
rv.SHIPPING_DOC = {rv.FACTORY1: 3}

rv.GROUND_EDGES = {0: [11, 17, 3, 5, 6, 8, 10, 15], 1: [7, 8, 14, 18], 2: [11], 3: [0, 9, 12], 4: [9, 12, 7, 11], 5: [0], 6: [0, 7, 16], 7: [4, 8, 14, 15, 1, 6], 8: [0, 1, 7, 13], 9: [3, 10, 15, 4, 12], 10: [0, 9, 11, 16], 11: [4, 15, 17, 18, 0, 2, 10, 200], 12: [3, 9, 4, 16, 200], 13: [8, 16, 18], 14: [1, 7, 16, 200], 15: [0, 7, 9, 11], 16: [6, 10, 12, 13, 14], 17: [0, 11], 18: [1, 13, 11], 200: [11, 12, 14]}
rv.GROUND_WEIGHTS = {(0, 11): 5.3607619654094165, (0, 17): 7.899602265322365, (0, 3): 8.896557466071922, (0, 5): 6.364515804654797, (0, 6): 11.13958304127428, (0, 8): 12.23690835471291, (0, 10): 3.803511965407756, (0, 15): 8.845415520229894, (1, 7): 12.081994603300211, (1, 8): 6.147903738174218, (1, 14): 7.699722091432688, (1, 18): 5.477378560331504, (2, 11): 7.777082085648736, (3, 9): 8.333867419754153, (3, 12): 9.738874331452772, (4, 9): 6.557686545782415, (4, 12): 8.15558685486369, (4, 7): 7.368689869741593, (4, 11): 10.717531057389529, (6, 7): 11.85944510006069, (6, 16): 8.952513077408454, (7, 8): 6.097879982470312, (7, 14): 6.115951469989998, (7, 15): 2.648370736557677, (8, 13): 5.800946628691404, (9, 10): 14.136044799817618, (9, 15): 5.996931263403525, (9, 12): 1, (10, 11): 1, (10, 16): 6.114202112870064, (11, 15): 1.4227269019682929, (11, 17): 12.031838108678414, (11, 18): 6.231503931325276, (11, 200): 1.6252279095270232, (12, 16): 9.248752850309282, (12, 200): 2.3134812472988173, (13, 16): 3.230384321815312, (13, 18): 16.414659588392222, (14, 16): 5.004537909227885, (14, 200): 11.853592546123032}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1,  'r14': rv.FACTORY1,  'r15': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 5.880828243862061, 'r1': 9.400145931751437, 'r2': 11.607404355345102, 'r3': 8.46973040734425, 'r4': 9.86239967329704, 'r5': 5.215270891726696, 'r6': 8.520167289660495, 'r7': 5.994774520681284, 'r8': 7.057673851921632, 'r9': 7.652395154232292, 'r10': 4.564961033525194, 'r11': 7.123205752027156, 'r12': 9.185883132020425, 'r13': 6.8367230166204935, 'r14': 7.715043190309786, 'r15': 10.780212858051023}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 6.8035214817094385, 'o1': 3.4154667010548696, 'o2': 4.202728207112549, 'o3': 6.689341001566463, 'o4': 5.971156947956787, 'o5': 9.113167486025432, 'o6': 7.769703661792257, 'o7': 9.077530169216217, 'o8': 6.598211075671048, 'o9': 6.465574481409726, 'o10': 6.01347436892704, 'o11': 4.1698215311807125, 'o12': 6.476891154131034, 'o13': 4.11966658537242, 'o14': 5.000235934417859, 'o15': 5.924127690486716, 'o16': 9.660798879829906, 'o17': 8.079788523903122, 'o18': 7.459144117812726}
rv.OBJ_CLASS = {'type0': ['o0', 'o1'], 'type1': ['o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17', 'o18']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 3, 'r2': 4, 'r3': 17, 'r4': 4, 'r5': 8, 'r6': 18, 'r7': 7, 'r8': 14, 'r9': 13, 'r10': 6, 'r11': 10, 'r12': 15, 'r13': 13, 'r14': 1, 'r15': 16, 'm0': 2, 'fixer0': 1, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK,}
    state.storedLoc = {'o0': 14, 'o1': 8, 'o2': 7, 'o3': 16, 'o4': 3, 'o5': 17, 'o6': 17, 'o7': 12, 'o8': 8, 'o9': 5, 'o10': 14, 'o11': 3, 'o12': 1, 'o13': 0, 'o14': 17, 'o15': 14, 'o16': 17, 'o17': 5, 'o18': 17}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL, 'r15': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'r14': False, 'r15': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 7}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    8: [['order', 'type0', 200]],
    4: [['order', 'type0', 200]],
}
eventsEnv = {
}