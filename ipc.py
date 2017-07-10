__author__ = 'patras'

'''This is a simple example of multi-threading in python'''

import threading
import time
import sys

'''class Stack(object):

    def __init__(self):
        self.top = -1
        self.ptr = -1
        self.list = []

    def push(self, item):
        self.list.append(item)'''

def a():
    a_1()
    execute("a_2", 1)
    execute("a_3", 1)
    return

def a_1():
    a_1_1()
    execute("a_1_2", 1)
    return

def a_1_1():
    execute("a_1_1_1_1", 1)
    execute("a_1_1_1_2", 1)

def b():
    execute("b_1", 2)
    b_2()
    execute("b_3", 2)
    return

def b_1():
    execute("b_1_1", 2)
    execute("b_1_2", 2)

def b_2():
    execute("b_2_1", 2)
    execute("b_2_2", 2)

def execute(command, stackid):
    (sem, master) = {
        1: (sem1, master1),
        2: (sem2, master2),
    }[stackid]

    sem.acquire()
    print "Executing %s %d %d\n" % (command, sem._Semaphore__value, master._Semaphore__value)
    sys.stdout.flush()
    #time.sleep(2)
    master.release()

master1 = threading.Semaphore(0)
master2 = threading.Semaphore(0)
sem1 = threading.Semaphore(0)
sem2 = threading.Semaphore(0)

def test():
   # s = [Stack(), Stack()]
   # s[0].push(a)
   # s[1].push(b)

    stack1 = threading.Thread(target = a)
    stack1.start()
    stack2 = threading.Thread(target = b)
    stack2.start()

    for x in range(0, 10):
        print x
        sys.stdout.flush()
        sem1.release()
        master1.acquire()
        sem2.release()
        master2.acquire()

def modify(var):
    var.value = 4

class Var(object):
    def __init__(self):
        pass

def passToFunc():
    var = Var()
    var.value = 5
    modify(var)
    print var.value
