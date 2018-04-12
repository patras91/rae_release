from __future__ import print_function
import threading
from state import State
import multiprocessing
import numpy
import random

"""
File rae1.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Sunandita Patra <patras@cs.umd.edu>, July 9, 2017
This has multiple execution stacks
"""

import sys, pprint
import os
import globals
import colorama
import rTree
from timer import globalTimer
from dataStructures import rL_APE, rL_PLAN
from APE_stack import print_entire_stack, print_stack_size
############################################################

### A goal is identical to a state except for the class name.
### I don't know if we'll need it or not, but it was trivial to write,
### and it might be useful if we want to reason about goals.

#class Goal():
 #   """A goal is just a collection of variable bindings."""
 #   def __init__(self):
 #       pass


### for debugging

verbose = 0
state = State()
apeLocals = rL_APE()
planLocals = rL_PLAN()
commands = {}
commandSimulations = {}
commandProb = {}
methods = {}
path = {}

def CleanState():
    global state
    state = State()

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
# Functions to tell Rae1 what the commands and methods are

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

def declare_prob(cmd, pList):
    commandProb[cmd] = pList

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
        return ((apeLocals.GetRefinementList() != None and apeLocals.GetRefinementList() != []) or (self.GetRefinementList() != None))

    def NoMethodApplicable(self):
        return ((apeLocals.GetRefinementList() == [] or apeLocals.GetRefinementList() == None) and (self.GetRefinementList() == []))

    def GetMethod(self):
        self.control = 'real'
        self.sem.acquire()

        if apeLocals.GetRefinementList() == None or apeLocals.GetRefinementList() == []:
            apeLocals.SetRefinementList(self.refinementList[:])
            self.refinementList = None

        chosen = apeLocals.GetRefinementList()[0].GetMethod()
        apeLocals.SetRefinementList(apeLocals.GetRefinementList()[1:])
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
            p = multiprocessing.Process(target=testRAE.APEPlanMain, args=[self.task, self.taskArgs, None, queue, self.candidates])
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

def CreateFailureNode():
    result = globals.G()
    result.retcode = 'Failure'
    result.method = None
    return result

def APE(task, raeArgs):
    """
    APE is the actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
    """

    apeLocals.SetStackId(raeArgs.stack)
    apeLocals.SetRetryCount(0)
    apeLocals.SetCommandCount({})

    taskArgs = raeArgs.taskArgs

    global path
    path.update({apeLocals.GetStackId(): []})

    apeLocals.SetRefinementList(None)
    if globals.GetConcurrentMode() == True:
        apeLocals.SetConcManagerList([])

    if verbose > 0:
        print('\n---- APE: Create stack {}, task {}{}\n'.format(apeLocals.GetStackId(), task, taskArgs))

    BeginCriticalRegion(apeLocals.GetStackId())

    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Initial state is:')
        print(state)

    try:
        result = do_task(task, *taskArgs)

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(apeLocals.GetStackId(), path)
            print('Failed command {}'.format(e))
        result = CreateFailureNode()

    except Failed_task as e:
        if verbose > 0:
            print_stack_size(apeLocals.GetStackId(), path)
            print('Failed task {}'.format(e))
        result = CreateFailureNode()
    else:
        pass
    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Final state is:')
        print(state)

    if verbose > 0:
        print("\n---- APE: Done with stack %d\n" %apeLocals.GetStackId())

    EndCriticalRegion()
    return (result, apeLocals.GetRetryCount(), apeLocals.GetCommandCount())

def InitializeSampling(m):
    planLocals.SetCandidates([m])
    planLocals.SetDepth(0)
    root = rTree.RTNode('root', 'root', 'root')
    planLocals.SetCurrentNode(root)

