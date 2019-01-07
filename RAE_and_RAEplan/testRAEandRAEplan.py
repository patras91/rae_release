import threading
import sys
sys.path.append('../shared/')
sys.path.append('../shared/domains/')
sys.path.append('../shared/problems/SD')
sys.path.append('../shared/problems/CR')
sys.path.append('../shared/problems/IP')
sys.path.append('../shared/problems/EE')
sys.path.append('../shared/problems/OF')
sys.path.append('../shared/problems/SR')
sys.setrecursionlimit(6000)
import argparse
import gui
import globals
from RAE import raeMult, InitializeDomain
from RAE1_and_RAEplan import verbosity
from timer import SetMode
import multiprocessing

def testRAEandRAEplan(domain, problem, useRAEplan):
    '''
    :param domain: the code of the domain
    :param problem: the problem id
    :param useRAEplan: bool value indicating whether to do planning or not before executing the tasks and events
    :return:
    '''
    domain_module = InitializeDomain(domain, problem)
    globals.SetDoSampling(useRAEplan)
    globals.SetPlanningMode(False) # planning mode is required to switch between acting and planning
                                   # because some code is shared by both RAE and RAEplan
    rM = threading.Thread(target=raeMult)
    rM.start()
    gui.start(domain, domain_module.rv) # graphical user interface to show action executions
    rM.join()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--v", help="verbosity of RAE's debugging output (0, 1 or 2)",
                           type=int, default=0, required=False)
    argparser.add_argument("--domain", help="name of the test domain (CR, SD, EE, IP, PD, SR)",
                           type=str, default='CR', required=False)
    argparser.add_argument("--problem", help="identifier for the problem eg. 'problem1', 'problem2', etc",
                           type=str, default="problem11", required=False)
    argparser.add_argument("--plan", help="Do you want to use RAEplan or not? ('y' or 'n')",
                           type=str, default='y', required=False)
    argparser.add_argument("--clockMode", help="Mode of the clock ('Counter' or 'Clock')",
                           type=str, default='Counter', required=False)
    argparser.add_argument("--showOutputs", help="Whether to display the outputs of commands or not? (set 'on' for more clarity and 'off' for batch runs)",
                           type=str, default='on', required=False)
    argparser.add_argument("--lazy", help="Whether to do lazy lookahead? ('y' or 'n') (not implemented yet)",
                           type=str, default='n', required=False)
    argparser.add_argument("--concurrent", help="Whether to do concurrent lookahead? ('y' or 'n') (not implemented yet)",
                           type=str, default='n', required=False)
    argparser.add_argument("--b", help="Number of methods RAEplan should look at",
                           type=int, default=2, required=False)
    argparser.add_argument("--k", help="Number of commands samples RAEplan should look at",
                           type=int, default=1, required=False)
    argparser.add_argument("--depth", help="Search Depth",
                           type=int, default=float("inf"), required=False)

    args = argparser.parse_args()

    if args.plan == 'y':
        s = True
    else:
        s = False

    #globals.Set(args.K)
    globals.SetLazy('n')
    globals.SetConcurrent('n')
    globals.Setb(args.b)
    globals.Setk(args.k)
    globals.SetSearchDepth(args.depth)
    verbosity(args.v)
    SetMode(args.clockMode)
    globals.SetShowOutputs(args.showOutputs)
    testRAEandRAEplan(args.domain, args.problem, s)

def testBatch(domain, problem, useRAEplan):
    SetMode('Counter')
    verbosity(0)
    globals.SetShowOutputs('off')
    p = multiprocessing.Process(target=testRAEandRAEplan, args=(domain, problem, useRAEplan))
    p.start()
    p.join(1800)
    if p.is_alive() == True:
        p.terminate()
        print("0 1 0 0 0 0")