from __future__ import print_function
__author__ = 'patras'

import mp
import threading
import multiprocessing
import os
import time
import globals

def TestThread(p):
    print("testing thread ", mp.common)
    a = threading.Thread(target=mp.raeThread, args=[p])
    time.sleep(5)
    a.start()
    a.join()

def TestProcess(p):
    print("testing Process ", mp.common)
    a = multiprocessing.Process(target=mp.raeProcess, args=[p])
    time.sleep(5)
    print("after", mp.common)
    a.start()
    a.join()

def TestFork(p):
    if p == True:
        newpid = os.fork()
        if newpid == 0:
            mp.common = 'b'
            mp.raeFork(False)
        else:
            time.sleep(5)
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d\n" % pids)
            mp.raeFork(p)
    else:
        mp.raeFork(p)

def thread1():
    while(True):
        print("pid ", os.getpid())
        time.sleep(2)

def TestProcessAndThread(p):
    a = multiprocessing.Process(target=mp.raeProcessAndThread, args=[p])
    time.sleep(5)
    a.start()
    a.join()

def TestGlobalVars():
    globals.SetSamplingMode(True)
    print("In mp2, ", globals.g.samplingMode)
    mp.CheckGlobals()

if __name__=="__main__":
    mp.SetCommon('a')
    #TestThread(True)
    #TestProcess(True)
    #TestFork(True)

    #b = threading.Thread(target=thread1)
    #mp.AddToList(b)
    #b.start()
    #TestProcessAndThread(True)

    TestGlobalVars()