def APEplan(task, planArgs):

    planLocals.SetStackId(planArgs.GetStackId())
    taskArgs = planArgs.GetTaskArgs()

    globalTimer.ResetSimCounter()
    bestFailCount = globals.GetSampleCount() + 1

    saved = state.copy()
    for m in planArgs.GetCandidates():
        if verbose > 0:
            print("Method ", m.__name__)
        failCount = 0
        for i in range(0, globals.GetSampleCount()):
            if verbose > 0:
                print("Rollout ", i)

            state.restore(saved)
            InitializeSampling(m)
            global path
            path.update({planLocals.GetStackId(): []})

            #BeginCriticalRegion(planLocals.GetStackId())

            if verbose > 1:
                print_stack_size(planLocals.GetStackId(), path)
                print('Initial state is:')
                print(state)

            try:
                resultTreeRoot = PlanTask(task, taskArgs).GetChild()

            except Failed_command as e:
                if verbose > 0:
                    print_stack_size(planLocals.GetStackId(), path)
                    print('Failed command {}'.format(e))
                resultTreeRoot = rTree.CreateFailureNode()
                failCount += 1

            except Failed_task as e:
                if verbose > 0:
                    print_stack_size(planLocals.GetStackId(), path)
                    print('Failed task {}'.format(e))
                resultTreeRoot = rTree.CreateFailureNode()
                failCount += 1

            else:
                pass
            if verbose > 1:
                print_stack_size(planLocals.GetStackId(), path)
                print('Final state is:')
                print(state)

        if bestFailCount > failCount:
            bestFailCount = failCount
            bestResultTree = resultTreeRoot

    #EndCriticalRegion()
    return (bestResultTree, globalTimer.GetSimulationCounter())

def GetCandidateBySampling(candidates, task, taskArgs):
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=testRAE.APEPlanMain, args=[task, taskArgs, queue, candidates])

    p.start()
    p.join()

    resultTree, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    retcode = resultTree.GetRetcode()

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(retcode), colorama.Style.RESET_ALL)

    if retcode == 'Failure':
        #random.shuffle(candidates)
        return (candidates[0], candidates[1:])
    else:
        resultTree.Print()
        resultList = resultTree.GetPreorderTraversal()
        if apeLocals.GetRefinementList() == []:
            apeLocals.SetRefinementList(None)
        else:
            apeLocals.SetRefinementList(resultList[1:])
        m = resultList[0]
        candidates.pop(candidates.index(m))
        return (m, candidates)

def choose_candidate(candidates, task, taskArgs):

    if globals.GetDoSampling() == False:
        #random.shuffle(candidates)
        return(candidates[0], candidates[1:])

    elif globals.GetConcurrentMode() == False:
        if (apeLocals.GetRefinementList() == None or apeLocals.GetRefinementList() == [] or globals.GetLazy() == False):
            return GetCandidateBySampling(candidates, task, taskArgs)

        else:
            #print("candidates are ", candidates)
            #PrintList(raelocals.GetRefinementList())
            chosen = apeLocals.GetRefinementList()[0].method
            apeLocals.SetRefinementList(apeLocals.GetRefinementList()[1:])
            if chosen in candidates:
                candidates.pop(candidates.index(chosen))
                return (chosen, candidates)
            else:
                apeLocals.SetRefinementList(None)
                return GetCandidateBySampling(candidates, task, taskArgs)
    else:
        currManager = apeLocals.GetConcManagerList()[-1]
        while(currManager.Ready() == False):
            pass

        if currManager.NoMethodApplicable() == True:
            #random.shuffle(candidates)
            return (candidates[0], candidates[1:])
        else:
            chosen = currManager.GetMethod()
            candidates.pop(candidates.index(chosen))
            return (chosen, candidates)

def GetHeuristicEstimate(task, taskArgs):
    result = globals.G()
    result.retcode = "Success"
    result.cost = 1
    result.method = task
    return result

def ChooseRandom(l):
    random.shuffle(l)
    return l[0]

def PlanTask(task, taskArgs):

    if planLocals.GetCandidates() != None:
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None)
    else:
        candidates = methods[task][:]

    m = ChooseRandom(candidates)
    return PlanMethod(m, task, taskArgs)

def PlanMethod(m, task, taskArgs):
    global path
    path[planLocals.GetStackId()].append([task, taskArgs])

    savedNode = planLocals.GetCurrentNode()
    newNode = rTree.RTNode(m, taskArgs, 'method')
    savedNode.AddChild(newNode)
    planLocals.SetCurrentNode(newNode)

    result = CallMethod(planLocals.GetStackId(), m, taskArgs)
    retcode = result.retcode

    path[planLocals.GetStackId()].pop()
    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        planLocals.SetCurrentNode(savedNode)
        return savedNode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

