#!/bin/sh
# This script is to just execute APE without calling APEplan. So, it is basically RAE

echo "Executing tests for RAE without any planning."

for domain in "EE" #"IP" "SD" #"EE"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34") 
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34" "problem35") 
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31") 
    fi
    for problem in ${P[@]}
    do
        setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/$domain')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testRAEandRAEplan import globals, testBatch
globals.Setb(1)
globals.Setk(1)"
counter=1
while [ $counter -le 10 ]
do
        echo $domain $problem $counter/10
        time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"

        fname="$domain/RAE_random.txt"

		echo "Time test of $domain $problem"  >> $fname
        python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
    done
done