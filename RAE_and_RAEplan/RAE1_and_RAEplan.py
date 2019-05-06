from __future__ import print_function

"""
File RAE1_and_RAEplan.py
Author:
Sunandita Patra <patras@cs.umd.edu>
"""

import threading
from state import GetState, PrintState, RestoreState, EvaluateParameters
import multiprocessing
import numpy
import random
from helper_functions import *
import types
import sys, pprint
import os
import GLOBALS
import colorama
import rTree
from timer import globalTimer, DURATION
from dataStructures import rL_APE, rL_PLAN
from APE_stack import print_entire_stack, print_stack_size
############################################################

### for debugging

verbose = 0     

def verbosity(level):
    """
    Specify how much debugging printout to produce:

    verbosity(0) makes RAE1 and RAEplan run silently; the only printout will be
    whatever the domain author has put into the commands and methods.

    verbosity(1) prints messages at the start and end, and
    print the name and args of each task and command.

    verbosity(2) makes RAE1 and RAEplan also print the states after executing commands.
    """

    global verbose
    verbose = level

# Both RAE and RAEplan
TASKS = {} # dictionary of tasknames and the task parameters

methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file
path = {} # global variable shared by all stacks for debugging

# Only RAE1
commands = {} # dictionary of commands, initialized once for every run via the domain file
raeLocals = rL_APE() # APE variables that are local to every stack

#only RAEplan
planLocals = rL_PLAN() # APEplan_systematic variables that are local to every call to APEplan_systematic, 
                       # we need this to be thread local because we have multiple stacks in APE as 
                       # multiple threads and each thread call its own APEplan_systematic
heuristic = {}

############################################################
# Functions to tell Rae1 what the commands and methods are

def declare_commands(cmd_list):
    """
    Call this after defining the commands, to tell APE and APE-plan what they are.
    cmd_list must be a list of functions, not strings.
    """
    commands.update({cmd.__name__:cmd for cmd in cmd_list})
    return commands

def GetCommand(cmd):
    """
        Get the actual operational model of the command 
    """
    name = cmd.__name__
    return commands[name]

class MethodInstance():
    def __init__(self, m):
        self.method = m
        self.params = None

    def SetParams(self, p):
        self.params = p

    def Call(self):
        self.method(*self.params)

    def GetName(self):
        return self.method.__name__

    def __repr__(self):
        return self.method.__name__ + str(self.params) 

    def __eq__(self, other):
        if other == 'heuristic' or other == 'Failure' or other == None:
            return False
        else:
            return self.method == other.method and self.params == other.params

def declare_task(t, *args):
    TASKS[t] = args

# declares the refinement methods for a task;
# ensuring that some constraints are satisfied
def declare_methods(task_name, *method_list):

    taskArgs = TASKS[task_name]
    q = len(taskArgs)
    
    methods[task_name] = []
    for m in method_list:

        variableArgs = False
        if len(taskArgs) == 1:
            if taskArgs[0] == "*":
                variableArgs = True
        if variableArgs != True:
            # ensure that the method has atleast as many parameters as the task
            assert(m.__code__.co_argcount >= q)
            
            # ensure that the variable names of the 
            # first q parameters of m match with the parameters of task t
            assert(m.__code__.co_varnames[0:q] == taskArgs)

        methods[task_name].append(m)

