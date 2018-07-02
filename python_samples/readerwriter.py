__author__ = 'patras'
'''This file illustrates how we simulate commands'''

import threading
import time

def master():
    commandReturn = {'state':'running'}
    t = threading.Thread(target=beginCommand, args = [slave, commandReturn, 1])
    t.start()
    while(t.isAlive()):
        print("Current state is %s" %commandReturn)
    print("Result is %s\n" %commandReturn)

def beginCommand(cName, cmdRet, cmdArgs):

    cmdRet['state'] = cName(cmdArgs)

def slave(a):
    print("starting %d...\n" %a)
    time.sleep(5)
    print("...ending %d\n" %a)
    return 'success'

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv:
        while cv.wait():
            logging.debug('Consumer waiting ...')
        logging.debug('Consumer consumed the resource')

def producer(cv):
    logging.debug('Producer thread started ...')
    with cv:
        logging.debug('Making resource available')
        logging.debug('Notifying to all consumers')
        cv.notifyAll()

def condition1():
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    pd.start()