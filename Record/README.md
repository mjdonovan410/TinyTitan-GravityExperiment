Recording
=========

Recording the object dropping is most important part of the experiment. If done incorrectly, final results may be skewed and imprecise.

--------------

#### Starting Checklist  
   1. Remove 2 Raspberry Pis from Tiny Titan being sure to keep the SD cards with the correct Pi  
   2. Mount the Raspberry Pis on the frame of the experiment within reach of the appropriate cables  
   3. On the claw Pi, plug in a monitor, mouse, keyboard, and an Ethernet cable into the Pi. Leave Pi unplugged from power.
   4. Also on the claw Pi, connect the jumper wires to the servo and then the Pi.  
   **Red - Pin 2, Black - Pin 6, Yellow - Pin 7** on the [GPIO](http://www.andremiller.net/wp-content/uploads/2013/01/RaspberryPiPinouts2.png)  
   5. On the camera Pi, place the ribbon cable from the Pi Camera into the slot closest to the Ethernet port. Make sure the bare wire side of the cable is facing the HDMI port. Also leave Pi unplugged from power.  
   6. Also on the camera Pi, plug in the loose end of the Ethernet cable thus connecting the claw Pi to the camera Pi.  
   7. Now move the frames apart making sure the center poles are at least 7ft apart (assuming a 6ft dropping height) and provide power to both Pis.  
   8. Assuming that the files have already been loaded on the Pis, open `nodes.txt` and edit it with the IP addresses from each Pi being sure that the first IP address is the claw Pi.  
   
At this point, everything should be properly setup and you can either move back to the root directory and run the script called `record_drop.sh` or type:  

```
mpirun -np 2 -machinefile ./nodes.txt python record.py
```

The Pis will take about 10 seconds to setup MPI, but once the GUI is loaded, it is ready to be used. This GUI will pop up:  

![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Record/Images/gui.png "Record GUI")

Now comes the simple part. Using the mouse, click on a button that will command the claw to either open or close the claw to prepare the object. 
Once nothing is obstructing the camera's view, press the `Drop` button. There will be a slight delay while the camera warms up and then the object will drop.

##### Keyboard Shortcuts  
* LEFT - Open
* RIGHT - Close
* SPACE - Drop
* ESC - Quit

The recording will be saved on the flash drive **NOT the SD card**, so make sure there is a flash drive plugged into the camera Pi. The program will only save the file if there is a flash drive plugged in.

-------
#### Inputs and Outputs
No inputs are require for this part of the experiment.  

To control the servo, we used ServoBlaster. The installation for ServoBlaster is terribly documented as it has changed several times over the years. To install ServoBlaster, type:  

```
$ git clone https://github.com/richardghirst/PiBits.git
```  
```
$ cd PiBits/ServoBlaster/user
```  
```
$ make
```  

Then every time you want to control the servo, you'll need to run `sudo ./servod` in that directory; then `sudo killall servod` to end the process. To send commands to the claw, you have to type:

```
echo [Servo]=[Angle] > /dev/servoblaster
``` *without the brackets on servo or angle*.  

The way ServoBlaster is setup, pin 7 on the GPIO is actually servo 0, so for simplicity, I would recommend using pin 7 for the yellow connector. Thus the command would change to  
`echo 0=[Angle] > /dev/servoblaster`.

The 2 Pis talk to each other using mpi4py. The claw Pi will send a signal to the camera Pi and will run this command:  
```
raspivid -fps 90 -h 640 -w 480 -t 3000 -o /media/FLASH_DRIVE_NAME/vid.h264
```  

The video is 3s long, but only the last second of video is converted. The camera takes about two seconds to be able to match the requested 90FPS. The video records to the flash drive because it has a faster write speed than the SD card, thus can reach 90FPS.