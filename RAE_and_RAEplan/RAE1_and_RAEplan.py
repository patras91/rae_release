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
from sharedData import *
#from learningData import trainingDataRecords
#from convertData import Encode, Decode, EncodeForHeuristic, DecodeForHeuristic
#import torch
#import torch.nn as nn
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
        pass
        #import colorama

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

goalChecks = {}

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

def declare_goalCheck(task, goalCheckMethod):
    goalChecks[task] = goalCheckMethod

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

    random.seed(100)
    random.shuffle(instanceList)
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
    #while(ipcArgs.nextStack != stackid):
    #    pass
    ipcArgs.sem[stackid].acquire()

def EndCriticalRegion():
    #ipcArgs.nextStack = 0
    ipcArgs.sem[0].release()

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
        raeLocals.SetEfficiency(0)

    if GLOBALS.GetOpt() == "max":
        if GLOBALS.GetDomain() != "OF":
            assert(numpy.isclose(raeLocals.GetEfficiency(), raeLocals.GetUtility().GetValue()))

    #raeLocals.GetActingTree().PrintUsingGraphviz()
    h, t, c = raeLocals.GetActingTree().GetMetaData()
    return (retcode, 
        raeLocals.GetRetryCount(), 
        raeLocals.GetEfficiency(), 
        h, t, c, 
        raeLocals.GetPlanningUtilitiesList())

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
    raeLocals.SetEfficiency(float("inf"))

    raeLocals.SetUseBackupUCT(False)

    if GLOBALS.GetDomain() == "SDN":
        cmdStatusStack[raeArgs.stack] = None
    
def DoOneRollout(task, taskArgs):
    goalCheck = goalChecks[task]
    if goalCheck() == True:
        return
    curNode = planLocals.GetSearchTreeNode()
    if curNode.children == []:
        for cmd in commands.values():
            newSearchTreeNode = rTree.CommandSearchTreeNode(cmd, 'command', [])
            curNode.AddChild(newSearchTreeNode)

    untried = []

    if curNode.N == 0:
        untried = curNode.children
    else:
        for child in curNode.children:
            if child.children == []:
                untried.append(child) # command that has not been simulated yet

    if untried != []:
        cNode = random.choice(untried)
        index = curNode.children.index(cNode)
    else:
        vmax = 0
        cNode = None
        index = None
        for i in range(0, len(curNode.children)):
            v = curNode.Q[i].GetValue() + \
                GLOBALS.GetC() * math.sqrt(math.log(curNode.N)/curNode.n[i])
            if v >= vmax:
                vmax = v
                cNode = curNode.children[i]
                index = i

    c = cNode.GetLabel()

    cmdRet = {'state':'running'}
    beginCommand(c, cmdRet, [])
    retcode = cmdRet['state']

    nextState = GetState().copy()

    if retcode == 'Failure':
        nSN = rTree.CommandSearchTreeNode(nextState, 'state', None) # next state node
        nSN.SetUtility(Utility('Failure'))
        cNode.AddChild(nSN)
        planLocals.SetUtilRollout(Utility('Failure'))
        return 
    else:
        nSN = cNode.FindAmongChildren(nextState) 
        if nSN == None:
            nSN = rTree.CommandSearchTreeNode(nextState, 'state', None)

            cNode.AddChild(nSN)
        
        util1 = planLocals.GetUtilRollout()
        util2 = GetUtility(c, []) # cmdArgs
        planLocals.SetUtilRollout(util1 + util2)
        nSN.SetUtility(GetUtility(c, [])) # cmdArgs
        planLocals.SetSearchTreeNode(nSN)
        DoOneRollout(task, taskArgs)
        curNode.Q[index] = Utility((curNode.Q[index].GetValue() * \
                                curNode.n[index] + \
                                planLocals.GetUtilRollout().GetValue()) / \
                            (curNode.n[index] + 1))
        curNode.n[index] += 1



def RunUCTwithCommandsOnlyMain(task, taskArgs, state, queue):

    root = rTree.CommandSearchTreeNode(state.copy() , 'state', None)

    plan = []
    for i in range(GLOBALS.GetUCTRuns()):
        print("rollout ", i)
        RestoreState(state)
        planLocals.SetSearchTreeNode(root)
        planLocals.SetUtilRollout(Utility("Success"))
        DoOneRollout(task, taskArgs)

    queue.put(plan)

