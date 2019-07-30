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
import math
import random
from helper_functions import *
import types
import sys, pprint
import os
import GLOBALS
import rTree
#import colorama
from timer import globalTimer, DURATION
from dataStructures import rL_APE, rL_PLAN
from APE_stack import print_entire_stack, print_stack_size
from utility import Utility
import time
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
    if level > 0:
        import colorama

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
        if other == 'heuristic' or other == 'Failure' or other == None or other == 'root' or other == 'task':
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

class Expanded_Search_Tree_Node(Exception):
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

#SLATE sampling strategy
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
        print('\n---- RAE: Create stack {}, task {}{}\n'.format(raeLocals.GetStackId(), task, raeArgs.taskArgs))

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
        print("\n---- RAE: Done with stack %d\n" %raeLocals.GetStackId())

    EndCriticalRegion()

    if retcode == 'Failure':
        raeLocals.SetUtility(Utility('Failure'))

    #raeLocals.GetActingTree().PrintUsingGraphviz()
    h, t, c = raeLocals.GetActingTree().GetMetaData()
    return (retcode, raeLocals.GetRetryCount(), raeLocals.GetUtility(), h, t, c)

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
    raeLocals.SetUtility(Utility('Success'))
    
def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    RAE calls this functions when it wants suggestions from RAEplan
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
    p.join(600)
    if p.is_alive() == True:
        p.terminate()
        methodInstance = 'Failure'
        simTime = 600
    else:
        methodInstance, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    #retcode = plannedTree.GetRetcode()

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(methodInstance), colorama.Style.RESET_ALL)

    if methodInstance == 'Failure':
        #random.shuffle(candidates)
        return (candidates[0], candidates[1:])
    else:
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
        if GLOBALS.GetUCTmode() == True:
            PlanTask_UCT(task, taskArgs)
        else:
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

    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    searchTreeRoot = planArgs.GetSearchTree()
    planLocals.SetSearchTreeRoot(searchTreeRoot)

    global path   # for debugging
    path.update({planLocals.GetStackId(): []})
        
    InitializePlanningTree() 

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    while (searchTreeRoot.GetSearchDone() == False): # all rollouts not explored
        try:
            planLocals.SetDepth(0)
            planLocals.SetRefDepth(float("inf"))
            planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
            do_task(task, *taskArgs) 
            searchTreeRoot.UpdateChildPointers()    
        except Failed_Rollout as e:
            v_failedCommand(e)
            searchTreeRoot.UpdateChildPointers()
        except DepthLimitReached as e:
            searchTreeRoot.UpdateChildPointers()
        except Expanded_Search_Tree_Node as e:
            pass
        else:
            pass

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    taskToRefine = planLocals.GetTaskToRefine()

    return (taskToRefine.GetBestMethod(), globalTimer.GetSimulationCounter())
    
def RAEplanChoice_UCT(task, planArgs):
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

    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    searchTreeRoot = planArgs.GetSearchTree()
    planLocals.SetSearchTreeRoot(searchTreeRoot)
    planLocals.SetTaskToRefine(-1)
    
    global path   # for debugging
    path.update({planLocals.GetStackId(): []})
        
    InitializePlanningTree() 

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    i = 1
    while (i <= GLOBALS.GetUCTRuns()): # all rollouts not explored
        try:
            planLocals.SetDepth(0)
            planLocals.SetRefDepth(float("inf"))
            planLocals.SetUtilRollout(Utility('Success'))
            planLocals.SetSearchTreeNode(searchTreeRoot.GetNext())
            planLocals.SetFlip(False)
            RestoreState(searchTreeRoot.GetNext().GetPrevState())
            do_task(task, *taskArgs)    
        except Failed_Rollout as e:
            v_failedCommand(e)
        except DepthLimitReached as e:
            pass
        else:
            pass
        i += 1

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    taskToRefine = planLocals.GetTaskToRefine()

    return (taskToRefine.GetBestMethod_UCT(), globalTimer.GetSimulationCounter())

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
        
    # b = max(1, GLOBALS.Getb() - int(planLocals.GetDepth() / 4))
    if GLOBALS.GetUCTmode() == True:
        cand = candidates
    else:
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

    if planLocals.GetRefDepth() + GLOBALS.GetSearchDepth() <= planLocals.GetDepth():
        newNode = rTree.SearchTreeNode('heuristic', 'heuristic')

        newNode.SetUtility(Utility(GetHeuristicEstimate()))
        taskNode.AddChild(newNode)
        raise Expanded_Search_Tree_Node()

    for m in cand:
        newSearchTreeNode = rTree.SearchTreeNode(m, 'method')
        newSearchTreeNode.SetPrevState(state)
        taskNode.AddChild(newSearchTreeNode)
    raise Expanded_Search_Tree_Node()

