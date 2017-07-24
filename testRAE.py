
from __future__ import print_function
import domain_ste
import domain_simpleFetch
import domain_chargeableRobot
import domain_simpleOpenDoor
import domain_springDoor
from rae1 import ipcArgs, verbosity, rae1
import threading
import sys

__author__ = 'patras'

def GetNextAlive(nextStack, NUMSTACKS, threadList):
    nextAlive = -1
    i = 1
    j = nextStack
    while i <= NUMSTACKS:
        if threadList[j-1].isAlive() == True:
            nextAlive = j
            break
        i = i + 1
        j = j % NUMSTACKS + 1

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
    }
    if GetNewTask.counter in task[domain]:
        return task[domain][GetNewTask.counter]
    else:
        return []

def testRAE(domain):

    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task

    threadList = []
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
    else:
        print("Invalid domain\n")
        return

    nextStack = 1
    NUMSTACKS = 0
    GetNewTask.counter = 0

    while (True):
        if ipcArgs.nextStack == 0 or threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()
            if nextStack == 1: # Check for incoming tasks after progressing each stack
                taskArgs = GetNewTask(domain)
                if taskArgs != []:
                    NUMSTACKS = NUMSTACKS + 1
                    taskArgs.append(NUMSTACKS)
                    threadList.append(threading.Thread(target=rae1, args = taskArgs))
                    threadList[NUMSTACKS-1].start()

            res = GetNextAlive(nextStack, NUMSTACKS, threadList)
            if res != -1:
                ipcArgs.nextStack = res
                nextStack = res % NUMSTACKS + 1
                ipcArgs.sem.release()
            else:
                break