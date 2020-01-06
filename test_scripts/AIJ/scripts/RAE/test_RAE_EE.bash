#!/bin/sh
domain="EE"
runs=1
P=(
"problem5" 
"problem170" 
"problem134" 
"problem108" 
"problem187" 
"problem91" 
"problem72" 
"problem159" 
"problem131" 
"problem190" 
"problem86" 
"problem7" 
"problem35" 
"problem85" 
"problem3" 
"problem173" 
"problem44" 
"problem31" 
"problem29" 
"problem103" 
"problem75" 
"problem20" 
"problem58" 
"problem129" 
"problem158" 
"problem78" 
"problem42" 
"problem14" 
"problem188" 
"problem161" 
"problem17" 
"problem50" 
"problem89" 
"problem136" 
"problem123" 
"problem104" 
"problem143" 
"problem163" 
"problem57" 
"problem2" 
"problem43" 
"problem52" 
"problem156" 
"problem183" 
"problem174" 
"problem168" 
"problem164" 
"problem68" 
"problem73" 
"problem178" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/EE/auto')
sys.path.append('../../../../shared/')
sys.path.append('../../../../learning/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
GLOBALS.SetUseTrainedModel('n')
GLOBALS.SetLearningMode(None)
GLOBALS.SetTimeLimit(300)"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"
            fname="../../../../../raeResults/${domain}_v_journal/RAE.txt"
            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
