#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for APEplan."

for domain in "CR" #"CR" "SD" "IP" "EE"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1") # "problem2" "problem3" "problem4" "problem5" "problem6") #   "problem7" "problem8" "problem9" "problem10") #
        B=("1" "2" "3" "4")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34") 
        B=("1" "2" "3")
    fi
    if [ "$domain" = "CR" ]; then
        P=(
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
"problem115"
"problem116"
"problem117"
"problem118"
"problem119"
"problem120"
"problem121"
"problem122"
"problem123"
"problem124"
"problem125"
"problem126"
"problem127"
"problem128"
"problem129"
"problem130"
"problem131"
"problem132"
"problem133"
"problem134"
"problem135"
"problem136"
"problem137"
"problem138"
"problem139"
"problem140"
)
        #P=()
        #P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28" "problem29" "problem30" "problem31" "problem32" "problem33" "problem34" "problem35") 
        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20") #   )
        B=("1" "2" "3") # "3")
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem21" "problem22" "problem23" "problem24" "problem25" "problem26" "problem27" "problem28") #) #"problem21" "problem22"  "problem11" "problem12" "problem13" "problem14" "problem15"  ) #
        B=("1" "2" "3") #"1") #"3")
    fi
    for problem in ${P[@]}
    do
        setup="
import sys
sys.path.append('../../APE_and_APEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/CR')
sys.path.append('../../shared/')
sys.setrecursionlimit(6000)
from testAPEandAPEplan import globals, testBatch"
counter=1
while [ $counter -le 10 ]
do
                echo $domain $problem $b $k $counter/10
                time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

                fname="$domain/ape_plan.txt"

                echo "Time test of $domain $problem $sampleCount" >> $fname
                python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
                #python3 ../../RAE_and_RAEplan/testRAEandRAEplan.py --domain $domain --problem $problem --b $b --k $k --showOutputs 'off' --v 0 --plan y >> $fname
((counter++))
done
    done
done
