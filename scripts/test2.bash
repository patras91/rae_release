#!/bin/sh

echo "Executing tests for APE."

#for problem in  "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" #"problem2" "problem3"
for problem in "problem14" #"problem14" "problem15" "problem16" "problem17" "problem18" "problem19" "problem20"
do
    for domain in "IP" #"SD" "IP" "CR" "EE"
    do
        for mode in 'y' 'n'
        do
            if [ "$mode" = "n" ]; then
                K=(1 2)
            else
                K=(1 2)
            fi
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
                    fname="outputs/$domain/normal/K$k.txt"
                else
                    fname="outputs/$domain/lazy/K$k.txt"
                fi

		        echo "Time test of $domain $problem" >> $fname
                python3 -m timeit -n 1 -s "$setup" "$time_test" >> $fname
            done
        done
    done
done