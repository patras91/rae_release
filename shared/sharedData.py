__author__ = 'patras'

import multiprocessing

taskQueue = multiprocessing.Queue()
cmdStatusQueue = multiprocessing.Queue()
cmdExecQueue = multiprocessing.Queue()

cmdStatusTable = {}