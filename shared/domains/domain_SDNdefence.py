__author__ = 'patras'

'''Domain to defend against SDN attacks.'''

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as alg
import gui
from state import state
from timer import globalTimer
import globals

def fail():
    return FAILURE

def turnOnSwitch(s):
    state.status.AcquireLock(s) # Several parallel tasks are running that share the states
                                # So, we need locks before changing the value of a variable
    if state.status[s] == 'off':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('turnOnSwitch', start) == False):
            pass
        res = Sense('turnOnSwitch') # Description of Sense is in the file env_SDNdefence.py
        if res == SUCCESS:
            gui.Simulate("Switch %s has been switch on.\n" %s)
            state.status[s] = 'on'
        else:
            gui.Simulate("Non-deterministic event has made the turnOnSwitch command fail\n")
    else:
        gui.Simulate("Switch %s is already on.\n" %s)
        res = SUCCESS
    state.status.ReleaseLock(s)
    return res

def turnOffSwitch(s):
    state.status.AcquireLock(s)
    if state.status[s] == 'on':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('turnOffSwitch', start) == False):
            pass
        res = Sense('turnOffSwitch') # Description of Sense is in the file env_SDNdefence.py
        if res == SUCCESS:
            gui.Simulate("Switch %s has been switch off.\n" %s)
            state.status[s] = 'off'
        else:
            gui.Simulate("Non-deterministic event has made the turnOffSwitch command fail\n")
    else:
        gui.Simulate("Switch %s is already off.\n" %s)
        res = SUCCESS
    state.status.ReleaseLock(s)
    return res

def turnOnComponent(c):
    state.status.AcquireLock(c) # Several parallel tasks are running that share the states
                                # So, we need locks before changing the value of a variable
    if state.status[c] == 'off':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('turnOnComponent', start) == False):
            pass
        res = Sense('turnOnComponent') # Description of Sense is in the file env_SDNdefence.py
        if res == SUCCESS:
            gui.Simulate("Component %s has been turned on.\n" %c)
            state.status[c] = 'on'
        else:
            gui.Simulate("Non-deterministic event has made the turnOnComponent command fail\n")
    else:
        gui.Simulate("Switch %s is already on.\n" %c)
        res = SUCCESS
    state.status.ReleaseLock(c)
    return res

def turnOffComponent(c):
    state.status.AcquireLock(c)
    if state.status[c] == 'on':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('turnOffComponent', start) == False):
            pass
        res = Sense('turnOffComponent') # Description of Sense is in the file env_SDNdefence.py
        if res == SUCCESS:
            gui.Simulate("Component %s has been turned off.\n" %c)
            state.status[c] = 'off'
        else:
            gui.Simulate("Non-deterministic event has made the turnOffComponent command fail\n")
    else:
        gui.Simulate("Component %s is already off.\n" %c)
        res = SUCCESS
    state.status.ReleaseLock(c)
    return res

def disconnect(plug):
    gui.Simulate("Plug %s is removed.\n" %plug)
    return SUCCESS

def Defend_Method1(network):
    for s in rv.SWITCHES[network]:
        if state.status[s] == 'on':
            alg.do_command(turnOffSwitch, s)
            alg.do_command(turnOnSwitch, s)

def Defend_Method2(network):
    alg.do_task('shutdown', network)

def Shutdown_Method1(network):
    for component in rv.COMPONENTS[network]:
        if state.status[component] == 'on':
            alg.do_command(turnOffComponent, component)

def Shutdown_Method2(network):
    plug = state.powerSource[network]
    alg.do_command(disconnect, plug)

rv = RV() # The rigid variables that never change

# the commandss
alg.declare_commands([
    turnOnSwitch,
    turnOffSwitch,
    turnOnComponent,
    turnOffComponent,
    disconnect,
    fail])

# the refinement methods for the tasks

alg.declare_methods('defend', 
    Defend_Method1, 
    Defend_Method2)

alg.declare_methods('shutdown', 
    Shutdown_Method1, 
    Shutdown_Method2)

from env_SDNdefence import *