#def declare_methods(task_name, *method_list):
    """
    Call this once for each task, to tell Rae1 what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
#    methods.update({task_name:list(method_list)})
#    return methods[task_name]

def GetMethodInstances(methods, tArgs):
    
    instanceList = [] # List of all applicable method instances for t

    for m in methods:

        q = m.__code__.co_argcount
        mArgs = m.__code__.co_varnames
        
        if len(tArgs) < q:
            # some parameters are uninstantiated
            paramList = EvaluateParameters(m.parameters, mArgs, tArgs)
            
            for params in paramList:
                instance = MethodInstance(m)
                instance.SetParams(tArgs + params)
                instanceList.append(instance)
        else:
            instance = MethodInstance(m)
            instance.SetParams(tArgs)
            instanceList.append(instance)

    return instanceList 

def declare_heuristic(task, name):
    heuristic[task] = name
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


############################################################
# Stuff for debugging printout

class Failed_command(Exception):
    pass

class Failed_Rollout(Exception):
    pass

class Failed_task(Exception):
    pass

class Incorrect_return_code(Exception):
    pass

class Search_Done(Exception):
    pass

class DepthLimitReached(Exception):
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

def RAE1(task, raeArgs):
    """
    RAE1 is the actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
    raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
    """
    InitializeStackLocals(task, raeArgs)

    global path                          # variable used for debugging
    path.update({raeLocals.GetStackId(): []})

    if verbose > 0:
        print('\n---- APE: Create stack {}, task {}{}\n'.format(raeLocals.GetStackId(), task, raeArgs.taskArgs))

    BeginCriticalRegion(raeLocals.GetStackId())

    if verbose > 1:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    try:
        taskArgs = raeArgs.taskArgs 
        retcode = do_task(task, *taskArgs)  # do acting

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(raeLocals.GetStackId(), path)
            print('Failed command {}'.format(e))
        retcode = 'Failure'

    except Failed_task as e:
        if verbose > 0:
            print_stack_size(raeLocals.GetStackId(), path)
            print('Failed task {}'.format(e))
        retcode = 'Failure'
    else:
        pass
    if verbose > 1:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    if verbose > 0:
        print("\n---- APE: Done with stack %d\n" %raeLocals.GetStackId())

    EndCriticalRegion()

    if retcode == 'Failure':
        raeLocals.SetEfficiency(0)

    #raeLocals.GetActingTree().PrintUsingGraphviz()
    return (retcode, raeLocals.GetRetryCount(), raeLocals.GetEfficiency())

def InitializeStackLocals(task, raeArgs):
    """ Initialize the local variables of a stack used during acting """
    raeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
    raeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
    raeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                         # This is a dictionary to accomodate for commands with different costs.
    raeLocals.SetMainTask(task)
    raeLocals.SetMainTaskArgs(raeArgs.taskArgs)

    aT = rTree.ActingTree()
    aT.SetPrevState(GetState().copy())
    raeLocals.SetActingTree(aT)
    raeLocals.SetEfficiency(float("inf"))
    
def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    APE calls this functions when it wants suggestions from APE-plan
    """
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    actingTree = raeLocals.GetActingTree()

    p = multiprocessing.Process(
        target=RAE.RAEPlanMain, 
        args=[raeLocals.GetMainTask(), 
        raeLocals.GetMainTaskArgs(), 
        queue, 
        candidates,
        GetState().copy(),
        raeLocals.GetGuideList(),
        raeLocals.GetSearchTree()])

    p.start()
    p.join()

    methodInstance, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    #retcode = plannedTree.GetRetcode()

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(methodInstance), colorama.Style.RESET_ALL)

    if methodInstance == 'Failure':
        #random.shuffle(candidates)
        return (candidates[0], candidates[1:])
    else:
        #plannedTreeFlat = plannedTree.GetPreorderTraversal()
        #indexToLook = actingTree.GetSize() - 2
        #m = plannedTreeFlat[indexToLook]
        candidates.pop(candidates.index(methodInstance))
        return (methodInstance, candidates)

def choose_candidate(candidates, task, taskArgs):
    if GLOBALS.GetDoPlanning() == False or len(candidates) == 1:
        #random.shuffle(candidates)
        return(candidates[0], candidates[1:])
    else:
        return GetCandidateByPlanning(candidates, task, taskArgs)

def DoTaskInRealWorld(task, taskArgs):
    """
    Function to do the task in real world
    """
    PushToPath(task, taskArgs)
    v_begin(task, taskArgs)

    retcode = 'Failure'
    candidateMethods = methods[task][:]
    candidates = GetMethodInstances(candidateMethods, taskArgs)
    if candidates == []:
        raise Failed_task('{}{}'.format(task, taskArgs))

    parent, node = raeLocals.GetCurrentNodes()

    while (retcode != 'Success'):

        node.Clear() # Clear it on every iteration for a fresh start
        node.SetPrevState(GetState().copy())

        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        node.SetLabelAndType(m, 'method')
        raeLocals.SetCurrentNode(node)
        retcode = CallMethod_OperationalModel(raeLocals.GetStackId(), m, taskArgs)

        if candidates == []:
            break

        if retcode == 'Failure':
            raeLocals.SetRetryCount(raeLocals.GetRetryCount() + 1)

    raeLocals.SetCurrentNode(parent)
    path[raeLocals.GetStackId()].pop()

    v_path()

    if retcode == 'Failure':
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))

