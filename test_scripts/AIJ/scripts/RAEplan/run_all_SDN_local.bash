#!/bin/sh
Domains=("SDN")
Planner=("UPOM")
Depth=("max")
Parts=("1") 
for domain in ${Domains[@]}
do
    for pl in ${Planner[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname1="../../../../autoGen_scripts/${domain}/test_${pl}_${domain}_${d}_part_${p}_eff.sh"
            	./$fname1
            done
        done
    done
done