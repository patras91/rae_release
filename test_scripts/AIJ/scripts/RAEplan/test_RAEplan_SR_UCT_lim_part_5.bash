#!/bin/sh
domain="SR"
runs=2
P=(
"problem95" 
"problem72" 
"problem46" 
"problem107" 
"problem92" 
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
sys.path.append('../../../../shared/problems/SR/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
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
            fname="../../results/${domain}_v_journal/rae_plan_uct_${uctCount}_d_${d}_part_5.txt"
            echo "Time test of $domain $problem $uctCount $d" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
            done
    done
done
