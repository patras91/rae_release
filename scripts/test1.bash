#!/bin/sh

echo "Executing tests for RAE-S."

for problem in "problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" #
do
    for domain in "CR" #"SD" "IP" "CR" "EE"
    do
        setup="
import sys
sys.path.append('..')
sys.path.append('../domains/')
sys.path.append('../problems/')
from testRAE import verbosity, SetMode, globals, testRAEBatch
verbosity(0)
SetMode('Counter')
globals.SetK(1)
globals.SetConcurrent('n')
globals.SetLazy('n')
globals.SetSimulationMode('off')"
        echo $domain $problem
        time_test="testRAEBatch(domain='$domain', problem='$problem', doSampling=True)"

        fname="test_batch10_CR_normalLA1_output.txt"
        #echo '' >> $fname

		echo "Time test of $domain $problem" >> $fname
        python3 -m timeit -n 1 -s "$setup" "$time_test" >> $fname
    done
done