#!/bin/sh

echo "Executing tests for RAE."

for problem in "problem1" # "problem2"
do
    for domain in "STE" "SF" "SOD" "SD" "IP" "CR" "EE"
    do
        python ../testRAE.py --v 0 --p $problem --d $domain --s y --simMode off
    done
done