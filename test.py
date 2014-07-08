import os
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename

Tk().withdraw()
infile = askopenfilename(filetypes=[("H264 Video","*.h264")])
os.system("avconv -i "+infile+" -r 25 -f image2 pic_temp/%05d.jpg")
os.system("rm -rf ./pic_temp")