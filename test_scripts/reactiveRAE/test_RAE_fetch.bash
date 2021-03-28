#!/bin/sh
domain="fetch"
runs=1
P=(
"problem1" 
"problem2" 
"problem3" 
"problem4" 
"problem5" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../planners/')
sys.path.append('../planners/UPOM/')
sys.path.append('../planners/RAEPlan/')
sys.path.append('../planners/APEPlan/')
sys.path.append('../learning/')
sys.path.append('../learning/encoders/')
from main import testBatch
from shared import GLOBALS
GLOBALS.SetUtility('efficiency')
GLOBALS.SetUseTrainedModel(None)
GLOBALS.SetDataGenerationMode(None)
GLOBALS.SetModelPath('../learning/models/')
GLOBALS.SetTimeLimit(300)"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', planner=None)"
            fname="../raeResults/2021/${domain}/RAE.txt"
            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
