#!/bin/sh
# This script is to just execute APE without calling APEplan. So, it is basically RAE

echo "Executing tests for RAE without any planning."

for domain in "CR" # "IP" "SD" # "CR"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6") # "problem7" "problem8" "problem9" "problem10")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem9" "problem10" "problem11"  "problem12" "problem13" "problem14") #"problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" 
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26")
        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20") # )
    fi
    if [ "$domain" = "EE" ]; then
        P=( "problem21" "problem22" "problem23" "problem24" "problem25" "problem26") #problem11" "problem12" "problem13" "problem14" "problem15") #"problem16" "problem17" "problem18") # "problem19"  
    fi
    for problem in ${P[@]}
    do
        setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/CR')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testRAEandRAEplan import globals, testBatch
globals.Setb(1)
globals.Setk(1)"
        echo $domain $problem
        time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"

        fname="$domain/RAE.txt"

		echo "Time test of $domain $problem" >> $fname
        python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
    done
done