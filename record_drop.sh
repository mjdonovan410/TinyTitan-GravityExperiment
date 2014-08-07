#!/usr/bin/env bash

curLoc=`dirname $BASH_SOURCE`
cd $curLoc/Record
mpirun -np 2 -machinefile ./nodes.txt python record.py