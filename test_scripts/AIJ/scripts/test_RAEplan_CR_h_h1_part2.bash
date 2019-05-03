#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
P=(
"problem1021"
"problem1022"
"problem1023"
"problem1025"
"problem1026"
"problem1027"
"problem1028"
"problem1029"
"problem1030"
"problem1031"
"problem1032"
"problem1033"
"problem1034"
"problem1035"
"problem1036"
"problem1037"
"problem1038"
"problem1039"
"problem1040"
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

            fname="../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}_h_h1_part2.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
        done
    done
done

