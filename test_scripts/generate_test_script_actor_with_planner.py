__author__ = 'patras' # patras@umd.edu
import random
import os
import argparse

#resultFolder="ICAPS2020"
#resultFolder="AIJ2020"
#resultFolder="SDN_USENIX_20"

def GetProblems(minId, maxId, seed, part):
    l = list(range(1000, 1124))
    random.seed(100)
    random.shuffle(l)
    p1 = l[0:50]
    begin = (part - 1)*5
    p2 = p1[begin: begin + 5]
    names = ["problem{}".format(item) for item in p2]
    return names

#b_max_depth = {
#    "fetch": [1,2,3],
#    "nav": [2,5,8],
#    "rescue": [2,3,4],
#    "EE": [1,2,3],
#    "IP": [1,2,3],
#    "deliver": [3,6,9],
#}

b_max_depth = {
    "fetch": [2],
    "nav": [2],
    "rescue": [2],
    "explore": [2],
    "IP": [2],
    "deliver": [2],
}


# k_max_depth = {
#     "fetch": [1,3,5],
#     "nav": [1,3,5],
#     "rescue": [1,3,5],
#     "EE": [],
#     "IP": [],
#     "deliver": [1,3,5],
# }

k_max_depth = {
    "fetch": [2],
    "nav": [2],
    "rescue": [2],
    "explore": [2],
    "IP": [],
    "deliver": [2],
}

#UCT_max_depth = {
#    "fetch": [5, 25, 50, 75, 100, 125],
#    "nav": [5, 25, 50, 75, 100, 125],
#    "rescue": [5, 25, 50, 75, 100, 125],
#    "explore": [5, 25, 50, 75, 100, 125],
#    "IP": [],
#    "deliver": [5, 25, 50, 75, 100, 125, 150],
#}

# for ICAPS 2020
#UCT_max_depth = {
#    "fetch": [5000],
#    "nav": [1000],
#    "explore": [1000],
#    "rescue": [1000],
#    "deliver": [0],
#}

# for AIJ2020
UCT_max_depth = {
    "fetch": [5, 10, 25], #[50, 100, 250, 500, 1000], 
    "nav": [5, 10, 25], #[50, 100, 250, 500, 1000],
    "rescue": [5, 10, 25], #[50, 100, 250, 500, 1000], 
    "explore": [5, 10, 25], #[25], #[50, 100, 250, 500, 1000],
    "deliver": [5, 10, 25], #[50, 100, 250, 500, 1000]
    "AIRS": [5, 10, 25, 50, 100],
}

b_lim_depth = {
    "fetch": [1,2],
    "nav": [2,5,8],
    "rescue": [2,3,4],
    "explore": [1,2,3],
    "IP": [1,2,3],
    "deliver": [3,6,9],
}

k_lim_depth = {
    "fetch": [3],
    "nav": [3],
    "rescue": [3],
    "explore": [],
    "IP": [],
    "deliver": [3],
}

UCT_lim_depth = {
    # "fetch": [1000],
    # "nav": [1000],
    # "rescue": [1000],
    # "explore": [1000],
    # "deliver": [1000],
    "fetch": [250],
    "nav": [250],
    "rescue": [250],
    "explore": [250],
    "deliver": [250],
}

DEPTH = {
    "fetch": [1, 2, 3, 4], # 10, 15, 20, 25, 30], # 35, 40, 45, 50],
    "nav": [1, 2, 3, 4], #[5, 10, 15, 20, 25, 30], # 35, 40, 45, 50],
    "rescue": [1, 2, 3, 4], #[5, 10, 15, 20, 25, 30], # 35, 40, 45, 50],
    "explore": [1, 2, 3, 4], #[5, 10, 15, 20, 25, 30], # 35, 40, 50, 60],
    "deliver": [1, 2, 3, 4], #[5, 10, 15, 20, 25, 30], # 35, 40, 45, 50],
}

# was 300 for ICAPS 2020 submission

timeLimit = {
    "deliver": 1800,
    "fetch": 1800,
    "rescue": 1800,
    "explore": 1800,
    "nav": 1800,
    "AIRS": 300,
}

