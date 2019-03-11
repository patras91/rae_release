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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 5}

rv.GROUND_EDGES = {0: [6, 8, 9, 2, 200], 1: [2, 7, 8, 12, 9, 10], 2: [0, 1, 3, 5, 7], 3: [2, 4, 7], 4: [6, 9, 10, 3, 7, 8], 5: [2, 10], 6: [4, 7, 0, 11], 7: [2, 3, 4, 9, 10, 12, 1, 6, 8], 8: [4, 7, 0, 1], 9: [1, 0, 4, 7], 10: [1, 5, 4, 7], 11: [6, 200], 12: [7, 1], 200: [0, 11]}
rv.GROUND_WEIGHTS = {(0, 6): 4.917021514925569, (0, 8): 5.549682866450274, (0, 9): 12.708157897011041, (0, 2): 6.639610458459614, (0, 200): 13.562049850880545, (1, 2): 8.116833229476585, (1, 7): 10.593943272625747, (1, 8): 4.064069944309695, (1, 12): 11.041193025104873, (1, 9): 9.597006136271622, (1, 10): 1, (2, 3): 7.7045867090697975, (2, 5): 9.694196735726415, (2, 7): 17.05879873808906, (3, 4): 11.197516774485395, (3, 7): 7.620618465319518, (4, 6): 8.442631893155955, (4, 9): 9.840117417858202, (4, 10): 15.654122665200648, (4, 7): 9.730624930536726, (4, 8): 8.508234404730542, (5, 10): 8.11359301037446, (6, 7): 9.839748305110586, (6, 11): 5.806554423188754, (7, 9): 12.614036211150784, (7, 10): 3.8400226352458224, (7, 12): 10.465024766706607, (7, 8): 5.170220936189552, (11, 200): 12.174268650384112}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 11.193862423166777, 'r1': 7.610532403872681, 'r2': 3.9819728660627494, 'r3': 4.443348473460192, 'r4': 7.750499680595786, 'r5': 11.8301507361888, 'r6': 7.568033419550897, 'r7': 6.174476015525274, 'r8': 7.722483251301364, 'r9': 8.888585500589073, 'r10': 8.733520548081152, 'r11': 10.303119789225274}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1,  'm7': rv.FACTORY1,  'm8': rv.FACTORY1,  'm9': rv.FACTORY1,  'm10': rv.FACTORY1,  'm11': rv.FACTORY1,  'm12': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14']
rv.OBJ_WEIGHT = {'o0': 4.985265419647385, 'o1': 8.163482253765157, 'o2': 9.262044412774191, 'o3': 7.797074816921224, 'o4': 5.322493621355893, 'o5': 6.55492647426014, 'o6': 7.039224457586506, 'o7': 6.135238605965274, 'o8': 8.786433959647773, 'o9': 8.961748450730262, 'o10': 6.082403011342788, 'o11': 7.443015758618878, 'o12': 7.549900480150155, 'o13': 9.592089824112787, 'o14': 7.078791007358069}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4'], 'type1': ['o5', 'o6'], 'type2': ['o7', 'o8', 'o9'], 'type3': ['o10', 'o11', 'o12', 'o13', 'o14']}

def ResetState():
    state.loc = { 'r0': 6, 'r1': 12, 'r2': 4, 'r3': 0, 'r4': 6, 'r5': 4, 'r6': 8, 'r7': 5, 'r8': 12, 'r9': 2, 'r10': 6, 'r11': 11, 'm0': 0, 'm1': 10, 'm2': 3, 'm3': 11, 'm4': 5, 'm5': 10, 'm6': 7, 'm7': 11, 'm8': 2, 'm9': 6, 'm10': 3, 'm11': 9, 'm12': 9, 'fixer0': 8, 'fixer1': 11, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK,}
    state.storedLoc = {'o0': 6, 'o1': 10, 'o2': 12, 'o3': 11, 'o4': 10, 'o5': 11, 'o6': 2, 'o7': 2, 'o8': 2, 'o9': 6, 'o10': 8, 'o11': 10, 'o12': 8, 'o13': 5, 'o14': 1}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'm7': False, 'm8': False, 'm9': False, 'm10': False, 'm11': False, 'm12': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 8, 'm1': 9, 'm2': 17, 'm3': 11, 'm4': 12, 'm5': 7, 'm6': 6, 'm7': 12, 'm8': 8, 'm9': 11, 'm10': 9, 'm11': 10, 'm12': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    1: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
}
eventsEnv = {
}