def CallMethod_OperationalModel(stackid, m, taskArgs):
    if verbose > 0:
        print_stack_size(stackid, path)
        print('Try method {}{}'.format(m.GetName(),taskArgs))

    retcode = 'Failure'
    try:
        if GLOBALS.GetPlanningMode() == False:
            EndCriticalRegion()
            BeginCriticalRegion(stackid)
            node = raeLocals.GetCurrentNode()
            node.SetPrevState(GetState().copy())

        if verbose > 0:
            print_stack_size(stackid, path)
            print("Executing method {}{}".format(m.GetName(), taskArgs))
        if verbose > 1:
            print_stack_size(stackid, path)
            print('Current state is:'.format(stackid))
            PrintState()

        m.Call()  # This is the main job of this function, CallMethod
        retcode = 'Success'
    except Failed_command as e:
        if verbose > 0:
            print_stack_size(stackid, path)
            print('Failed command {}'.format(e))
    except Failed_task as e:
        if verbose > 0:
            print_stack_size(stackid, path)
            print('Failed task {}'.format(e))

    if verbose > 1:
        print_stack_size(stackid, path)
        print('{} for method {}{}'.format(retcode, m.GetName(), taskArgs))

    return retcode

def do_task(task, *taskArgs):
    if GLOBALS.GetPlanningMode() == True:
        planLocals.IncreaseDepthBy1()
        nextNode = planLocals.GetSearchTreeNode().GetNext()
        if nextNode != None:
            assert(nextNode.GetType() == "task" or nextNode.GetType() == "heuristic")
            return FollowSearchTree_task(task, taskArgs, nextNode)
        else:
            return PlanTask(task, taskArgs)
    else:
        return DoTaskInRealWorld(task, taskArgs)

def InitializePlanningTree():
    root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
    planLocals.SetCurrentNode(root)
    planLocals.SetPlanningTree(root)
    #planLocals.SetBestTree(None)

def RAEplanChoice(task, planArgs):
    """
    RAEplanChoice is the main routine of the planner used by RAE which plans using the available operational models
    """

    #planLocals is the set of variables local to this call to RAEplanChoice but used throughout
    planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is not important.
                                                 # This will be useful if we decide to simulate multiple stacks in future.
    planLocals.SetCandidates(planArgs.GetCandidates())
    planLocals.SetState(planArgs.GetState())

    taskArgs = planArgs.GetTaskArgs()
    planLocals.SetHeuristicArgs(task, taskArgs)
    planLocals.SetDepth(0)
    planLocals.SetRefDepth(float("inf"))

    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    #gL = planArgs.GetGuideList()
    #planLocals.SetGuideList(gL) # which is basically the stack in the pseudocode
    #RestoreState(gL.GetStartState())

    searchTreeRoot = planArgs.GetSearchTree()
    planLocals.SetSearchTreeRoot(searchTreeRoot)
    #planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())

    global path   # for debugging
    path.update({planLocals.GetStackId(): []})
        
    InitializePlanningTree()

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    while (searchTreeRoot.GetSearchDone() == False):
        try:
            planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
            do_task(task, *taskArgs) 
            #if planLocals.GetBestTree() != None:
            #    plannedTree = planLocals.GetBestTree().GetChild() # doing GetChild because the root is just a node labelled 'root'
            #else:
            #    plannedTree = rTree.CreateFailureNode()
            searchTreeRoot.UpdateChildPointers()    
        except Failed_Rollout as e:
            v_failedCommand(e)
            #plannedTree = rTree.CreateFailureNode()
            searchTreeRoot.UpdateChildPointers()
        except Failed_task as e:
            v_failedTask(e)
            #plannedTree = rTree.CreateFailureNode()

        except DepthLimitReached as e:
            searchTreeRoot.UpdateChildPointers()
        except Search_Done as e:
            #searchTreeRoot.PrintUsingGraphviz()
            #if planLocals.GetBestTree() != None:
            #    plannedTree = planLocals.GetBestTree().GetChild() # doing GetChild because the root is just a node labelled 'root'
            #else:
            #    plannedTree = rTree.CreateFailureNode()
            pass
        else:
            pass

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    taskToRefine = planLocals.GetTaskToRefine()

    return (taskToRefine.GetBestMethod(), globalTimer.GetSimulationCounter())
    
