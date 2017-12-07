from __future__ import print_function
from rae1 import ipcArgs, envArgs, verbosity, rae1, ResetState, CleanState
import threading
import sys
sys.path.append('domains/')
sys.path.append('problems/')
import argparse

from timer import globalTimer, SetMode
import gui
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

def GetNewTask():
    '''
    :return: gets the new task that appears in the problem at the current time
    '''
    GetNewTask.counter += 1
    if GetNewTask.counter in domain_module.tasks:
        return domain_module.tasks[GetNewTask.counter]
    else:
        return []

def InitializeDomain(domain, problem):
    '''
    :param domain: code of the domain which you are running
    :param problem: id of the problem
    :return:none
    '''
    if domain in ['SF', 'CR', 'STE', 'SOD', 'SD', 'EE', 'IP']:
        module = problem + '_' + domain
        global domain_module
        domain_module = __import__(module)
        CleanState()
        domain_module.ResetState()
    else:
        print("Invalid domain\n", domain)
        exit(11)

def testRAE(domain, problem, doSampling):
    '''
    :param domain: the code of the domain
    :param problem: the problem id
    :param doSampling: bool value indicating whether to do sampling or not before executing the stacks
    :return:
    '''
    InitializeDomain(domain, problem)
    globals.SetDoSampling(doSampling)
    globals.SetSamplingMode(False) # sampling mode is required to switch between sampling and non-sampling states
    rM = threading.Thread(target=raeMult)
    rM.start()
    gui.start() # graphical user interface to show action executions
    rM.join()

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
    taskRes = rae1(raeArgs.task, raeArgs)
    taskInfo[stackid] = (raeArgs.taskArgs, taskRes.retcode)

def PrintResult(taskInfo):
    for stackid in taskInfo:
        args, res = taskInfo[stackid]
        print(stackid,'\t','Task {}{}'.format(args[0], args[1:]),'\t\t',res,'\n')

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
    GetNewTask.counter = 0
    StartEnv.counter = 0
    taskInfo = {}

    envArgs.sem = threading.Semaphore(1)
    envArgs.envActive = False
    envArgs.exit = False

    envThread = threading.Thread(target=StartEnv)
    envThread.start()


    while (True):
        if ipcArgs.nextStack == 0 or ipcArgs.threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()

            if numstacks == 0 or BeginFreshIteration(lastActiveStack, numstacks, ipcArgs.threadList) == True: # Check for incoming tasks after progressing all stacks

                taskParams = GetNewTask()
                if taskParams != []:

                    numstacks = numstacks + 1
                    raeArgs = globals.RaeArgs()
                    raeArgs.stack = numstacks
                    raeArgs.task = taskParams[0]
                    raeArgs.taskArgs = taskParams[1:]

                    ipcArgs.threadList.append(threading.Thread(target=CreateNewStack, args = (taskInfo, raeArgs)))
                    ipcArgs.threadList[numstacks-1].start()

                lastActiveStack = 0

                envArgs.envActive = True
                envArgs.sem.release()
                while(envArgs.envActive == True):
                    pass
                envArgs.sem.acquire()

                globalTimer.IncrementTime()

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
    if globals.GetSimulationMode() == 'on':
        print("----Done with RAE----\n")
        PrintResult(taskInfo)

def CreateNewStackSimulation(raeArgs):
    methodList = rae1(raeArgs.task, raeArgs)
    raeArgs.queue.put(methodList)

def raeMultSimulator(task, taskArgs, method, queue, candidateMethods):
    # Simulating one stack now
    # TODO: Simulate multiple stacks in future

    SetMode('Counter') #Counter mode in simulation
    globals.SetSamplingMode(True)
    ResetState()

    raeArgs = globals.RaeArgs()
    raeArgs.taskArgs = taskArgs
    raeArgs.stack = 1
    raeArgs.task = task
    raeArgs.candidates = candidateMethods
    raeArgs.method = method
    raeArgs.queue = queue

    ipcArgs.nextStack = 0
    ipcArgs.sem = threading.Semaphore(1)

    thread = threading.Thread(target=CreateNewStackSimulation, args=[raeArgs])

    thread.start()

    while(True):
        if ipcArgs.nextStack == 0 or thread.isAlive() == False:
            ipcArgs.sem.acquire()
            globalTimer.IncrementTime()
            if thread.isAlive() == False:
                break
            else:
                ipcArgs.nextStack = 1
                ipcArgs.sem.release()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--v", help="verbosity of RAE's debugging output (0, 1 or 2)",
                           type=int, default=0, required=False)
    argparser.add_argument("--d", help="name of the test domain (STE, CR, SD, EE, SOD, IP or SF)",
                           type=str, default='STE', required=False)
    argparser.add_argument("--p", help="identifier for the problem eg. 'problem1', 'problem2', etc",
                           type=str, default="problem1", required=False)
    argparser.add_argument("--s", help="Do you want to use sampling or not? ('y' or 'n')",
                           type=str, default='y', required=False)
    argparser.add_argument("--c", help="Mode of the clock ('Counter' or 'Clock')",
                           type=str, default='Counter', required=False)
    argparser.add_argument("--simMode", help="Mode of simulation output ('on' or 'off')",
                           type=str, default='on', required=False)
    argparser.add_argument("--lazy", help="Whether to do lazy lookahead? ('y' or 'n')",
                           type=str, default='n', required=False)
    argparser.add_argument("--concurrent", help="Whether to do concurrent lookahead? ('y' or 'n')",
                           type=str, default='n', required=False)

    args = argparser.parse_args()

    if args.s == 'y':
        s = True
    else:
        s = False

    globals.SetLazy(args.lazy)
    globals.SetConcurrent(args.concurrent)
    verbosity(args.v)
    SetMode(args.c)
    globals.SetSimulationMode(args.simMode)
    testRAE(args.d, args.p, s)