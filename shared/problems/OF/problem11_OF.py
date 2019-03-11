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

rv.LOCATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 200]
rv.FACTORY1 = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22})
rv.FACTORY_UNION = rv.FACTORY1
rv.SHIPPING_DOC = {rv.FACTORY1: 3}

rv.GROUND_EDGES = {0: [6, 12], 1: [12, 16, 8, 17], 2: [5, 12, 13, 19, 3, 11, 17], 3: [2, 13, 19, 22], 4: [17, 200], 5: [2], 6: [0, 11, 15, 18], 7: [19, 18], 8: [1, 22, 18], 9: [12, 17, 20, 14], 10: [15, 19, 21], 11: [2, 6, 17, 16, 19, 20, 200], 12: [0, 15, 16, 21, 1, 2, 9], 13: [14, 2, 3, 19, 20], 14: [9, 13, 19, 21], 15: [6, 19, 10, 12], 16: [11, 1, 12], 17: [1, 2, 11, 4, 9], 18: [6, 7, 8, 200], 19: [11, 13, 14, 2, 3, 7, 10, 15], 20: [11, 13, 21, 9], 21: [10, 14, 12, 20], 22: [3, 8], 200: [4, 11, 18]}
rv.GROUND_WEIGHTS = {(0, 6): 9.269886453448501, (0, 12): 11.81555328897423, (1, 12): 8.453988813887607, (1, 16): 1, (1, 8): 1, (1, 17): 7.293640484863735, (2, 5): 8.790762306713644, (2, 12): 9.418133379465253, (2, 13): 12.093438957951513, (2, 19): 9.818999929929914, (2, 3): 1, (2, 11): 12.04842414760601, (2, 17): 7.396536790700892, (3, 13): 5.242319637913575, (3, 19): 10.255727907832553, (3, 22): 16.112427538087395, (4, 17): 4.522176838367895, (4, 200): 7.972648117854833, (6, 11): 8.311738274793505, (6, 15): 7.914168889192686, (6, 18): 4.3007761952939525, (7, 19): 8.651184376142359, (7, 18): 10.040781498891477, (8, 22): 9.240203103588135, (8, 18): 6.361654196380402, (9, 12): 1.1093912082677875, (9, 17): 8.48250081551015, (9, 20): 3.198355840063811, (9, 14): 4.062534108733649, (10, 15): 6.3818828865373876, (10, 19): 14.011068354687001, (10, 21): 6.477814053822925, (11, 17): 11.565807188893833, (11, 16): 14.148014450839469, (11, 19): 10.559244196585777, (11, 20): 12.013700317209185, (11, 200): 4.489841685809592, (12, 15): 11.557350921443057, (12, 16): 12.423537216593733, (12, 21): 8.514331979549107, (13, 14): 10.804394992645909, (13, 19): 6.08061705800353, (13, 20): 6.797728096331827, (14, 19): 13.235194232409356, (14, 21): 10.646006605558297, (15, 19): 6.975194815473062, (18, 200): 10.124986461493236, (20, 21): 16.14471891084213}

rv.ROBOTS = { 'r0': rv.FACTORY1,  'r1': rv.FACTORY1,  'r2': rv.FACTORY1,  'r3': rv.FACTORY1,  'r4': rv.FACTORY1,  'r5': rv.FACTORY1,  'r6': rv.FACTORY1,  'r7': rv.FACTORY1,  'r8': rv.FACTORY1,  'r9': rv.FACTORY1,  'r10': rv.FACTORY1,  'r11': rv.FACTORY1,  'r12': rv.FACTORY1, }
rv.ROBOT_CAPACITY = {'r0': 7.705864073598879, 'r1': 11.631643932864046, 'r2': 9.615869415724882, 'r3': 7.383443021086257, 'r4': 4.154720968886441, 'r5': 9.921421360937002, 'r6': 8.417419231198544, 'r7': 5.911027984987562, 'r8': 6.669953469041136, 'r9': 7.894008423415527, 'r10': 9.269455751440542, 'r11': 6.5807375670762, 'r12': 10.192171056621175}
rv.MACHINES = { 'm0': rv.FACTORY1,  'm1': rv.FACTORY1,  'm2': rv.FACTORY1,  'm3': rv.FACTORY1,  'm4': rv.FACTORY1,  'm5': rv.FACTORY1, }
rv.REPAIR_BOT = { 'fixer0': rv.FACTORY1,  'fixer1': rv.FACTORY1, }

