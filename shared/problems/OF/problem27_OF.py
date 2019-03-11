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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 4}

rv.GROUND_EDGES = {0: [7, 12, 3, 200], 1: [3, 16], 2: [13, 18], 3: [0, 1, 9, 11], 4: [22, 5, 13], 5: [4, 7, 11, 9, 18], 6: [7, 20], 7: [17, 0, 5, 6, 8, 20, 22, 23], 8: [7, 18, 15], 9: [3, 5, 12], 10: [11, 14, 18], 11: [3, 10, 12, 20, 5, 14], 12: [0, 9, 11, 13, 19], 13: [4, 12, 2], 14: [11, 15, 20, 10], 15: [8, 18, 23, 14], 16: [21, 1], 17: [22, 7], 18: [5, 2, 8, 10, 15, 21], 19: [12], 20: [7, 6, 11, 14], 21: [18, 16], 22: [7, 4, 17], 23: [7, 15], 200: [0]}
rv.GROUND_WEIGHTS = {(0, 7): 2.3914481153093705, (0, 12): 7.902448906317945, (0, 3): 6.852711575351456, (0, 200): 12.210410569224235, (1, 3): 4.609112544137735, (1, 16): 1, (2, 13): 11.990558350937564, (2, 18): 11.462674413816398, (3, 9): 9.102615138837875, (3, 11): 1, (4, 22): 1.718225030477317, (4, 5): 5.082589864178027, (4, 13): 15.61851073785758, (5, 7): 3.7936195658119622, (5, 11): 8.624468887584348, (5, 9): 1.54450753280988, (5, 18): 9.437940485369197, (6, 7): 3.718578963731864, (6, 20): 10.63342861411068, (7, 17): 6.014771567150797, (7, 8): 13.11541711816446, (7, 20): 6.108433107327314, (7, 22): 5.09656428824185, (7, 23): 9.317505252193616, (8, 18): 9.551860554611805, (8, 15): 1.8508926922475357, (9, 12): 5.331668367785892, (10, 11): 1.125954423421815, (10, 14): 8.760087582198757, (10, 18): 1, (11, 12): 7.987138953958666, (11, 20): 7.904782429538006, (11, 14): 7.271683711180895, (12, 13): 10.601602987051917, (12, 19): 12.538272190691455, (14, 15): 13.845759615731467, (14, 20): 13.10171435416205, (15, 18): 8.844922268685677, (15, 23): 5.2994459744087745, (16, 21): 5.2934814707143865, (17, 22): 6.159439718196656, (18, 21): 11.655189510607338}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 14.089671767796048, 'r1': 9.708359839127931, 'r2': 6.408146288303286, 'r3': 5.055717454825599, 'r4': 7.940773941130517, 'r5': 6.21745300816354, 'r6': 7.960522553148606}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1,  'fixer2': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']
rv.OBJ_WEIGHT = {'o0': 4.92320436659357, 'o1': 7.237906083062712, 'o2': 4.654190381398983, 'o3': 8.128709741222155, 'o4': 6.384345046741543, 'o5': 9.820531247742785, 'o6': 6.634399226508052, 'o7': 7.537198983702001, 'o8': 8.027368020575649, 'o9': 10.997281587102101, 'o10': 4.6116046847807, 'o11': 6.717832873124071, 'o12': 7.643061021930856, 'o13': 6.741605497027365, 'o14': 7.518593810136991, 'o15': 6.899577965721088, 'o16': 4.251599428255995, 'o17': 4.420395078086617, 'o18': 6.082808263973226, 'o19': 7.005761393020093, 'o20': 6.59364260779029, 'o21': 7.767845749630917, 'o22': 9.812734738239783}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22']}

def ResetState():
    state.loc = { 'r0': 14, 'r1': 20, 'r2': 21, 'r3': 19, 'r4': 23, 'r5': 11, 'r6': 2, 'm0': 4, 'm1': 11, 'fixer0': 0, 'fixer1': 2, 'fixer2': 5, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK,}
    state.storedLoc = {'o0': 0, 'o1': 3, 'o2': 4, 'o3': 5, 'o4': 7, 'o5': 18, 'o6': 11, 'o7': 14, 'o8': 7, 'o9': 10, 'o10': 15, 'o11': 4, 'o12': 14, 'o13': 23, 'o14': 16, 'o15': 2, 'o16': 12, 'o17': 22, 'o18': 13, 'o19': 4, 'o20': 3, 'o21': 8, 'o22': 23}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'fixer0': False, 'fixer1': False, 'fixer2': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'm0': False, 'm1': False, 'fixer0': False, 'fixer1': False, 'fixer2': False}
    state.numUses = {'m0': 18, 'm1': 10}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    1: [['order', 'type0', 200]],
    11: [['order', 'type0', 200]],
}
eventsEnv = {
}