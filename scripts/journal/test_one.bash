#!/bin/sh
# This script is to just execute APE without calling APEplan. So, it is basically RAE

echo "Executing tests for APE."

for domain in "CR" #"SD" "IP" "CR" "EE"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10")
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12" "problem13" "problem14")
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem11") # "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20")
    fi
    if [ "$domain" = "EE" ]; then
        P=( "problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18") # "problem19"
    fi
    for problem in ${P[@]}
    do
        setup="
import sys
sys.path.append('../..')
sys.path.append('../../domains/')
sys.path.append('../../problems/')
from testAPE import verbosity, SetMode, globals, testRAEBatch
verbosity(0)
SetMode('Counter')
globals.SetConcurrent('n')
globals.SetLazy('n')
globals.SetSampleCount(100)
globals.SetSearchDepth(float('inf'))
globals.SetSimulationMode('off')"
        echo $domain $problem
        time_test="testRAEBatch(domain='$domain', problem='$problem', useAPEplan=False)"

        fname="outputs/$domain/APE.txt"
        #echo '' >> $fname

		echo "Time test of $domain $problem" >> $fname
        python3 -m timeit -n 2 -s "$setup" "$time_test" >> $fname
    done
done