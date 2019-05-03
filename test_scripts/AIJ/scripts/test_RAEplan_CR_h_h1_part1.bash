#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
P=(
"problem1000"
"problem1001"
"problem1002"
"problem1003"
"problem1004"
"problem1005"
"problem1006"
"problem1007"
"problem1008"
"problem1009"
"problem1010"
"problem1011"
"problem1012"
"problem1013"
"problem1014"
"problem1015"
"problem1016"
"problem1017"
"problem1018"
"problem1019"
"problem1020"
)
B=("3") # Can be 1, 2 or 3
for problem in ${P[@]}
do
    for b in ${B[@]}
    do 
        for k in "3" # can be any positive integer
        do
            for d in "1" "3" "5" "7" "9"
            do
            setup="
import sys
sys.path.append('../../../RAE_and_RAEplan/')
sys.path.append('../../../shared/domains/')
sys.path.append('../../../shared/problems/CR/auto/')
sys.path.append('../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.Setb($b)
GLOBALS.Setk($k)
GLOBALS.SetSearchDepth($d)
GLOBALS.SetHeuristicName(\"h1\")"
counter=1
while [ $counter -le 20 ]
do
            echo $domain $problem "b = " $b ", k = " $k ", d = " $d ", Run " $counter/20
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}_h_h1_part1.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
        done
    done
done

