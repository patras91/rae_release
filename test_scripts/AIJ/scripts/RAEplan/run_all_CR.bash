#!/bin/sh
Domains=("EE")
Mode=("UCT")
Depth=("lim")
Parts=("4") 
for domain in ${Domains[@]}
do
    for m in ${Mode[@]}
    do
        for d in ${Depth[@]}
        do
            for p in ${Parts[@]}
            do
            	fname1="../../../../autoGen_scripts/${domain}/test_RAEplan_${domain}_${m}_${d}_part_${p}_eff.bash"
                #sbatch -n 1 -N 1 --share -t 2:00:00 ./$fname1
                #fname2="../../../../autoGen_scripts/CR/test_RAEplan_${domain}_${m}_${d}_part_${p}_sr.bash"
                #sbatch -n 1 -N 1 --share -t 2:00:00 ./$fname2
                fname2="../../../../autoGen_scripts/${domain}/test_RAEplan_${domain}_${m}_${d}_part_${p}_eff_h_h0.bash"
                #sbatch -n 1 -N 1 --share -t 2:00:00 ./$fname2
                ./$fname1
                #./$fname2
            done
        done
    done
done