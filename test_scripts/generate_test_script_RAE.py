__author__ = 'patras'
import random
import os
import argparse

#resultFolder="AIJ2020"
resultFolder="SDN"

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

def GetProblemsSD():
    l = list(range(1000, 1128))
    random.seed(300)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

def GetProblemsEE():
    l = list(range(1, 193))
    random.seed(750)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

def GetProblemsSDN():
    l = list(range(1, 100))
    random.seed(625)
    random.shuffle(l)
    p1 = l[0:50]
    names = ["problem{}".format(item) for item in p1]
    return names

timeLimit = {
    "OF": 1800,
    "CR": 1800,
    "SR": 1800,
    "EE": 1800,
    "IP": 1800,
    "SD": 1800,
    "SDN": 300,
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
    elif domain == "SDN":
        l = GetProblemsSDN()
    writeList(name, l, file)

def GenerateTestScriptRAE(domain):
    fname = '../../../../autoGen_scripts/{}/test_RAE_{}.bash'.format(domain, domain)
    
    file = open(fname,"w") 
    file.write("#!/bin/sh\n")
    file.write("domain=\"{}\"\n".format(domain))
    file.write("runs={}\n".format(runs))

    writeProblems("P", file, domain)

    file.write("for problem in ${P[@]}\n")
    file.write("do\n")

    file.write("setup=\"\n")
    file.write("import sys\n")
    file.write("sys.path.append(\'../../RAE_and_RAEplan/\')\n")
    file.write("sys.path.append(\'../../shared/domains/\')\n")
    file.write("sys.path.append(\'../../shared/problems/{}/auto\')\n".format(domain))
    file.write("sys.path.append(\'../../shared/\')\n")
    file.write("sys.path.append(\'../../learning/\')\n")
    file.write("sys.path.append(\'../../learning/encoders/\')\n")
    file.write("from testRAEandRAEplan import GLOBALS, testBatch\n")
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
    file.write("            time_test=\"testBatch(domain=\'$domain\', problem=\'$problem\', usePlanner=None)\"\n")
    
    str1 = "            fname=\"../../../raeResults/" + resultFolder + "/${domain}_v_journal/RAE.txt\"\n"
    file.write(str1)
    file.write("            echo \"Time test of $domain $problem\" >> $fname\n")

    file.write("            python3 -m timeit -n 1 -r 1 -s \"$setup\" \"$time_test\" >> $fname\n")

    file.write("((counter++))\n")
    file.write("done\n") # for counter

    file.write("done\n") # for the problems
    os.system("chmod 777 {}".format(fname))


if __name__=="__main__":
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['CR', 'SR', 'OF', 'SD', 'EE', 'SDN']",
                           type=str, required=True)
    argparser.add_argument("--count", help="Number of runs for each combination of parameters for a problem ",
                           type=int, required=True)
    args = argparser.parse_args()

    global runs
    runs = args.count
    GenerateTestScriptRAE(args.domain)
