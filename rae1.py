from __future__ import print_function
import types
import threading
from state import State
import multiprocessing

"""
File rae1.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Sunandita Patra <patras@cs.umd.edu>, July 9, 2017
This has multiple execution stacks
"""

import sys, pprint

import globals
import random
import colorama

############################################################

### A goal is identical to a state except for the class name.
### I don't know if we'll need it or not, but it was trivial to write,
### and it might be useful if we want to reason about goals.

class Goal():
    """A goal is just a collection of variable bindings."""
    def __init__(self):
        pass

def print_stack_size(stackid, path):
    stacksize = len(path[stackid])
    print(' stack {}.{}: '.format(stackid,stacksize),end=' '*stacksize)

def print_entire_stack(stackid, path):
    if len(path[stackid]) == 0:
        print(' stack {} = []\n'.format(stackid), end='')
        return

    print(' stack {} = ['.format(stackid), end='')
    punctuation = ', '
    for i in range(0,len(path[stackid])):
        (name,args) = path[stackid][i]
        if type(name) is types.FunctionType:
            name = name.__name__
        if i >= len(path[stackid]) - 1:
            punctuation = ']\n'
        print('{}{}'.format(name, args), end=punctuation)

### for debugging

verbose = 0
state = State()

def CleanState():
    state = State()

raelocals = threading.local()

def ResetState():
    state.ReleaseLocks()

def verbosity(level):
    """
    Specify how much debugging printout to produce:

    verbosity(0) makes Rae1 run silently; the only printout will be
    whatever the domain author has put into the commands and methods.

    verbosity(1) makes Rae1 print messages at the start and end, and
    print the name and args of each task and command.

    verbosity(2) makes Rae1 print a lot of stuff.
    """

    global verbose
    verbose = level

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True

def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None

############################################################
# Functions to tell Rae1 what the commands and methods are

commands = {}
commandSimulations = {}
methods = {}

def declare_commands(cmd_list, cmdSim_list):
    """
    Call this after defining the commands, to tell Rae1 what they are.
    cmd_list must be a list of functions, not strings.
    """
    commands.update({cmd.__name__:cmd for cmd in cmd_list})
    for cmd in cmdSim_list:
        cmdParts = cmd.__name__.split('_')
        key = '_'.join(cmdParts[0:-1])
        commandSimulations[key] = cmd
    return commands

def GetCommand(cmd):
    name = cmd.__name__
    if globals.GetSamplingMode() == True:
        return commandSimulations[name]
    else:
        return commands[name]

