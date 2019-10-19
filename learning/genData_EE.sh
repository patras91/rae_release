#!/bin/sh
domain="EE"
runs=1
P=(
"problem1"
"problem2"
"problem3"
"problem4"
"problem5"
"problem6"
"problem7"
"problem8"
"problem9"
"problem10"
"problem11"
"problem12"
"problem13"
"problem14"
"problem15"
"problem16"
"problem17"
"problem18"
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
"problem141"
"problem142"
"problem143"
"problem144"
"problem145"
"problem146"
"problem147"
"problem148"
"problem149"
"problem150"
"problem151"
"problem152"
"problem153"
"problem154"
"problem155"
"problem156"
"problem157"
"problem158"
"problem159"
"problem160"
"problem161"
"problem162"
"problem163"
"problem164"
"problem165"
"problem166"
"problem167"
"problem168"
"problem169"
"problem170"
"problem171"
"problem172"
"problem173"
"problem174"
"problem175"
"problem176"
"problem177"
"problem178"
"problem179"
"problem180"
"problem181"
"problem182"
"problem183"
"problem184"
"problem185"
"problem186"
"problem187"
"problem188"
"problem189"
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
sys.path.append('../RAE_and_RAEplan/')
sys.path.append('../shared/domains/')
sys.path.append('../shared/problems/EE/auto')
sys.path.append('../shared/')
from testRAEandRAEplan import GLOBALS, testBatch
GLOBALS.SetTimeLimit(300)
GLOBALS.SetUCTRuns($uctCount)
GLOBALS.SetUCTmode('UCT')
GLOBALS.SetOpt('max')
GLOBALS.SetLearningMode('genDataPlanner')
GLOBALS.SetSearchDepth(float(\"inf\"))"
counter=1
while [ $counter -le $runs ]
do
            echo $domain $problem " Run " $counter/$runs
            time_test="testBatch(domain='$domain', problem='$problem', useRAEplan=True)"
            echo "uctCount = " $uctCount
            fname="../../raeResults/${domain}_v_journal_eff/training_data_rae_plan_uct_${uctCount}.txt"
            echo "Time test of $domain $problem $uctCount" >> $fname
            python3 -m timeit -n 1 -r 1 -s "$setup" "$time_test" >> $fname
((counter++))
done
    done
done
