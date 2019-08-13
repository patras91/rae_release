#!/bin/sh
Domains=("SR")
Mode=("SLATE" "UCT")
Depth=("lim" "max")
Parts=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10") 
for domain in ${Domains[@]}
do
    for m in ${Mode[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname="test_RAEplan_${domain}_${m}_${d}_part_${p}.bash"
            	sbatch -n 1 -N 1 --share -t 20:00:00 ./$fname
            done
        done
    done
done