def GetCandidates(task, tArgs):
    """ Called from PlanTask """
    if planLocals.GetCandidates() != None:
        # when candidates is a subset of the applicable methods, it is available from planLocals
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
        prevState = planLocals.GetState()
        flag = 1
    else:
        candidateMethods = methods[task][:] # set of applicable methods
        candidates = GetMethodInstances(candidateMethods, tArgs)
        prevState = GetState()
        flag = 0
        
    b = GLOBALS.Getb()
    cand = candidates[0:min(b, len(candidates))]
    return cand, prevState, flag

def FollowSearchTree_task(task, taskArgs, node):
    nextNode = node.GetNext()
    m = nextNode.GetLabel()
    if m == 'heuristic':
        raise DepthLimitReached()
    else:
        RestoreState(nextNode.GetPrevState())
        planLocals.SetSearchTreeNode(nextNode)
        tree = PlanMethod(m, task, taskArgs)
        return tree

def Reinitialize(m, s, newNode, guideList, name, args):
    guideList.RemoveAllAfter(newNode)
    if m == 'command':
        newNode.SetLabel(name)
        newNode.SetCost(GetCost(name, args))
        newNode.SetNextState(s)
    else:
        newNode.SetLabel(m)
        newNode.SetPrevState(s)
    
    pRoot = planLocals.GetPlanningTree()
    if pRoot.children == []:
        firstTask = name
        firstTaskArgs = args
    else:
        firstTask = pRoot.GetChild().GetLabel()
        firstTaskArgs = pRoot.GetChild().GetArgs()
    
    pRoot.DeleteAllChildren()
    planLocals.SetCurrentNode(pRoot)
    guideList.ResetPtr()
        
    startState = guideList.GetStartState()
    RestoreState(startState)

    return firstTask, firstTaskArgs, pRoot

def GetBestEff():
    """ Helper function for PlanTask """
    bestTree = planLocals.GetBestTree()
    if bestTree != None:
        bestEff = bestTree.GetEff()
    else:
        bestEff = 0
    return bestEff

def GetHeuristicEstimate():
    task, args = planLocals.GetHeuristicArgs()
    return heuristic[task](args)
    
def PlanTask(task, taskArgs):
    # Need to look through several candidates for this task
    cand, state, flag = GetCandidates(task, taskArgs)

    #guideList = planLocals.GetGuideList()
    searchTreeNode = planLocals.GetSearchTreeNode()
    taskNode = rTree.SearchTreeNode('task', 'task')
    searchTreeNode.AddChild(taskNode)
    if flag == 1:
        planLocals.SetTaskToRefine(taskNode)
        planLocals.SetRefDepth(planLocals.GetDepth())
    # Pruning here if efficiency is already lower
    #currEff = guideList.GetEff()
    #if currEff <= GetBestEff():
    #    raise Failed_task('{}{}'.format(task, taskArgs))

    #newNode = guideList.append()

    if planLocals.GetRefDepth() + GLOBALS.GetSearchDepth() <= planLocals.GetDepth():
        #print("here", planLocals.GetRefDepth() + globals.GetSearchDepth(),planLocals.GetDepth() )
        newNode = rTree.SearchTreeNode('heuristic', 'heuristic')

        newNode.SetEff(GetHeuristicEstimate())
        taskNode.AddChild(newNode)
        raise Search_Done()

    for m in cand:
        newSearchTreeNode = rTree.SearchTreeNode(m, 'method')
        newSearchTreeNode.SetPrevState(state)
        taskNode.AddChild(newSearchTreeNode)
    raise Search_Done()
        #firstTask, firstTaskArgs, pRoot = Reinitialize(m, state, newNode, guideList, task, taskArgs)
        #try:
            #do_task(firstTask, *firstTaskArgs) # to recreate the execution stack
            #tree = pRoot
            #assert(planLocals.GetCurrentNode() == pRoot)
            
            #bestEff = GetBestEff()

            #if tree.GetEff() > bestEff:
            #    planLocals.SetBestTree(tree.copy())
        #except Failed_task:
        #    planLocals.SetCurrentNode(pRoot)
        #except Search_Done:
        #    pass

    #raise Search_Done()

