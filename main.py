__author__ = 'patras'

import threading
import sys

sys.path.append('./shared/')
sys.path.append('./domains/')

for d in ["UnitTests", "nav", "fetch", "explore", "rescue", "deliver", "AIRS"]:
    sys.path.append("./domains/" + d + "/")
    sys.path.append("./domains/" + d + "/problems/auto/")

sys.path.append('./actors/RAE/')
sys.path.append('./actors/APE/')

sys.path.append('./planners/')
sys.path.append('./planners/APEPlan/')
sys.path.append('./planners/RAEPlan/')
sys.path.append('./planners/UPOM/')
sys.path.append('./planners/StateSpaceUCT/')
sys.path.append('./planners/shared/')

sys.path.append('./learning/')
sys.path.append('./learning/encoders/')

import argparse
import gui
import GLOBALS
from RAE import rae
from timer import SetMode
import multiprocessing
import os
from domain_fetch import Fetch

def testRAEandPlanner(domain, problem, planner, plannerParams, showOutputs, v):
    '''
    :param domain: the code of the domain ('fetch', 'nav', 'explore', 'rescue', AIRS', 'deliver', 'UnitTests')
    :param problem: the problem id
    :param planner: None, APEPlan, RAEPlan, UPOM, StateSpaceUCT
    '''
    if domain == "fetch":
        domainInstance = Fetch(problem, planner, plannerParams, v)
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared between RAE, RAEplan and UPOM
    try:
        rM = threading.Thread(target=domainInstance.actor.raeMult)
        rM.start()
        gui.start(domain, showOutputs) # graphical user interface to show action executions
        rM.join()
    except Exception as e:
        print('Failed RAE and {}, for domain {}, {}'.format(planner, domain, e))

def testBatch(domain, problem, usePlanner):
    SetMode('Counter')
    verbosity(0)
    GLOBALS.SetShowOutputs('off')
    GLOBALS.SetDomain(domain)
    GLOBALS.SetDoIterativeDeepening(False)
    p = multiprocessing.Process(target=testRAEandPlanner, args=(domain, problem, usePlanner))
    p.start()
    p.join(GLOBALS.GetTimeLimit())
    if p.is_alive() == True:
        p.terminate()
        print("0 1 0 0 0 0 0 0 0")
    
# Specifically set parameters for the SDN domain
def InitializeSecurityDomain(v, state):
    GLOBALS.SetMaxDepth(float("inf"))
    verbosity(v)
    SetMode('Counter')
    GLOBALS.SetShowOutputs('on')
    GLOBALS.SetPlanner("UPOM")
    GLOBALS.SetDataGenerationMode(None) # for learning
    GLOBALS.Set_nRO(50) # to decide accordingly
    GLOBALS.SetTimeLimit(300) # in secs
    GLOBALS.SetDoIterativeDeepening(False)
    '''
    :param domain: the code of the domain
    :param problem: the problem id
    '''
    InitializeDomain('AIRS_dev', None, state) # no concept of separate problem in SDN, so the second argument is None
    GLOBALS.SetDomain('AIRS_dev')
    GLOBALS.SetUtility('resilience') # maximizing the resilience (0 or 1+1/sum(cost))
    GLOBALS.SetUseTrainedModel(None) # for learning, in case you have models
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared by both RAE and RAEplan
    try:
        rM = threading.Thread(target=raeMult)
        rM.start()
    except Exception as e:
        print('Failed to start RAE and RAEplan {}'.format(e))
    return taskQueue, cmdExecQueue, cmdStatusQueue 


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--v", help="verbosity of RAE's debugging output (0, 1 or 2)",
                           type=int, default=0, required=False)
    argparser.add_argument("--domain", help="name of the test domain (fetch, nav, explore, rescue, AIRS, deliver)",
                           type=str, default='fetch', required=False)
    argparser.add_argument("--problem", help="identifier for the problem eg. 'problem1', 'problem2', etc",
                           type=str, default="problem1", required=False)
    argparser.add_argument("--planner", help="Which planner? ('APEPlan', RAEPlan' or 'UPOM' or 'None')",
                           type=str, default='UPOM', required=False)
    argparser.add_argument("--clockMode", help="Mode of the clock ('Counter' or 'Clock')",
                           type=str, default='Counter', required=False)
    argparser.add_argument("--showOutputs", help="Whether to display the outputs of commands or not? (set 'on' for more clarity and 'off' for batch runs)",
                           type=str, default='on', required=False)
    
    # parameters of RAEPlan
    argparser.add_argument("--b", help="Number of methods RAEplan should look at",
                           type=int, default=2, required=False)
    argparser.add_argument("--k", help="Number of commands samples RAEplan should look at",
                           type=int, default=1, required=False)


    # parameter for UPOM
    argparser.add_argument("--n_RO", help="Number of rollouts in UPOM?",
                           type=int, default=100, required=False)

    argparser.add_argument("--depth", help="Search Depth",
                           type=int, default=50, required=False)

    argparser.add_argument("--heuristic", help="Name of the heuristic function",
                           type=str, default='h2', required=False)

    argparser.add_argument("--timeLim", help="What is the time limit? ",
                           type=int, default=300, required=False)

    #what to optimize?
    argparser.add_argument("--utility", help="efficiency or successRatio or resilience?",
                           type=str, default="efficiency", required=False)
    
    #use learned models?
    argparser.add_argument("--useTrainedModel", help="learnM1 or learnM2 or learnH or learnMI or None?", 
                        type=str, default=None, required=False)
    
    argparser.add_argument("--useBackupUCT", help="If planners fails, do you want to run UCT with only commands?",
                        type=bool, default=False, required=False)

    argparser.add_argument("--doIterativeDeepening", help="Increment depth in steps of 5?",
                        type=bool, default=False, required=False)

    args = argparser.parse_args()

    if args.planner == 'UPOM' or args.planner == "RAEPlan":
        assert(args.useTrainedModel == None or args.useTrainedModel == 'None' or args.useTrainedModel == 'learnH')

    assert(args.depth >= 1)
    if args.planner == "RAEPlan":
        plannerParams = [args.b, args.k, args.depth]
    elif args.planner == "UPOM":
        plannerParams = [args.n_RO, args.depth]
    else:
        plannerParams = []

    GLOBALS.SetHeuristicName(args.heuristic)

    SetMode(args.clockMode)

    GLOBALS.SetTimeLimit(args.timeLim)

    # learning related info
    GLOBALS.SetDataGenerationMode(None)
    GLOBALS.SetUseTrainedModel(args.useTrainedModel)
    GLOBALS.SetModelPath("../learning/models/AIJ2020/")

    GLOBALS.SetDoIterativeDeepening(args.doIterativeDeepening)

    GLOBALS.SetBackupUCT(args.useBackupUCT) # for SDN

    assert(args.utility == "efficiency" or args.utility == "successRatio" or args.utility == "resilience")
    GLOBALS.SetUtility(args.utility)

    testRAEandPlanner(args.domain, args.problem, args.planner, plannerParams, args.showOutputs, args.v)
    