def PlanTask_UCT(task, taskArgs):
    searchTreeNode = planLocals.GetSearchTreeNode()
    
    if searchTreeNode.children == []:
        # add new nodes with this task and its applicable method instances
        taskNode = rTree.SearchTreeNode('task', 'task')
        searchTreeNode.AddChild(taskNode)
        # Need to look through several candidates for this task
        cand, state, flag = GetCandidates(task, taskArgs)

        if flag == 1:
            planLocals.SetTaskToRefine(taskNode)
            planLocals.SetRefDepth(planLocals.GetDepth())
            planLocals.SetFlip(True)

        if planLocals.GetRefDepth() + GLOBALS.GetSearchDepth() <= planLocals.GetDepth():
            newNode = rTree.SearchTreeNode('heuristic', 'heuristic')

            util1 = planLocals.GetUtilRollout()
            util2 = Utility(GetHeuristicEstimate())
            planLocals.SetUtilRollout(util1 + util2)

            # Is this node needed?
            taskNode.AddChild(newNode)
            raise DepthLimitReached()

        for m in cand:
            newSearchTreeNode = rTree.SearchTreeNode(m, 'method')
            newSearchTreeNode.SetPrevState(state)
            taskNode.AddChild(newSearchTreeNode)
    else:
        taskNode = searchTreeNode.children[0]
        assert(taskNode.type == 'task')
        if taskNode == planLocals.GetTaskToRefine():
            planLocals.SetFlip(True)
            planLocals.SetRefDepth(planLocals.GetDepth())

        if planLocals.GetRefDepth() + GLOBALS.GetSearchDepth() <= planLocals.GetDepth():
            newNode = taskNode.children[0]

            util1 = planLocals.GetUtilRollout()
            util2 = Utility(GetHeuristicEstimate())
            planLocals.SetUtilRollout(util1 + util2)

            raise DepthLimitReached()
    
    untried = []

    if taskNode.N == 0:
        untried = taskNode.children
    else:
        for child in taskNode.children:
            if child.children == []:
                untried.append(child)

    if untried != []:
        mNode = random.choice(untried)
        index = taskNode.children.index(mNode)
    else:
        vmax = 0
        mNode = None
        index = None
        for i in range(0, len(taskNode.children)):
            v = taskNode.Q[i].GetValue() + \
                GLOBALS.GetC() * math.sqrt(math.log(taskNode.N)/taskNode.n[i])
            if v >= vmax:
                vmax = v
                mNode = taskNode.children[i]
                index = i

    m = mNode.GetLabel()
    RestoreState(mNode.GetPrevState())
    planLocals.SetSearchTreeNode(mNode)
    failed = False
    depthLimReached = False
    try:
        PlanMethod(m, task, taskArgs)
    except Failed_Rollout as e:
        failed = True
        pass
    except DepthLimitReached as e:
        depthLimReached = True

    utilVal = planLocals.GetUtilRollout().GetValue()
    if taskNode.n[index] > 0:
        taskNode.Q[index] = \
            Utility(((utilVal + taskNode.n[index] * taskNode.Q[index].GetValue()) / \
            (1 + taskNode.n[index])))
    else:
        taskNode.Q[index] = Utility(utilVal)

    taskNode.n[index] += 1
    taskNode.N += 1
    if failed:
        raise Failed_Rollout()
    elif depthLimReached:
        raise DepthLimitReached()

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
        print("Error: retcode should not be Failure inside PlanMethod.\n")
        raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))
    elif retcode == 'Success':
        util = Utility('Success')
        for child in savedNode.children:
            util = util + child.GetUtility()
        savedNode.SetUtility(util)
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
        #planLocals.IncreaseDepthBy1()
        if GLOBALS.GetUCTmode() == True:
            PlanCommand_UCT(cmd, cmdArgs)
        else:
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
        util1 = GetFailureUtility(cmd, cmdArgs)
    else:
        util1 = GetUtility(cmd, cmdArgs)
    util2 = raeLocals.GetUtility()
    raeLocals.SetUtility(util1 + util2)

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

    if stateNode.GetUtility() != Utility('Failure'):
        util = GetUtility(cmd, cmdArgs)
        stateNode.SetUtility(util)
        newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
        planLocals.GetCurrentNode().AddChild(newNode)
        planLocals.GetCurrentNode().AddUtility(util)
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
    #outcomeStates = []

    searchTreeNode = planLocals.GetSearchTreeNode()
    prevState = GetState().copy()
    newCommandNode = rTree.SearchTreeNode(cmd, 'command')
    searchTreeNode.AddChild(newCommandNode)

    #k = max(1, GLOBALS.Getk() - int(planLocals.GetDepth() / 2))
    k = GLOBALS.Getk()
    for i in range(0, k):
        RestoreState(prevState)
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        nextState = GetState().copy()

        if retcode == 'Failure':
            newNode = rTree.SearchTreeNode(nextState, 'state')
            newNode.SetUtility(Utility('Failure'))
            newNode.SetPrevState(prevState)
            newCommandNode.AddChild(newNode)
            #outcomeStates.append(nextState)
        else:
            #index = IndexOf(nextState, outcomeStates)
            index = -1
            if index != -1:
                # this state has already been planned for, so just use the previous result
                #effList.append(effs[index])
                #childNode = searchNodes[index]
                newCommandNode.IncreaseWeight(nextState)
            else:
                newNode = rTree.SearchTreeNode(nextState, 'state')
                newNode.SetPrevState(prevState)
                newCommandNode.AddChild(newNode)
                #outcomeStates.append(nextState)
                
    raise Expanded_Search_Tree_Node

