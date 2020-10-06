#!/bin/sh
Domains=("SDN")
Planner=("UPOM")
Depth=("max")
Parts=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10") 
for domain in ${Domains[@]}
do
    for pl in ${Planner[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname1="../../../../autoGen_scripts/${domain}/test_${domain}_${pl}_${d}_part_${p}_res.bash"
            	./$fname1
                #fname2="../../../../autoGen_scripts/${domain}/test_${domain}_${pl}_${d}_part_${p}_sr.bash"
                #./$fname2
            done
        done
    done
done