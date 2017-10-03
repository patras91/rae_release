from __future__ import print_function
from rae1 import ipcArgs, verbosity, rae1, ResetState
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
    GetNewTask.counter += 1
    if GetNewTask.counter in domain_module.tasks:
        return domain_module.tasks[GetNewTask.counter]
    else:
        return []

def InitializeDomain(domain, problem):
    if domain in ['SF', 'CR', 'STE', 'SOD', 'SD', 'EE', 'IP']:
        module = problem + '_' + domain
        global domain_module
        domain_module = __import__(module)
    else:
        print("Invalid domain\n")
        exit(11)

def testRAE(domain, problem, doSampling):
    InitializeDomain(domain, problem)
    globals.SetDoSampling(doSampling)
    globals.SetSamplingMode(False)
    rM = threading.Thread(target=raeMult)
    rM.start()
    gui.start()
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

def CreateNewStack(taskInfo, taskArgs):
    stackid = taskArgs[-1]
    taskRes = rae1(*taskArgs)
    taskInfo[stackid] = (taskArgs[0:-1], taskRes.retcode)

def PrintResult(taskInfo):
    for stackid in taskInfo:
        args, res = taskInfo[stackid]
        print(stackid,'\t','Task {}{}'.format(args[0], args[1:]),'\t\t',res,'\n')

def raeMult():
    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task
    ipcArgs.threadList = [] #keeps track of all the stacks in RAE Agenda
    lastActiveStack = 0 #keeps track of the last stack that was Progressed
    numstacks = 0 #keeps track of the total number of stacks
    GetNewTask.counter = 0
    taskInfo = {}

    while (True):
        if ipcArgs.nextStack == 0 or ipcArgs.threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()

            if numstacks == 0 or BeginFreshIteration(lastActiveStack, numstacks, ipcArgs.threadList) == True: # Check for incoming tasks after progressing all stacks
                taskArgs = GetNewTask()
                if taskArgs != []:
                    numstacks = numstacks + 1
                    taskArgs.append(numstacks)
                    ipcArgs.threadList.append(threading.Thread(target=CreateNewStack, args = (taskInfo, taskArgs)))
                    ipcArgs.threadList[numstacks-1].start()
                lastActiveStack = 0
                globalTimer.IncrementTime()

            res = GetNextAlive(lastActiveStack, numstacks, ipcArgs.threadList)
            if res != -1:
                ipcArgs.nextStack = res
                lastActiveStack = res
                ipcArgs.sem.release()
            else:
                break
    print("----Done with RAE----\n")
    PrintResult(taskInfo)

def CreateNewStackSimulation(queue, taskArgs):
    taskRes = rae1(*taskArgs)
    queue.put(taskRes)

def raeMultSimulator(task, taskArgs, method, queue):
    # Simulating one stack now
    # TODO: Simulate multiple stacks in future

    SetMode('Counter') #Counter mode in simulation
    globals.SetSamplingMode(True)
    ResetState()

    if callable(method):
        taskArgs = [task] + list(taskArgs) + [method] + [1]
    else:
        taskArgs = [task] + list(taskArgs) + [1]

    ipcArgs.nextStack = 0
    ipcArgs.sem = threading.Semaphore(1)

    thread = threading.Thread(target=CreateNewStackSimulation, args=[queue, taskArgs])

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

    args = argparser.parse_args()

    if args.s == 'y':
        s = True
    else:
        s = False

    verbosity(args.v)
    SetMode(args.c)
    testRAE(args.d, args.p, s)