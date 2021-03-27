#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for APEplan."

domain="IP"
P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34") 
for problem in ${P[@]}
do
    setup="
import sys
sys.path.append('../../APE_and_APEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/IP')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testAPEandAPEplan import globals, testBatch"
counter=1
while [ $counter -le 10 ]
do
                echo $domain $problem $b $k $counter/10
                time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

                fname="$domain/ape_plan.txt"

                echo "Time test of $domain $problem $sampleCount" >> $fname
                python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
                #python3 ../../RAE_and_RAEplan/testRAEandRAEplan.py --domain $domain --problem $problem --b $b --k $k --showOutputs 'off' --v 0 --plan y >> $fname
((counter++))
done
done
