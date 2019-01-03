from __future__ import print_function
import threading
from state import GetState, PrintState, RestoreState
import multiprocessing
import numpy
import random
import sys, pprint
import os
import globals
import colorama
import rTree
from timer import globalTimer, DURATION
from dataStructures import rL_APE, rL_PLAN
from APE_stack import print_entire_stack, print_stack_size
from helper_functions import *
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

# Both APE and APEplan
methods = {} # dictionary of the list of methods for every task, initialized once for every run via the domain file
path = {} # global variable shared by all stacks for debugging

# Only APE1
commands = {} # dictionary of commands, initialized once for every run via the domain file
apeLocals = rL_APE() # APE variables that are local to every stack

#only APEplan
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

def GetCommand(cmd):
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

def APE1(task, raeArgs):
    """
    APE1 is the actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
    raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
    """

    apeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
    apeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
    apeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                         # This is a dictionary to accomodate for commands with different costs.

    taskArgs = raeArgs.taskArgs   
    apeLocals.SetMainTask(task)
    apeLocals.SetMainTaskArgs(taskArgs) 
    InitializeTreeAPE1()

    global path                          # variable used for debugging
    path.update({apeLocals.GetStackId(): []})

    if verbose > 0:
        print('\n---- APE: Create stack {}, task {}{}\n'.format(apeLocals.GetStackId(), task, taskArgs))

    BeginCriticalRegion(apeLocals.GetStackId())

    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

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
        PrintState()

    if verbose > 0:
        print("\n---- APE: Done with stack %d\n" %apeLocals.GetStackId())

    if retcode == 'Failure':
        apeLocals.SetEfficiency(0)

    EndCriticalRegion()
    return (retcode, apeLocals.GetRetryCount(), apeLocals.GetCommandCount(), apeLocals.GetEfficiency())

def InitializeTreeAPE1():
    """
    Helper function for APE
    """
    aT = rTree.ActingTree()
    aT.SetPrevState(GetState().copy())
    apeLocals.SetActingTree(aT)
    apeLocals.SetEfficiency(float("inf"))

def InitializeRollout():
    """
    This is a helper function for APEplan
    When APE-plan is called for the first time, some parameters need to be initialized. 
    """

    root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
    planLocals.SetCurrentNode(root)
    planLocals.SetPlanningTree(root)

def APEplan(task, planArgs):
    """
    APEplan is the planner used by APE.
    The arguments of APEplan are same as APE.
    """

    planLocals.SetStackId(planArgs.GetStackId()) # Right now, the stack id is always set to 1 and is used to switch between 
                                                 # the main Simulation thread in testRAE.py and APEplan.
                                                 # This will be more useful if we decide to simulate multiple stacks in future
    taskArgs = planArgs.GetTaskArgs()
    
    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan

    planLocals.SetCandidates(planArgs.GetCandidates())  # only methods from this set will be tried
    if len(planArgs.GetCandidates()) == 1:
        tree = rTree.CreateFailureNode()
        return (tree, 0)
    
    InitializeRollout()

    global path   # for debugging
    path.update({planLocals.GetStackId(): []})


    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    try:
        resultTreeRoot = PlanTask(task, taskArgs)  # going GetChild because the root is just a node labelled 'root'
        resultTree = resultTreeRoot.GetChild()

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Failed command {}'.format(e))
        resultTree = rTree.CreateFailureNode()

    except Failed_task as e:
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Failed task {}'.format(e))
        resultTree = rTree.CreateFailureNode()
    else:
        pass
    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    return (resultTree, globalTimer.GetSimulationCounter())

