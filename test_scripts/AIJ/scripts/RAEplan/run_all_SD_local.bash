#!/bin/sh
Domains=("SD")
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
                fname1="../../../../autoGen_scripts/SD/test_RAEplan_${domain}_${m}_${d}_part_${p}_eff.bash"
                ./$fname1
            	fname2="../../../../autoGen_scripts/SD/test_RAEplan_${domain}_${m}_${d}_part_${p}_sr.bash"
            	./$fname2                
            done
        done
    done
done