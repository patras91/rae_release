from __future__ import print_function
from rae1 import ipcArgs, verbosity, rae1
import threading
import sys
sys.path.append('domains/')
sys.path.append('problems/')

from timer import globalTimer, SetMode
import gui

__author__ = 'patras'

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
    global mod
    if GetNewTask.counter in mod.tasks:
        return mod.tasks[GetNewTask.counter]
    else:
        return []

def InitializeDomain(domain, problem):
    if domain in ['SF', 'CR', 'STE', 'SOD', 'SD', 'EE', 'IP']:
        module = problem + '_' + domain
        global mod
        mod = __import__(module)
    else:
        print("Invalid domain\n")
        exit(11)

def testRAE(domain, problem):
    InitializeDomain(domain, problem)
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
    taskInfo[stackid] = (taskArgs[0:-1], taskRes)

def PrintResult(taskInfo):
    for stackid in taskInfo:
        args, res = taskInfo[stackid]
        print(stackid,'\t','Task {}{}'.format(args[0], args[1:]),'\t\t',res,'\n')

def raeMult():
    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task

    threadList = [] #keeps track of all the stacks in RAE Agenda
    lastActiveStack = 0 #keeps track of the last stack that was Progressed
    numstacks = 0 #keeps track of the total number of stacks
    GetNewTask.counter = 0
    taskInfo = {}

    while (True):
        if ipcArgs.nextStack == 0 or threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()

            if numstacks == 0 or BeginFreshIteration(lastActiveStack, numstacks, threadList) == True: # Check for incoming tasks after progressing all stacks
                taskArgs = GetNewTask()
                if taskArgs != []:
                    numstacks = numstacks + 1
                    taskArgs.append(numstacks)
                    threadList.append(threading.Thread(target=CreateNewStack, args = (taskInfo, taskArgs)))
                    threadList[numstacks-1].start()
                lastActiveStack = 0
                globalTimer.IncrementTime()

            res = GetNextAlive(lastActiveStack, numstacks, threadList)
            if res != -1:
                ipcArgs.nextStack = res
                lastActiveStack = res
                ipcArgs.sem.release()
            else:
                break
    print("----Done with RAE----\n")
    PrintResult(taskInfo)