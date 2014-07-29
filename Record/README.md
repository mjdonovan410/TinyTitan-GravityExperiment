Recording
=========

Recording the object dropping is most important part of the experiment. If done incorrectly, final results may be skewed and imprecise.

--------------

#### Starting Checklist  
   1. Remove 2 Raspberry Pis from Tiny Titan being sure to keep the SD cards with the correct Pi  
   2. Mount the Raspberry Pis on the frame of the experiment within reach of the appropriate cables  
   3. On the larger frame with the claw, plug in a monitor, mouse, keyboard, and an Ethernet cable into the Pi. Leave Pi unplugged from power.
   4. On the same frame, connect the jumper wires to the servo and then the Pi. Red - Pin 2, Black - Pin 6, Yellow - Pin 7 on the [GPIO](http://www.andremiller.net/wp-content/uploads/2013/01/RaspberryPiPinouts2.png)  
   5. On the smaller frame, place the ribbon cable from the Pi Camera into the slot closest to the Ethernet port. Make sure the bare wire side of the cable is facing the HDMI port.  
   6. Also on the smaller frame pi, plug in the other end of the Ethernet cable connecting the two Pis together.  
   7. Now move the frames apart making sure the poles are at least 7ft apart (assuming a 6ft dropping height) and provide power to the Pis.  
   8. Assuming that the files have already been loaded on the Pis, open `nodes.txt` and edit it with the IP addresses from each Pi being sure that the first IP address is the Pi connected to the claw.  
   
--------------

At this point, everything should be properly setup and you can either move back a directory and run the script called `record_drop.sh` or type:  
```
mpirun -np 2 -machinefile ./nodes.txt sudo -E python record.py
```

The Pis will take about 10 seconds to setup MPI, but once the GUI is loaded, it is ready to be used.

Once ready, this GUI will pop up:  
![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Record/Images/gui.png "Record GUI")

Now comes the simple part. Using the mouse, click on a button that will command the claw to either open or close the claw to prepare the object. 
Once nothing is obstructing the camera's view, press the `Drop` button. There will be a slight delay while the camera warms up and then the object will drop.

The recording will be saved on the flash drive **NOT the SD card**, so make sure there is a flash drive plugged into the Pi connected to the camera.
