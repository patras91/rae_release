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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 8}

rv.GROUND_EDGES = {0: [3, 5, 2, 6, 7, 9], 1: [2, 4, 9], 2: [0, 1], 3: [4, 0, 8], 4: [6, 1, 3, 5, 200], 5: [4, 7, 0], 6: [0, 4, 8], 7: [0, 5], 8: [3, 6, 200], 9: [0, 1], 200: [4, 8]}
rv.GROUND_WEIGHTS = {(0, 3): 10.335533814381277, (0, 5): 10.49252677573075, (0, 2): 9.14487577880262, (0, 6): 5.488089769218206, (0, 7): 6.192502619726908, (0, 9): 7.28376193509114, (1, 2): 1, (1, 4): 6.341949990176294, (1, 9): 7.3709045566328815, (3, 4): 7.198765295304974, (3, 8): 7.652673536892436, (4, 6): 5.2871175625983975, (4, 5): 9.762826274746452, (4, 200): 5.809094252486254, (5, 7): 11.470964755784813, (6, 8): 8.146337723953351, (8, 200): 3.7014804904434184}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 3.9784309469220007, 'r1': 9.181066610955407, 'r2': 12.041145508043039, 'r3': 11.06850259119977, 'r4': 7.216119592081244}
rv.MACHINES = { 'm0': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']
rv.OBJ_WEIGHT = {'o0': 7.615737289247281, 'o1': 5.167098469521377, 'o2': 6.540533612182902, 'o3': 8.921122028524465, 'o4': 6.164950517606625, 'o5': 12.041145508043039, 'o6': 6.301032178507088, 'o7': 7.054532820474025, 'o8': 7.705502847090817, 'o9': 5.616031067946906, 'o10': 4.86138810102951, 'o11': 8.666550776543511, 'o12': 5.279532748937423, 'o13': 11.402301926413845, 'o14': 9.644385096713322, 'o15': 7.265217486629779, 'o16': 7.62970691887324, 'o17': 5.511578598276078, 'o18': 7.322975846746581, 'o19': 11.519836922252043, 'o20': 5.377014158604004, 'o21': 2.9439632803504976, 'o22': 4.029703700516715, 'o23': 7.161231947205362, 'o24': 4.224265073350298}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12'], 'type2': ['o13', 'o14', 'o15', 'o16'], 'type3': ['o17', 'o18', 'o19', 'o20'], 'type4': ['o21', 'o22', 'o23', 'o24']}

def ResetState():
    state.loc = { 'r0': 4, 'r1': 5, 'r2': 5, 'r3': 6, 'r4': 4, 'm0': 7, 'fixer0': 3, 'fixer1': 7, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK,}
    state.storedLoc = {'o0': 4, 'o1': 4, 'o2': 2, 'o3': 4, 'o4': 4, 'o5': 1, 'o6': 1, 'o7': 4, 'o8': 8, 'o9': 4, 'o10': 5, 'o11': 1, 'o12': 2, 'o13': 1, 'o14': 4, 'o15': 7, 'o16': 9, 'o17': 6, 'o18': 8, 'o19': 1, 'o20': 2, 'o21': 8, 'o22': 6, 'o23': 5, 'o24': 2}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'm0': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 11}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    21: [['order', 'type2', 200]],
    1: [['order', 'type2', 200]],
}
eventsEnv = {
}