#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE with RAE-plan."

domain="CR"
runs=1
P=(
"problem1000"
"problem1001"
"problem1002"
"problem1003"
"problem1004"
"problem1005"
"problem1006"
"problem1007"
"problem1008"
"problem1009"
"problem1010"
"problem1011"
"problem1012"
"problem1013"
"problem1014"
"problem1015"
"problem1016"
"problem1017"
"problem1018"
"problem1019"
"problem1020"
"problem1021"
"problem1022"
"problem1023"
"problem1025"
"problem1026"
"problem1027"
"problem1028"
"problem1029"
"problem1030"
"problem1031"
"problem1032"
"problem1033"
"problem1034"
"problem1035"
"problem1036"
"problem1037"
"problem1038"
"problem1039"
"problem1040"
"problem1041"
"problem1042"
"problem1043"
"problem1044"
"problem1045"
"problem1046"
"problem1047"
"problem1048"
"problem1049"
"problem1050"
"problem1051"
"problem1052"
"problem1053"
"problem1054"
"problem1055"
"problem1056"
"problem1057"
"problem1058"
"problem1059"
"problem1060"
"problem1061"
"problem1062"
"problem1063"
"problem1064"
"problem1065"
"problem1066"
"problem1067"
"problem1068"
"problem1069"
"problem1070"
"problem1071"
"problem1072"
"problem1073"
"problem1074"
"problem1075"
"problem1076"
"problem1077"
"problem1078"
"problem1079"
"problem1080"
"problem1081"
"problem1082"
"problem1083"
"problem1084"
"problem1085"
"problem1086"
"problem1087"
"problem1088"
"problem1089"
"problem1090"
"problem1091"
"problem1092"
"problem1093"
"problem1094"
"problem1095"
"problem1096"
"problem1097"
"problem1098"
"problem1099"
"problem1100"
"problem1101"
"problem1102"
"problem1103"
"problem1104"
"problem1105"
"problem1106"
"problem1107"
"problem1108"
"problem1109"
"problem1110"
"problem1111"
"problem1112"
"problem1113"
"problem1114"
"problem1115"
"problem1116"
"problem1117"
"problem1118"
"problem1119"
"problem1120"
"problem1121"
"problem1122"
"problem1123"
)
B=("1" "2" "3") # Can be 1, 2 or 3
for problem in ${P[@]}
do
    for uct in "25" "50" "100"
    #for b in ${B[@]}
    do 
    #    for k in "1" "3" "5" "8" "10" # can be any positive integer
    #    do
            setup="
import sys
sys.path.append('../../../../RAE_and_RAEplan/')
sys.path.append('../../../../shared/domains/')
sys.path.append('../../../../shared/problems/CR/auto')
sys.path.append('../../../../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetUCTRuns($uct)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetOpt('max')
GLOBALS.SetSearchDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " uct = " $uct ", Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

            fname="../../results/${domain}_v_journal/rae_plan_uct_${uct}.txt" # You should have a folder called CR in the current folder

            echo "Time test of $domain $problem" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
        #done
    done
done

