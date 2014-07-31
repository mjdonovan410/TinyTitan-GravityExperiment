Processing Video
=============

Once the video has been recorded to the flash drive, the apparatus is no longer needed for the rest of the experiment. This program is 
for grabbing the coordinates of the ball in each frame as the ball is dropping. This program does not require parallelization so it can run
on just one Raspberry Pi.

----------
#### Setup  
   1. Connect one of the Raspberry Pis with a monitor, keyboard, and mouse. Then supply it power.  
   2. Plug in the flash drive that was used to record the video.  
   3. Either run the script called `load_video.sh` in the root directory or while in the Load_Video directory, type: `python load_video.py`

Once loaded, the GUI will look like this:  
![alt text](https://github.com/mjdonovan410/TinyTitan-PhysicsExperiment/raw/master/Load_Video/Images/gui.png "Video Processing GUI")

---------
#### Controls
There are a mixture of buttons and keyboard shortcuts to make things easier.  

| Button            | Key        | Description  
|:-----------------:|:----------:| --------------------------
| Load              | N/A        | Converts and loads a .h264 video file
| Start             | s          | Sets the start frame
| Finish            | f          | Sets the last frame
| Reset Range       | c          | Clears the frame
| Show/Hide         | N/A        | Shows/Hides all data points clicked
| Clear             | N/A        | Clears all data points
| Save              | N/A        | Save a Python Pickle File of the coordinates
| **&#124;<**       | N/A        | Move to the beginning of the range
| **<&#124;**       | q          | Skip backwards
| **&#124;<&#124;** | LEFT or a  | Steps one frame backwards
| **&#124;>&#124;** | RIGHT or d | Steps one frame forwards 
| **&#124;>**       | e          | Skip forwards
| **>&#124;**       | N/A        | Move to the end of the range
| N/A               | ESC        | Exit program

---------
#### Recommended Instructions   
   1. Click the `Load` button and navigate to the flash drive, `/media/FLASH_DRIVE_NAME`, then select the video file you would like to load.  
   2. Get a cup of coffee while converting and loading (The Pis can only convert at about 1FPS)
   3. Once loaded, move to the first frame the ball moves and then go back one frame. Click the `Start` button to set the start point.
   4. Now move to the frame where the ball touches the ground. Click the `Finish` button to set the end point. Because the range is set, 
   now you can only move between the frames in the range.
   5. Go back to the start of the ball dropping. For each frame in the range, click on the ball in the picture. Try to click the same part of the ball 
   (we recommend that you track the leading end of the ball). The X-Coordinate doesn't matter but the Y-Coordinate should be as accurate as possible.  
   6. Once every frame has a point on it, click the `Show` button and make sure there aren't any jump or large gaps in the points. If there are, the camera could have skipped a frame thus rendering the data unreliable. (Out of 10 views tested, this only happened once)  
   7. If all is well, press the `Save` button and name your .p file. If there was a skipped frame, start over and make another recording.  

----------
#### Inputs and Outputs
For those that would like to make the program themselves, the input of this program is an .h264 file converted into images using avconv. The program doesn't recognize the file as being 90FPS so the timing was manually calculated. Also, because the camera takes time to warm up to 90FPS, I started converting at t = 1.5s (4.8) and only converted 1s (3.6).  
```
avconv -i fileName.h264 -ss 00:00:04.8 -t 00:00:03.6 -r 25 -f image2 pic_temp/%05d.jpg
```

The output of this program is a Python Pickle file. It is a list of tuples formatted like:  
```
[((x1,y1),time1),((x2,y2),time2),((x3,y3),time3),...]
```  
So the first element of the tuple is a tuple of the coordinates, and the second element of the tuple is the time which will be about a factor of 1/90.