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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 1}

rv.GROUND_EDGES = {0: [4, 1, 7, 8, 12], 1: [0, 3], 2: [5, 11], 3: [1, 5, 4, 6, 11], 4: [3, 15, 0, 200], 5: [6, 10, 2, 3, 13], 6: [3, 9, 11, 5, 15, 200], 7: [0, 10, 11, 15, 9], 8: [0, 11], 9: [7, 6, 10, 13, 14], 10: [9, 5, 7, 11], 11: [2, 3, 8, 10, 6, 7], 12: [0], 13: [5, 9], 14: [9, 15], 15: [6, 14, 4, 7], 200: [4, 6]}
rv.GROUND_WEIGHTS = {(0, 4): 7.6242732763575685, (0, 1): 4.6451695889645555, (0, 7): 3.988986665546318, (0, 8): 15.282730621258397, (0, 12): 10.153982472104325, (1, 3): 12.57983449770448, (2, 5): 4.030885494910138, (2, 11): 6.455574625083316, (3, 5): 1, (3, 4): 1.9094014777740602, (3, 6): 11.01459646524018, (3, 11): 6.261898087610945, (4, 15): 3.4170636640484764, (4, 200): 7.5512660417680175, (5, 6): 4.059078008664073, (5, 10): 10.131807223922227, (5, 13): 7.437954996977452, (6, 9): 5.853711343443321, (6, 11): 7.199043906671107, (6, 15): 6.1478705083188805, (6, 200): 11.445440333421145, (7, 10): 3.5976309555833526, (7, 11): 10.22778236804009, (7, 15): 7.237745920137269, (7, 9): 12.813183815306004, (8, 11): 4.987371259323722, (9, 10): 10.194160136097816, (9, 13): 4.3378468128951635, (9, 14): 8.87980220943679, (10, 11): 7.079819198124444, (14, 15): 13.602430448909743}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 10.769040002937324, 'r1': 7.248044870704281, 'r2': 10.72036482910855, 'r3': 2.0593826951730687, 'r4': 6.411424248168577, 'r5': 6.822037468948866, 'r6': 10.490339778496153, 'r7': 9.191089258010072, 'r8': 8.68446090856322, 'r9': 9.33183673861472, 'r10': 7.0047194390375624, 'r11': 10.810442346480613}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18']
rv.OBJ_WEIGHT = {'o0': 8.104598658315316, 'o1': 5.8675428914186085, 'o2': 8.056163307764741, 'o3': 5.544159335999201, 'o4': 5.075608026390325, 'o5': 4.053116514545312, 'o6': 7.994876667721648, 'o7': 6.44252760994694, 'o8': 5.215607563779819, 'o9': 7.168671305342019, 'o10': 7.900245796873181, 'o11': 9.591835304292058, 'o12': 10.810442346480613, 'o13': 7.19227168966459, 'o14': 5.5747624514629806, 'o15': 7.848635228285933, 'o16': 7.732690257214262, 'o17': 7.040909947316012, 'o18': 6.449798561994199}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3'], 'type1': ['o4', 'o5', 'o6'], 'type2': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type3': ['o12', 'o13'], 'type4': ['o14', 'o15', 'o16', 'o17', 'o18']}

def ResetState():
    state.loc = { 'r0': 3, 'r1': 11, 'r2': 4, 'r3': 0, 'r4': 0, 'r5': 14, 'r6': 13, 'r7': 5, 'r8': 10, 'r9': 11, 'r10': 10, 'r11': 1, 'm0': 11, 'm1': 5, 'm2': 2, 'm3': 13, 'm4': 3, 'm5': 7, 'm6': 13, 'fixer0': 7, 'fixer1': 8, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK,}
    state.storedLoc = {'o0': 13, 'o1': 13, 'o2': 13, 'o3': 10, 'o4': 0, 'o5': 13, 'o6': 15, 'o7': 10, 'o8': 10, 'o9': 6, 'o10': 7, 'o11': 7, 'o12': 0, 'o13': 4, 'o14': 12, 'o15': 8, 'o16': 6, 'o17': 5, 'o18': 3}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 12, 'm1': 7, 'm2': 12, 'm3': 11, 'm4': 6, 'm5': 7, 'm6': 10}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    13: [['order', 'type0', 200]],
    27: [['order', 'type0', 200]],
}
eventsEnv = {
}