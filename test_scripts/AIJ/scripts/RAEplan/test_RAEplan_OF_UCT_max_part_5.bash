#!/bin/sh
domain="OF"
runs=3
P=(
"problem76" 
"problem39" 
"problem105" 
"problem15" 
"problem68" 
)
UCT=(
"5" 
"25" 
"50" 
"75" 
)
for problem in ${P[@]}
do
    for uctCount in ${UCT[@]}
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
GLOBALS.SetSearchDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount
            fname="../../results/${domain}_v_journal/rae_plan_uct_${uctCount}_part_5.txt"
            echo "Time test of $domain $problem $uctCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
    done
done
