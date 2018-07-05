from __future__ import print_function
import threading
from state import GetState, PrintState, RestoreState
import multiprocessing
import numpy
import random

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

def RAE1(task, raeArgs):
    """
    APE is the actor with a single execution stack. The first argument is the name (which
    should be a string) of the task to accomplish, and raeArgs are the arguments for the task and other stack parameters.
    raeArgs has a stack id, stack, and parameters to the task, taskArgs. 
    """

    raeLocals.SetStackId(raeArgs.stack)  # to keep track of the id of the current stack.
    raeLocals.SetRetryCount(0)           # to keep track of the number of retries in the current stack. This is used to calculate retry ratio
    raeLocals.SetCommandCount({})        # to keep track of the number of instances of every commands executed. Used to calculate the speed to success
                                         # This is a dictionary to accomodate for commands with different costs.

    taskArgs = raeArgs.taskArgs   
    raeLocals.SetMainTask(task)
    raeLocals.SetMainTaskArgs(taskArgs) 
    InitializeActingTree()

    global path                          # variable used for debugging
    path.update({raeLocals.GetStackId(): []})

    #raeLocals.SetRefinementList(None)    # used in lazy and concurrent modes
    #if globals.GetConcurrentMode() == True:
    #    raeLocals.SetConcManagerList([])  #concurrent manager keeps tracks of the threads in concurrent mode

    if verbose > 0:
        print('\n---- APE: Create stack {}, task {}{}\n'.format(raeLocals.GetStackId(), task, taskArgs))

    BeginCriticalRegion(raeLocals.GetStackId())

    if verbose > 1:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    try:
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

def InitializeActingTree():
    """
    Helper function for RAE1
    """
    root = rTree.ActingTree('root')
    raeLocals.SetCurrentNode(root)
    raeLocals.SetRootNode(root)
    root.SetNextState(GetState().copy())

def GetCandidateByPlanning(candidates, task, taskArgs):
    """
    APE calls this functions when it wants suggestions from APE-plan
    """
    if verbose > 0:
        print(colorama.Fore.RED, "Starting simulation for stack")

    queue = multiprocessing.Queue()
    actingTree = raeLocals.GetRootNode()
    #tree.Print()
    
    #print("Calling APE-plan for ", raeLocals.GetMainTask())
    p = multiprocessing.Process(target=RAE.RAEPlanMain, args=[raeLocals.GetMainTask(), raeLocals.GetMainTaskArgs(), queue, candidates, actingTree])

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
        indexToLook = actingTree.GetSize() - 1 
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
    global path # for debugging
    path[raeLocals.GetStackId()].append([task, taskArgs])

    if verbose > 0:
        print_stack_size(raeLocals.GetStackId(), path)
        print('Begin task {}{}'.format(task, taskArgs))

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    retcode = None
    candidates = methods[task][:]

    parent = raeLocals.GetCurrentNode()
    if parent.GetLabel() == 'root':
        currentNode = parent
    else:
        currentNode = parent.AddChild()
    
    while (retcode != 'Success' and candidates != []):
        if retcode == 'Failure':
            raeLocals.SetRetryCount(raeLocals.GetRetryCount() + 1)
        currentNode.Clear()
        (m,candidates) = choose_candidate(candidates, task, taskArgs)
        if m != None:
            currentNode.SetLabelAndType(m, 'method')
            raeLocals.SetCurrentNode(currentNode)
            retcode = CallMethod(raeLocals.GetStackId(), m, taskArgs)

    raeLocals.SetCurrentNode(parent)
    path[raeLocals.GetStackId()].pop()

    if verbose > 1:
        print_entire_stack(raeLocals.GetStackId(), path)

    if retcode == 'Failure' or retcode == None:
        raise Failed_task('{}{}'.format(task, taskArgs))
    elif retcode == 'Success':
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))


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

    taskArgs = planArgs.GetTaskArgs()
    
    globalTimer.ResetSimCounter()           # SimCounter keeps track of the number of ticks for every call to APE-plan
    
    
    actingTree = planArgs.GetActingTree() # which is basically the stack in the pseudocode
    startState = actingTree.GetNextState()
    RestoreState(startState)
    planLocals.SetActingTree(actingTree)
    planLocals.SetActingTreeCurrPtr(actingTree)
    
    global path   # for debugging
    path.update({planLocals.GetStackId(): []})
        
    root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
    planLocals.SetCurrentNode(root)
    planLocals.SetPlanningTree(root)
    
    guideRoot = rTree.GuideTree('root')
    planLocals.SetGuideNode(guideRoot)
    planLocals.SetGuideTree(guideRoot)

    planLocals.SetBestTree(None)

    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Initial state is:')
        PrintState()

    try:
        PlanTask(task, taskArgs) 
        plannedTree = planLocals.GetBestTree().GetChild() # doing GetChild because the root is just a node labelled 'root'

    except Failed_command as e:
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Failed command {}'.format(e))
        plannedTree = rTree.CreateFailureNode()

    except Failed_task as e:
        if verbose > 0:
            print_stack_size(planLocals.GetStackId(), path)
            print('Failed task {}'.format(e))
        plannedTree = rTree.CreateFailureNode()
    else:
        pass
    if verbose > 1:
        print_stack_size(planLocals.GetStackId(), path)
        print('Final state is:')
        PrintState()

    return (plannedTree, globalTimer.GetSimulationCounter())
    
def ChooseRandom(l):
    random.shuffle(l)
    return l[0]

