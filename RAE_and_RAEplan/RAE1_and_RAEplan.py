from __future__ import print_function
import threading
from state import GetState, PrintState, RestoreState
import multiprocessing
import numpy
import random
from helper_functions import *

"""
File RAE1_and_RAEplan.py
Author:
Sunandita Patra <patras@cs.umd.edu>
"""

import sys, pprint
import os
import globals
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
methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file
path = {} # global variable shared by all stacks for debugging

# Only RAE1
commands = {} # dictionary of commands, initialized once for every run via the domain file
raeLocals = rL_APE() # APE variables that are local to every stack

#only RAEplan
commandSimulations = {} # dictionary of descriptive models of commands, initialized once for every run via the domain file
planLocals = rL_PLAN() # APEplan_systematic variables that are local to every call to APEplan_systematic, 
                       # we need this to be thread local because we have multiple stacks in APE as 
                       # multiple threads and each thread call its own APEplan_systematic
commandProb = {} # dictionary of probabilities of outcomes of commands, initialized once for every run via the domain file
listCommandsDependingOnParams = [] # list of commands whose descriptive models depend on the parameters

############################################################
# Functions to tell Rae1 what the commands and methods are

def declare_commands(cmd_list):
    """
    Call this after defining the commands, to tell APE and APE-plan what they are.
    cmd_list must be a list of functions, not strings.
    """
    commands.update({cmd.__name__:cmd for cmd in cmd_list})
    return commands

def UpdatePerceiveProb(comm, l, obj, newp):
    pList = commandProb[comm][l][obj]
    commandProb[comm][l][obj] = [newp, 1 - newp]

def AddCommandToSpecialList(cmd):
    listCommandsDependingOnParams.append(cmd)

def GetCommand(cmd):
    """
        Get the actual operational model of the command 
    """
    name = cmd.__name__
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


############################################################
# Stuff for debugging printout

class Failed_command(Exception):
    pass

class Failed_task(Exception):
    pass

class Incorrect_return_code(Exception):
    pass

class Search_Done(Exception):
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
    return (retcode, raeLocals.GetRetryCount(), raeLocals.GetCommandCount())

def InitializeStackLocals(task, raeArgs):
    raeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
    raeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
    raeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                         # This is a dictionary to accomodate for commands with different costs.
    raeLocals.SetMainTask(task)
    raeLocals.SetMainTaskArgs(raeArgs.taskArgs)

    aT = rTree.ActingTree()
    aT.SetNextState(GetState().copy())
    raeLocals.SetActingTree(aT)
    
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
        raeLocals.GetGuideList()])

    p.start()
    p.join()

    plannedTree, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    retcode = plannedTree.GetRetcode()

    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(retcode), colorama.Style.RESET_ALL)

    if retcode == 'Failure':
        #random.shuffle(candidates)
        return (candidates[0], candidates[1:])
    else:
        plannedTreeFlat = plannedTree.GetPreorderTraversal()
        indexToLook = actingTree.GetSize() - 2
        m = plannedTreeFlat[indexToLook]
        candidates.pop(candidates.index(m))
        return (m, candidates)

def choose_candidate(candidates, task, taskArgs):
    if globals.GetDoSampling() == False or len(candidates) == 1:
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
    candidates = methods[task][:]
    assert(candidates != [])

    parent, node = raeLocals.GetCurrentNodes()

    while (retcode != 'Success'):

        node.Clear() # Clear it on every iteration for a fresh start
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        node.SetLabelAndType(m, 'method')
        raeLocals.SetCurrentNode(node)
        node.SetNextState(GetState().copy())
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
            PrintState()

        retcode = m(*taskArgs)  # This is the main job of this function, CallMethod
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

def do_task(task, *taskArgs):
    if globals.GetPlanningMode() == True:
        nextNode = planLocals.GetGuideList().GetNext()
        if nextNode != None:
            return FollowGuide_task(task, taskArgs, nextNode)
        else:
            return PlanTask(task, taskArgs)
    else:
        return DoTaskInRealWorld(task, taskArgs)

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
    
    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    gL = planArgs.GetGuideList()
    planLocals.SetGuideList(gL) # which is basically the stack in the pseudocode
    RestoreState(gL.GetStartState())

    global path   # for debugging
    path.update({planLocals.GetStackId(): []})
        
    root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
    planLocals.SetCurrentNode(root)
    planLocals.SetPlanningTree(root)
    planLocals.SetBestTree(None)

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    try:
        do_task(task, *taskArgs) 
        if planLocals.GetBestTree() != None:
            plannedTree = planLocals.GetBestTree().GetChild() # doing GetChild because the root is just a node labelled 'root'
        else:
            plannedTree = rTree.CreateFailureNode()
            
    except Failed_command as e:
        v_failedCommand(e)
        plannedTree = rTree.CreateFailureNode()

    except Failed_task as e:
        v_failedTask(e)
        plannedTree = rTree.CreateFailureNode()

    except Search_Done as e:
        if planLocals.GetBestTree() != None:
            plannedTree = planLocals.GetBestTree().GetChild() # doing GetChild because the root is just a node labelled 'root'
        else:
            plannedTree = rTree.CreateFailureNode()
    else:
        pass

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    return (plannedTree, globalTimer.GetSimulationCounter())
    
