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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 15}

rv.GROUND_EDGES = {0: [9, 14, 6, 8, 12, 13, 200], 1: [3, 7, 14, 2], 2: [1, 5, 9, 10, 7], 3: [14, 1, 7, 10, 17], 4: [5, 10, 11], 5: [16, 2, 4], 6: [0, 15, 17], 7: [2, 3, 11, 1, 17], 8: [0], 9: [10, 14, 0, 2, 15], 10: [3, 2, 4, 9, 15], 11: [4, 7], 12: [0, 15], 13: [0, 200], 14: [3, 16, 0, 1, 9], 15: [6, 9, 10, 12, 16], 16: [15, 5, 14], 17: [3, 6, 7], 200: [0, 13]}
rv.GROUND_WEIGHTS = {(0, 9): 9.085760772357991, (0, 14): 5.397917482170811, (0, 6): 6.145022245643342, (0, 8): 1, (0, 12): 3.4304281578149567, (0, 13): 8.410264646588661, (0, 200): 7.447151771364974, (1, 3): 5.11480504787637, (1, 7): 3.687626756135706, (1, 14): 10.471482209445703, (1, 2): 10.018810672031325, (2, 5): 11.685686985321786, (2, 9): 6.6610940699231485, (2, 10): 6.730148301128206, (2, 7): 6.648090470948661, (3, 14): 9.975237850545666, (3, 7): 8.272413930127847, (3, 10): 9.482314783624926, (3, 17): 7.4222911132313705, (4, 5): 2.4689572278105736, (4, 10): 15.218353558275954, (4, 11): 6.14053578151067, (5, 16): 11.164917302392016, (6, 15): 4.112563463748279, (6, 17): 5.6697279591003795, (7, 11): 4.547616125103694, (7, 17): 16.707079978896743, (9, 10): 8.579887061436892, (9, 14): 10.267063066127207, (9, 15): 3.5158588588738953, (10, 15): 10.400625526126984, (12, 15): 6.498264838539245, (13, 200): 8.880301304619149, (14, 16): 9.322761034505058, (15, 16): 4.488346670407218}

rv.ROBOTS = { 'r0': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 8.905303263722027}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1,  'm6': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']
rv.OBJ_WEIGHT = {'o0': 8.457565170035977, 'o1': 7.130586635499137, 'o2': 7.089654888191273, 'o3': 6.640188044601038, 'o4': 8.905303263722027, 'o5': 4.4428441670357035, 'o6': 8.182621987518194, 'o7': 6.472029636623807, 'o8': 8.87395549218396, 'o9': 5.674359078018697, 'o10': 6.532737130308578, 'o11': 2.272657088679292, 'o12': 4.8561574879943015, 'o13': 6.542341722644219, 'o14': 2.3627259007777006, 'o15': 7.490164236964756, 'o16': 6.405128602830502, 'o17': 8.855823920239805, 'o18': 5.359489309257067, 'o19': 8.905303263722027, 'o20': 4.317634188736749, 'o21': 7.132553137749122, 'o22': 5.493991215304185, 'o23': 3.441700979194826, 'o24': 8.016445296176036}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6'], 'type1': ['o7', 'o8', 'o9', 'o10'], 'type2': ['o11', 'o12', 'o13', 'o14'], 'type3': ['o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24']}

def ResetState():
    state.loc = { 'r0': 5, 'm0': 5, 'm1': 6, 'm2': 13, 'm3': 9, 'm4': 8, 'm5': 6, 'm6': 7, 'fixer0': 13, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK,}
    state.storedLoc = {'o0': 1, 'o1': 10, 'o2': 13, 'o3': 6, 'o4': 1, 'o5': 8, 'o6': 0, 'o7': 15, 'o8': 5, 'o9': 15, 'o10': 0, 'o11': 1, 'o12': 3, 'o13': 16, 'o14': 11, 'o15': 6, 'o16': 12, 'o17': 14, 'o18': 1, 'o19': 2, 'o20': 7, 'o21': 16, 'o22': 3, 'o23': 7, 'o24': 11}
    state.load = { 'r0': NIL, 'fixer0': False,}
    state.busy = {'r0': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'm6': False, 'fixer0': False}
    state.numUses = {'m0': 8, 'm1': 8, 'm2': 2, 'm3': 13, 'm4': 6, 'm5': 14, 'm6': 12}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    19: [['order', 'type0', 200]],
    14: [['order', 'type0', 200]],
}
eventsEnv = {
}