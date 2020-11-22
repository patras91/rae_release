#!/bin/sh
# This script is to delete unused problems
counter=100
while [ $counter -le 120 ]
do
	fname=problem{$counter}.py
	rm fname
	((counter++))
done