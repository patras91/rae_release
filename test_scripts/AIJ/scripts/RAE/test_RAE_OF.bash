#!/bin/sh
domain="OF"
runs=3
P=(
"problem55" 
"problem109" 
"problem72" 
"problem12" 
"problem25" 
"problem48" 
"problem53" 
"problem45" 
"problem57" 
"problem73" 
"problem103" 
"problem89" 
"problem20" 
"problem51" 
"problem74" 
"problem37" 
"problem11" 
"problem21" 
"problem36" 
"problem29" 
"problem76" 
"problem39" 
"problem105" 
"problem15" 
"problem68" 
"problem67" 
"problem90" 
"problem27" 
"problem56" 
"problem95" 
"problem77" 
"problem18" 
"problem34" 
"problem66" 
"problem23" 
"problem91" 
"problem28" 
"problem22" 
"problem59" 
"problem97" 
"problem47" 
"problem30" 
"problem78" 
"problem42" 
"problem64" 
"problem49" 
"problem75" 
"problem94" 
"problem61" 
"problem13" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/OF/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
GLOBALS.SetTimeLimit(600)"
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
