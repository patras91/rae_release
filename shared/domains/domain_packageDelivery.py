__author__ = 'mason'

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape

from state import state
import gui
from timer import globalTimer
import globals

def fail():
    return FAILURE

def Order_Method1(item, l, type):
    # order from item i of shipping type type, to location l
    ape.do_task('find', item)
    ape.do_task('pack', item)
    ape.do_task('deliver', item, l, type)

# Refinement methods for find

def Find_Method1(item):
    # search an online database
    loc_item = state.loc[item]
    if loc_item == UNK:
        ape.do_command(lookupDB, item, state.NationalDatabase)

def lookupDB(item, database):
    state.loc.AcquireLock(item)
    database.AcquireLock(item)
    start = globalTimer.GetTime()

    while(globalTimer.IsCommandExecutionOver('lookupDB', start) == False):
        pass

    res = Sense('lookupDB')
    if res == SUCCESS:
        gui.Simulate("Found item %s from database %database \n" % (item, database))
        state.loc[item] = database[item]
    else:
        gui.Simulate("Database %database is down \n" % (item, database))

    state.NationalDatabase.ReleaseLock(item)
    state.loc.ReleaseLock(item)

'''
def Find_Method2(item):
    # search some local warehouse database
    gui.Simulate("Method not implemented")
    ape.do_command(fail)

def Find_Method3(item):
    # query a supplier of that item
    gui.Simulate("Method not implemented")
    ape.do_command(fail)
'''

# Refinement methods for pack

def Pack_Method1(item):
    r = ape.do_task('getRobot', loc(item))
    m = ape.do_task('getMachine', loc(item))
    ape.do_command('move', r, loc(item))
    ape.do_command('wrap', m, item)

# Refinement methods for getRobot
def GetRobot_Method1(l):
    # return the one which is nearest
    gui.Simulate("Method not implemented")
    ape.do_command(fail)

'''
def GetRobot_Method2(l):
    # return the one which is already going to l or nearby areas
    gui.Simulate("Method not implemented")
    ape.do_command(fail)

def GetRobot_Method3(l):
    # return the one which is free
    gui.Simulate("Method not implemented")
    ape.do_command(fail)
'''

# Refinement methods for deliver

def Deliver_Method1(item, l, type):
    if type == 'slow':
        '''Search for the transport that minimizes the cost:
                there can be multiple methods fo doing this
        '''
    elif type == 'fast':
        ''' Search for the fastest flight/ground transportation
        '''
    else:
        gui.Simulate("%s is an unsupported delivery type\n" % type)
        ape.do_command(fail)

rv = RV()
ape.declare_commands([lookupDB, fail])

ape.declare_methods('order', Order_Method1)
ape.declare_methods('find', Find_Method1)
ape.declare_methods('ape', Pack_Method1)
ape.declare_methods('getRobot', GetRobot_Method1)


from env_packageDelivery import *


