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
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [1, 2, 7, 11, 13], 1: [2, 10, 0, 5, 11], 2: [0, 1, 8, 12, 4, 200], 3: [5, 10, 11, 200], 4: [2, 7, 11, 12, 8, 10], 5: [1, 6, 3, 9], 6: [8, 5, 10, 12], 7: [0, 8, 11, 4], 8: [4, 9, 2, 6, 7], 9: [5, 10, 8], 10: [4, 6, 1, 3, 9], 11: [0, 1, 3, 4, 7, 12], 12: [6, 11, 2, 4, 200], 13: [0], 200: [2, 3, 12]}
rv.GROUND_WEIGHTS = {(0, 1): 9.857007792003694, (0, 2): 16.75736763316951, (0, 7): 12.960600224093671, (0, 11): 7.702845027429869, (0, 13): 10.300469385785178, (1, 2): 10.162652154648343, (1, 10): 6.095825706761472, (1, 5): 3.897353033632916, (1, 11): 12.53934521522828, (2, 8): 10.18681952899972, (2, 12): 3.8585452722558093, (2, 4): 11.01758673430188, (2, 200): 4.56575646773031, (3, 5): 11.9425621647989, (3, 10): 7.594858567981563, (3, 11): 10.55399091311538, (3, 200): 8.4175033752133, (4, 7): 8.653821534102283, (4, 11): 6.911706808623055, (4, 12): 3.018149609962852, (4, 8): 6.272579743662172, (4, 10): 1.203955346444162, (5, 6): 9.832245051620351, (5, 9): 12.201149854382592, (6, 8): 2.2577468276917605, (6, 10): 7.612245434669492, (6, 12): 12.650375488876024, (7, 8): 2.526117877330316, (7, 11): 9.105210351679208, (8, 9): 4.741194125049686, (9, 10): 9.533174305012198, (11, 12): 6.696260554883127, (12, 200): 6.872989375645158}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 5.160676797801053, 'r1': 7.74441856572802, 'r2': 7.6145887658036, 'r3': 3.617108338391513, 'r4': 10.04781589069762, 'r5': 10.87500283658833, 'r6': 6.245963073909404, 'r7': 8.315023431688402, 'r8': 3.847094721913896, 'r9': 7.2306723699136795, 'r10': 5.556670820079358, 'r11': 5.72683056600958, 'r12': 9.287409316647349}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = ['fixer0', 'fixer1']

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23']
rv.OBJ_WEIGHT = {'o0': 7.035170915549936, 'o1': 6.699347948410018, 'o2': 9.483967202858505, 'o3': 6.93749454705989, 'o4': 7.498420712485631, 'o5': 4.4234549960617855, 'o6': 6.902347657085805, 'o7': 7.9983422589632385, 'o8': 6.811440129867468, 'o9': 3.2223857668897145, 'o10': 7.196876073105926, 'o11': 4.181351737468167, 'o12': 3.9140353717990792, 'o13': 6.983794465246633, 'o14': 5.0861928414756585, 'o15': 7.558103782604917, 'o16': 6.890328301633174, 'o17': 7.978078984916776, 'o18': 7.754308321908186, 'o19': 7.814397439846863, 'o20': 6.066912354673571, 'o21': 10.001146600343395, 'o22': 5.957593169076982, 'o23': 5.918207487659027}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13'], 'type3': ['o14'], 'type4': ['o15', 'o16', 'o17', 'o18', 'o19', 'o20'], 'type5': ['o21', 'o22', 'o23']}

def ResetState():
    state.loc = { 'r0': 8, 'r1': 1, 'r2': 7, 'r3': 3, 'r4': 6, 'r5': 4, 'r6': 6, 'r7': 11, 'r8': 12, 'r9': 10, 'r10': 6, 'r11': 4, 'r12': 4, 'm0': 1, 'm1': 4, 'fixer0': 0, 'fixer1': 6, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK,}
    state.storedLoc = {'o0': 10, 'o1': 13, 'o2': 2, 'o3': 3, 'o4': 0, 'o5': 13, 'o6': 10, 'o7': 7, 'o8': 6, 'o9': 0, 'o10': 1, 'o11': 7, 'o12': 7, 'o13': 7, 'o14': 2, 'o15': 2, 'o16': 2, 'o17': 10, 'o18': 2, 'o19': 3, 'o20': 3, 'o21': 13, 'o22': 4, 'o23': 0}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 13, 'm1': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'shouldRedo': False}

tasks = {
    3: [['order', 'type0', 200]],
    23: [['order', 'type0', 200]],
}
eventsEnv = {
}