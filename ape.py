from __future__ import print_function
import threading
from state import State
import multiprocessing
import numpy
import random

"""
File rae1.py
Authors:
Dana Nau <nau@cs.umd.edu>, last update: July 7, 2017
Sunandita Patra <patras@cs.umd.edu>, last update: April 25, 2018
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


### for debugging

verbose = 0     

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

state = State()  # the global state of APE, this is shared by all stacks
apeLocals = rL_APE() # APE variables that are local to every stack
planLocals = rL_PLAN() # APEplan variables that are local to every stack
commands = {} # dictionary of commands, initialized once for every run via the domain file
commandSimulations = {} # dictionary of descriptive models of commands, initialized once for every run via the domain file
commandProb = {} # dictionary of probabilities of outcomes of commands, initialized once for every run via the domain file
listCommandsDependingOnParams = [] # list of commands whose descriptive models depend on the parameters
methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file
path = {} # global variable shared by all stacks for debugging

def ReinitializeState():   
    """
    State is reinitialized before every run, useful in batch runs
    """
    global state
    state = State()

def RemoveLocksFromState():
    """
    We get rid of all the locks in the simulated state used in APE-plan because we simulate only one stack.
    """
    state.ReleaseLocks()

############################################################
# Functions to tell Rae1 what the commands and methods are

def declare_commands(cmd_list, cmdSim_list):
    """
    Call this after defining the commands, to tell APE and APE-plan what they are.
    cmd_list must be a list of functions, not strings.
    """
    commands.update({cmd.__name__:cmd for cmd in cmd_list})
    for cmd in cmdSim_list:
        cmdParts = cmd.__name__.split('_')
        key = '_'.join(cmdParts[0:-1])
        commandSimulations[key] = cmd
    return commands

def declare_prob(cmd, pList):
    """
    Call this function to declare the probabities of the different outcomes in the descriptive models of commands.
    """
    commandProb[cmd] = pList

def UpdatePerceiveProb(comm, l, obj, newp):
    pList = commandProb[comm][l][obj]
    #print("Updated value is ", newp)
    commandProb[comm][l][obj] = [newp, 1 - newp]

def AddCommandToSpecialList(cmd):
    listCommandsDependingOnParams.append(cmd)

def GetCommand(cmd):
    """
        Get the actual operational model of the command or the descriptive model depending on whether we are in planning or acting mode
    """
    name = cmd.__name__
    if globals.GetPlanningMode() == True:
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
            p = multiprocessing.Process(target=testAPE.APEPlanMain, args=[self.task, self.taskArgs, None, queue, self.candidates])
            self.sem.release()
            p.start()
            p.join()

            resultTree, simTime = queue.get()
            #TODO: Update with new return value of testAPE.raeMultSimulator
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
    raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
    """

    apeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
    apeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
    apeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                         # This is a dictionary to accomodate for commands with different costs.

    taskArgs = raeArgs.taskArgs         

    global path                          # variable used for debugging
    path.update({apeLocals.GetStackId(): []})

    apeLocals.SetRefinementList(None)    # used in lazy and concurrent modes
    if globals.GetConcurrentMode() == True:
        apeLocals.SetConcManagerList([])  #concurrent manager keeps tracks of the threads in concurrent mode

    if verbose > 0:
        print('\n---- APE: Create stack {}, task {}{}\n'.format(apeLocals.GetStackId(), task, taskArgs))

    BeginCriticalRegion(apeLocals.GetStackId())

    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Initial state is:')
        print(state)

    try:
        retcode = do_task(task, *taskArgs)  # do acting

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(apeLocals.GetStackId(), path)
            print('Failed command {}'.format(e))
        retcode = 'Failure'

    except Failed_task as e:
        if verbose > 0:
            print_stack_size(apeLocals.GetStackId(), path)
            print('Failed task {}'.format(e))
        retcode = 'Failure'
    else:
        pass
    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Final state is:')
        print(state)

    if verbose > 0:
        print("\n---- APE: Done with stack %d\n" %apeLocals.GetStackId())

    EndCriticalRegion()
    return (retcode, apeLocals.GetRetryCount(), apeLocals.GetCommandCount())

def InitializeRollout():
    """
    This is a helper function for APEplan
    When APE-plan is called for the first time, some parameters need to be initialized. 
    """

    planLocals.SetDepth(0)         # start at depth 0 and go till depth d_max
    root = rTree.RTNode('root', 'root', 'root') # initialize the root of the refinement tree being built
    planLocals.SetCurrentNode(root)

def UpdateValueDict(valueDict, tree):
    """
    Helper function for APEplan
    """
    m = tree.GetMethod()
    if m not in valueDict:
        valueDict[m] = (0, None)

    if tree.GetCost() > 0:
        newVal = valueDict[m][0] + 1/tree.GetCost()
    else:
        newVal = float("inf")
    if valueDict[m][1] == None:
        newTree = tree
    else:
        newTree = valueDict[m][1]
        if newTree.GetCost() < tree.GetCost():
            newTree = tree
    valueDict[m] = (newVal, newTree)

def GetBestTree(valueDict):
    """
    Helper function for APEplan
    """
    bestValue = 0
    bestTree = None
    for m in valueDict:
        (value, tree) = valueDict[m]
        if value > bestValue:
            bestValue = value
            bestTree = tree
    return bestTree

