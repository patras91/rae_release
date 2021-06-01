#!/usr/bin/env python3
__author__ = 'sunandita'
# Last Modified: Sunandita: May 3, 2021

import functools
import operator
import threading

from main import initialize_unitTest_for_online_method_addition
from shared.state import State
#from domains.AIRS.domain_AIRS import *


def beginCommand(cmd, cmdRet, args):
    cmdRet['state'] = cmd(*args)


def exec_cmds(exec_queue, status_queue):
    """TODO: add documentation.
    """

    while True:
        if not exec_queue.empty():
            (id, cmd, args) = exec_queue.get()
            # TODO: execute planned command
            print('Got cmd to exec: id=' + str(id) + ', cmd=' + str(cmd) + ', args=' + str(args))
            cmdRet = {'state': 'running'}
            t = threading.Thread(target=beginCommand, args=(cmd, cmdRet, args))
            t.start()
            t.join()
            print('Done executing cmd: ' + str(cmd.__name__))
            status_queue.put([id, cmdRet['state'], state.copy()])


if __name__ == '__main__':

    verbosity = 1

    #set the state variables for RAE
    state = State()
    
    (task_queue, exec_queue, status_queue, domain) = initialize_unitTest_for_online_method_addition(verbosity, state)
    
    def m_newMethod(self, a):
        self.actor.do_task('testMethodAddition_sub', a)

    domain.add_refinement_method('testMethodAddition', m_newMethod)
    task_queue.put(['testMethodAddition', 'a']) 

    # Execute planned commands
    exec_thread = threading.Thread(
        target=exec_cmds, args=(exec_queue, status_queue)
    )
    exec_thread.start()
