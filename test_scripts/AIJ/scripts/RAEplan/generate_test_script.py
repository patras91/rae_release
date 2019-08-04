import random
import os

def GetProblemsCR(part):
    l = list(range(1000, 1124))
    random.seed(100)
    random.shuffle(l)
    p1 = l[0:50]
    begin = (part - 1)*5
    p2 = p1[begin: begin + 5]
    names = ["problem{}".format(item) for item in p2]
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

runs=8

def writeList(name, l, file):
    file.write("{}=(\n".format(name))
    for item in l:
        file.write("\"{}\" \n".format(item))
    file.write(")\n")

def writeProblems(name, file, part, domain):
    if domain == "CR":
        l = GetProblemsCR(part)
        writeList(name, l, file)

def GenerateTestScriptRAEplan(mode, domain, depth, part):
    fname = 'test_RAEplan_{}_{}_{}_part_{}.bash'.format(domain, mode, depth, part)
    
    file = open(fname,"w") 
    file.write("#!/bin/sh\n")
    file.write("domain=\"{}\"\n".format(domain))
    file.write("runs={}\n".format(runs))

    writeProblems("P", file, part, domain)

    if mode == "SLATE" and depth == "max":
        writeList("B", b_max_depth[domain], file)
        writeList("K", k_max_depth[domain], file)
    elif mode == "UCT" and depth == "max":
        writeList("UCT", UCT_max_depth[domain], file)
    elif mode == "SLATE" and depth == "lim":
        writeList("B", b_lim_depth[domain], file)
        writeList("K", k_lim_depth[domain], file)
        writeList("Depth", DEPTH[domain], file)
    else:
        writeList("UCT", UCT_lim_depth[domain], file)
        writeList("Depth", DEPTH[domain], file)

    file.write("for problem in ${P[@]}\n")
    file.write("do\n")

    if mode == "SLATE":
        file.write("    for b in ${B[@]}\n")
        file.write("    do\n")
        file.write("        for k in ${K[@]}\n")
        file.write("        do\n")
    else:
        file.write("    for uctCount in ${UCT[@]}\n")
        file.write("    do\n")

    if depth == "lim":
        file.write("            for d in ${Depth[@]}\n")
        file.write("            do\n")
    

    file.write("setup=\"\n")
    file.write("import sys\n")
    file.write("sys.path.append(\'../../../../RAE_and_RAEplan/\')\n")
    file.write("sys.path.append(\'../../../../shared/domains/\')\n")
    file.write("sys.path.append(\'../../../../shared/problems/{}/auto\')\n".format(domain))
    file.write("sys.path.append(\'../../../../shared/\')\n")
    file.write("from testRAEandRAEplan import GLOBALS, testBatch\n")
    file.write("GLOBALS.SetOpt('max')\n")

    if mode == "SLATE":
        file.write("GLOBALS.Setb($b)\n")
        file.write("GLOBALS.Setk($k)\n")
        file.write("GLOBALS.SetUCTmode(\'SLATE\')\n")
    else:
        file.write("GLOBALS.SetUCTRuns($uctCount)\n")
        file.write("GLOBALS.SetUCTmode(\'UCT\')\n")

    if depth == "max":
        file.write("GLOBALS.SetSearchDepth(float(\\\"inf\\\"))\"\n")
    else:
        file.write("GLOBALS.SetSearchDepth($d)\n")
        file.write("GLOBALS.SetHeuristicName(\\\"h2\\\")\"\n")
    file.write("counter=1\n")
    file.write("while [ $counter -le $runs ]\n")
    file.write("do\n")

    file.write("            echo $domain $problem \" Run \" $counter/$runs\n")
    file.write("            time_test=\"testBatch(domain=\'$domain\', problem=\'$problem\', useRAEplan=True)\"\n")
    
    if mode == "SLATE" and depth == "max":
        file.write("            echo \"b = \" $b \" k = \" $k\n")
        str1 = "            fname=\"../../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}"
        str2 = "_part_{}.txt\"\n".format(part)
        file.write(str1 + str2)
        file.write("            echo \"Time test of $domain $problem $b $k\" >> $fname\n")
    elif mode == "SLATE" and depth == "lim":
        file.write("            echo \"b = \" $b \" k = \" $k \" d = \" $d\n")
        str1 = "            fname=\"../../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}"
        str2 = "_part_{}.txt\"\n".format(part)
        file.write(str1 + str2)
        file.write("            echo \"Time test of $domain $problem $b $k $d\" >> $fname\n")
    elif mode == "UCT" and depth == "max":
        file.write("            echo \"uctCount = \" $uctCount\n")
        str1 = "            fname=\"../../results/${domain}_v_journal/rae_plan_uct_${uctCount}"
        str2 = "_part_{}.txt\"\n".format(part)
        file.write(str1 + str2)
        file.write("            echo \"Time test of $domain $problem $uctCount\" >> $fname\n")
    else:
        file.write("            echo \"uctCount = \" $uctCount \" d = \" $d\n")
        str1 = "            fname=\"../../results/${domain}_v_journal/rae_plan_uct_${uctCount}_d_${d}"
        str2 = "_part_{}.txt\"\n".format(part)
        file.write(str1 + str2)
        file.write("            echo \"Time test of $domain $problem $uctCount $d\" >> $fname\n")

    file.write("            python3 -m timeit -n 1 -r 1 -s \"$setup\" \"$time_test\" >> $fname\n")

    file.write("((counter++))\n")
    file.write("done\n") # for counter

    if depth == "lim":
        file.write("            done\n") # for depth

    if mode == "SLATE":
        file.write("        done\n") # for k
        file.write("    done\n") # for b
    else:
        file.write("    done\n") # for uct

    file.write("done\n") # for the problems
    os.system("chmod 777 {}".format(fname))


if __name__=="__main__":
    for mode in ["UCT", "SLATE"]:
        for depth in ["max", "lim"]:
            for domain in ["CR"]: #, "EE", "IP", "SD", "OF", "SR"]:
                for part in range(1, 11):
                    GenerateTestScriptRAEplan(mode, domain, depth, part)
