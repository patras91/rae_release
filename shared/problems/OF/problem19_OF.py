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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 7}

rv.GROUND_EDGES = {0: [3, 5, 13, 1, 6, 7, 200], 1: [0, 4, 9, 3, 5], 2: [7, 10, 11, 13], 3: [1, 7, 0, 9], 4: [1, 6, 10, 8, 13], 5: [1, 0, 6, 10, 13], 6: [0, 5, 9, 4, 14], 7: [0, 200, 2, 3, 9, 10], 8: [4, 9], 9: [3, 7, 8, 10, 11, 1, 6], 10: [2, 5, 7, 11, 4, 9], 11: [2, 14, 9, 10], 12: [13, 14], 13: [2, 4, 5, 0, 12], 14: [6, 11, 12], 200: [0, 7]}
rv.GROUND_WEIGHTS = {(0, 3): 9.401411888425368, (0, 5): 6.647344828828647, (0, 13): 1.4950683058935272, (0, 1): 9.284797893576254, (0, 6): 6.634722429440145, (0, 7): 10.356216616693793, (0, 200): 1, (1, 4): 9.669191702497123, (1, 9): 3.632286123611701, (1, 3): 5.164148782850544, (1, 5): 1, (2, 7): 8.049754450077689, (2, 10): 9.18079677673413, (2, 11): 9.863498770473448, (2, 13): 6.115982929755149, (3, 7): 8.61128752158957, (3, 9): 10.934595071488689, (4, 6): 7.603906837476489, (4, 10): 6.549453118938137, (4, 8): 6.268544946325625, (4, 13): 5.296962867585334, (5, 6): 7.168445912196171, (5, 10): 8.87734091966879, (5, 13): 7.760956799697277, (6, 9): 8.863058214040226, (6, 14): 2.101435463287756, (7, 200): 6.058484207938523, (7, 9): 9.9242355615051, (7, 10): 11.608283720137738, (8, 9): 14.481078990678679, (9, 10): 14.358439123801988, (9, 11): 8.82637154922752, (10, 11): 12.931202006253688, (11, 14): 14.561361460743793, (12, 13): 1, (12, 14): 7.226732910951306}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 5.826898966925391, 'r1': 9.156993854349665, 'r2': 4.321822602582952, 'r3': 7.660235482371372, 'r4': 6.6902862685724, 'r5': 10.571122812442884, 'r6': 5.164990333343976, 'r7': 6.922586923125195}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1,  'm11': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21']
rv.OBJ_WEIGHT = {'o0': 7.33328735781424, 'o1': 6.203221150204831, 'o2': 10.571122812442884, 'o3': 7.5920631622339725, 'o4': 6.261688783631462, 'o5': 3.1918303668493286, 'o6': 8.91070929792405, 'o7': 5.6177869085242795, 'o8': 8.276966587811884, 'o9': 6.728121259676684, 'o10': 5.860624632214053, 'o11': 3.265217784561505, 'o12': 6.276364020033757, 'o13': 7.577057281813666, 'o14': 7.626642652110909, 'o15': 7.218359634739985, 'o16': 8.459573603836544, 'o17': 6.063298691870324, 'o18': 10.158273823027127, 'o19': 10.571122812442884, 'o20': 6.590747289565924, 'o21': 8.001142212421414}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2'], 'type1': ['o3', 'o4', 'o5', 'o6', 'o7', 'o8'], 'type2': ['o9', 'o10', 'o11', 'o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17', 'o18'], 'type4': ['o19', 'o20', 'o21']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 4, 'r2': 5, 'r3': 10, 'r4': 4, 'r5': 10, 'r6': 7, 'r7': 13, 'm0': 7, 'm1': 6, 'm2': 1, 'm3': 11, 'm4': 12, 'm5': 12, 'm6': 13, 'm7': 10, 'm8': 1, 'm9': 13, 'm10': 12, 'm11': 8, 'fixer0': 8, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK,}
    state.storedLoc = {'o0': 5, 'o1': 0, 'o2': 8, 'o3': 14, 'o4': 8, 'o5': 3, 'o6': 2, 'o7': 7, 'o8': 3, 'o9': 8, 'o10': 0, 'o11': 0, 'o12': 13, 'o13': 11, 'o14': 11, 'o15': 7, 'o16': 13, 'o17': 12, 'o18': 3, 'o19': 0, 'o20': 6, 'o21': 0}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'm11': False, 'fixer0': False}
    state.numUses = {'m0': 9, 'm1': 7, 'm2': 11, 'm3': 5, 'm4': 10, 'm5': 9, 'm6': 11, 'm7': 10, 'm8': 11, 'm9': 8, 'm10': 16, 'm11': 9}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    13: [['order', 'type0', 200]],
    24: [['order', 'type0', 200]],
}
eventsEnv = {
}