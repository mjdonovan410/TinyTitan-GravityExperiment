#!/usr/bin/env bash

curLoc=`dirname $BASH_SOURCE`
cd $curLoc
cd ./Record
mpirun -np 2 -machinefile ./nodes.txt sudo -E python record.py