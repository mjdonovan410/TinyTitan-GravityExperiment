Plotting
========

Plotting the data is obviously where the meat of this experiment lies. Plotting can either be done by the students, using this program, or both with this being a benchmark for the students. For this program, the data has been fit using the least squares algorithm due to its simplicity.  

-----------
#### Setup
1. Connect all the Raspberry Pis together or reassemble Tiny Titan (Whichever is easier).
2. Make sure all the Pis can see each other. `$ ping pi#` (# being replaced with each pi's number)
3. It can be started from the root directory by running `./plot_data.sh #` (# is replaced with the number of processor to be used), or from the `Plotting` folder:  
   ```
   mpirun -np # ./nodes.txt python plotting.py
   ```

Again, with MPI, there is a lot of overhead waiting for the connections between the Pis to be made so it will take a few seconds to load. Once loaded, the GUI will pop up.  
![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Plotting/Images/gui.PNG"Plotting GUI")

------------------
#### Recommended Instructions
1. Once the program has loaded, press the `Load` button and select the data from which you would like to plot. It will take about 10 seconds to plot.  
2. Next, press the `Fit Data` button and again wait for the plot to load.
3. Lastly, press the `Advanced` button and go through all of the questions providing the correct mass, cross-sectional area, and air density(generally assume 1.1839).

*The red line on the plot is at the ideal conditions: g = 9.81 m/s^2, vi = 0 m/s, Cd = 0.47*

----------------
#### Input and Output
The input to this program is a list of coordinates and their timing. The format is a list that looks like
```
[((x1,y1),time1),...,((xN,yN),timeN)]
```
 
It's a list of tuples with the first element being the tuple coordinates and the second element being the time at which that coordinate occurs.

No output for this program outside of the final results.