def declare_methods(task_name,*method_list):
    """
    Call this once for each task, to tell Rae1 what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

############################################################
# The user can use these to see what the commands and methods are.

def print_commands(olist=commands):
    """Print out the names of the commands"""
    print('commands:', ', '.join(olist))

def print_methods(mlist=methods):
    """Print out a table of what the methods are for each task"""
    print('{:<14}{}'.format('TASK:','METHODS:'))
    for task in mlist:
        print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

def PrintList(list):
    print('[')
    for item in list:
        print(item.method.__name__)
    print(']')
############################################################
# Stuff for debugging printout

path = {}

class Failed_command(Exception):
    pass

class Failed_task(Exception):
    pass

class Incorrect_return_code(Exception):
    pass

#****************************************************************
#Functions to control Progress of each stack step by step
class IpcArgs():
    """ IPCArgs is just a collection of variable bindings to share data among the threads."""
    def __init__(self):
        pass

ipcArgs = IpcArgs()
envArgs = IpcArgs()

def BeginCriticalRegion(stackid):
    while(ipcArgs.nextStack != stackid):
        pass
    ipcArgs.sem.acquire()

def EndCriticalRegion():
    ipcArgs.nextStack = 0
    ipcArgs.sem.release()

#****************************************************************

############################################################
# The actual acting engine

class concLA():
    def __init__(self, task, taskArgs, candidates, rList=None):
        self.sem = threading.Semaphore(1)
        self.refinementList = rList
        self.control = 'sim'
        self.task = task
        self.candidates = candidates
        self.taskArgs = taskArgs
        self.thread = threading.Thread(target=self.DoConcurrentSampling,args=[])
        self.thread.setDaemon(True)
        self.thread.start()

    def Ready(self):
        return (self.refinementList != None)

    def NoMethodApplicable(self):
        return (self.refinementList == [])

    def GetMethod(self):
        chosen = self.refinementList[0].method
        self.refinementList = self.refinementList[1:]
        self.control = 'real'
        self.sem.acquire()
        self.candidates.pop(self.candidates.index(chosen))
        self.control = 'sim'
        self.sem.release()
        return chosen

    def DoConcurrentSampling(self):
        while (True):
            if verbose > 0:
                print(colorama.Fore.RED, "Starting simulation for stack")

            queue = multiprocessing.Queue()
            while(self.control == 'real'):
                pass
            self.sem.acquire()
            p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[self.task, self.taskArgs, None, queue, self.candidates])
            self.sem.release()
            p.start()
            p.join()

            resultList = queue.get()
            result = resultList[0]

            if verbose > 0:
                print("Done with one concurrent simulation. Result = {} \n".format(result.retcode), colorama.Style.RESET_ALL)

            if result.retcode != 'Failure':
                self.refinementList = resultList[:]
            else:
                self.refinementList = []


def InitializeSampling(raeArgs):
    samplingMode = globals.GetSamplingMode()
    if samplingMode == True:
        raelocals.method = raeArgs.method
        raelocals.candidates = raeArgs.candidates
        raelocals.resultList = []
    return samplingMode

def rae1(task, raeArgs):
    """
    Rae1 is the Rae actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and args[0:-1] are the arguments for the task.
    The current stack is args[-1].
    """
    # To Sunandita: I think it's getting unwieldy to have multiple unnamed args at the end of
    # the arglist. Perhaps put them before the args variable and give them names? --Dana
    #
    # To Dana: Only using the stackid at the end now. Removed other arguments which consisted of state
    # and thread communication parameters. They are now global variables --Sunandita

    raelocals.stackid = raeArgs.stack
    raelocals.refinementList = None  # required for lazy lookahead
    taskArgs = raeArgs.taskArgs

    global path
    path.update({raelocals.stackid: []})

    samplingMode = InitializeSampling(raeArgs)

    if globals.GetConcurrentMode() == True:
        raelocals.conManagerList = []

    if verbose > 0:
        if samplingMode == False:
            print('\n---- Rae1: Create stack {}, task {}{}\n'.format(raelocals.stackid, task, taskArgs))

    BeginCriticalRegion(raelocals.stackid)

    if verbose > 1:
        print_stack_size(raelocals.stackid, path)
        print('Initial state is:')
        print(state)

    try:
        result = do_task(task, *taskArgs)
        if samplingMode == True:
            resultList = raelocals.resultList  # In sampling mode, we save a refinement list in resultList instead of just one result

    except Failed_command,e:
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Failed command {}'.format(e))
        result = globals.G()
        result.retcode = 'Failure'
        result.cost = float("inf")
        resultList = [result]
    except Failed_task, e:
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Failed task {}'.format(e))
        result = globals.G()
        result.retcode = 'Failure'
        result.cost = float("inf")
        resultList = [result]
    else:
        pass
    if verbose > 1:
        print_stack_size(raelocals.stackid, path)
        print('Final state is:')
        print(state)
    if verbose > 0:
        if samplingMode == False:
            print("\n---- Rae1: Done with stack %d\n" %raelocals.stackid)

    EndCriticalRegion()
    if samplingMode == True:
        return resultList
    else:
        return result

def GetCandidateBySampling(candidates, task, taskArgs):
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[task, taskArgs, None, queue, candidates])

    p.start()
    p.join()

    resultList = queue.get()

    raelocals.refinementList = resultList[1:]
    if raelocals.refinementList == []:
        raelocals.refinementList = None
    result = resultList[0]

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(result.retcode), colorama.Style.RESET_ALL)

    if result.retcode != 'Failure':
        m = result.method
        candidates.pop(candidates.index(m))
        return(m, candidates)
    else:
        return(None, [])

def choose_candidate(candidates, task, taskArgs):

    if globals.GetDoSampling() == False:
        return(candidates[0],candidates[1:])

    elif globals.GetConcurrentMode() == False:
        if (raelocals.refinementList == None) or (globals.GetLazy() == False):
            return GetCandidateBySampling(candidates, task, taskArgs)

        else:
            chosen = raelocals.refinementList[0].method
            raelocals.refinementList = raelocals.refinementList[1:]
            candidates.pop(candidates.index(chosen))
            return (chosen, candidates)

    else:
        currManager = raelocals.conManagerList[-1]
        while(currManager.Ready() == False):
            pass

        if currManager.NoMethodApplicable() == True:
            return (None, [])
        else:
            chosen = currManager.GetMethod()
            candidates.pop(candidates.index(chosen))
            return (chosen, candidates)

def SimulateTask(task, taskArgs):
    global path

    if raelocals.method != None:
        methodChosen = raelocals.method
        raelocals.method = None
    else:
        methodChosen = None

    # If a method has already been supplied
    if type(methodChosen) == types.FunctionType:
        path[raelocals.stackid].append([task, taskArgs])
        result = taskProgress(raelocals.stackid, path, methodChosen, taskArgs)
        retcode = result.retcode

        path[raelocals.stackid].pop()
        if verbose > 1:
            print_entire_stack(raelocals.stackid, path)

        if retcode == 'Failure':
            raise Failed_task('{}{}'.format(task, taskArgs))
        elif retcode == 'Success':
            raelocals.resultList = [result] + raelocals.resultList
            return result
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))
        #return result
    else:
    # need to choose from candidates which may already be supplied
        if raelocals.candidates != None:
            candidates = raelocals.candidates[:]
            raelocals.candidates = None
        else:
            candidates = methods[task][:]
        random.shuffle(candidates)
        candidates = candidates[0:min(len(candidates), globals.getK())]
        result = {}
        for m in candidates:
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[task, taskArgs, m, queue, None])
            p.start()
            p.join()
            resultList = queue.get()
            result[m.__name__] = resultList

        minCostMethod = candidates[0]
        for m_name in result:
            if result[m_name][0].retcode == 'Success' and result[m_name][0].cost < result[minCostMethod.__name__][0].cost:
                minCostMethod = result[m_name][0].method

        if result[minCostMethod.__name__][0].retcode == 'Failure':
            raise Failed_task('{}{}'.format(task, taskArgs))
        else:
            global state
            state.restore(result[minCostMethod.__name__][0].state)
            raelocals.resultList = result[minCostMethod.__name__] + raelocals.resultList
            return result[minCostMethod.__name__][0]

def taskProgress(stackid, path, m, taskArgs):
    if verbose > 0:
        print_stack_size(stackid, path)
        print('Try method {}{}'.format(m.__name__,taskArgs))

    result = globals.G()
    result.retcode = "Failure"
    result.cost = float("inf")
    result.state = state.copy()
    try:
        EndCriticalRegion()
        BeginCriticalRegion(stackid)
        if verbose > 0:
            print_stack_size(stackid, path)
            print("Executing method {}{}".format(m.__name__, taskArgs))
        if verbose > 1:
            print_stack_size(stackid, path)
            print('Current state is:'.format(stackid))
            print(state)

        retcode = m(*taskArgs)
        result.method = m
        result.retcode = retcode
        result.cost = 1
        result.state = state.copy()
    except Failed_command, e:
        if verbose > 0:
            print_stack_size(stackid, path)
            print('Failed command {}'.format(e))
    except Failed_task,e:
        if verbose > 0:
            print_stack_size(stackid, path)
            print('Failed task {}'.format(e))
    else:
        pass

    if verbose > 1:
        print_stack_size(stackid, path)
        print('{} for method {}{}'.format(result.retcode, m.__name__, taskArgs))
    return result

def InitializeConcurrentSimulations(task, candidates, taskArgs):
    newManager = concLA(task, taskArgs, candidates)
    raelocals.conManagerList.append(newManager)

def DoTaskInRealWorld(task, taskArgs):
    global path
    path[raelocals.stackid].append([task, taskArgs])

    if verbose > 0:
        print_stack_size(raelocals.stackid, path)
        print('Begin task {}{}'.format(task, taskArgs))

    if verbose > 1:
        print_entire_stack(raelocals.stackid, path)

    retcode = None
    candidates = methods[task][:]

    if globals.GetConcurrentMode() == True:
         InitializeConcurrentSimulations(task, methods[task][:], taskArgs)

    while (retcode != 'Success' and candidates != []):
        if retcode == 'Failure':
            raelocals.refinementList = None
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        if m != None:
            result = taskProgress(raelocals.stackid, path, m, taskArgs)
            retcode = result.retcode

    path[raelocals.stackid].pop()
    raelocals.conManagerList.pop()

    if verbose > 1:
        print_entire_stack(raelocals.stackid, path)

    if retcode == 'Failure' or retcode == None:
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        return result
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))

def do_task(task, *taskArgs):
    """
    This is the workhorse for rae1. The arguments are the same as for rae1.
    """
    if globals.GetSamplingMode() == True:
        return SimulateTask(task, taskArgs)
    else:
        return DoTaskInRealWorld(task, taskArgs)

def beginCommand(cmd, cmdRet, cmdArgs):
    cmd = GetCommand(cmd)
    cmdRet['state'] = cmd(*cmdArgs)

def do_command(cmd, *cmdArgs):
    """
    Perform command cmd(cmdArgs). Last arg must be the current state
    """
    global path
    path[raelocals.stackid].append([cmd, cmdArgs])

    if verbose > 1:
        print_entire_stack(raelocals.stackid, path)

    if verbose > 0:
        print_stack_size(raelocals.stackid, path)
        print('Begin command {}{}'.format(cmd.__name__,cmdArgs))

    cmdRet = {'state':'running'}
    cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    cmdThread.start()

    EndCriticalRegion()
    BeginCriticalRegion(raelocals.stackid)

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
        EndCriticalRegion()
        BeginCriticalRegion(raelocals.stackid)

    if verbose > 0:
        print_stack_size(raelocals.stackid, path)
        print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

    retcode = cmdRet['state']
    if verbose > 1:
        print_stack_size(raelocals.stackid, path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(raelocals.stackid, path)
        print('Current state is')
        print(state)

    path[raelocals.stackid].pop()
    if verbose > 1:
        print_entire_stack(raelocals.stackid, path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

import testRAE