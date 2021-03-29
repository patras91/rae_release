__author__ = 'patras'
import random
import os
import argparse

def GetProblems(minId, maxId, seed):
    l = list(range(minId, maxId))
    random.seed(seed)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

timeLimit = {
    "fetch": 1800,
    "rescue": 1800,
    "explore": 1800,
    "nav": 1800,
    "AIRS": 300,
    "deliver": 1800,
}

def writeList(name, l, file):
    file.write("{}=(\n".format(name))
    for item in l:
        file.write("\"{}\" \n".format(item))
    file.write(")\n")

def writeProblems(name, file, domain):
    if domain == "fetch":
        l = GetProblems(minId=1000, maxId=1124, seed=100)       
    elif domain == "rescue":
        l = GetProblems(minId=20, maxId=115, seed=500)
    elif domain == "deliver":
        l = GetProblems(minId=11, maxId=111, seed=250)
    elif domain == "nav":
        l = GetProblems(minId=1000, maxId=1128, seed=300)
    elif domain == "explore":
        l = GetProblems(minId=1, maxId=193, seed=750)
    elif domain == "AIRS":
        l = GetProblems(minId=1, maxId=100, seed=625)
    writeList(name, l, file)

def GenerateTestScriptActor(domain, runs, actor, resultFolder):
    fname = './test_scripts/autoGen_scripts/{}/test_{}_{}.bash'.format(domain, actor, domain)
    
    file = open(fname,"w") 
    file.write("#!/bin/sh\n")
    file.write("domain=\"{}\"\n".format(domain))
    file.write("runs={}\n".format(runs))

    writeProblems("P", file, domain)

    file.write("for problem in ${P[@]}\n")
    file.write("do\n")

    file.write("setup=\"\n")
    file.write("from main import testBatch\n")
    file.write("from shared import GLOBALS\n")
    file.write("GLOBALS.SetUtility('efficiency')\n")
    file.write("GLOBALS.SetTimeLimit({})\n".format(timeLimit[domain]))
    file.write("GLOBALS.SetHeuristicName(\\\"h2\\\")\n")
    file.write("GLOBALS.SetMaxDepth(80)\n")
    file.write("GLOBALS.SetDataGenerationMode(None)\n")
    file.write("GLOBALS.SetModelPath(\'../learning/models\')\n")
    file.write("GLOBALS.SetUseTrainedModel(None)\"\n")

    file.write("counter=1\n")
    file.write("while [ $counter -le $runs ]\n")
    file.write("do\n")

    file.write("            echo $domain $problem \" Run \" $counter/$runs\n")
    file.write("            time_test=\"testBatch(domain=\'$domain\', problem=\'$problem\', planner=None, plannerParams=[])\"\n")
    
    str1 = "            fname=\"" + resultFolder + "/${domain}/RAE.txt\"\n"
    file.write(str1)
    file.write("            echo \"Time test of $domain $problem\" >> $fname\n")

    file.write("            python3 -m timeit -n 1 -r 1 -s \"$setup\" \"$time_test\" >> $fname\n")

    file.write("((counter++))\n")
    file.write("done\n") # for counter

    file.write("done\n") # for the problems
    os.system("chmod 777 {}".format(fname))


if __name__=="__main__":
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['fetch', 'rescue', 'deliver', 'nav', 'explore', 'AIRS']",
                           type=str, required=True)
    argparser.add_argument("--runs", help="Number of runs for each test case",
                           type=int, required=True)
    argparser.add_argument("--actor", help="Which actor? RAE or APE?",
                           type=str, required=True)
    argparser.add_argument("--resultFolder", help="Folder in which results will be saved",
                           type=str, required=True)
    args = argparser.parse_args()

    GenerateTestScriptActor(args.domain, args.runs, args.actor, args.resultFolder)
