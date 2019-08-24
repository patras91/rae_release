#!/bin/sh
domain="SD"
runs=1
P=(
"problem1119" 
"problem1059" 
"problem1014" 
"problem1070" 
"problem1068" 
"problem1106" 
"problem1028" 
"problem1029" 
"problem1046" 
"problem1103" 
"problem1100" 
"problem1121" 
"problem1086" 
"problem1063" 
"problem1057" 
"problem1069" 
"problem1116" 
"problem1055" 
"problem1124" 
"problem1083" 
"problem1049" 
"problem1039" 
"problem1125" 
"problem1087" 
"problem1115" 
"problem1033" 
"problem1084" 
"problem1066" 
"problem1019" 
"problem1089" 
"problem1053" 
"problem1010" 
"problem1078" 
"problem1120" 
"problem1085" 
"problem1051" 
"problem1110" 
"problem1107" 
"problem1045" 
"problem1032" 
"problem1007" 
"problem1104" 
"problem1036" 
"problem1016" 
"problem1003" 
"problem1094" 
"problem1013" 
"problem1127" 
"problem1027" 
"problem1043" 
)
for problem in ${P[@]}
do
setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/SD/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetOpt('max')
GLOBALS.SetTimeLimit(300)"
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
