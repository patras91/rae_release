#!/bin/sh
# This script is to just run RAE without calling any planner. 

echo "Executing tests for RAE without any planning."
domain="CR" # SR, EE, CR, IP, SD, OF
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34") 
    fi
    if [ "$domain" = "CR" ]; then
        #P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34" "problem35") 
P=(
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
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31") 
    fi
    if [ "$domain" = "SR" ]; then
        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18") # "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31") 
        P=(
"problem19"
"problem20"
"problem21"
"problem22"
"problem23"
"problem24"
"problem25"
"problem26"
"problem27"
"problem28"
"problem29"
"problem30"
"problem31"
"problem32"
"problem33"
"problem34"
"problem35"
"problem36"
"problem37"
"problem38"
"problem39"
"problem40"
"problem41"
"problem42"
"problem43"
"problem44"
"problem45"
"problem46"
"problem47"
"problem48"
"problem49"
"problem50"
"problem51"
"problem52"
"problem53"
"problem54"
"problem55"
"problem56"
"problem57"
"problem58"
"problem59"
"problem60"
"problem61"
"problem62"
"problem63"
"problem64"
"problem65"
"problem66"
"problem67"
"problem68"
"problem69"
"problem70"
"problem71"
"problem72"
"problem73"
"problem74"
"problem75"
"problem76"
"problem77"
"problem78"
"problem79"
"problem80"
"problem81"
"problem82"
"problem83"
"problem84"
"problem85"
"problem86"
"problem87"
"problem88"
"problem89"
"problem90"
"problem91"
"problem92"
"problem93"
"problem94"
"problem95"
"problem96"
"problem97"
"problem98"
"problem99"
"problem100"
"problem101"
"problem102"
"problem103"
"problem104"
"problem105"
"problem106"
"problem107"
"problem108"
"problem109"
"problem110"
"problem111"
"problem112"
"problem113"
"problem114"
)
    fi

    for problem in ${P[@]}
    do
        setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/$domain')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testRAEandRAEplan import globals, testBatch
globals.Setb(1)
globals.Setk(1)"
counter=1
while [ $counter -le 1 ]
do
        echo $domain $problem $counter/1
        time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=False)"

        fname="${domain}_v7/RAE.txt"

		echo "Time test of $domain $problem"  >> $fname
        python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
    done
done