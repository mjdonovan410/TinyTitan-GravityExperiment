TinyTitan-PhysicsExperiment
===========================

This physics experiment is a fun and interactive way for students to learn about the effects of gravity and drag on a falling object.
Once the apparatus has been built, these user-friendly programs will be able to assist in the collection of data and provide a detailed 
description of the results. This experiment can be performed by people of all skill levels.

The experiment is broken up into three stages:  
   1. Recording the object falling  
   2. Obtaining data coordinates from the recorded video  
   3. Plotting and fitting the data  

Any stage of this experiment can be replaced with user code, but these programs provide both a simplistic user interface and a benchmark 
for the students to compare results.

Each folder has a separate README file explaining each program and how to properly operate them. Provided are some shell scripts that 
make running in terminal simpler.

------------
#### Software Dependencies
##### Python  
* pygame  
* mpi4py  
* matplotlib   
* six  
* parsing  
* dateutil  

##### Other  
* libav-tools

-----------
#### Hardware Dependencies

* *Tiny Titan Recording Apparatus*  
* *Tiny Titan* (recommended) **OR** 2 Raspberry Pi's and Linux Desktop  
* Pi Camera  
* Claw with Servo  
* 3 GPIO Jumper Wires  
* 10' Ethernet Cable  
* Flash Drive (Most sizes will suffice)  

----------

##Tiny Titan Recording Apparatus Instructions
This apparatus is built with a mixture of 80/20 and some material from the hardware store. The design was developed as simplistically as possible keeping in mind that not everyone has power tools or a high levels of building skills. Below will give very detailed instructions on how to develop both frames and assemble the claw.

------
#### Parts for Frames
##### 80/20  
|Part # | Quantity | Name                         | 
|:-----:|:--------:|------------------------------|
| 1010  |  3       | 1' 10 Series T-Slot          |
| 1010  |  3       | 2' 10 Series T-Slot          |
| 1010  |  3       | 3' 10 Series T-Slot          |
| 1010  |  1       | 6' 10 Series T-Slot          |
| 4112  |  2       | 7-Hole Tee Joining Plate     |
| 4140  |  2       | 5-Hole Tee Joining Plate     |
| 4115  |  12      | 4-Hole Inside Corner Bracket |
| 3393  |  14      | 10 Series BHSCS & ECON T-NUT |
| 3321  |  14      | 10 Series FBHSCS & ECON T-NUT|
| 3393  |  48      | 10 Series BHSCS & ECON T-NUT |
| 3321  |  10      | 10 Series FBHSCS & ECON T-NUT|
| 2015  |  10      | 10 Series End Cap            |

*End caps are not necessary, and they hardly stay on*