def PlanMethod(m, task, taskArgs):
    global path
    #path[planLocals.GetStackId()].append([task, taskArgs])
    savedNode = planLocals.GetCurrentNode()
    
    newNode = rTree.PlanningTree(m, taskArgs, 'method')
    savedNode.AddChild(newNode)
    planLocals.SetCurrentNode(newNode)

    retcode = CallMethod_OperationalModel(planLocals.GetStackId(), m, taskArgs)

    #path[planLocals.GetStackId()].pop()
    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        eff = float("inf")
        for child in savedNode.children:
            eff = addEfficiency(eff, child.GetEff())
        savedNode.SetEff(eff)
        planLocals.SetCurrentNode(savedNode)

        return planLocals.GetPlanningTree()
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

def beginCommand(cmd, cmdRet, cmdArgs):
    cmdPtr = GetCommand(cmd)
    cmdRet['state'] = cmdPtr(*cmdArgs)

def do_command(cmd, *cmdArgs):
    """
    Perform command cmd(cmdArgs).
    """
    if GLOBALS.GetPlanningMode() == True:
        planLocals.IncreaseDepthBy1()
        nextNode = planLocals.GetSearchTreeNode().GetNext()
        if nextNode == None:
            return PlanCommand(cmd, cmdArgs)
        else:
            assert(nextNode.GetType() == "command")
            return FollowSearchTree_command(cmd, cmdArgs, nextNode)
    else:
        return DoCommandInRealWorld(cmd, cmdArgs)

def DoCommandInRealWorld(cmd, cmdArgs):
    global path
    path[raeLocals.GetStackId()].append([cmd, cmdArgs])

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

    cmdRet = {'state':'running'}
    cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    cmdThread.start()
    if cmd.__name__ in raeLocals.GetCommandCount():
        raeLocals.GetCommandCount()[cmd.__name__] += 1
    else:
        raeLocals.GetCommandCount()[cmd.__name__] = 1

    EndCriticalRegion()
    BeginCriticalRegion(raeLocals.GetStackId())

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(raeLocals.GetStackId(), path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

        EndCriticalRegion()
        BeginCriticalRegion(raeLocals.GetStackId())

    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

    retcode = cmdRet['state']

    par, cmdNode = raeLocals.GetCurrentNodes()

    cmdNode.SetLabelAndType(cmd, 'command', cmdArgs)
    cmdNode.SetNextState(GetState().copy())

    if verbose > 1:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format(cmd.__name__, cmdArgs, retcode))
        print_stack_size(raeLocals.GetStackId(), path)
        print('Current state is')
        PrintState()

    path[raeLocals.GetStackId()].pop()

    if cmd.__name__ == "fail":
        cost = 20
    else:
        cost = GetCost(cmd, cmdArgs)
    eff = raeLocals.GetEfficiency()
    raeLocals.SetEfficiency(addEfficiency(eff, 1/cost))

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

def FollowSearchTree_command(cmd, cmdArgs, searchNode):
    #planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
    assert(cmd == searchNode.GetLabel())
    stateNode = searchNode.GetNext()
    RestoreState(stateNode.GetLabel())
    planLocals.SetSearchTreeNode(stateNode)

    if stateNode.GetEff() != 0:
        cost = GetCost(cmd, cmdArgs)
        stateNode.SetEff(1/cost)
        newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
        planLocals.GetCurrentNode().AddChild(newNode)
        planLocals.GetCurrentNode().AddEfficiency(1/cost)
        return 'Success'
    else:
        raise Failed_Rollout('{}{}'.format(cmd.__name__, cmdArgs))

def CallCommand_OperationalModel(cmd, cmdArgs):
    global path
    v_path()
    v_begin_c(cmd, cmdArgs)
    path[planLocals.GetStackId()].append([cmd, cmdArgs])
    cmdRet = {'state':'running'}
    cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    cmdThread.start()

    if GLOBALS.GetPlanningMode() == False:
        EndCriticalRegion()
        BeginCriticalRegion(planLocals.GetStackId())

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
        if GLOBALS.GetPlanningMode() == False:
            EndCriticalRegion()
            BeginCriticalRegion(planLocals.GetStackId())

    if verbose > 0:
        print_stack_size(planLocals.GetStackId(), path)
        print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

    retcode = cmdRet['state']
    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(planLocals.GetStackId(), path)
        print('Current state is')
        PrintState()

    path[planLocals.GetStackId()].pop()
    v_path()

    return retcode

