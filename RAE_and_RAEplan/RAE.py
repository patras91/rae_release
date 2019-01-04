from __future__ import print_function
from RAE1_and_RAEplan import ipcArgs, envArgs, RAE1, RAEplanChoice
from dataStructures import PlanArgs
from timer import globalTimer, SetMode
#from time import time
from state import ReinitializeState, RemoveLocksFromState
import threading
import globals

__author__ = 'patras'

domain_module = None

def GetNextAlive(lastActiveStack, numstacks, threadList):
    '''
    :param lastActiveStack: the stack which was progressed before this
    :param numstacks: total number of stacks in the Agenda
    :param threadList: list of all the threads, each running a RAE stack
    :return: The stack which should be executed next
    '''
    nextAlive = -1
    i = 1
    j = lastActiveStack % numstacks + 1
    while i <= numstacks:
        if threadList[j-1].isAlive() == True:
            nextAlive = j
            break
        i = i + 1
        j = j % numstacks + 1

    return nextAlive

def GetNewTasks():
    '''
    :return: gets the new task that appears in the problem at the current time
    '''
    GetNewTasks.counter += 1
    if GetNewTasks.counter in domain_module.tasks:
        return domain_module.tasks[GetNewTasks.counter]
    else:
        return []

def InitializeDomain(domain, problem):
    '''
    :param domain: code of the domain which you are running
    :param problem: id of the problem
    :return:none
    '''
    if domain in ['CR', 'SD', 'EE', 'IP', 'PD', 'SR', 'SDN', 'test']:
        module = problem + '_' + domain
        global domain_module
        ReinitializeState()    # useful for batch runs to start with the first state
        domain_module = __import__(module)
        domain_module.ResetState()
        return domain_module
    else:
        print("Invalid domain\n", domain)
        exit(11)

def BeginFreshIteration(lastActiveStack, numstacks, threadList):
    begin = True
    i = lastActiveStack % numstacks + 1
    while i != 1:
        if threadList[i - 1].isAlive() == True:
            begin = False
            break
        i = i % numstacks + 1
    return begin

def CreateNewStack(taskInfo, raeArgs):
    stackid = raeArgs.stack
    retcode, retryCount, eff = RAE1(raeArgs.task, raeArgs)
    taskInfo[stackid] = ([raeArgs.task] + raeArgs.taskArgs, retcode, retryCount, eff)

def PrintResult(taskInfo):
    for stackid in taskInfo:
        args, res, retryCount, eff = taskInfo[stackid]
        print(stackid,'\t','Task {}{}'.format(args[0], args[1:]),'\t\t',res,'\t\t', retryCount, '\t\t', eff, '\n')

def PrintResultSummary(taskInfo):
    succ = 0
    fail = 0
    retries = 0
    effTotal = 0
    for stackid in taskInfo:
        args, res, retryCount, eff = taskInfo[stackid]
        if res == 'Success':
            succ += 1
        else:
            fail += 1
        retries += retryCount
        effTotal += eff
    print(succ, succ+fail, retries, globalTimer.GetSimulationCounter(), globalTimer.GetRealCommandExecutionCounter(), effTotal)
    #print(' '.join('-'.join([key, str(cmdNet[key])]) for key in cmdNet))

def StartEnv():
    while(True):
        while(envArgs.envActive == False):
            pass
        envArgs.sem.acquire()
        if envArgs.exit == True:
            return

        StartEnv.counter += 1
        if StartEnv.counter in domain_module.eventsEnv:
            eventArgs = domain_module.eventsEnv[StartEnv.counter]
            event = eventArgs[0]
            eventParams = eventArgs[1]
            t = threading.Thread(target=event, args=eventParams)
            t.setDaemon(True)  # Setting the environment thread to daemon because we don't want the environment running once the tasks are done
            t.start()
        envArgs.envActive = False
        envArgs.sem.release()

def raeMult():
    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task
    ipcArgs.threadList = [] #keeps track of all the stacks in RAE Agenda
    lastActiveStack = 0 #keeps track of the last stack that was Progressed
    numstacks = 0 #keeps track of the total number of stacks
    GetNewTasks.counter = 0
    StartEnv.counter = 0
    taskInfo = {}

    envArgs.sem = threading.Semaphore(1)
    envArgs.envActive = False
    envArgs.exit = False

    envThread = threading.Thread(target=StartEnv)
    #startTime = time()
    envThread.start()


    while (True):
        if ipcArgs.nextStack == 0 or ipcArgs.threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()

            if numstacks == 0 or BeginFreshIteration(lastActiveStack, numstacks, ipcArgs.threadList) == True: # Check for incoming tasks after progressing all stacks

                taskParams = GetNewTasks()
                if taskParams != []:

                    for newTask in taskParams:
                        numstacks = numstacks + 1
                        raeArgs = globals.RaeArgs()
                        raeArgs.stack = numstacks
                        raeArgs.task = newTask[0]
                        raeArgs.taskArgs = newTask[1:]

                        ipcArgs.threadList.append(threading.Thread(target=CreateNewStack, args = (taskInfo, raeArgs)))
                        ipcArgs.threadList[numstacks-1].start()

                lastActiveStack = 0 # for the environment

                envArgs.envActive = True
                envArgs.sem.release()
                while(envArgs.envActive == True):
                    pass
                envArgs.sem.acquire()

                globalTimer.IncrementTime()

            if numstacks > 0:
                res = GetNextAlive(lastActiveStack, numstacks, ipcArgs.threadList)

                if res != -1:
                    ipcArgs.nextStack = res
                    lastActiveStack = res
                    ipcArgs.sem.release()
                else:
                    envArgs.envActive = True
                    envArgs.exit = True
                    envArgs.sem.release()
                    break
            else:
                ipcArgs.sem.release()

    if globals.GetShowOutputs() == 'on':
        print("----Done with RAE----\n")
        PrintResult(taskInfo)
    else:
        PrintResultSummary(taskInfo)
        #globalTimer.Callibrate(startTime)

    return taskInfo # for unit tests

def CreateNewStackSimulation(pArgs, queue):
    tree, planningTime = RAEplanChoice(pArgs.GetTask(), pArgs)
    queue.put((tree, planningTime))

def RAEPlanMain(task, taskArgs, queue, candidateMethods, state, gL):
    # Simulating one stack now
    # TODO: Simulate multiple stacks in future

    SetMode('Counter') #Counter mode in simulation
    globals.SetPlanningMode(True)
    RemoveLocksFromState()

    pArgs = PlanArgs()
    pArgs.SetTaskArgs(taskArgs)
    pArgs.SetStackId(1)
    pArgs.SetTask(task)
    pArgs.SetCandidates(candidateMethods)
    pArgs.SetGuideList(gL)
    pArgs.SetState(state)

    ipcArgs.nextStack = 0
    ipcArgs.sem = threading.Semaphore(1)

    thread = threading.Thread(target=CreateNewStackSimulation, args=[pArgs, queue])

    thread.start()
    thread.join()
    #while(True):
    #    if ipcArgs.nextStack == 0 or thread.isAlive() == False:
    #        ipcArgs.sem.acquire()
    #        globalTimer.IncrementTime()
    #        if thread.isAlive() == False:
    #            break
    #        else:
    #            ipcArgs.nextStack = 1
    #           ipcArgs.sem.release()