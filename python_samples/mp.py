from __future__ import print_function
__author__ = 'patras'
import os
import sys
import time
sys.path.append("../problems")
sys.path.append("../domains")
sys.path.append("..")
from multiprocessing import Process
from threading import Thread, local
import globals
common = None
threadList = []

def AddToList(t):
    threadList.append(t)

def SetCommon(a):
    global common
    common = a

def doubler(number):
    """
    A doubling function that can be used by a process
    """
    result = number * 2
    proc = os.getpid()
    print('{0} doubled to {1} by process id: {2}'.format(
        number, result, proc))

def test1():
    numbers = [5, 10, 15, 20, 25]
    procs = []

    for index, number in enumerate(numbers):
        proc = Process(target=doubler, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

def raeThread(p):
    global common
    print("rae = ", common)
    if p == True:
        mp2.TestThread(False)
        time.sleep(5)
    else:
        common = 'b'
        print("rae = ", common)
    print("Done rae ", common)

def raeProcess(p):
    global common
    print("pid, rae = ",os.getpid(), common)
    if p == True:
        #pass
        mp2.TestProcess(False)
        time.sleep(5)
    else:
        common = 'b'
        print("pid, rae = ", os.getpid(), common)
    print("Done rae ", common)

def raeProcessAndThread(p):
    print("pid = ",os.getpid())
    if p == True:
        #threadList[0].start()
        mp2.TestProcessAndThread(False)
        time.sleep(5)
    else:
        print("pid = ", os.getpid())
    print("Done rae ")

def raeFork(p):
    print("rae = ", common, os.getpid())
    if p == True:
        mp2.TestFork(False)
    else:
        print("rae = ", common, os.getpid())
    print("Done rae ", common, os.getpid())

def CheckGlobals():
    print("Global in mp:", globals.g.samplingMode)

import mp2