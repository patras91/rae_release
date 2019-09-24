#!/bin/sh
domain="CR"
runs=1
P=(
"problem1062" 
"problem1092" 
"problem1079" 
"problem1111" 
"problem1085" 
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
sys.path.append('../../../../shared/problems/CR/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetTimeLimit(300)
GLOBALS.SetUCTRuns($uctCount)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetOpt('sr')
GLOBALS.SetSearchDepth($d)
GLOBALS.SetHeuristicName(\"h2\")"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount " d = " $d
            fname="../../results/${domain}_v_journal_sr/rae_plan_uct_${uctCount}_d_${d}_part_4.txt"
            echo "Time test of $domain $problem $uctCount $d" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
            done
    done
done
