#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE and RAE-plan."

for domain in "CR" #"CR" "SD" "IP" "EE"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6") #   "problem7" "problem8" "problem9" "problem10") #
        B=("1" "2" "3" "4")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12" "problem13" "problem14")
        B=("1" "2")
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26") 
        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20") #   )
        B=("1" "2" "3")
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26") #"problem21" "problem22"  "problem11" "problem12" "problem13" "problem14" "problem15"  ) #
        B=("1" "2" "3") #"1") #"3")
    fi
    for problem in ${P[@]}
    do
        for b in ${B[@]}
        do 
            for k in "1" "2" "3" "4" "8" "12" "16" # "25" "50" "75"
            do
                setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/CR')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testRAEandRAEplan import globals, testBatch
globals.Setb($b)
globals.Setk($k)"
                echo $domain $problem $b $k
                time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

                fname="$domain/plan_b_${b}_k_$k.txt"

                echo "Time test of $domain $problem $sampleCount" >> $fname
                python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
                #python3 ../../RAE_and_RAEplan/testRAEandRAEplan.py --domain $domain --problem $problem --b $b --k $k --showOutputs 'off' --v 0 --plan y >> $fname
            done
        done
    done
done