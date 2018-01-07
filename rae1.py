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
import rTree
from timer import globalTimer
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
    if list == None:
        print('[ None ]')
    else:
        print('Refinement list: [', ' '.join(item.method.__name__ for item in list), ']')
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
    def __init__(self, task, taskArgs, candidates):
        self.sem = threading.Semaphore(1)
        self.refinementList = None
        self.control = 'sim'
        self.task = task
        self.candidates = candidates
        self.taskArgs = taskArgs
        self.thread = threading.Thread(target=self.DoConcurrentSampling,args=[])
        self.thread.setDaemon(True)
        self.thread.start()

    def Ready(self):
        return ((raelocals.refinementList != None and raelocals.refinementList != []) or (self.refinementList != None))

    def NoMethodApplicable(self):
        return ((raelocals.refinementList == [] or raelocals.refinementList == None) and (self.refinementList == []))

    def GetMethod(self):
        self.control = 'real'
        self.sem.acquire()

        if raelocals.refinementList == None or raelocals.refinementList == []:
            raelocals.refinementList = self.refinementList[:]
            self.refinementList = None

        chosen = raelocals.refinementList[0].method
        raelocals.refinementList = raelocals.refinementList[1:]
        self.candidates.pop(self.candidates.index(chosen))

        if self.candidates == []:
            self.refinementList = []
            self.control = 'exit'
        else:
            self.control = 'sim'
        self.sem.release()
        return chosen

    def DoConcurrentSampling(self):
        while (self.control != 'exit'):
            if verbose > 0:
                print(colorama.Fore.RED, "Starting simulation for stack")

            queue = multiprocessing.Queue()
            while(self.control == 'real'):
                pass
            self.sem.acquire()

            if self.control == 'exit':
                break
            p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[self.task, self.taskArgs, None, queue, self.candidates])
            self.sem.release()
            p.start()
            p.join()

            resultTree, simTime = queue.get()
            #TODO: Update with new return value of testRAE.raeMultSimulator
            globalTimer.UpdateSimCounter(simTime)

            resultList = resultTree.GetPreorderTraversal()
            result = resultList[0]

            if verbose > 0:
                print("Done with one concurrent simulation. Result = {} \n".format(result.retcode), colorama.Style.RESET_ALL)

            while(self.control == 'real'):
                pass
            self.sem.acquire()
            if result.retcode != 'Failure':
                if result.method not in self.candidates:
                    self.refinementList = None
                else:
                    self.refinementList = resultList[:]
            else:
                self.refinementList = []

            self.sem.release()

    def EndSimulations(self):
        self.refinementList = []
        self.control = 'exit'

def InitializeSampling(raeArgs):
    samplingMode = globals.GetSamplingMode()
    if samplingMode == True:
        globalTimer.ResetSimCounter()
        raelocals.method = raeArgs.method
        raelocals.candidates = raeArgs.candidates

        ncs = globals.G()
        ncs.node = rTree.RTNode('ROOT')
        ncs.state = state.copy()
        ncs.cost = 0
        raelocals.NCSList = [ncs] #NCS = Node Cost and State

    return samplingMode

def rae1(task, raeArgs):
    """
    Rae1 is the Rae actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
    """

    raelocals.stackid = raeArgs.stack
    raelocals.retryCount = 0
    raelocals.refinementList = None  # required for lazy lookahead and concurrent lookahead
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
            ncsList = raelocals.NCSList

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Failed command {}'.format(e))
        ncs = globals.G()
        result = globals.G()
        result.retcode = 'Failure'
        result.method = None
        ncs.node = rTree.RTNode(result)
        ncsList = [ncs]
    except Failed_task as e:
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Failed task {}'.format(e))
        ncs = globals.G()
        result = globals.G()
        result.retcode = 'Failure'
        result.method = None
        ncs.node = rTree.RTNode(result)
        ncsList = [ncs]
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
        return (ncsList, globalTimer.GetSimulationCounter())
    else:
        return (result, raelocals.retryCount)

def GetBest(ncsList):
    minCost = float('inf')
    retcode = 'Failure'
    best = None
    print(len(ncsList))
    for ncs in ncsList:
        if ncs.node.GetRetcode() == 'Success':
            print("\n")
            ncs.node.Print()
            if ncs.cost < minCost:
                best = ncs.node
                minCost = ncs.cost
                retcode = 'Success'
    return retcode, best


def GetCandidateBySampling(candidates, task, taskArgs):
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[task, taskArgs, None, queue, candidates])

    p.start()
    p.join()

    ncsList, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    retcode, resultTree = GetBest(ncsList)

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(retcode), colorama.Style.RESET_ALL)

    if retcode == 'Failure':
        random.shuffle(candidates)
        return (candidates[0], candidates[1:])
    else:
        resultList = resultTree.GetPreorderTraversal()
        if raelocals.refinementList == []:
            raelocals.refinementList = None
        else:
            raelocals.refinementList = resultList[1:]
        result = resultList[0]
        m = result.method
        candidates.pop(candidates.index(m))
        return (m, candidates)

