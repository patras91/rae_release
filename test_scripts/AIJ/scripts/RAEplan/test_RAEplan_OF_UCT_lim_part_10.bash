#!/bin/sh
domain="OF"
runs=3
P=(
"problem49" 
"problem75" 
"problem94" 
"problem61" 
"problem13" 
)
UCT=(
"5" 
"25" 
"50" 
)
Depth=(
"5" 
"10" 
"15" 
)
for problem in ${P[@]}
do
    for uctCount in ${UCT[@]}
    do
            for d in ${Depth[@]}
            do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/OF/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
GLOBALS.SetTimeLimit(600)
GLOBALS.SetUCTRuns($uctCount)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetSearchDepth($d)
GLOBALS.SetHeuristicName(\"h2\")"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount " d = " $d
            fname="../../results/${domain}_v_journal/rae_plan_uct_${uctCount}_d_${d}_part_10.txt"
            echo "Time test of $domain $problem $uctCount $d" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
            done
    done
done
