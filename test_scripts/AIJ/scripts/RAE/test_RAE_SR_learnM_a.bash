#!/bin/sh
domain="SR"
runs=1
P=(
"problem43" 
"problem32" 
"problem102" 
"problem96" 
"problem73" 
"problem105" 
"problem27" 
"problem85" 
"problem35" 
"problem36" 
"problem38" 
"problem24" 
"problem89" 
"problem75" 
"problem76" 
"problem106" 
"problem108" 
"problem78" 
"problem88" 
"problem39" 
"problem95" 
"problem72" 
"problem46" 
"problem107" 
"problem92" 
"problem21" 
"problem110" 
"problem71" 
"problem30" 
"problem113" 
"problem60" 
"problem64" 
"problem42" 
"problem84" 
"problem23" 
"problem97" 
"problem111" 
"problem90" 
"problem65" 
"problem54" 
"problem56" 
"problem112" 
"problem98" 
"problem109" 
"problem55" 
"problem81" 
"problem100" 
"problem50" 
"problem104" 
"problem74" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/SR/training')
sys.path.append('../../../../shared/')
sys.path.append('../../../../learning/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
GLOBALS.SetUseTrainedModel('a')
GLOBALS.SetLearningMode(None)
GLOBALS.SetModelPath('../../../../learning/models/')
GLOBALS.SetTimeLimit(300)"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"
            fname="../../../../../raeResults/${domain}_v_journal/RAE_with_learnM_a_training.txt"
            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
