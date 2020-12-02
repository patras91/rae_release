#!/usr/bin/env python3
"""Environment for AIRS SDN domain.

This file defines the command probabilities for the AIRS SDN domain.
"""
__author__ = 'alex'

import numpy as np
from domain_constants import SUCCESS, FAILURE

# Each command is associated with a tuple indicating probability of success vs. failure
commandProb = {
    'restart_vm': (0.95, 0.05),
    'add_vcpu': (0.95, 0.05),
    'increase_mem': (0.95, 0.05),
    'kill_top_proc': (0.95, 0.05),
    'apply_update': (0.6, 0.4),
    'add_switch': (0.75, 0.25),
    'move_critical_hosts': (0.6, 0.4),
    'clear_ctrl_state_besteffort': (0.6, 0.4),
    'clear_ctrl_state_fallback': (0.8, 0.2),
    'reinstall_ctrl_besteffort': (0.75, 0.25),
    'reinstall_ctrl_fallback': (0.9, 0.1),
    'reconnect_switch_to_ctrl': (0.8, 0.2),
    'clear_switch_state_besteffort': (0.8, 0.2),
    'clear_switch_state_fallback': (0.9, 0.1),
    'disconnect_reconnect_switch_port': (0.75, 0.25),
    'disconnect_switch_port': (0.9, 0.1),
    'succeed': (1, 0),
    'unsure': (0.5, 0.5),
    'fail': (0, 1)
}


def Sense(cmd):
    """Return ``SUCCESS`` or ``FAILURE`` based on random choice according to ``commandProb``."""

    p = commandProb[cmd]
    outcome = np.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE