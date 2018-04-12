__author__ = 'patras'

import os
import multiprocessing

def TestFork():
    q = multiprocessing.Queue()
    count = 0
    while (True):
        pid = os.fork()

        if pid == 0:
            count += 1
            print(count)
            q.put('a')
        else:
            print("main")
            print(q.get())

if __name__=="__main__":
    TestFork()
    print("b")