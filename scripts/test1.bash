#!/bin/sh

echo "Executing tests for RAE-S."

for problem in "problem1" # "problem2"
do
    for domain in "STE" "SF" "SOD" "SD" "IP" "CR" "EE"
    do
        setup="
import sys
sys.path.append('..')
sys.path.append('../domains/')
sys.path.append('../problems/')
from testRAE import testRAE, verbosity, SetMode, globals
verbosity(0)
SetMode('Counter')
globals.SetSimulationMode('off')"

        time_test="testRAE(domain='$domain', problem='$problem', doSampling='y')"

        fname="test_output.txt"
        echo '' >> $fname

		echo "Time test of '$domain $problem'" >> $fname
        python -m timeit -s "$setup" "$time_test" >> $fname
    done
done