rv.OBJECTS = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18', 'o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']
rv.OBJ_WEIGHT = {'o0': 5.1763676369673455, 'o1': 8.344085977694123, 'o2': 6.432249498719909, 'o3': 7.25550601212883, 'o4': 8.007062915778882, 'o5': 6.002139143949664, 'o6': 6.023439418700865, 'o7': 5.790492223461889, 'o8': 6.606649091509915, 'o9': 6.473766226798527, 'o10': 8.6776132053337, 'o11': 5.714009171461081, 'o12': 4.790378679801499, 'o13': 5.60881978469046, 'o14': 8.826990131266218, 'o15': 3.4374896905025687, 'o16': 7.41524351555181, 'o17': 5.851013099588839, 'o18': 9.642294196966036, 'o19': 7.643316162387353, 'o20': 7.39224831722801, 'o21': 5.755510736095518, 'o22': 9.963850099736147, 'o23': 4.621728725617388, 'o24': 7.488397249461975, 'o25': 5.178836071682583}
rv.OBJ_CLASS = {'type0': ['o0', 'o1', 'o2', 'o3', 'o4', 'o5'], 'type1': ['o6', 'o7', 'o8', 'o9', 'o10', 'o11'], 'type2': ['o12', 'o13', 'o14', 'o15', 'o16', 'o17', 'o18'], 'type3': ['o19', 'o20', 'o21', 'o22', 'o23', 'o24', 'o25']}

def ResetState():
    state.loc = { 'r0': 0, 'r1': 19, 'r2': 6, 'r3': 4, 'r4': 21, 'r5': 15, 'r6': 22, 'r7': 19, 'r8': 9, 'r9': 3, 'r10': 7, 'r11': 21, 'r12': 16, 'm0': 21, 'm1': 9, 'm2': 18, 'm3': 12, 'm4': 15, 'm5': 18, 'fixer0': 4, 'fixer1': 17, 'o0': UNK, 'o1': UNK, 'o2': UNK, 'o3': UNK, 'o4': UNK, 'o5': UNK, 'o6': UNK, 'o7': UNK, 'o8': UNK, 'o9': UNK, 'o10': UNK, 'o11': UNK, 'o12': UNK, 'o13': UNK, 'o14': UNK, 'o15': UNK, 'o16': UNK, 'o17': UNK, 'o18': UNK, 'o19': UNK, 'o20': UNK, 'o21': UNK, 'o22': UNK, 'o23': UNK, 'o24': UNK, 'o25': UNK,}
    state.storedLoc = {'o0': 2, 'o1': 22, 'o2': 13, 'o3': 3, 'o4': 7, 'o5': 11, 'o6': 1, 'o7': 18, 'o8': 6, 'o9': 4, 'o10': 5, 'o11': 0, 'o12': 4, 'o13': 20, 'o14': 7, 'o15': 8, 'o16': 12, 'o17': 9, 'o18': 4, 'o19': 19, 'o20': 21, 'o21': 9, 'o22': 21, 'o23': 15, 'o24': 4, 'o25': 12}
    state.load = { 'r0': NIL, 'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL, 'r5': NIL, 'r6': NIL, 'r7': NIL, 'r8': NIL, 'r9': NIL, 'r10': NIL, 'r11': NIL, 'r12': NIL, 'fixer0': False, 'fixer1': False,}
    state.busy = {'r0': False, 'r1': False, 'r2': False, 'r3': False, 'r4': False, 'r5': False, 'r6': False, 'r7': False, 'r8': False, 'r9': False, 'r10': False, 'r11': False, 'r12': False, 'm0': False, 'm1': False, 'm2': False, 'm3': False, 'm4': False, 'm5': False, 'fixer0': False, 'fixer1': False}
    state.numUses = {'m0': 2, 'm1': 8, 'm2': 10, 'm3': 9, 'm4': 2, 'm5': 8}
    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}
    state.shouldRedo = {}

tasks = {
    14: [['order', 'type0', 200]],
    5: [['order', 'type0', 200]],
}
eventsEnv = {
}