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

Once loaded, the GUI will look like this:  
![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Load_Video/Images/gui.png "Video Processing GUI")

---------
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
| **&#124;<**      | N/A        | Move to the beginning of the range
| **<&#124;**      | q          | Skip backwards
| **&#124;<&#124;**     | LEFT or a  | Steps one frame backwards
| **&#124;>&#124;**     | RIGHT or d | Steps one frame forwards 
| **&#124;>**      | e          | Skip forwards
| **>&#124;**      | N/A        | Move to the end of the range
| N/A         | ESC        | Exit program

---------
#### Recommended Instructions   
   1. Click Load and navigate to the flash drive, `/media/FLASH_DRIVE_NAME`, then select the video file you would like to load.  
   2. Get a cup of coffee while converting and loading (The Pis can only convert at about 1FPS)
   3. Once loaded, move to the first frame the ball moves and then go back one frame. Click the Start button to set the start point.
   4. Now move to the frame where the ball touches the ground. Click the Finish button to set the end point. Because the range is set, 
   now you can only move between the frames in the range.
   5. Go back to the start of the ball dropping. For each frame in the range, click on the ball. Try to click the same part of the ball 
   (we recommend that you track the front end of the ball). The X-Coordinate doesn't matter but the Y-Coordinate should be as close as possible.