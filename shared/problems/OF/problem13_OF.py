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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 9}

rv.GROUND_EDGES = {0: [8, 10, 1, 6, 7, 9, 14, 15, 16], 1: [0, 11, 13, 16], 2: [4, 5, 3, 13], 3: [2, 4, 12], 4: [8, 12, 16, 2, 3], 5: [6, 15, 2], 6: [0, 14, 5], 7: [0], 8: [0, 4, 10, 11], 9: [0, 12], 10: [0, 8], 11: [8, 12, 13, 1], 12: [9, 3, 4, 11, 200], 13: [2, 16, 1, 11], 14: [0, 6], 15: [0, 5], 16: [0, 1, 4, 13], 200: [12]}
rv.GROUND_WEIGHTS = {(0, 8): 10.881874885922663, (0, 10): 9.139924965768548, (0, 1): 8.703487753934848, (0, 6): 6.907094459153903, (0, 7): 8.115241948947657, (0, 9): 12.002155970381503, (0, 14): 7.4447509946051, (0, 15): 9.004410941064878, (0, 16): 7.066433236346859, (1, 11): 5.69357663069892, (1, 13): 5.724479281425166, (1, 16): 8.006470125962517, (2, 4): 17.35197173908955, (2, 5): 9.732439372915115, (2, 3): 15.533722420905892, (2, 13): 5.0431621894876155, (3, 4): 6.708022725045028, (3, 12): 7.209737111579878, (4, 8): 5.2797051068255545, (4, 12): 9.453456992424709, (4, 16): 2.432535553438343, (5, 6): 3.1403563186490304, (5, 15): 3.169732935813851, (6, 14): 4.801307527513833, (8, 10): 10.58112003564986, (8, 11): 6.784079661132543, (9, 12): 5.70081517996624, (11, 12): 8.288880135406336, (11, 13): 8.804316210114825, (12, 200): 5.288928874251317, (13, 16): 10.000209842918302}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.699125991107619, 'r1': 10.900195505858502, 'r2': 5.4099830650505165, 'r3': 8.78728155510086, 'r4': 7.454969897312611, 'r5': 11.602191964063152, 'r6': 7.102629625608365, 'r7': 8.163416688317575, 'r8': 9.326993384125231, 'r9': 8.258033379708165}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25', 'o26', 'o27', 'o28', 'o29', 'o30', 'o31']
rv.OBJ_WEIGHT = {'o0': 6.402984530850462, 'o1': 4.3759132505011245, 'o2': 8.352837267587013, 'o3': 6.597865374302149, 'o4': 7.545150057414101, 'o5': 8.402064949765624, 'o6': 10.420218546807146, 'o7': 4.961509246172018, 'o8': 7.8453797855351, 'o9': 8.89575633339689, 'o10': 5.401850479420382, 'o11': 9.556627858640635, 'o12': 5.98775746474393, 'o13': 8.411328135065567, 'o14': 3.5029709243583715, 'o15': 7.760087940001739, 'o16': 5.994529057958531, 'o17': 9.19885847693915, 'o18': 8.25255359983877, 'o19': 5.5096343018429135, 'o20': 4.847276219594932, 'o21': 7.902119541777906, 'o22': 7.154305952004757, 'o23': 8.228411587460277, 'o24': 9.896663985115302, 'o25': 8.535430123225254, 'o26': 3.7842970581440345, 'o27': 10.196470403566138, 'o28': 7.160052853913785, 'o29': 7.4279861862651355, 'o30': 5.775697953449475, 'o31': 7.113878313676113}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13'], 'type2': ['o14', 'o15', 'o16', 'o17', 'o18', 'o19'], 'type3': ['o20', 'o21', 'o22', 'o23', 'o24', 'o25'], 'type4': ['o26', 'o27', 'o28', 'o29', 'o30', 'o31']}

def ResetState():
    state.loc = { 'r0': 1, 'r1': 11, 'r2': 15, 'r3': 11, 'r4': 9, 'r5': 14, 'r6': 10, 'r7': 14, 'r8': 7, 'r9': 12, 'm0': 10, 'm1': 1, 'm2': 1, 'm3': 6, 'm4': 5, 'fixer0': 14, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK, 'o26': UNK, 'o27': UNK, 'o28': UNK, 'o29': UNK, 'o30': UNK, 'o31': UNK,}
    state.storedLoc = {'o0': 8, 'o1': 9, 'o2': 7, 'o3': 8, 'o4': 7, 'o5': 0, 'o6': 5, 'o7': 7, 'o8': 9, 'o9': 16, 'o10': 8, 'o11': 15, 'o12': 9, 'o13': 6, 'o14': 9, 'o15': 15, 'o16': 5, 'o17': 2, 'o18': 10, 'o19': 4, 'o20': 5, 'o21': 15, 'o22': 10, 'o23': 13, 'o24': 9, 'o25': 3, 'o26': 0, 'o27': 16, 'o28': 9, 'o29': 11, 'o30': 0, 'o31': 15}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'fixer0': False}
    state.numUses = {'m0': 10, 'm1': 8, 'm2': 14, 'm3': 6, 'm4': 13}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    2: [['order', 'type0', 200]],
    50: [['order', 'type0', 200]],
}
eventsEnv = {
}