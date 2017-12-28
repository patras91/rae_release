#!/bin/sh

echo "Executing tests for RAE-S."

for problem in "problem1" "problem2" "problem3" "problem4" "problem5" "problem6" #"problem2" "problem3" "problem4"
do
    for domain in "EE" #"SD" "IP" "CR" "EE"
    do
        setup="
import sys
sys.path.append('..')
sys.path.append('../domains/')
sys.path.append('../problems/')
from testRAE import testRAE, verbosity, SetMode, globals
verbosity(0)
SetMode('Counter')
globals.SetK(1)
globals.SetConcurrent('n')
globals.SetLazy('n')
globals.SetSimulationMode('off')"

        time_test="testRAE(domain='$domain', problem='$problem', doSampling=False)"

        fname="test_batch10_noLA_output.txt"
        #echo '' >> $fname

		echo "Time test of $domain $problem" >> $fname
        python3 -m timeit -n 1 -s "$setup" "$time_test" >> $fname
    done
done