def RunUCTwithCommandsOnly(task, taskArgs):

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(
            target=RunUCTwithCommandsOnlyMain,
            args=[task, taskArgs, GetState(), queue])

    p.start()
    p.join(GLOBALS.GetTimeLimit())

    if p.is_alive() == True:
        p.terminate()
        return 'Failure'
    else:
        plan = queue.get()
        return plan

def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    RAE calls this functions when it wants suggestions from RAEplan
    """
    if verbose > 0:
        #print(colorama.Fore.RED, "Starting simulation for stack")
        print("Starting simulation for stack")

    if raeLocals.GetUseBackupUCT() == True:
        plan = RunUCTwithCommandsOnly(task, taskArgs)
        if plan != 'Failure':
            return (plan, "usingBackupUCT")
        else:
            raise Failed_task('{}{}'.format(task, taskArgs))

    queue = multiprocessing.Queue()
    actingTree = raeLocals.GetActingTree()
    #actingTree.PrintUsingGraphviz()
    p = multiprocessing.Process(
        target=RAE.PlannerMain, 
        args=[raeLocals.GetMainTask(), 
        raeLocals.GetMainTaskArgs(), 
        queue, 
        candidates,
        GetState().copy(),
        raeLocals.GetActingTree(),
        raeLocals.GetUtility()])

    p.start()
    p.join(GLOBALS.GetTimeLimit())

    if p.is_alive() == True:
        p.terminate()
        methodInstance, expUtil, simTime = queue.get()
    else:
        methodInstance, expUtil, simTime = queue.get()
        curUtil = raeLocals.GetUtility()
        raeLocals.AddToPlanningUtilityList(curUtil)
        raeLocals.AddToPlanningUtilityList(expUtil)
        raeLocals.AddToPlanningUtilityList(expUtil + curUtil)
        globalTimer.UpdateSimCounter(simTime)

    #retcode = plannedTree.GetRetcode()

    if verbose > 0:
        #print("Done with simulation. Result = {} \n".format(methodInstance), colorama.Style.RESET_ALL)
        print("Done with simulation. Result = {} \n".format(methodInstance))

    if methodInstance == 'Failure':
        #random.shuffle(candidates)
        if GLOBALS.GetBackupUCT() == True:
            raeLocals.SetUseBackupUCT(True)
            plan = RunUCTwithCommandsOnly(task, taskArgs)
            if plan != 'Failure':
                return (plan, "usingBackupUCT")
            else:
                return (candidates[0], candidates[1:])
        else:
            return (candidates[0], candidates[1:])
    else:
        if GLOBALS.GetLearningMode() == "genDataPlanner":
            trainingDataRecords.Add(
                    GetState(), 
                    methodInstance, 
                    raeLocals.GetEfficiency(),
                    task,
                    raeLocals.GetMainTask(),
                )
        candidates.pop(candidates.index(methodInstance))
        return (methodInstance, candidates)



def GetCandidateFromLearnedModel(fname, task, candidates):
    device = "cpu"

    # features = {
    #     "EE": 22,
    #     "SD": 24,
    #     "SR": 23,
    #     "OF": 0,
    #     "CR": 22,
    # }

    features = {
    "EE": 182, #22,
    "SD": 126, #24,
    "SR": 330, #23,
    "OF": 0,
    "CR": 97, #22, #91
    }
    outClasses = {
        "EE": 17,
        "SD": 9,
        "SR": 16,
        "OF": 0,
        "CR": 10,
    }

    #model = nn.Sequential(nn.Linear(features[GLOBALS.GetDomain()], 1)).to(device) 
    model = nn.Sequential(nn.Linear(features[GLOBALS.GetDomain()], 512), nn.ReLU(inplace=True), nn.Linear(512, outClasses[GLOBALS.GetDomain()]))
    model.load_state_dict(torch.load(fname))
    model.eval()

    x = Encode(GLOBALS.GetDomain(), GetState().GetFeatureString(), task, raeLocals.GetMainTask())
    np_x = numpy.array(x)
    x_tensor = torch.from_numpy(np_x).float()
    y = model(x_tensor)
    m = Decode(GLOBALS.GetDomain(), y)

    for i in range(len(candidates)):
        if m == candidates[i].GetName():
            res = candidates[i]
            candidates.pop(i)
            return res, candidates

    return (candidates[0], candidates[1:])

def choose_candidate(candidates, task, taskArgs):
    if len(candidates) == 1 or (GLOBALS.GetDoPlanning() == False and GLOBALS.GetUseTrainedModel() == "n"):
        #random.shuffle(candidates)
        return(candidates[0], candidates[1:])
    elif GLOBALS.GetDoPlanning() == False and GLOBALS.GetUseTrainedModel() == "a":
        fname = GLOBALS.GetModelPath() + "model_to_choose_{}_actor".format(GLOBALS.GetDomain())
        return GetCandidateFromLearnedModel(fname, task, candidates)
    elif GLOBALS.GetDoPlanning() == False and GLOBALS.GetUseTrainedModel() == "p":
        fname = GLOBALS.GetModelPath() + "model_to_choose_{}_planner".format(GLOBALS.GetDomain())
        return GetCandidateFromLearnedModel(fname, task, candidates)
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
        if GLOBALS.GetOpt() == "sr": # there may be a better way to do this
            raeLocals.SetUtility(Utility("Success"))

        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        if candidates == "usingBackupUCT":
            plan = m
            retcode = "Success"
            for (cmd, cmdArgs) in plan:
                try:
                    DoCommandInRealWorld(cmd, cmdArgs)
                except Failed_command as e:
                    retcode = "Failure"
                    break
        else:
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
        if GLOBALS.GetLearningMode() == "genDataActor" or GLOBALS.GetLearningMode() == "genDataPlanner":
            trainingDataRecords.Add(
                GetState(), 
                m, 
                raeLocals.GetEfficiency(),
                task,
                raeLocals.GetMainTask(),
            )
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
    planLocals.SetRolloutDepth(planArgs.GetDepth())

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

    planLocals.SetRefDepth(float("inf"))
    while (searchTreeRoot.GetSearchDone() == False): # all rollouts not explored
        try:
            planLocals.SetDepth(0)
            
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
    if GLOBALS.GetLearningMode() == "genEffDataPlanner":
        taskToRefine.GetTrainingItems_SLATE(
            trainingDataRecords, 
            planArgs.GetCurUtil(), 
            planArgs.GetTask())

    return (taskToRefine.GetBestMethodAndUtility(), globalTimer.GetSimulationCounter())
    
def GetBestTillNow():
    taskToRefine = planLocals.GetTaskToRefine()
    return (taskToRefine.GetBestMethodAndUtility_UCT(), globalTimer.GetSimulationCounter())

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
    planLocals.SetRolloutDepth(planArgs.GetDepth())

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
            searchTreeRoot.updateIndex = 0
            do_task(task, *taskArgs) 
            #searchTreeRoot.PrintUsingGraphviz()
            searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())   
        except Failed_Rollout as e:
            v_failedCommand(e)
            #searchTreeRoot.PrintUsingGraphviz()
            searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())
        except DepthLimitReached as e:
            #searchTreeRoot.PrintUsingGraphviz()
            searchTreeRoot.UpdateQValues(planLocals.GetUtilRollout().GetValue())
            pass
        else:
            pass
        i += 1

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    taskToRefine = planLocals.GetTaskToRefine()
    if GLOBALS.GetLearningMode() == "genEffDataPlanner":
        taskToRefine.UpdateAllUtilities()
        taskToRefine.GetTrainingItems(
            trainingDataRecords, 
            planArgs.GetCurUtil(), 
            planArgs.GetTask())

    return GetBestTillNow()

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

def GetHeuristicEstimate(task=None, tArgs=None):
    if GLOBALS.GetUseTrainedModel() == "hp" and GLOBALS.GetOpt() == "max":
        domain = GLOBALS.GetDomain()
        features = {
            "EE": 204, #23 - 2,
            "SD": 144,
            "SR": 401,
            "OF": 0,
            "CR": 100 #98, #23 - 2,
        }

        outClasses = {
            "EE": 200,
            "SD": 75,
            "SR": 10,
            "OF": 1,
            "CR": 100, #1
        }
        #model = nn.Sequential(nn.Linear(features[domain], 512), 
        #nn.ReLU(inplace=True),
        #nn.Linear(512, outClasses[domain]))

        # if domain == "CR1":
        #     model = nn.Sequential(nn.Linear(features[domain], 512), 
        #     nn.ReLU(inplace=True),
        #     nn.Linear(512, 512), 
        #     nn.Dropout(p=0.1),
        #     nn.Linear(512, 512), 
        #     nn.ReLU(inplace=True), 
        #     nn.Linear(512, outClasses[domain]))
        if domain == "SR" or domain == "SD" or domain == "EE" or domain == "CR":
            model = nn.Sequential(nn.Linear(features[domain], 1024), 
            nn.ReLU(inplace=True),
            nn.Linear(1024, outClasses[domain]))

        fname = GLOBALS.GetModelPath() + "model_for_eff_{}_planner_task_all".format(GLOBALS.GetDomain())
        model.load_state_dict(torch.load(fname))
        model.eval()

        cand, prevState, flag = GetCandidates(task, tArgs)
        effMax = 0
        for m in cand:
            x = EncodeForHeuristic(
                domain, 
                prevState.GetFeatureString(),
                m.GetName(),
                task+" "+str(tArgs))

            np_x = numpy.array(x)
            x_tensor = torch.from_numpy(np_x).float()
            y = model(x_tensor)
            eff = DecodeForHeuristic(GLOBALS.GetDomain(), y)
            if eff > effMax:
                effMax = eff
        return effMax

    elif GLOBALS.GetOpt() == "sr":
        mtask, args = planLocals.GetHeuristicArgs()
        res = heuristic[mtask](args)
        if res > 0:
            return 1
        else:
            return 0
    else:
        mtask, args = planLocals.GetHeuristicArgs()
        res = heuristic[mtask](args)
    return res
    
def PlanTask(task, taskArgs):
    # Need to look through several candidates for this task
    cand, state, flag = GetCandidates(task, taskArgs)

    searchTreeNode = planLocals.GetSearchTreeNode()
    taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
    searchTreeNode.AddChild(taskNode)
    if flag == 1:
        planLocals.SetTaskToRefine(taskNode)
        planLocals.SetRefDepth(planLocals.GetDepth())

        
    if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():

        newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs)
        newNode.SetPrevState(state)
        newNode.SetUtility(Utility(GetHeuristicEstimate()))
        taskNode.AddChild(newNode)
        raise Expanded_Search_Tree_Node()

    for m in cand:
        newSearchTreeNode = rTree.SearchTreeNode(m, 'method', taskArgs)
        newSearchTreeNode.SetPrevState(state)
        taskNode.AddChild(newSearchTreeNode)
    raise Expanded_Search_Tree_Node()

def PlanTask_UCT(task, taskArgs):
    searchTreeNode = planLocals.GetSearchTreeNode()
    
    if searchTreeNode.children == []:
        # add new nodes with this task and its applicable method instances
        taskNode = rTree.SearchTreeNode(task, 'task', taskArgs)
        searchTreeNode.AddChild(taskNode)
        # Need to look through several candidates for this task
        cand, state, flag = GetCandidates(task, taskArgs)

        if flag == 1:
            planLocals.SetTaskToRefine(taskNode)
            planLocals.SetRefDepth(planLocals.GetDepth())
            planLocals.SetFlip(True)
        if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():
            newNode = rTree.SearchTreeNode('heuristic', 'heuristic', taskArgs)

            util1 = planLocals.GetUtilRollout()
            util2 = Utility(GetHeuristicEstimate(task, taskArgs))
            planLocals.SetUtilRollout(util1 + util2)

            # Is this node needed?
            taskNode.AddChild(newNode)
            taskNode.updateIndex = 0
            raise DepthLimitReached()

        for m in cand:
            newSearchTreeNode = rTree.SearchTreeNode(m, 'method', taskArgs)
            newSearchTreeNode.SetPrevState(state)
            taskNode.AddChild(newSearchTreeNode)
    else:
        taskNode = searchTreeNode.children[0]
        assert(taskNode.type == 'task')
        if taskNode == planLocals.GetTaskToRefine():
            planLocals.SetFlip(True)
            planLocals.SetRefDepth(planLocals.GetDepth())

        if planLocals.GetRefDepth() + planLocals.GetRolloutDepth() <= planLocals.GetDepth():
            newNode = taskNode.children[0]
            taskNode.updateIndex = 0
            util1 = planLocals.GetUtilRollout()
            util2 = Utility(GetHeuristicEstimate(task, taskArgs))
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
    except DepthLimitReached as e:
        depthLimReached = True

    taskNode.updateIndex = index


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
        planLocals.IncreaseDepthBy1()
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

def GetNewId():
    GetNewId.num += 1
    return GetNewId.num
GetNewId.num = 0

def AddEfficiency(e1, e2):

    if e1 == float("inf"):
        res = e2
    elif e2 == float("inf"):
        res = e1
    elif e1 == 0 and e2 == 0:
        res = 0
    else:
        res = e1 * e2 / (e1 + e2)
    return res

def DoCommandInRealWorld(cmd, cmdArgs):
    global path
    path[raeLocals.GetStackId()].append([cmd, cmdArgs])

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

    cmdRet = {'state':'running'}

    domain = GLOBALS.GetDomain()
    if domain != 'SDN':
        cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
        cmdThread.start()
    else:
        newCmdId = GetNewId()
        AddToCommandStackTable(newCmdId, raeLocals.GetStackId())
        cmdExecQueue.put([newCmdId, cmd, cmdArgs])

    if cmd.__name__ in raeLocals.GetCommandCount():
        raeLocals.GetCommandCount()[cmd.__name__] += 1
    else:
        raeLocals.GetCommandCount()[cmd.__name__] = 1

    EndCriticalRegion()
    BeginCriticalRegion(raeLocals.GetStackId())

    if domain != 'SDN':
        while (cmdRet['state'] == 'running'):
            if verbose > 0:
                print_stack_size(raeLocals.GetStackId(), path)
                print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

            EndCriticalRegion()
            BeginCriticalRegion(raeLocals.GetStackId())
    else:
        while(cmdStatusStack[raeLocals.GetStackId()] == None):
            EndCriticalRegion()
            BeginCriticalRegion(raeLocals.GetStackId())

    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Command {}{} is done'.format( cmd.__name__, cmdArgs))

    if domain != 'SDN':
        retcode = cmdRet['state']
    else:
        [id, retcode, nextState] = cmdStatusStack[raeLocals.GetStackId()]
        assert(retcode == 'Success' or retcode == 'Failure')
        RestoreState(nextState)

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

    if cmd.__name__ == "fail" or retcode == 'Failure':
        util1 = GetFailureUtility(cmd, cmdArgs)
        raeLocals.AddToPlanningUtilityList('fail')
        eff1 = GetFailureEfficiency(cmd, cmdArgs)
    else:
        util1 = GetUtility(cmd, cmdArgs)
        eff1 = GetEfficiency(cmd, cmdArgs)
        wait = False
        if GLOBALS.GetDomain() == "OF": # to avoid overflow in output files
            if cmd.__name__ == "wait":
                wait = True
                if len(raeLocals.GetPlanningUtilitiesList()) > 1:
                    lastItem = str(raeLocals.GetPlanningUtilitiesList()[-1])
                    if lastItem[0:4] == "wait":
                        n = int(lastItem[4:]) + 1
                        raeLocals.GetPlanningUtilitiesList()[-1] = "wait" + str(n)
                    else:
                        raeLocals.AddToPlanningUtilityList("wait0")
                else:
                    raeLocals.AddToPlanningUtilityList("wait0")
        if wait == False:
            raeLocals.AddToPlanningUtilityList(cmd.__name__)
    util2 = raeLocals.GetUtility()
    raeLocals.SetUtility(util1 + util2)
    eff2 = raeLocals.GetEfficiency()
    raeLocals.SetEfficiency(AddEfficiency(eff1, eff2))

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
    #cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    #cmdThread.start()

    beginCommand(cmd, cmdRet, cmdArgs)
    #if GLOBALS.GetPlanningMode() == False:
    #    EndCriticalRegion()
    #    BeginCriticalRegion(planLocals.GetStackId())

    #while (cmdRet['state'] == 'running'):
    #    if verbose > 0:
    #        print_stack_size(planLocals.GetStackId(), path)
    #        print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
    #    if GLOBALS.GetPlanningMode() == False:
    #        EndCriticalRegion()
    #        BeginCriticalRegion(planLocals.GetStackId())

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
    newCommandNode = rTree.SearchTreeNode(cmd, 'command', cmdArgs)
    searchTreeNode.AddChild(newCommandNode)

    #k = max(1, GLOBALS.Getk() - int(planLocals.GetDepth() / 2))
    k = GLOBALS.Getk()
    for i in range(0, k):
        RestoreState(prevState)
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        nextState = GetState().copy()

        if retcode == 'Failure':
            newNode = rTree.SearchTreeNode(nextState, 'state', None)
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
                newNode = rTree.SearchTreeNode(nextState, 'state', None)
                newNode.SetPrevState(prevState)
                newCommandNode.AddChild(newNode)
                #outcomeStates.append(nextState)
                
    raise Expanded_Search_Tree_Node

def PlanCommand_UCT(cmd, cmdArgs):

    searchTreeNode = planLocals.GetSearchTreeNode()
    #planLocals.GetSearchTreeRoot().PrintUsingGraphviz()
    if searchTreeNode.children == []:
        commandNode = rTree.SearchTreeNode(cmd, 'command', None)
        searchTreeNode.AddChild(commandNode)
    else:
        commandNode = searchTreeNode.children[0]
        assert(commandNode.GetType() == 'command')
        assert(commandNode.GetLabel() == cmd)

    if planLocals.GetFlip() == False:
        retcode = 'Success'
        nextState = commandNode.GetNext().GetLabel()
        RestoreState(nextState)
    else:
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        nextState = GetState().copy()

    if retcode == 'Failure':
        nextStateNode = rTree.SearchTreeNode(nextState, 'state', None)
        nextStateNode.SetUtility(Utility('Failure'))
        commandNode.AddChild(nextStateNode)
        planLocals.SetUtilRollout(Utility('Failure'))
        commandNode.updateChild = nextStateNode
        raise Failed_Rollout()
    else:
        nextStateNode = commandNode.FindAmongChildren(nextState) 
        if nextStateNode == None:
            nextStateNode = rTree.SearchTreeNode(nextState, 'state', None)

            commandNode.AddChild(nextStateNode)
        
        util1 = planLocals.GetUtilRollout()
        util2 = GetUtility(cmd, cmdArgs)
        planLocals.SetUtilRollout(util1 + util2)
        commandNode.updateChild = nextStateNode
        nextStateNode.SetUtility(GetUtility(cmd, cmdArgs))
        planLocals.SetSearchTreeNode(nextStateNode)

def GetCost(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    if GLOBALS.GetDomain() == "SD" and cmd.__name__ == "helpRobot":
        cost = 7
    else:
        cost = DURATION.COUNTER[cmd.__name__]
    if type(cost) == types.FunctionType:
        return cost(*cmdArgs)
    else:
        return cost

def GetFailureUtility(cmd, cmdArgs):
    if GLOBALS.GetOpt() != "sr":
        return Utility(1/20)
    else:
        return Utility("Failure")

def GetUtility(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    if GLOBALS.GetDomain() == "SD" and cmd.__name__ == "helpRobot": # kluge because I forgot to add this cost in the auto-gen problems
        cost = 7
    else:
        cost = DURATION.COUNTER[cmd.__name__]
    if GLOBALS.GetOpt() == "sr":
        return Utility("Success")
    elif type(cost) == types.FunctionType:
        return Utility(1/cost(*cmdArgs))
    else:
        return Utility(1/cost)

def GetFailureEfficiency(cmd, cmdArgs):
    return 1/20

def GetEfficiency(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    if GLOBALS.GetDomain() == "SD" and cmd.__name__ == "helpRobot": # kluge because I forgot to add this cost in the auto-gen problems
        cost = 7
    else:
        cost = DURATION.COUNTER[cmd.__name__]
    if type(cost) == types.FunctionType:
        return 1/cost(*cmdArgs)
    else:
        return 1/cost

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
