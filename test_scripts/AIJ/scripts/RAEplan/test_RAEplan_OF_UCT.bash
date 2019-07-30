#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="OF"
runs=5
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
uct=("100" "300" "500" "700" "900") 
for problem in ${P[@]}
do
    for uct in ${uct[@]}
    do
            setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/OF')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetUCTRuns($uct)
GLOBALS.SetOpt('max')
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetSearchDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem "uct = " $uct ", Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="../../results/${domain}_v_journal/rae_plan_uct_${uct}.txt" # You should have a folder called OF in the current folder

            echo "Time test of $domain $problem $uct" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
    done
done