def PlanCommand_UCT(cmd, cmdArgs):

    searchTreeNode = planLocals.GetSearchTreeNode()
    if searchTreeNode.children == []:
        commandNode = rTree.SearchTreeNode(cmd, 'command')
        searchTreeNode.AddChild(commandNode)
    else:
        commandNode = searchTreeNode.children[0]
    if planLocals.GetFlip() == False:
        retcode = 'Success'
        nextState = commandNode.GetNext().GetLabel()
        RestoreState(nextState)
    else:
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        nextState = GetState().copy()

    if retcode == 'Failure':
        nextStateNode = rTree.SearchTreeNode(nextState, 'state')
        nextStateNode.SetUtility(Utility('Failure'))
        commandNode.AddChild(nextStateNode)
        planLocals.SetUtilRollout(Utility('Failure'))
        raise Failed_Rollout()
    else:
        nextStateNode = commandNode.FindAmongChildren(nextState) 
        if nextStateNode == None:
            nextStateNode = rTree.SearchTreeNode(nextState, 'state')

            commandNode.AddChild(nextStateNode)

        planLocals.SetCurrentNode(nextStateNode)
        
        util1 = planLocals.GetUtilRollout()
        util2 = GetUtility(cmd, cmdArgs)
        planLocals.SetUtilRollout(util1 + util2)

        planLocals.SetSearchTreeNode(nextStateNode)

def GetCost(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    cost = DURATION.COUNTER[cmd.__name__]
    if type(cost) == types.FunctionType:
        return cost(*cmdArgs)
    else:
        return cost

def GetFailureUtility(cmd, cmdArgs):
    return Utility(1/20)

def GetUtility(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    cost = DURATION.COUNTER[cmd.__name__]
    if type(cost) == types.FunctionType:
        return Utility(1/cost(*cmdArgs))
    else:
        return Utility(1/cost)

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