def writeList(name, l, file):
    file.write("{}=(\n".format(name))
    for item in l:
        file.write("\"{}\" \n".format(item))
    file.write(")\n")

def writeProblems(name, file, part, domain):
    if domain == "fetch":
        l = GetProblems(minId=1000, maxId=1124, seed=100, part=part)
    elif domain == "rescue":
        l = GetProblems(minId=20, maxId=115, seed=500, part=part)
    elif domain == "nav":
        l = GetProblems(minId=1000, maxId=1128, seed=300, part=part)
    elif domain == "explore":
        l = GetProblems(minId=1, maxId=193, seed=750, part=part)
    elif domain == "deliver":
        l = GetProblems(minId=11, maxId=111, seed=250, part=part)
    elif domain == "AIRS":
        l = GetProblems(minId=1, maxId=100, seed=625, part=part)
    writeList(name, l, file)

def GenerateTestScript_actor_with_planner(domain, actor, planner, part, utility, heuristic, resultFolder, runs):
    fname = './test_scripts/autoGen_scripts/{}/test_{}_{}_{}_h_{}_part_{}_{}.bash'.format( \
        domain, domain, actor, planner, heuristic, part, utility)
    
    file = open(fname,"w") 
    file.write("#!/bin/sh\n")
    file.write("domain=\"{}\"\n".format(domain))
    file.write("runs={}\n".format(runs))

    writeProblems("P", file, part, domain)

    if planner == "RAEPlan" and heuristic == "None":
        writeList("B", b_max_depth[domain], file)
        writeList("K", k_max_depth[domain], file)
    elif planner == "UPOM" and heuristic == "None":
        writeList("UCT", UCT_max_depth[domain], file)
    elif planner == "RAEPlan" and heuristic != "None":
        writeList("B", b_lim_depth[domain], file)
        writeList("K", k_lim_depth[domain], file)
        writeList("Depth", DEPTH[domain], file)
    else:
        writeList("UPOM", UCT_lim_depth[domain], file)
        writeList("Depth", DEPTH[domain], file)

    file.write("for problem in ${P[@]}\n")
    file.write("do\n")

    if planner == "RAEPlan":
        file.write("    for b in ${B[@]}\n")
        file.write("    do\n")
        file.write("        for k in ${K[@]}\n")
        file.write("        do\n")
    else:
        file.write("    for nro in ${UCT[@]}\n")
        file.write("    do\n")

    if heuristic != "None":
        file.write("            for d in ${Depth[@]}\n")
        file.write("            do\n")
    

    file.write("setup=\"\n")
    file.write("from main import testBatch\n")
    file.write("from shared import GLOBALS\n")
    file.write("GLOBALS.SetTimeLimit({})\n".format(timeLimit[domain]))

    if planner=="RAEPlan":
        planerParams="[$b,$k]"
    elif planner=="UPOM":
        plannerParams="[$nro, $d]"

    file.write("GLOBALS.SetUtility(\'{}\')\n".format(utility))
    if heuristic == "None" or heuristic == None:
        #file.write("GLOBALS.SetMaxDepth(float(\\\"inf\\\"))\"\n")
        if planner == "RAEPlan":
            file.write("GLOBALS.SetMaxDepth(20)\n")
        else:
            #file.write("GLOBALS.SetMaxDepth(30)\n")
            file.write("GLOBALS.SetMaxDepth(80)\n")
        file.write("GLOBALS.SetHeuristicName(\\\"h2\\\")\n")
    else:
        file.write("GLOBALS.SetMaxDepth($d)\n")
        if heuristic == "zero":
            file.write("GLOBALS.SetHeuristicName(\\\"h1\\\")\n")
        elif heuristic == "DS":
            file.write("GLOBALS.SetHeuristicName(\\\"h2\\\")\n")


    file.write("GLOBALS.SetDataGenerationMode(None)\n")
    file.write("GLOBALS.SetModelPath(\'./learning/models/AIJ2020/\')\n")

    if heuristic == "learnH":
        file.write("GLOBALS.SetUseTrainedModel('learnH')\"\n")
    else:
        file.write("GLOBALS.SetUseTrainedModel(None)\"\n")

    file.write("counter=1\n")
    file.write("while [ $counter -le $runs ]\n")
    file.write("do\n")

    file.write("            echo $domain $problem \" Run \" $counter/$runs\n")
    file.write("            time_test=\"testBatch(domain=\'$domain\', problem=\'$problem\', planner=\'{}\', plannerParams=\'{}\')\"\n".format(planner, plannerParams))
    
    str1 = "            fname=\"" + resultFolder + "/${domain}" 
    str3 = "_part_{}.txt\"\n".format(part)

    if planner == "RAEPlan" and heuristic != "None":
        file.write("            echo \"b = \" $b \" k = \" $k\n")    
        str2 = "/RAEPlan_b_${b}_k_${k}"
        file.write(str1 + "_" + utility + str2 + str3)
        file.write("            echo \"Time test of $domain $problem $b $k\" >> $fname\n")
    elif planner == "RAEPlan" and heuristic != "None":
        file.write("            echo \"b = \" $b \" k = \" $k \" d = \" $d\n")
        if heuristic == "zero":
            str2 = "/RAEPlan_b_${b}_k_${k}_d_${d}_h_h0"
        elif heuristic == "DS":
            str2 = "/RAEPlan_b_${b}_k_${k}_d_${d}"
        file.write(str1 + "_" + utility + str2 + str3)
        file.write("            echo \"Time test of $domain $problem $b $k $d\" >> $fname\n")
    elif planner == "UPOM" and heuristic != "None":
        file.write("            echo \"number of rollouts = \" $nro\n")
        str2 = "/UPOM_${nro}"
        file.write(str1 + "_" + utility + str2 + str3)
        file.write("            echo \"Time test of $domain $problem $nro\" >> $fname\n")
    else:
        file.write("            echo \"number of rollouts = \" $nro \" d = \" $d\n")
        if heuristic == "zero":
            str2 = "/UPOM_${nro}_d_${d}_h_h0"
        elif heuristic == "DS":
            str2 = "/UPOM_${nro}_d_${d}"
        else:
            str2 = "/UPOM_${nro}_d_${d}_h_learnH"

        file.write(str1 + "_" + utility + str2 + str3)
        file.write("            echo \"Time test of $domain $problem $nro $d\" >> $fname\n")

    file.write("            python3 -m timeit -n 1 -r 1 -s \"$setup\" \"$time_test\" >> $fname\n")

    file.write("((counter++))\n")
    file.write("done\n") # for counter

    if heuristic != "None":
        file.write("            done\n") # for depth

    if planner == "RAEPlan":
        file.write("        done\n") # for k
        file.write("    done\n") # for b
    else:
        file.write("    done\n") # for uct

    file.write("done\n") # for the problems
    os.system("chmod 777 {}".format(fname))


if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--domain", help="domain in ['fetch', 'rescue', 'nav', 'explore', 'deliver', 'AIRS']",
                           type=str, required=True)
    argparser.add_argument("--runs", help="Number of runs for test case",
                           type=int, required=True)
    argparser.add_argument("--actor", help="Which actor? RAE or APE?",
                           type=str, required=True)
    argparser.add_argument("--planner", help="Which planner? UPOM or RAEPlan or APEPlan?",
                           type=str, required=True)
    argparser.add_argument("--utility", help=" efficiency or successRatio or resilience? ",
                           type=str, required=True, default="efficiency")
    argparser.add_argument("--heuristic", help="None or zero or DS or learnH? ",
                           type=str, required=True, default="zero")
    argparser.add_argument("--resultFolder", help="Which folder to save the test results at? ",
                           type=str, required=True, default="zero")
    args = argparser.parse_args()

    for domain in [args.domain]:
        for optz in [args.utility]:
            for actor in [args.actor]:
                for planner in [args.planner]: 
                    for heuristic in [args.heuristic]: #['zero', 'DS', 'learnH']:
                        for part in range(1, 11):
                            GenerateTestScript_actor_with_planner(domain, actor, planner, part, optz, heuristic, args.resultFolder, args.runs)
