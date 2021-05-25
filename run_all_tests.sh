#!/bin/sh
mkdir ../raeResults/2021/fetch
./test_scripts/autoGen_scripts/fetch/test_RAE_fetch.bash
mkdir ../raeResults/2021/fetch_efficiency
./test_scripts/autoGen_scripts/fetch/test_fetch_RAE_UPOM_h_None_part_1_efficiency.bash