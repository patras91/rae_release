#!/bin/sh
domain="OF"
runs=1
P=(
"problem72" 
"problem12" 
"problem25" 
"problem48" 
"problem53" 
"problem45"
)
UCT=(
"10" 
)
for problem in ${P[@]}
do
    for uctCount in ${UCT[@]}
    do
setup="
import sys
sys.path.append('../RAE_and_RAEplan/')
sys.path.append('../shared/domains/')
sys.path.append('../shared/problems/OF/auto')
sys.path.append('../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetTimeLimit(300)
GLOBALS.SetUCTRuns($uctCount)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetOpt('max')
GLOBALS.SetHeuristicName('h2')
GLOBALS.SetLearningMode('genEffDataPlanner')
GLOBALS.SetUseTrainedModel('n')
GLOBALS.SetSearchDepth(30)"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount
        
            echo "Time test of $domain $problem $uctCount" 
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" 
((counter++))
done
    done
done
