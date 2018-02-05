#!/bin/sh

echo "Executing tests for APE."

#for problem in "problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" #
#for problem in "problem11" "problem12" "problem13" "problem14" # "problem15" #  "problem18" "problem19" "problem20"  "problem19" #"problem17" #
#do
for domain in "EE" # "CR" # "SD" "IP"
do
    if [ "$domain" = "SD" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10")
        K=(1 2 3 4)
    fi
    if [ "$domain" = "IP" ]; then
        P=("problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12" "problem13" "problem14")
        K=(1 2)
    fi
    if [ "$domain" = "CR" ]; then
        P=("problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20")
        K=(1 2 3)
    fi
    if [ "$domain" = "EE" ]; then
        P=("problem19") # "problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18"
        K=(1 2 3 4)
    fi
    for problem in ${P[@]}
    do
        for mode in 'n' 'y'
        do
            for k in ${K[@]}
            do
                setup="
import sys
sys.path.append('..')
sys.path.append('../domains/')
sys.path.append('../problems/')
from testRAE import verbosity, SetMode, globals, testRAEBatch
verbosity(0)
SetMode('Counter')
globals.SetK($k)
globals.SetConcurrent('n')
globals.SetLazy('$mode')
globals.SetSimulationMode('off')"
                echo $domain $problem $k $mode
                time_test="testRAEBatch(domain='$domain', problem='$problem', doSampling=True)"

                if [ "$mode" = "n" ]; then
                    fname="outputs_with_arbitrary_order/$domain/active/K$k.txt"
                else
                    fname="outputs_with_arbitrary_order/$domain/lazy/K$k.txt"
                fi

		        echo "Time test of $domain $problem" >> $fname
                python3 -m timeit -n 2 -s "$setup" "$time_test" >> $fname
            done
        done
    done
done