def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    APE calls this functions when it wants suggestions from APE-plan
    """
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=APE.APEPlanMain, args=[task, taskArgs, queue, candidates])

    p.start()
    p.join()

    resultTree, simTime = queue.get()
    globalTimer.UpdateSimCounter(simTime)

    retcode = resultTree.GetRetcode()
    #resultTree.Print()
    if verbose > 0:
        print("Done with simulation. Result = {} \n".format(retcode), colorama.Style.RESET_ALL)

    #print("retcode is ", retcode)
    #resultTree.PrintInTerminal()
    if retcode == 'Failure':
        return (candidates[0], candidates[1:])
    else:
        m = resultTree.GetMethod()
        candidates.pop(candidates.index(m))
        return (m, candidates)

def choose_candidate(candidates, task, taskArgs):
    if globals.GetDoSampling() == False:
        #random.shuffle(candidates)
        return(candidates[0], candidates[1:])
    else:
        return GetCandidateByPlanning(candidates, task, taskArgs)

def GetBestTree(l):
    best = float("inf")
    for m in l:
        numberOfCommands = l[m].GetNumberOfCommands()
        if numberOfCommands < best:
            best = numberOfCommands
            bestTree = l[m]
    return bestTree

def PlanTask(task, taskArgs):
    if planLocals.GetCandidates() != None:
        # when candidates is a subset of the applicable methods, it is available from planLocals
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
    else:
        candidates = methods[task][:] # set of applicable methods
    
    solnFound = False
    result = {}

    for m in candidates:
        try:
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=PlanMethodNewProcess, args=[m, task, taskArgs, queue])
            p.start()
            p.join()
            tree = queue.get()
            if tree.GetRetcode() == 'Success':
                result[m.__name__] = tree
                solnFound = True
        except Failed_task as e:
            continue
        except Failed_command as e:
            continue

    if solnFound == True:
        bestTree = GetBestTree(result)
        RestoreState(bestTree.GetState())
        return bestTree
    else:
        raise Failed_task()

def PlanMethodNewProcess(m, task, taskArgs, queue):
    try:
        tree = PlanMethod(m, task, taskArgs)
    except Failed_task as e:
        tree = rTree.CreateFailureNode()
    except Failed_command as e:
        tree = rTree.CreateFailureNode()
    tree.SetState(GetState().copy())
    queue.put(tree)

def PlanMethod(m, task, taskArgs):
    global path
    path[planLocals.GetStackId()].append([task, taskArgs])

    savedNode = planLocals.GetCurrentNode()
    newNode = rTree.PlanningTree(m, taskArgs, 'method')
    savedNode.AddChild(newNode)
    planLocals.SetCurrentNode(newNode)

    retcode = CallMethod(planLocals.GetStackId(), m, taskArgs)

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

    retcode = 'Failure'
    try:
        if globals.GetPlanningMode() == False:
            EndCriticalRegion()
            BeginCriticalRegion(stackid)
        if verbose > 0:
            print_stack_size(stackid, path)
            print("Executing method {}{}".format(m.__name__, taskArgs))
        if verbose > 1:
            print_stack_size(stackid, path)
            print('Current state is:'.format(stackid))
            PrintState()

        m(*taskArgs)
        retcode = 'Success'
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

    parent, node = apeLocals.GetCurrentNodes()

    while (retcode != 'Success'):

        node.Clear()
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        node.SetLabelAndType(m, 'method')
        apeLocals.SetCurrentNode(node)
        retcode = CallMethod(apeLocals.GetStackId(), m, taskArgs)
        
        if candidates == []:
            break

        if retcode == 'Failure':
            apeLocals.SetRetryCount(apeLocals.GetRetryCount() + 1)
    
    apeLocals.SetCurrentNode(parent)
    path[apeLocals.GetStackId()].pop()

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
    cmdRet['state'] = cmdPtr(*cmdArgs)

def do_command(cmd, *cmdArgs):
    """
    Perform command cmd(cmdArgs).
    """
    if globals.GetPlanningMode() == True:
        return SimulateCommand(cmd, cmdArgs)
    else:
        return DoCommandInRealWorld(cmd, cmdArgs)

def GetCost(cmd, cmdArgs):
    assert(cmd.__name__ != "fail")
    cost = DURATION.COUNTER[cmd.__name__]
    return cost

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

    currentNode, child = apeLocals.GetCurrentNodes()
    child.SetLabelAndType(cmd, 'command')

    if verbose > 1:
        print_stack_size(apeLocals.GetStackId(), path)
        print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
        print_stack_size(apeLocals.GetStackId(), path)
        print('Current state is')
        print(state)

    path[apeLocals.GetStackId()].pop()

    if cmd.__name__ == "fail":
        cost = 20
    else:
        cost = GetCost(cmd, cmdArgs)
    eff = apeLocals.GetEfficiency()
    apeLocals.SetEfficiency(addEfficiency(eff, 1/cost))

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

    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if verbose > 0:
        print_stack_size(planLocals.GetStackId(), path)
        print('Begin command {}{}'.format(cmd.__name__, cmdArgs))

    cmdRet = {'state':'running'}
    cmdThread = threading.Thread(target=beginCommand, args = [cmd, cmdRet, cmdArgs])
    cmdThread.start()

    while (cmdRet['state'] == 'running'):
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Command {}{} is running'.format( cmd.__name__, cmdArgs))

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

    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    if retcode == 'Failure':
        raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
    elif retcode == 'Success':
        currNode = planLocals.GetCurrentNode()
        newNode = rTree.PlanningTree(cmd, cmdArgs, 'command')
        currNode.AddChild(newNode)
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

import APE