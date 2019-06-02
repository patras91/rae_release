#!/bin/sh
# This script is to run RAE by calling RAE-plan

echo "Executing tests for RAE and RAE-plan."

for domain in "SR" #"CR" "SD" "IP" "EE"
do
    if [ "$domain" = "SR" ]; then
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

        #P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18") # "problem11" "problem12") #   "problem7" "problem8" "problem9" "problem10") #
        B=("1" "2" "3" "4")
    fi
    for problem in ${P[@]}
    do
        for b in ${B[@]}
        do 
            for k in "3" #"20" # "1" "2" "3" "4" "8" "12" "16" # 
            do
            for d in "3" "6" "9" "12" "15" 
            do
                setup="
import sys
sys.path.append('../../RAE_and_RAEplan/')
sys.path.append('../../shared/domains/')
sys.path.append('../../shared/problems/SR')
sys.path.append('../../shared/')
from testRAEandRAEplan import globals, testBatch
globals.SetSearchDepth($d)
globals.Setb($b)
globals.Setk($k)"
counter=1
while [ $counter -le 1 ]
do
                echo $domain $problem $b $k $d $counter/1
                time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"

                fname="${domain}_v8/rae_plan_b_${b}_k_${k}_d_${d}.txt"

                echo "Time test of $domain $problem $sampleCount" >> $fname
                python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
                #python3 ../../RAE_and_RAEplan/testRAEandRAEplan.py --domain $domain --problem $problem --b $b --k $k --showOutputs 'off' --v 0 --plan y >> $fname
((counter++))
done
done
            done
        done
    done
done