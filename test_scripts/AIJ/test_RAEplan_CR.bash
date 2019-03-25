#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
#P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34" "problem35") 
#for i in $(seq 1000 1023); 
#do
#problem="problem${i}"
P=(
"problem1052"
"problem1053"
"problem1054"
"problem1055"
"problem1056"
"problem1057"
"problem1058"
"problem1059"
"problem1060"
"problem1061"
"problem1062"
"problem1063"
"problem1064"
"problem1065"
"problem1066"
"problem1067"
)
B=("1" "2" "3") # Can be 1, 2 or 3
for problem in ${P[@]}
do
    for b in ${B[@]}
    do 
        for k in "1" "3" "5" "8" "10" # can be any positive integer
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
while [ $counter -le 2 ]
do
            echo $domain $problem $b $k $counter/2
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="${domain}_v6/rae_plan_b_${b}_k_$k.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
        done
    done
done

