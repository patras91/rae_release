#!/bin/sh
Domains=("OF")
Mode=("UCT")
Depth=("max")
Parts=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10") 
for domain in ${Domains[@]}
do
    for m in ${Mode[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname1="test_RAEplan_${domain}_${m}_${d}_part_${p}_eff.bash"
            	sbatch -n 1 -N 1 --share -t 1:00:00 ./$fname1
                #fname2="test_RAEplan_${domain}_${m}_${d}_part_${p}_sr.bash"
                #sbatch -n 1 -N 1 --share -t 0:30:00 ./$fname2
            done
        done
    done
done