def APEplan(task, planArgs):
    """
    APEplan is the planner used by APE which plans using the descriptive models of commands.
    The arguments of APEplan are same as APE.
    """

    planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is used to switch between 
                                                 # the main Simulation thread in testRAE.py and APEplan.
                                                 # This will be more useful if we decide to simulate multiple stacks in future
    taskArgs = planArgs.GetTaskArgs()
    
    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    valueDict = {}  # keeps track of the values of each method

    saved = state.copy() # need to save the state before doing a Monte-Carlo rollout

    for i in range(0, globals.GetSampleCount()):   
        """
        Do a rollout
        """
        if verbose > 0:
            print("Rollout ", i + 1)

        planLocals.SetCandidates(planArgs.GetCandidates())  # only methods from this set will be tried
        state.restore(saved)
        InitializeRollout()

        global path   # for debugging
        path.update({planLocals.GetStackId(): []})

        #BeginCriticalRegion(planLocals.GetStackId())  Not needed for now

        if verbose > 1:
            print_stack_size(planLocals.GetStackId(), path)
            print('Initial state is:')
            print(state)

        try:
            resultTreeRoot = PlanTask(task, taskArgs).GetChild()  # going GetChild because the root is just a node labelled 'root'
            UpdateValueDict(valueDict, resultTreeRoot) # update the value dictionary depending on the result of the rollout

        except Failed_command as e:
            if verbose > 0:
                print_stack_size(planLocals.GetStackId(), path)
                print('Failed command {}'.format(e))

        except Failed_task as e:
            if verbose > 0:
                print_stack_size(planLocals.GetStackId(), path)
                print('Failed task {}'.format(e))
        else:
            pass
        if verbose > 1:
            print_stack_size(planLocals.GetStackId(), path)
            print('Final state is:')
            print(state)

        if valueDict != {}:
            bestResultTree = GetBestTree(valueDict)
        else:
            bestResultTree = rTree.CreateFailureNode()

    #EndCriticalRegion()  Not needed for now
    return (bestResultTree, globalTimer.GetSimulationCounter())

def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    APE calls this functions when it wants suggestions from APE-plan
    """
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=testAPE.APEPlanMain, args=[task, taskArgs, queue, candidates])

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
        #resultTree.Print()
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
            return GetCandidateByPlanning(candidates, task, taskArgs)

            # the following else part is old and might be obsolete, it is for the lazy and concurrent modes of APE-plan
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
                return GetCandidateByPlanning(candidates, task, taskArgs)
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
    """
    This is incomplete.
    """
    result = globals.G()
    result.retcode = "Success"
    result.cost = 1
    result.method = task
    return result

def ChooseRandom(l):
    """
    This is a helper function used by PlanTask
    """
    random.shuffle(l)
    return l[0]

def PlanTask(task, taskArgs):

    if planLocals.GetCandidates() != None:
        # when candidates is a subset of the applicable methods, it is available from planLocals
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
    else:
        candidates = methods[task][:] # set of applicable methods

    m = ChooseRandom(candidates)
    return PlanMethod(m, task, taskArgs)

def PlanMethod(m, task, taskArgs):
    global path
    path[planLocals.GetStackId()].append([task, taskArgs])

    savedNode = planLocals.GetCurrentNode()
    newNode = rTree.RTNode(m, taskArgs, 'method')
    savedNode.AddChild(newNode)
    planLocals.SetCurrentNode(newNode)

    retcode = CallMethod(planLocals.GetStackId(), m, taskArgs)

    path[planLocals.GetStackId()].pop()
    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        newCost = savedNode.GetCost() + newNode.GetCost()
        savedNode.SetCost(newCost)
        planLocals.SetCurrentNode(savedNode)
        return savedNode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

def CallMethod(stackid, m, taskArgs):
    if verbose > 0:
        print_stack_size(stackid, path)
        print('Try method {}{}'.format(m.__name__,taskArgs))

    retcode = 'Failure'
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
        print('{} for method {}{}'.format(retcode, m.__name__, taskArgs))
    return retcode

def InitializeConcurrentSimulations(task, candidates, taskArgs):
    newManager = concLA(task, taskArgs, candidates)
    apeLocals.GetConcManagerList().append(newManager)

def StopConcurrentSimulations():
    currManager = apeLocals.GetConcManagerList()[-1]
    currManager.EndSimulations()
    apeLocals.GetConcManagerList.pop()

def DoTaskInRealWorld(task, taskArgs):
    """
    Acting engine
    """
    global path # for debugging
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
            retcode = CallMethod(apeLocals.GetStackId(), m, taskArgs)

    path[apeLocals.GetStackId()].pop()
    if globals.GetConcurrentMode() == True:
        StopConcurrentSimulations()

    if verbose > 1:
        print_entire_stack(apeLocals.GetStackId(), path)

    if retcode == 'Failure' or retcode == None:
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))

def do_task(task, *taskArgs):
    if globals.GetPlanningMode() == True:
        return PlanTask(task, taskArgs)
    else:
        return DoTaskInRealWorld(task, taskArgs)

def beginCommand(cmd, cmdRet, cmdArgs):
    cmdPtr = GetCommand(cmd)
    if globals.GetPlanningMode() == True:
        if cmd in listCommandsDependingOnParams:
            # this code is specific for sensing command, 'perceive'
            loc = cmdArgs[0]
            pDict = commandProb[cmd][loc]
            res = []
            for obj in pDict:
                outcome = numpy.random.choice(len(pDict[obj]), 1, p=pDict[obj])
                if outcome[0] == 0:
                    res.append(obj)
        else:
            p = commandProb[cmd]
            outcome = numpy.random.choice(len(p), 1, p=p)
            res = outcome[0]
        cmdArgs = cmdArgs + (res,)
    cmdRet['state'] = cmdPtr(*cmdArgs)

def do_command(cmd, *cmdArgs):
    """
    Perform command cmd(cmdArgs).
    """
    if globals.GetPlanningMode() == True:
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
        cost = 1
        planLocals.GetCurrentNode().IncreaseCost(cost)
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

import testAPE