def CallMethod(stackid, m, taskArgs):
    if verbose > 0:
        print_stack_size(stackid, path)
        print('Try method {}{}'.format(m.__name__,taskArgs))

    result = CreateFailureNode()
    result.cost = 0
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
    apeLocals.GetConcManagerList().append(newManager)

def StopConcurrentSimulations():
    currManager = apeLocals.GetConcManagerList()[-1]
    currManager.EndSimulations()
    apeLocals.GetConcManagerList.pop()

def DoTaskInRealWorld(task, taskArgs):
    global path
    path[apeLocals.GetStackId()].append([task, taskArgs])

    if verbose > 0:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Begin task {}{}'.format(task, taskArgs))

    if verbose > 1:
        print_entire_stack(apeLocals.GetStackId(), path)

    retcode = None
    candidates = methods[task][:]

    if globals.GetConcurrentMode() == True:
         InitializeConcurrentSimulations(task, methods[task][:], taskArgs)

    while (retcode != 'Success' and candidates != []):
        if retcode == 'Failure':
            apeLocals.SetRefinementList(None)
            apeLocals.SetRetryCount(apeLocals.GetRetryCount() + 1)
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        if m != None:
            result = CallMethod(apeLocals.GetStackId(), m, taskArgs)
            retcode = result.retcode

    path[apeLocals.GetStackId()].pop()
    if globals.GetConcurrentMode() == True:
        StopConcurrentSimulations()

    if verbose > 1:
        print_entire_stack(apeLocals.GetStackId(), path)

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
        return PlanTask(task, taskArgs)
    else:
        return DoTaskInRealWorld(task, taskArgs)

def beginCommand(cmd, cmdRet, cmdArgs):
    cmdPtr = GetCommand(cmd)
    if globals.GetSamplingMode() == True:
        p = commandProb[cmd]
        outcome = numpy.random.choice(len(p), 1, p=p)
        cmdArgs = cmdArgs + (outcome[0],)
    cmdRet['state'] = cmdPtr(*cmdArgs)

def do_command(cmd, *cmdArgs):
    """
    Perform command cmd(cmdArgs). Last arg must be the current state
    """
    if globals.GetSamplingMode() == True:
        return SimulateCommand(cmd, cmdArgs)
    else:
        return DoCommandInRealWorld(cmd, cmdArgs)

def DoCommandInRealWorld(cmd, cmdArgs):
    global path
    path[apeLocals.GetStackId()].append([cmd, cmdArgs])

    if verbose > 1:
        print_entire_stack(apeLocals.GetStackId(), path)

    if verbose > 0:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

    cmdRet = {'state':'running'}
    cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    cmdThread.start()
    if cmd.__name__ in apeLocals.GetCommandCount():
        apeLocals.GetCommandCount()[cmd.__name__] += 1
    else:
        apeLocals.GetCommandCount()[cmd.__name__] = 1

    EndCriticalRegion()
    BeginCriticalRegion(apeLocals.GetStackId())

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(apeLocals.GetStackId(), path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

        EndCriticalRegion()
        BeginCriticalRegion(apeLocals.GetStackId())

    if verbose > 0:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

    retcode = cmdRet['state']

    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(apeLocals.GetStackId(), path)
        print('Current state is')
        print(state)

    path[apeLocals.GetStackId()].pop()

    if verbose > 1:
        print_entire_stack(apeLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

def SimulateCommand(cmd, cmdArgs):
    global path
    path[planLocals.GetStackId()].append([cmd, cmdArgs])
    planLocals.SetDepth(planLocals.GetDepth() + 1)

    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if True:
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

        cmdRet = {'state':'running'}
        cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
        cmdThread.start()
        cost = 1

        EndCriticalRegion()
        BeginCriticalRegion(planLocals.GetStackId())

        while (cmdRet['state'] == 'running'):
            if verbose > 0:
                print_stack_size(planLocals.GetStackId(), path)
                print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
            EndCriticalRegion()
            BeginCriticalRegion(planLocals.GetStackId())

        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

        retcode = cmdRet['state']
    #else:
    #    retcode = GetHeuristicEstimate(cmd, cmdArgs)

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(planLocals.GetStackId(), path)
        print('Current state is')
        print(state)

    path[planLocals.GetStackId()].pop()
    planLocals.SetDepth(planLocals.GetDepth() - 1)

    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        planLocals.GetCurrentNode().IncreaseCost(cost)
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

import testRAE