#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
P=(
"problem1081"
"problem1082"
"problem1083"
"problem1084"
"problem1085"
"problem1086"
"problem1087"
"problem1088"
"problem1089"
"problem1090"
"problem1091"
"problem1092"
"problem1093"
"problem1094"
"problem1095"
"problem1096"
"problem1097"
"problem1098"
"problem1099"
"problem1100"
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

            fname="../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}_h_h1_part5.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
        done
    done
done

