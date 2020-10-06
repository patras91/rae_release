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
            	fname1="../../../../autoGen_scripts/${domain}/test_${domain}_${pl}_${d}_part_${p}_eff.bash"
            	sbatch -n 1 -N 1 --share -t 4:00:00 ./$fname1
                fname2="../../../../autoGen_scripts/${domain}/test_${domain}_${pl}_${d}_part_${p}_sr.bash"
                sbatch -n 1 -N 1 --share -t 4:00:00 ./$fname2
                fname3="../../../../autoGen_scripts/${domain}/test_${domain}_${pl}_${d}_part_${p}_res.bash"
                sbatch -n 1 -N 1 --share -t 4:00:00 ./$fname3
            done
        done
    done
done