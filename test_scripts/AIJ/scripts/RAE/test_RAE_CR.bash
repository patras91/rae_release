#!/bin/sh
domain="CR"
runs=5
P=(
"problem1106" 
"problem1004" 
"problem1002" 
"problem1096" 
"problem1073" 
"problem1012" 
"problem1005" 
"problem1114" 
"problem1087" 
"problem1069" 
"problem1089" 
"problem1001" 
"problem1008" 
"problem1013" 
"problem1053" 
"problem1062" 
"problem1092" 
"problem1079" 
"problem1111" 
"problem1085" 
"problem1011" 
"problem1076" 
"problem1036" 
"problem1110" 
"problem1099" 
"problem1120" 
"problem1038" 
"problem1100" 
"problem1028" 
"problem1088" 
"problem1118" 
"problem1056" 
"problem1007" 
"problem1017" 
"problem1040" 
"problem1108" 
"problem1074" 
"problem1078" 
"problem1009" 
"problem1045" 
"problem1061" 
"problem1065" 
"problem1032" 
"problem1046" 
"problem1112" 
"problem1067" 
"problem1027" 
"problem1041" 
"problem1019" 
"problem1066" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/CR/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"
            fname="../../results/${domain}_v_journal/RAE.txt"
            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
done
