#!/usr/bin/env bash

curLoc=`dirname $BASH_SOURCE`
cd $curLoc
cd ./Plotting
mpirun -np 2 -machinefile ./nodes.txt python plotting.py