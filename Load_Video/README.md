Processing Video
=============

Once the video has been recorded to the flash drive, the apparatus is no longer needed for the rest of the experiment. This program is 
for grabbing the coordinates of the ball in each frame as the ball is dropping. This program does not require parallelization so it can run
on just one Raspberry Pi.

----------
#### Setup  
   1. Connect one of the Raspberry Pis with a monitor, keyboard, and mouse. Then supply it power.  
   2. Plug in the flash drive that was used to record the video.  
   3. Either run the script called `load_video.sh` or while in the Load_Video directory, type:  
```
python load_video.py
```
---------

Once loaded, the GUI will look like this:  
![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Load_Video/Images/gui.png "Video Processing GUI")

#### Controls
There are a mixture of buttons and keyboard shortcuts to make things easier.  

| Button      | Key        | Description  
|:-----------:|:----------:| --------------------------
| Load        | N/A        | Converts and loads a .h264 video file
| Start       | s          | Sets the start frame
| Finish      | f          | Sets the last frame
| Reset Range | c          | Clears the frame
| Show/Hide   | N/A        | Shows/Hides all data points clicked
| Clear       | N/A        | Clears all data points
| Save        | N/A        | Save a Python Pickle File of the coordinates
| **|<**      | N/A        | Move to the beginning of the range
| **<|**      | q          | Skip backwards
| **|<|**     | LEFT or a  | Steps one frame backwards
| **|>|**     | RIGHT or d | Steps one frame forwards 
| **|>**      | e          | Skip forwards
| **>|**      | N/A        | Move to the end of the range
| N/A         | ESC        | Exit program
