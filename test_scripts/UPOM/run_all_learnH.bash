#!/bin/sh
Domains=("CR" "SD" "SR" "EE" "OF")
Mode=("UCT")
Depth=("lim")
Parts=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10") 
for domain in ${Domains[@]}
do
    for m in ${Mode[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname1="../../../../autoGen_scripts/${domain}/test_RAEplan_${domain}_${m}_${d}_part_${p}_eff_h_learnH.bash"
            	./$fname1
            done
        done
    done
done