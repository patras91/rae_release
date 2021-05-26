#!/usr/bin/env python3
__author__ = 'sunandita'
# Last Modified: Sunandita: May 26, 2021

import threading

from main import InitializeMobipickDomain
from shared.state import State

def beginCommand(cmd, cmdRet, args):
    cmdRet['state'] = 'Success'


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
            print('Done executing cmd: ' + str(cmd))
            status_queue.put([id, cmdRet['state'], state.copy()])


def initialize_state():
    """TODO: add documentation.
    """

    pass


if __name__ == '__main__':

    verbosity = 1
    #set the state variables for RAE
    state = State()
    state.loc = {
            'r1': 1,
        }

    (task_queue, exec_queue, status_queue, domain) = InitializeMobipickDomain(verbosity, state)

    task_queue.put(['nonEmergencyMove', 'r1', '1', '2', 5])

    # Execute planned commands
    exec_thread = threading.Thread(
        target=exec_cmds, args=(exec_queue, status_queue)
    )
    exec_thread.start()
