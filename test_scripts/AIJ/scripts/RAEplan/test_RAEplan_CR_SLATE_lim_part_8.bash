#!/bin/sh
domain="CR"
runs=5
P=(
"problem1108" 
"problem1074" 
"problem1078" 
"problem1009" 
"problem1045" 
)
B=(
"1" 
"2" 
)
K=(
"3" 
)
Depth=(
"5" 
"10" 
"15" 
)
for problem in ${P[@]}
do
    for b in ${B[@]}
    do
        for k in ${K[@]}
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
GLOBALS.SetOpt('max')
GLOBALS.Setb($b)
GLOBALS.Setk($k)
GLOBALS.SetUCTmode('SLATE')
GLOBALS.SetSearchDepth($d)
GLOBALS.SetHeuristicName(\"h2\")"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "b = " $b " k = " $k " d = " $d
            fname="../../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}_part_8.txt"
            echo "Time test of $domain $problem $b $k $d" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
            done
        done
    done
done
