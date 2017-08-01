
from __future__ import print_function
import domain_ste
import domain_simpleFetch
import domain_chargeableRobot
import domain_simpleOpenDoor
import domain_springDoor
import domain_exploreEnv
from rae1 import ipcArgs, verbosity, rae1
import threading
import sys
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

def GetNewTask(domain):
    GetNewTask.counter += 1
    task = {
        'STE': {
            1: ['travel', 'Dana', 'home', 'park'],
            2: ['travel','Paolo','home','park'],
            3: ['travel','Malik','home2','park2']
        },
        'CR' : {
            1: ['fetch', 'r1', 'o1'],
            2: ['fetch', 'r1', 'o2'],
            3: ['relocateCharger', 'c1', 8]
        },
        'SF' : {
            1: ['fetch', 'r1', 'o1'],
            2: ['fetch', 'r1', 'o2'],
            3: ['emergency', 'r1', 2, 1]
        },
        'SOD' : {
            1: ['openDoor', 'r1', 'd1', 'o1'],
            2: ['openDoor', 'r2', 'd2', 'o2']
        },
        'SD' : {
            1: ['fetch', 'r1', 'o1', 5],
            2: ['closeDoors']
        },
        'EE' : {
            1: ['explore', 'UAV', 'survey', 'z1'],
            2: ['explore', 'UAV', 'sample', 'z3'],
            3: ['explore', 'r1', 'process', 'z5']
        }
    }
    if GetNewTask.counter in task[domain]:
        return task[domain][GetNewTask.counter]
    else:
        return []

def testRAE(domain):
    if domain == 'SF':
        domain_simpleFetch.simpleFetch_init()
    elif domain == 'CR':
        domain_chargeableRobot.chargeableRobot_init()
    elif domain == 'STE':
        domain_ste.ste_init()
    elif domain == 'SOD':
        domain_simpleOpenDoor.simpleOpenDoor_init()
    elif domain == 'SD':
        domain_springDoor.springDoor_init()
    elif domain == 'EE':
        domain_exploreEnv.exploreEnv_init()
    else:
        print("Invalid domain\n")
        return

    rM = threading.Thread(target=raeMult, args=[domain])
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

def raeMult(domain):
    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task

    threadList = [] #keeps track of all the stacks in RAE Agenda
    lastActiveStack = 0 #keeps track of the last stack that was Progressed
    numstacks = 0 #keeps track of the total number of stacks
    GetNewTask.counter = 0

    while (True):
        if ipcArgs.nextStack == 0 or threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()

            if numstacks == 0 or BeginFreshIteration(lastActiveStack, numstacks, threadList) == True: # Check for incoming tasks after progressing all stacks
                taskArgs = GetNewTask(domain)
                if taskArgs != []:
                    numstacks = numstacks + 1
                    taskArgs.append(numstacks)
                    threadList.append(threading.Thread(target=rae1, args = taskArgs))
                    threadList[numstacks-1].start()
                globalTimer.IncrementTime()

            res = GetNextAlive(lastActiveStack, numstacks, threadList)
            if res != -1:
                ipcArgs.nextStack = res
                lastActiveStack = res
                ipcArgs.sem.release()
            else:
                break
    print("----Done with RAE----\n")