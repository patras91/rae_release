__author__ = 'patras'
import random
import os
import argparse

def GetProblemsCR():
    l = list(range(1000, 1124))
    random.seed(100)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

def GetProblemsSR():
    l = list(range(20, 115))
    random.seed(500)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

def GetProblemsOF():
    l = list(range(11, 111))
    random.seed(250)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

#problems = {
#    "CR": GetProblemsCR(),
#    "SD": [],
#    "SR": [],
#    "EE": [],
#    "IP": [],
#    "OF": [],
#}

b_max_depth = {
    "CR": [1,2,3],
    "SD": [2,3,4],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_max_depth = {
    "CR": [1,3,5],
    "SD": [],
    "SR": [1,3,5],
    "EE": [],
    "IP": [],
    "OF": [1,3,5],
}

UCT_max_depth = {
    "CR": [5, 25, 50, 75],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

UCT_max_depth = {
    "CR": [5, 25, 50, 75],
    "SD": [],
    "SR": [5, 25, 50, 75],
    "EE": [],
    "IP": [],
    "OF": [5, 25, 50, 75],
}

b_lim_depth = {
    "CR": [1,2],
    "SD": [2,3,4],
    "SR": [2,3,4],
    "EE": [1,2,3],
    "IP": [1,2,3],
    "OF": [3,6,9],
}

k_lim_depth = {
    "CR": [3],
    "SD": [],
    "SR": [3],
    "EE": [],
    "IP": [],
    "OF": [3],
}

UCT_lim_depth = {
    "CR": [5, 25, 50],
    "SD": [],
    "SR": [5, 25, 50],
    "EE": [],
    "IP": [],
    "OF": [5, 25, 50],
}

DEPTH = {
    "CR": [5, 10, 15],
    "SD": [5, 10, 15],
    "SR": [5, 10, 15],
    "EE": [5, 10, 15],
    "IP": [5, 10, 15],
    "OF": [5, 10, 15],
}

timeLimit = {
    "OF": 450,
    "CR": 300,
    "SR": 300,
    "EE": 300,
    "IP": 300,
    "SD": 300,
}

def writeList(name, l, file):
    file.write("{}=(\n".format(name))
    for item in l:
        file.write("\"{}\" \n".format(item))
    file.write(")\n")

def writeProblems(name, file, domain):
    if domain == "CR":
        l = GetProblemsCR()       
    elif domain == "SR":
        l = GetProblemsSR()
    elif domain == "OF":
        l = GetProblemsOF()
    elif domain == "SD":
        l = GetProblemsSD()
    elif domain == "IP":
        l = GetProblemsIP()
    elif domain == "EE":
        l = GetProblemsEE()
    writeList(name, l, file)

def GenerateTestScriptRAE(domain):
    fname = 'test_RAE_{}.bash'.format(domain)
    
    file = open(fname,"w") 
    file.write("#!/bin/sh\n")
    file.write("domain=\"{}\"\n".format(domain))
    file.write("runs={}\n".format(runs))

    writeProblems("P", file, domain)

    file.write("for problem in ${P[@]}\n")
    file.write("do\n")

    file.write("setup=\"\n")
    file.write("import sys\n")
    file.write("sys.path.append(\'../../../../RAE_and_RAEplan/\')\n")
    file.write("sys.path.append(\'../../../../shared/domains/\')\n")
    file.write("sys.path.append(\'../../../../shared/problems/{}/auto\')\n".format(domain))
    file.write("sys.path.append(\'../../../../shared/\')\n")
    file.write("from testRAEandRAEplan import GLOBALS, testBatch\n")
    file.write("GLOBALS.SetOpt('max')\n")
    file.write("GLOBALS.SetTimeLimit({})\"\n".format(timeLimit[domain]))

    file.write("counter=1\n")
    file.write("while [ $counter -le $runs ]\n")
    file.write("do\n")

    file.write("            echo $domain $problem \" Run \" $counter/$runs\n")
    file.write("            time_test=\"testBatch(domain=\'$domain\', problem=\'$problem\', useRAEplan=False)\"\n")
    
    str1 = "            fname=\"../../results/${domain}_v_journal/RAE.txt\"\n"
    file.write(str1)
    file.write("            echo \"Time test of $domain $problem\" >> $fname\n")

    file.write("            python3 -m timeit -n 1 -r 1 -s \"$setup\" \"$time_test\" >> $fname\n")

    file.write("((counter++))\n")
    file.write("done\n") # for counter

    file.write("done\n") # for the problems
    os.system("chmod 777 {}".format(fname))


if __name__=="__main__":
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SR', 'OF']",
                           type=str, required=True)
    argparser.add_argument("--count", help="Number of runs for each combination of parameters for a problem ",
                           type=int, required=True)
    args = argparser.parse_args()

    global runs
    runs = args.count
    GenerateTestScriptRAE(args.domain)
