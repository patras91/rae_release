#!/bin/sh
# This script is to just run RAE without calling any planner.

echo "Executing tests for RAE without any planning."
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

for problem in ${P[@]}
do
    setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/$domain/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.Setb(1)
GLOBALS.Setk(1)
GLOBALS.SetOpt('max')"
counter=1
while [ $counter -le $runs ]
do
        echo $domain $problem " Run " $counter/$runs
        time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"

        fname="../../results/${domain}_v_journal/RAE.txt"

		echo "Time test of $domain $problem"  >> $fname
        python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
