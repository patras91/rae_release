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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 5.315041143019441}

rv.GROUND_EDGES = {0: [6, 1, 2, 10, 11], 1: [0, 14], 2: [0, 3, 7, 8], 3: [2, 6, 4], 4: [3, 6, 12], 5: [8, 15, 9, 200], 6: [0, 4, 3, 12], 7: [2], 8: [2, 5, 13], 9: [5, 10, 16], 10: [0, 9, 12], 11: [0], 12: [4, 6, 10, 16, 200], 13: [8, 14, 16, 200], 14: [1, 15, 13], 15: [5, 16, 14], 16: [12, 9, 13, 15], 200: [5, 12, 13]}
rv.GROUND_WEIGHTS = {(0, 6): 8.567960617149923, (0, 1): 4.066674092236864, (0, 2): 6.53166388111473, (0, 10): 3.666844031788415, (0, 11): 7.996231325898968, (1, 14): 8.62116799608952, (2, 3): 7.857333785437453, (2, 7): 8.55022742948599, (2, 8): 8.814484571596443, (3, 6): 2.8358815470255125, (3, 4): 1, (4, 6): 9.639371990936905, (4, 12): 12.688298188927629, (5, 8): 10.275749620379889, (5, 15): 9.235262415274198, (5, 9): 7.7310501793296025, (5, 200): 4.059753263641305, (6, 12): 6.308880861302993, (8, 13): 9.401167839215242, (9, 10): 12.105689234754347, (9, 16): 6.768963870444525, (10, 12): 5.199240398522241, (12, 16): 4.684838727803076, (12, 200): 8.296550028808763, (13, 14): 3.801200997147677, (13, 16): 9.378325488053333, (13, 200): 12.382304076061157, (14, 15): 5.969378365507499, (15, 16): 16.81169058702863}

rv.ROBOTS = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']
rv.ROBOT_CAPACITY = {'r0': 13.156602193491793, 'r1': 9.570606660782962, 'r2': 13.886069915014392, 'r3': 4.897396605823234, 'r4': 11.316557795446366, 'r5': 7.581651035167925, 'r6': 4.636020127221707, 'r7': 8.272472746630644, 'r8': 5.212363641366345, 'r9': 7.549736137977021, 'r10': 9.225050482089376, 'r11': 5.874451964829842, 'r12': 8.06257852248774, 'r13': 6.5032408080004105, 'r14': 7.752736476941836}
rv.MACHINES = ['m0', 'fixer0', 'fixer1']
rv.REPAIR_BOT = []

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11']
rv.OBJ_WEIGHT = {'o0': 7.618360277872142, 'o1': 6.910033488667948, 'o2': 7.980237188602078, 'o3': 3.6592429743822583, 'o4': 8.818385826841343, 'o5': 9.993504651666282, 'o6': 4.213407013679989, 'o7': 8.257775231189463, 'o8': 7.413555792025336, 'o9': 7.0981761526268, 'o10': 6.622002236556503, 'o11': 2.8312584757277506}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7'], 'type1': ['o8'], 'type2': ['o9'], 'type3': ['o10', 'o11']}

def ResetState():
    state.loc = { 'r0': 2, 'r1': 2, 'r2': 14, 'r3': 11, 'r4': 7, 'r5': 4, 'r6': 8, 'r7': 2, 'r8': 4, 'r9': 14, 'r10': 15, 'r11': 16, 'r12': 14, 'r13': 16, 'r14': 9, 'm0': 4, 'fixer0': 3, 'fixer1': 16, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK,}
    state.storedLoc = {'o0': 7, 'o1': 1, 'o2': 6, 'o3': 14, 'o4': 11, 'o5': 7, 'o6': 7, 'o7': 0, 'o8': 8, 'o9': 7, 'o10': 1, 'o11': 5}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'r13': NIL, 'r14': NIL,}
    state.busy = {"'r0'": False, "'r1'": False, "'r2'": False, "'r3'": False, "'r4'": False, "'r5'": False, "'r6'": False, "'r7'": False, "'r8'": False, "'r9'": False, "'r10'": False, "'r11'": False, "'r12'": False, "'r13'": False, "'r14'": False, "'m0'": False, "'fixer0'": False, "'fixer1'": False}
    state.numUses = {'m0': 12, 'fixer0': 11, 'fixer1': 11}
    state.var1 = {'temp': 'r1', 'temp1': 'r1'}

tasks = {
    9: [['order', 'type0', 200]],
    1: [['order', 'type0', 200]],
    2: [['order', 'type0', 200]],
    21: [['order', 'type0', 200]],
    8: [['order', 'type0', 200]],
    10: [['order', 'type0', 200]],
    17: [['order', 'type0', 200]],
    12: [['order', 'type0', 200]],
    16: [['order', 'type1', 200]],
    20: [['order', 'type2', 200]],
    14: [['order', 'type3', 200]],
}
eventsEnv = {
}