import random
import os

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
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

UCT_max_depth = {
    "CR": [5, 25, 50, 75],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
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
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

UCT_lim_depth = {
    "CR": [5, 25, 50],
    "SD": [],
    "SR": [],
    "EE": [],
    "IP": [],
    "OF": [],
}

DEPTH = {
    "CR": [5, 10, 15],
    "SD": [5, 10, 15],
    "SR": [5, 10, 15],
    "EE": [5, 10, 15],
    "IP": [5, 10, 15],
    "OF": [5, 10, 15],
}

runs=5

def writeList(name, l, file):
    file.write("{}=(\n".format(name))
    for item in l:
        file.write("\"{}\" \n".format(item))
    file.write(")\n")

def writeProblems(name, file, domain):
    if domain == "CR":
        l = GetProblemsCR()
        writeList(name, l, file)
    elif domain == "SR":
        l = GetProblemsSR()
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
    file.write("GLOBALS.SetOpt('max')\"\n")

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
    for domain in ["SR"]: #, "EE", "IP", "SD", "OF", "SR"]:
        GenerateTestScriptRAE(domain)
