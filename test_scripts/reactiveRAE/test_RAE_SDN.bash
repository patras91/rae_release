#!/bin/sh
domain="SDN"
runs=1
P=(
"problem1"
"problem2"
"problem3"
"problem4"
"problem5"
"problem6"
"problem7"
"problem8"
"problem9"
"problem10"  
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/SDN/auto')
sys.path.append('../../../../shared/')
sys.path.append('../../../../learning/')
sys.path.append('../../../../learning/encoders/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetUtility('efficiency')
GLOBALS.SetUseTrainedModel(None)
GLOBALS.SetDataGenerationMode(None)
GLOBALS.SetModelPath('../../../../learning/models/')
GLOBALS.SetTimeLimit(300)"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', usePlanner=None)"
            fname="../../../../../raeResults/SDN/${domain}/RAE.txt"
            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
