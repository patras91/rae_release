__author__ = 'patras' # Sunandita Patra patras@umd.edu

import threading
import argparse
from shared import gui
from shared import GLOBALS
from shared.timer import SetMode
import multiprocessing
from shared.setup import Setup

def testActorandPlanner(domain, problem, actor, useLearningStrategy, planner, plannerParams, showGui, v, outputQueue=None):
    '''
    :param domain: the code of the domain ('fetch', 'nav', 'explore', 'rescue', AIRS', 'deliver', 'UnitTests')
    :param problem: the problem id
    :param planner: None, APEPlan, RAEPlan, UPOM, StateSpaceUCT
    '''
    problemInstance = Setup(domain, problem, actor, useLearningStrategy, planner, plannerParams, v)
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared between RAE, RAEplan and UPOM
    try:
        rM = threading.Thread(target=problemInstance.actor.raeMult, args=[outputQueue])
        rM.start()
        gui.start(domain, showGui) # graphical user interface to show action executions
        rM.join()
    except Exception as e:
        print('Failed {} and {}, for domain {}, {}'.format(actor, planner, domain, e))

def testBatch(domain, problem, actor, useLearningStrategy, planner, plannerParams):
    SetMode('Counter')
    GLOBALS.SetDoIterativeDeepening(False)
    p = multiprocessing.Process(target=testActorandPlanner, args=(domain, problem, actor, useLearningStrategy, planner, plannerParams, 'off', 0))
    p.start()
    p.join(GLOBALS.GetTimeLimit())
    if p.is_alive() == True:
        p.terminate()
        print("0 1 0 0 0 0 0 0 0")
    
def initialize_unitTest_for_online_method_addition(v, state):
    SetMode('Counter')
    GLOBALS.SetDataGenerationMode(None) # for learning
    GLOBALS.SetTimeLimit(300) # in secs
    GLOBALS.SetHeuristicName(None)
    GLOBALS.SetDoIterativeDeepening(False)
    problemInstance = Setup(
        domain="UnitTest", 
        problem=None, 
        actor="RAE",
        useLearningStrategy=None, 
        planner="UPOM", 
        plannerParams=[50], 
        v=v,
        startState=state)
    
    GLOBALS.SetUtility('efficiency') 
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared by both RAE and RAEplan
    try:
        rM = threading.Thread(target=problemInstance.actor.raeMult)
        rM.start()
    except Exception as e:
        print('Failed to start RAE and UPOM {}'.format(e))
    return problemInstance.actor.taskQueue, \
        problemInstance.actor.cmdExecQueue, \
        problemInstance.actor.cmdStatusQueue, \
        problemInstance.domain


# Specifically set parameters for the AIRS domain
def InitializeAIRSDomain(v, state):
    SetMode('Counter')
    GLOBALS.SetDataGenerationMode(None) # for learning
    GLOBALS.SetTimeLimit(300) # in secs
    GLOBALS.SetHeuristicName(None)
    GLOBALS.SetDoIterativeDeepening(False)
    problemInstance = Setup(
        domain="AIRS_dev", 
        problem=None, 
        actor="RAE",
        useLearningStrategy=None, 
        planner="UPOM", 
        plannerParams=[50], 
        v=v,
        startState=state)
    
    GLOBALS.SetUtility('costEffectiveness') # maximizing the costEffectiveness (0 or 1+1/sum(cost))
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared by both RAE and RAEplan
    try:
        rM = threading.Thread(target=problemInstance.actor.raeMult)
        rM.start()
    except Exception as e:
        print('Failed to start RAE and UPOM {}'.format(e))
    return problemInstance.actor.taskQueue, \
        problemInstance.actor.cmdExecQueue, \
        problemInstance.actor.cmdStatusQueue, \
        problemInstance.domain

# Specifically set parameters for the Mobipick domain
def InitializeMobipickDomain(v, state):
    SetMode('Counter')
    GLOBALS.SetDataGenerationMode(None) # for learning
    GLOBALS.SetTimeLimit(300) # in secs
    GLOBALS.SetHeuristicName(None)
    GLOBALS.SetDoIterativeDeepening(False)
    problemInstance = Setup(
        domain="Mobipick",
        problem=None,
        actor="RAE",
        useLearningStrategy=None,
        planner="UPOM",
        plannerParams=[50],
        v=v,
        startState=state)

    GLOBALS.SetUtility('efficiency') # maximizing the efficiency (1/sum(cost))
    GLOBALS.SetPlanningMode(False) # planning mode is required to switch between acting and planning
    # because some code is shared by both RAE and RAEplan
    try:
        rM = threading.Thread(target=problemInstance.actor.raeMult)
        rM.start()
    except Exception as e:
        print('Failed to start RAE and UPOM {}'.format(e))
    return problemInstance.actor.taskQueue, \
           problemInstance.actor.cmdExecQueue, \
           problemInstance.actor.cmdStatusQueue, \
           problemInstance.domain

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--v", help="verbosity of RAE's debugging output (0, 1 or 2)",
                           type=int, default=0, required=False)
    argparser.add_argument("--domain", help="name of the test domain (fetch, nav, explore, rescue, AIRS, deliver)",
                           type=str, default='fetch', required=False)
    argparser.add_argument("--problem", help="identifier for the problem eg. 'problem1', 'problem2', etc",
                           type=str, default="problem100", required=False)
    argparser.add_argument("--actor", help="Which actor? ('RAE' or APE')",
                           type=str, default='RAE', required=False)
    argparser.add_argument("--planner", help="Which planner? ('APEPlan', RAEPlan' or 'UPOM' or 'None')",
                           type=str, default='UPOM', required=False)
    argparser.add_argument("--clockMode", help="Mode of the clock ('Counter' or 'Clock')",
                           type=str, default='Counter', required=False)
    argparser.add_argument("--showOutputs", help="Whether to display the outputs of commands or not? (set 'on' for more clarity and 'off' for batch runs)",
                           type=str, default='off', required=False)
    
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
    argparser.add_argument("--useLearningStrategy", help="learnM1 or learnM2 or learnH or learnMI or None?", 
                        type=str, default=None, required=False)
    
    argparser.add_argument("--useBackupUCT", help="If planners fails, do you want to run UCT with only commands?",
                        type=bool, default=False, required=False)

    argparser.add_argument("--doIterativeDeepening", help="Increment depth in steps of 5?",
                        type=bool, default=False, required=False)

    args = argparser.parse_args()

    if args.planner == 'UPOM' or args.planner == "RAEPlan":
        assert(args.useLearningStrategy == None or args.useLearningStrategy == 'None' or args.useLearningStrategy == 'learnH')

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
    GLOBALS.SetModelPath("../learning/models/AIJ2020/")

    GLOBALS.SetDoIterativeDeepening(args.doIterativeDeepening)

    GLOBALS.SetBackupUCT(args.useBackupUCT) # for AIRS

    assert(args.utility == "efficiency" or args.utility == "successRatio" or args.utility == "resilience")
    GLOBALS.SetUtility(args.utility)

    testActorandPlanner(args.domain, args.problem, args.actor, args.useLearningStrategy, args.planner, plannerParams, args.showOutputs, args.v)
    