def GetCandidates(task):
    if planLocals.GetCandidates() != None:
        # when candidates is a subset of the applicable methods, it is available from planLocals
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
        state = planLocals.GetState()
    else:
        candidates = methods[task][:] # set of applicable methods
        state = GetState()
        
    b = globals.Getb()
    cand = candidates[0:min(b - 1, len(candidates))]
    return cand, state

def FollowGuide_task(task, taskArgs, nextNode):
    m = nextNode.GetLabel()
    RestoreState(nextNode.GetNextState())
    tree = PlanMethod(m, task, taskArgs)
    return tree

def Reinitialize(m, s, newNode, guideList, name, args):
    guideList.RemoveAllAfter(newNode)
    if m == 'command':
        newNode.SetLabel(name)
    else:
        newNode.SetLabel(m)
    newNode.SetNextState(s)
    
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

def PlanTask(task, taskArgs):
    # Need to look through several candidates for this task
    cand, state = GetCandidates(task)
    # TODO : Can do pruning here if efficiency is already lower
    guideList = planLocals.GetGuideList()
    newNode = guideList.append()

    for m in cand:
        firstTask, firstTaskArgs, pRoot = Reinitialize(m, state, newNode, guideList, task, taskArgs)
        try:
            do_task(firstTask, *firstTaskArgs) # to recreate the execution stack
            tree = pRoot
            assert(planLocals.GetCurrentNode() == pRoot)
            bestTree = planLocals.GetBestTree()
            if bestTree != None:
                bestEff = bestTree.GetEff()
            else:
                bestEff = 0

            if tree.GetEff() > bestEff:
                bestTree = tree.copy()
                planLocals.SetBestTree(bestTree)
        except Failed_task:
            planLocals.SetCurrentNode(pRoot)
        except Search_Done:
            pass

    raise Search_Done()

def PlanMethod(m, task, taskArgs):
    global path
    path[planLocals.GetStackId()].append([task, taskArgs])
    savedNode = planLocals.GetCurrentNode()
    
    newNode = rTree.PlanningTree(m, taskArgs, 'method')
    savedNode.AddChild(newNode)
    planLocals.SetCurrentNode(newNode)

    retcode = CallMethod_OperationalModel(planLocals.GetStackId(), m, taskArgs)

    path[planLocals.GetStackId()].pop()
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
    if globals.GetPlanningMode() == True:
        nextNode = planLocals.GetGuideList().GetNext()
        if nextNode == None:
            return PlanCommand(cmd, cmdArgs)
        else:
            return FollowGuide_command(cmd, cmdArgs, nextNode)
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
    cmdNode.SetLabelAndType(cmd, 'command')
    cmdNode.SetNextState(GetState().copy())

    if verbose > 1:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(raeLocals.GetStackId(), path)
        print('Current state is')
        PrintState()

    path[raeLocals.GetStackId()].pop()

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

def FollowGuide_command(cmd, cmdArgs, nextNode):
    
    assert(cmd == nextNode.GetLabel())
    RestoreState(nextNode.GetNextState())
    
    cost = GetCost(cmd, cmdArgs)
    newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
    planLocals.GetCurrentNode().AddChild(newNode)
    planLocals.GetCurrentNode().AddEfficiency(1/cost)
    
    return 'Success'

def CallCommand_OperationalModel(cmd, cmdArgs):
    global path
    v_path()
    v_begin_c(cmd, cmdArgs)
    path[planLocals.GetStackId()].append([cmd, cmdArgs])
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
    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(planLocals.GetStackId(), path)
        print('Current state is')
        PrintState()

    path[planLocals.GetStackId()].pop()
    v_path()

    return retcode

def PlanCommand(cmd, cmdArgs):
    savedState = GetState().copy()
    gL = planLocals.GetGuideList()
    newNode = gL.append()
    effList = []
    for i in range(0, globals.Getk()):
        RestoreState(savedState)
        retcode = CallCommand_OperationalModel(cmd, cmdArgs)
        
        if retcode == 'Failure':
            effList.append(0)
            # No need to plan any further, it will always be 0
        else:
            firstTask, firstTaskArgs, pRoot = Reinitialize('command', GetState().copy(), newNode, gL, cmd, cmdArgs)
            
            try:
                do_task(firstTask, *firstTaskArgs)
            except Search_Done:
                pass
            except Failed_task:
                effList.append(0)
                continue

            tree = pRoot
            assert(planLocals.GetCurrentNode() == pRoot)
            
            effList.append(tree.GetEff())
    
    avgEff = TakeAvg(effList)
    bestTree = planLocals.GetBestTree()
    if ((bestTree == None or (avgEff > bestTree.GetEff())) and (avgEff > 0)):
        planLocals.SetBestTree(tree.copy())

    if avgEff == 0:
        pRoot = planLocals.GetPlanningTree()
        pRoot.SetEff(0)
        planLocals.SetCurrentNode(pRoot)
    raise Search_Done

def GetCost(cmd, cmdArgs):
    cost = DURATION.COUNTER[cmd.__name__]
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
        if globals.GetPlanningMode() == True:
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