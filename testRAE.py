
from __future__ import print_function
import ste
import threading
import sys

__author__ = 'patras'

class ipcArgs():
	"""A state is just a collection of variable bindings."""
	def __init__(self):
		pass

ste.ste_init()

stack1 = ipcArgs()
stack2 = ipcArgs()
stack3 = ipcArgs()

stack1.master = threading.Semaphore(0)
stack2.master = threading.Semaphore(0)
stack3.master = threading.Semaphore(0)

stack1.sem = threading.Semaphore(0)
stack2.sem = threading.Semaphore(0)
stack3.sem = threading.Semaphore(0)

stack1.id = 1
stack2.id = 2
stack3.id = 3

thread1 = threading.Thread(target = ste.ste_run_travel1, args=(stack1,))
thread1.start()
thread2 = threading.Thread(target = ste.ste_run_travel2, args=(stack2,))
thread2.start()
thread3 = threading.Thread(target = ste.ste_run_travel3, args=(stack3,))
thread3.start()

for x in range(0, 10):
    if thread1.is_alive:
        stack1.sem.release()
        print("waiting for master 1\n")
        sys.stdout.flush()
        stack1.master.acquire()
        print("got master 1\n")
        sys.stdout.flush()

    if thread2.is_alive:
        stack2.sem.release()
        print("waiting for master 2\n")
        sys.stdout.flush()
        stack2.master.acquire()
        print("got master 2\n")
        sys.stdout.flush()

    if thread3.is_alive:
        stack3.sem.release()
        print("waiting for master 3\n")
        sys.stdout.flush()
        stack3.master.acquire()
        print("got master 3\n")
        sys.stdout.flush()