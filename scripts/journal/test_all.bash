#!/bin/sh
# This script is to run APE by calling APE-plan

echo "Executing tests for APE."

for domain in "IP" #"CR" "SD" "IP" "EE"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10") 
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12" "problem13" "problem14")
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20")
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem17" "problem18") # "problem19" "problem11" "problem12" "problem13" "problem14" "problem15"  "problem16" 
    fi
    for problem in ${P[@]}
    do
        for sampleCount in "5" "10" "25" "50" "75"
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
globals.SetSampleCount($sampleCount)
globals.SetSearchDepth(float('inf'))
globals.SetSimulationMode('off')"
            echo $domain $problem $sampleCount
            time_test="testRAEBatch(domain='$domain', problem='$problem', useAPEplan=True)"

            fname="outputs2/$domain/plan$sampleCount.txt"

            echo "Time test of $domain $problem $sampleCount" >> $fname
            python3 -m timeit -n 1 -s "$setup" "$time_test" >> $fname
        done
    done
done