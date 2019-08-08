#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="OF"
runs=1
P=(
"problem2"
"problem3"
"problem4"
"problem5"
"problem6"
"problem7"
"problem8"
"problem9"
)
B=("1" "2") # Can be 1, 2
for problem in ${P[@]}
do
    for b in ${B[@]}
    do
        for k in "1" "3" "5" # can be any positive integer
        do
            setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/OF')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.Setb($b)
GLOBALS.Setk($k)
GLOBALS.SetOpt('max')
GLOBALS.SetUCTmode('SLATE')
GLOBALS.SetSearchDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem "b = " $b ", k = " $k ", Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="../../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $k" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
        done
    done
done