def choose_candidate(candidates, task, taskArgs):

    if globals.GetDoSampling() == False:
        random.shuffle(candidates)
        return(candidates[0], candidates[1:])

    elif globals.GetConcurrentMode() == False:
        if (raelocals.refinementList == None or raelocals.refinementList == [] or globals.GetLazy() == False):
            return GetCandidateBySampling(candidates, task, taskArgs)

        else:
            #print("candidates are ", candidates)
            #PrintList(raelocals.refinementList)
            chosen = raelocals.refinementList[0].method
            raelocals.refinementList = raelocals.refinementList[1:]
            if chosen in candidates:
                candidates.pop(candidates.index(chosen))
                return (chosen, candidates)
            else:
                raelocals.refinementList = None
                return GetCandidateBySampling(candidates, task, taskArgs)
    else:
        currManager = raelocals.conManagerList[-1]
        while(currManager.Ready() == False):
            pass

        if currManager.NoMethodApplicable() == True:
            random.shuffle(candidates)
            return (candidates[0], candidates[1:])
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
        assert(len(raelocals.NCSList) == 1)
        raelocals.NCSList[0].node.UpdateDummy(methodChosen)
        result = taskProgress(raelocals.stackid, path, methodChosen, taskArgs)
        retcode = result.retcode

        path[raelocals.stackid].pop()
        if verbose > 1:
            print_entire_stack(raelocals.stackid, path)

        if retcode == 'Failure':
            raise Failed_task('{}{}'.format(task, taskArgs))
        elif retcode == 'Success':
            for ncs in raelocals.NCSList:
                ncs.node.Update(result)
                ncs.cost += 1
                global state
                ncs.state = state.copy()
            return result
        else:
            raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))
    else:
    # need to choose from candidates which may already be supplied
        if raelocals.candidates != None:
            candidates = raelocals.candidates[:]
            raelocals.candidates = None
        else:
            candidates = methods[task][:]
        random.shuffle(candidates)
        candidates = candidates[0:min(len(candidates), globals.getK())]
        failedTask = True

        nextNCSList = []
        for ncs in raelocals.NCSList: #NCS = Node Cost State
            for m in candidates:
                state.restore(ncs.state)
                queue = multiprocessing.Queue()
                p = multiprocessing.Process(target=testRAE.raeMultSimulator, args=[task, taskArgs, m, queue, None])
                p.start()
                p.join()
                ncsListAfterSampling, simTime = queue.get()
                globalTimer.UpdateSimCounter(simTime)

                for ncsAfterSampling in ncsListAfterSampling:
                    if ncsAfterSampling.node.GetRetcode() == 'Success':
                        failedTask = False

                        newNode = ncs.node.Duplicate()
                        if newNode.value == 'ROOT':
                            newNode = ncsAfterSampling.node
                        else:
                            newNode.AddChild(ncsAfterSampling.node)

                        newNCS = globals.G()
                        newNCS.node = newNode
                        newNCS.cost = ncs.cost + ncsAfterSampling.cost
                        newNCS.state = ncsAfterSampling.state

                        nextNCSList.append(newNCS)

        if failedTask == True:
            raise Failed_task('{}{}'.format(task, taskArgs))
        else:
            raelocals.NCSList = nextNCSList
            return raelocals.NCSList

def taskProgress(stackid, path, m, taskArgs):
    if verbose > 0:
        print_stack_size(stackid, path)
        print('Try method {}{}'.format(m.__name__,taskArgs))

    result = globals.G()
    result.retcode = "Failure"
    result.method = None
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
        result.state = state.copy()
    except Failed_command as e:
        if verbose > 0:
            print_stack_size(stackid, path)
            print('Failed command {}'.format(e))
    except Failed_task as e:
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

def StopConcurrentSimulations():
    currManager = raelocals.conManagerList[-1]
    currManager.EndSimulations()
    raelocals.conManagerList.pop()

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
            raelocals.retryCount += 1
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        if m != None:
            result = taskProgress(raelocals.stackid, path, m, taskArgs)
            retcode = result.retcode

    path[raelocals.stackid].pop()
    if globals.GetConcurrentMode() == True:
        StopConcurrentSimulations()

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
    cost = 0

    EndCriticalRegion()
    BeginCriticalRegion(raelocals.stackid)

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(raelocals.stackid, path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
        cost += 1
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
        if globals.GetSamplingMode() == True:
            raelocals.NCSList[0].cost = float('inf')
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        if globals.GetSamplingMode() == True:
            raelocals.NCSList[0].cost += cost
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

import testRAE