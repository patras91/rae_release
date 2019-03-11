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
rv.SHIPPING_DOC = {rv.FACTORY1: 15}

rv.GROUND_EDGES = {0: [2, 9, 16, 20, 4, 6, 10, 17, 200], 1: [13, 11], 2: [10, 12, 13, 0, 5], 3: [12, 17, 20, 14, 16], 4: [0, 13, 15], 5: [2, 6, 19], 6: [0, 5, 14, 15], 7: [13, 20], 8: [16, 11, 19], 9: [13, 0], 10: [0, 18, 20, 2], 11: [1, 8, 19, 12, 16], 12: [11, 13, 2, 3], 13: [9, 1, 2, 4, 7, 12], 14: [3, 6], 15: [6, 16, 4], 16: [3, 11, 0, 8, 15, 200], 17: [0, 3], 18: [10, 20], 19: [5, 8, 11], 20: [7, 0, 3, 10, 18], 200: [0, 16]}
rv.GROUND_WEIGHTS = {(0, 2): 5.36637523786961, (0, 9): 6.161037762875919, (0, 16): 2.3316587482728846, (0, 20): 2.857484650851644, (0, 4): 4.931533041878785, (0, 6): 12.770444133975264, (0, 10): 12.815544474388194, (0, 17): 15.084545152531648, (0, 200): 1, (1, 13): 12.302162442196904, (1, 11): 14.938919463979563, (2, 10): 13.69237796112896, (2, 12): 1, (2, 13): 4.273142303314727, (2, 5): 4.001519105381309, (3, 12): 4.307567942347388, (3, 17): 7.416152205809839, (3, 20): 6.938732038912951, (3, 14): 5.212596684416549, (3, 16): 7.102966061610471, (4, 13): 4.938430574519805, (4, 15): 3.8223503418965983, (5, 6): 6.643449881420001, (5, 19): 1, (6, 14): 6.94933138645197, (6, 15): 6.700124504543625, (7, 13): 8.556664469064795, (7, 20): 4.797279065018579, (8, 16): 11.73761370120169, (8, 11): 6.784436686587611, (8, 19): 14.872730113825707, (9, 13): 1.2826191949585848, (10, 18): 4.468987806384188, (10, 20): 5.377371726403635, (11, 19): 8.212598853717358, (11, 12): 10.116705342872676, (11, 16): 5.86597169275017, (12, 13): 7.513032030704071, (15, 16): 10.434643409405835, (16, 200): 1.191823781513028, (18, 20): 6.590593754885269}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1,  'r13': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 4.318743911809472, 'r1': 11.158164042113546, 'r2': 6.109150149697834, 'r3': 7.804478265703591, 'r4': 5.452167632152383, 'r5': 8.745071704816551, 'r6': 9.524898509343846, 'r7': 6.856123522563492, 'r8': 7.648338633122781, 'r9': 8.517569486786247, 'r10': 11.678743807913856, 'r11': 7.754724816943247, 'r12': 9.515036793004423, 'r13': 9.628303817320738}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1,  'fixer2': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17']
rv.OBJ_WEIGHT = {'o0': 6.9308301906460015, 'o1': 9.554828907605941, 'o2': 3.7446230027143463, 'o3': 7.744839733823972, 'o4': 5.165107048258493, 'o5': 5.4372299438309355, 'o6': 5.331094545444749, 'o7': 8.858144555463792, 'o8': 7.191549425583343, 'o9': 4.431462866037618, 'o10': 6.040165672357492, 'o11': 9.467924904787546, 'o12': 7.335533798524998, 'o13': 9.02795592329443, 'o14': 7.549871742489586, 'o15': 7.462300653810477, 'o16': 4.8944219679094445, 'o17': 9.001075151763942}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3'], 'type2': ['o4', 'o5', 'o6', 'o7'], 'type3': ['o8', 'o9', 'o10', 'o11', 'o12'], 'type4': ['o13', 'o14', 'o15', 'o16', 'o17']}

def ResetState():
    state.loc = { 'r0': 15, 'r1': 7, 'r2': 8, 'r3': 7, 'r4': 5, 'r5': 7, 'r6': 1, 'r7': 9, 'r8': 13, 'r9': 3, 'r10': 2, 'r11': 15, 'r12': 20, 'r13': 10, 'm0': 11, 'm1': 20, 'm2': 0, 'm3': 19, 'm4': 17, 'fixer0': 20, 'fixer1': 12, 'fixer2': 20, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK,}
    state.storedLoc = {'o0': 18, 'o1': 0, 'o2': 2, 'o3': 7, 'o4': 14, 'o5': 5, 'o6': 4, 'o7': 1, 'o8': 18, 'o9': 12, 'o10': 15, 'o11': 1, 'o12': 8, 'o13': 14, 'o14': 7, 'o15': 3, 'o16': 6, 'o17': 0}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'r13': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 14, 'm1': 10, 'm2': 12, 'm3': 8, 'm4': 4}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    10: [['order', 'type2', 200]],
    13: [['order', 'type2', 200]],
}
eventsEnv = {
}