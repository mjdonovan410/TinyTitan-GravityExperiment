#!/usr/bin/env bash

curLoc=`dirname $BASH_SOURCE`
cd $curLoc/Plotting
mpirun -np $1 -machinefile ./nodes.txt python plotting.py