def IndexOf(s, l):
    """ Helper function of PlanCommand """
    i = 0
    for item in l:
        if item.EqualTo(s):
            return i
        i += 1 
    return -1

def PlanCommand(cmd, cmdArgs):
    #savedState = GetState().copy()
    #gL = planLocals.GetGuideList()
    #newNode = gL.append()
    #effList = []

    outcomeStates = []
    #effs = []

    searchTreeNode = planLocals.GetSearchTreeNode()
    prevState = GetState().copy()
    newCommandNode = rTree.SearchTreeNode(cmd, 'command')
    searchTreeNode.AddChild(newCommandNode)

    for i in range(0, GLOBALS.Getk()):
        RestoreState(prevState)
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        nextState = GetState().copy()

        if retcode == 'Failure':
            newNode = rTree.SearchTreeNode(nextState, 'state')
            newNode.SetEff(0)
            newNode.SetPrevState(prevState)
            newCommandNode.AddChild(newNode)
            outcomeStates.append(nextState)
            #effList.append(0)
            # No need to plan any further, it will always be 0
        else:
            index = IndexOf(nextState, outcomeStates)
            if index != -1:
                # this state has already been planned for, so just use the previous result
                #effList.append(effs[index])
                #childNode = searchNodes[index]
                newCommandNode.IncreaseWeight(nextState)
            else:
                #firstTask, firstTaskArgs, pRoot = Reinitialize('command', nextState, newNode, gL, cmd, cmdArgs)
                newNode = rTree.SearchTreeNode(nextState, 'state')
                newNode.SetPrevState(prevState)
                newCommandNode.AddChild(newNode)
                outcomeStates.append(nextState)
                #try:
                #    do_task(firstTask, *firstTaskArgs)
                #except Search_Done:
                #    pass
                #except Failed_task:
                #    effList.append(0)
                #    outcomeStates.append(nextState)
                #    effs.append(0)
                #    planLocals.SetCurrentNode(pRoot)
                #    continue

                #tree = pRoot
                #e = tree.GetEff()
                #assert(planLocals.GetCurrentNode() == pRoot)
                
                #effList.append(e)
                #outcomeStates.append(nextState)
                #searchNodes.append(newNode)
                #effs.append(e)
    
    #avgEff = TakeAvg(effList)
    #bestTree = planLocals.GetBestTree()
    #if ((bestTree == None or (avgEff > bestTree.GetEff())) and (avgEff > 0)):
    #    planLocals.SetBestTree(tree.copy())

    #if avgEff == 0:
    #    pRoot = planLocals.GetPlanningTree()
    #    pRoot.SetEff(0)
    #    planLocals.SetCurrentNode(pRoot)
    raise Search_Done

def GetCost(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    cost = DURATION.COUNTER[cmd.__name__]
    if type(cost) == types.FunctionType:
        return cost(*cmdArgs)
    else:
        return cost

## Verbosity functions 

def v_begin(task, taskArgs):
    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Begin task {}{}'.format(task, taskArgs))

    v_path()

def v_begin_c(cmd, cmdArgs):
    if verbose > 0:
        print_stack_size(planLocals.GetStackId(), path)
        print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

def PushToPath(task, taskArgs):
    global path # for debugging
    path[raeLocals.GetStackId()].append([task, taskArgs])

def v_path():
    if verbose > 1:
        if GLOBALS.GetPlanningMode() == True:
            print_entire_stack(planLocals.GetStackId(), path)
        else:
            print_entire_stack(raeLocals.GetStackId(), path)

def v_failedCommand(e):
    if verbose > 0:
        print_stack_size(planLocals.GetStackId(), path)
        print('Failed command {}'.format(e))

def v_failedTask(e):
    if verbose > 0:
        print_stack_size(planLocals.GetStackId(), path)
        print('Failed task {}'.format(e))

import RAE