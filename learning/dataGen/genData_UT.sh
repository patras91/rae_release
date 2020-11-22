#!/bin/sh
domain="testInstantiation"
runs=1
P=(
"problem6"
)
UCT=(
"100" 
)
for problem in ${P[@]}
do
    for uctCount in ${UCT[@]}
    do
setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/unitTests')
sys.path.append('../../shared/')
sys.path.append('../../learning/')
sys.path.append('../../learning/encoders/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetTimeLimit(1800)
GLOBALS.SetUCTRuns($uctCount)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetOpt('max')
GLOBALS.SetHeuristicName('h2')
GLOBALS.SetDataGenerationMode('learnH')
GLOBALS.SetUseTrainedModel('n')
GLOBALS.SetMaxDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test"
((counter++))
done
    done
done
