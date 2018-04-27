#!/bin/sh
# This script is to just execute APE without calling APEplan. So, it is basically RAE

echo "Executing tests for APE."

#for problem in "problem1" "problem2" "problem3" "problem4" "problem5" "problem6" "problem7" "problem8" "problem9" "problem10" "problem11" "problem12" "problem13" "problem14" #
for problem in "problem11" "problem12" "problem13" "problem14" "problem15" "problem16" "problem17" "problem18" "problem19"  # "problem20" #
do
    for domain in "EE" #"SD" "IP" "CR" "EE"
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
globals.SetSimulationMode('off')"
        echo $domain $problem
        time_test="testRAEBatch(domain='$domain', problem='$problem', useAPEplan=False)"

        fname="outputs/$domain/APE.txt"
        #echo '' >> $fname

		echo "Time test of $domain $problem" >> $fname
        python3 -m timeit -n 2 -s "$setup" "$time_test" >> $fname
    done
done