def GetCandidates(task):
    if planLocals.GetCandidates() != None:
        # when candidates is a subset of the applicable methods, it is available from planLocals
        candidates = planLocals.GetCandidates()[:]
        planLocals.SetCandidates(None) # resetting planLocals for the rest of the search
    else:
        candidates = methods[task][:] # set of applicable methods
    
    b = globals.Getb()
    cand = candidates[0:min(b - 1, len(candidates))]
    return cand

def PlanTask(task, taskArgs):

    actingTreeCurrPtr = planLocals.GetActingTreeCurrPtr()

    if actingTreeCurrPtr == None or actingTreeCurrPtr.GetLabel() == None: 
        
        # done catching up with the acting stack, it is time to start planning/continue planning
            
        currNode = planLocals.GetCurrentNode()
        guideNode = planLocals.GetGuideNode()
        nextNode = guideNode.GetSuccessor() # successor of the current guide node is the possible task Node
        
        # checking whether a task node has already been created in the guide
        if nextNode != None:
            m = nextNode.GetLabel()
            planLocals.SetGuideNode(nextNode)
            tree = PlanMethod(m, task, taskArgs)
            return tree
        else:
            # Need to look through several candidates for this task
            cand = GetCandidates(task)

            # TODO : Can do pruning here if efficiency is already lower

            newNode = guideNode.AddChild()
            
            pRoot = planLocals.GetPlanningTree()
            if pRoot.children == []:
                firstTask = task
                firstTaskArgs = taskArgs
            else:
                firstTask = pRoot.GetChild().GetLabel()
                firstTaskArgs = pRoot.GetChild().GetArgs()
            
            print(cand)
            for m in cand:

                newNode.Clear()
                newNode.SetLabel(m)    
                pRoot.DeleteAllChildren()
                pRoot.SetEff(float("inf"))
                planLocals.SetCurrentNode(pRoot)
                planLocals.SetGuideNode(planLocals.GetGuideTree())
                
                startState = planLocals.GetActingTree().GetNextState()
                RestoreState(startState)

                tree = PlanTask(firstTask, firstTaskArgs) # to recreate the execution stack
                print("For the following guide, the best tree is ")
                planLocals.GetGuideTree().Print()
                tree.PrintInTerminal()

                bestTree = planLocals.GetBestTree()
                if bestTree != None:
                    bestEff = bestTree.GetEff()
                else:
                    bestEff = 0

                if tree.GetEff() > bestEff:
                    bestEff = tree.GetEff()
                    bestTree = tree.copy()
                    planLocals.SetBestTree(bestTree)

            guideNode.DeleteChild(newNode)
            planLocals.SetGuideNode(guideNode)
            planLocals.SetCurrentNode(currNode)


            return bestTree
    else: 
        # still catching up with the acting tree
        m = actingTreeCurrPtr.GetLabel()
        oldGuide = planLocals.GetGuideNode()
        gC = oldGuide.AddChild()
        gC.SetLabel(m)
        planLocals.SetGuideNode(gC)
        planLocals.SetActingTreeCurrPtr(actingTreeCurrPtr.GetSuccessor())
        tree = PlanMethod(m, task, taskArgs)
        #planLocals.SetGuideNode(oldGuide)
        return tree

def addEfficiency(e1, e2):
    if e1 == float("inf"):
        return e2
    elif e2 == float("inf"):
        return e1
    else:
        return e1 * e2 / (e1 + e2)

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
        newEff = addEfficiency(savedNode.GetEff(), newNode.GetEff())
        savedNode.SetEff(newEff)
        planLocals.SetCurrentNode(savedNode)
        return savedNode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, m, taskArgs))

def beginCommand(cmd, cmdRet, cmdArgs):
    cmdPtr = GetCommand(cmd)
    #if globals.GetPlanningMode() == True:
    #    if cmd in listCommandsDependingOnParams:
    #        # this code is specific for sensing command, 'perceive'
    #        loc = cmdArgs[0]
    #        pDict = commandProb[cmd][loc]
    #        res = []
    #        for obj in pDict:
    #            outcome = numpy.random.choice(len(pDict[obj]), 1, p=pDict[obj])
    #            if outcome[0] == 0:
    #                res.append(obj)
    #    else:
    #        pFunc = commandProb[cmd]
    #        p = pFunc(*cmdArgs)
    #        outcome = numpy.random.choice(len(p), 1, p=p)
    #        res = outcome[0]
    #    cmdArgs = cmdArgs + (res,)
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

    currentNode = raeLocals.GetCurrentNode()
    newChild = currentNode.AddChild()
    newChild.SetLabelAndType(cmd, 'command')
    newChild.SetNextState(GetState().copy())

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

def SimulateCommand(cmd, cmdArgs):
    global path
    path[planLocals.GetStackId()].append([cmd, cmdArgs])

    if verbose > 1:
        print_entire_stack(planLocals.GetStackId(), path)

    currNode = planLocals.GetActingTreeCurrPtr()
    if currNode == None or currNode.GetLabel() == None:
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
    else:
        RestoreState(currNode.GetNextState())
        planLocals.SetActingTreeCurrPtr(currNode.GetSuccessor())
        retcode = 'Success'

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
        cost = GetCost(cmd, cmdArgs)
        newNode = rTree.PlanningTree(cmd, cmdArgs, 'cmd')
        planLocals.GetCurrentNode().AddChild(newNode)
        planLocals.GetCurrentNode().AddEfficiency(1/cost)
        return retcode
    else:
        raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))

def GetCost(cmd, cmdArgs):
    cost = DURATION.COUNTER[cmd.__name__]
    return cost

import RAE