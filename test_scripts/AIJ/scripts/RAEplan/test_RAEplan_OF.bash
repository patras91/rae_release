#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE and RAE-plan."

for domain in "OF" # "SR" "CR" "SD" "IP" "EE"
do
    if [ "$domain" = "OF" ]; then
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

        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18") # "problem11" "problem12") #   "problem7" "problem8" "problem9" "problem10") #
        B=("1" "2" "3" "4")
    fi
    for problem in ${P[@]}
    do
        for b in ${B[@]}
        do
            for k in "3" #"20" # "1" "2" "3" "4" "8" "12" "16" #
            do
            for d in "3" "6" "9" "12" "15"
            do
                setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/SR')
sys.path.append('../../shared/')
from testRAEandRAEplan import globals, testBatch
globals.SetSearchDepth($d)
globals.Setb($b)
globals.Setk($k)"
counter=1
while [ $counter -le 1 ]
do
                echo $domain $problem $b $k $d $counter/1
                time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

                fname="../../results/${domain}_v_journal/rae_plan_b_${b}_k_${k}_d_${d}.txt"

                echo "Time test of $domain $problem $sampleCount" >> $fname
                python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
                #python3 ../../RAE_and_RAEplan/testRAEandRAEplan.py --domain $domain --problem $problem --b $b --k $k --showOutputs 'off' --v 0 --plan y >> $fname
((counter++))
done
done
            done
        done
    done
done