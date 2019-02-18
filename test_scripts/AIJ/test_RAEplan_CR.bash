#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34" "problem35") 
B=("2") # Can be 1, 2 or 3
for problem in ${P[@]}
do
    for b in ${B[@]}
    do 
        for k in "2" # can be any positive integer
        do
            setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/CR')
sys.path.append('../../shared/')
from testRAEandRAEplan import globals, testBatch
globals.Setb($b)
globals.Setk($k)"
counter=1
while [ $counter -le 1 ]
do
            echo $domain $problem $b $k $counter/1
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="$domain/rae_plan_b_${b}_k_$k.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
        done
    done
done
