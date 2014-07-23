'''
Author:   Matthew Donovan
Created:  7/8/14
File:     functions.py
Purpose:  Provide functions for exp.py in a way to keep the driver file less cluttered
'''	

import pygame, os, sys, pickle
from pygame.locals import *
sys.path.insert(0, '../lib/')
from button import *
from textrect import render_textrect
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename

global FPS
FPS = 90

# Steps a frame back
def left_key(curFrame,frame_range):
	if curFrame > frame_range[0]:
		curFrame -= 1
	return curFrame

# Steps a frame forwards
def right_key(curFrame,frame_range):
	if curFrame < frame_range[1]:
		curFrame += 1
	return curFrame

# Manager for when a button is pressed and does the appropriate function
def button_pressed(screen,curFrame,str,frame_range):
	if str == "stepf":
		return right_key(curFrame,frame_range)
	elif str == "stepb":
		return left_key(curFrame,frame_range)
	elif str == "skipf":
		if curFrame+(FPS/4) >= frame_range[1]:
			return frame_range[1]
		else:
			return curFrame+(FPS/4)
	elif str == "skipb":
		if curFrame-(FPS/4) <= frame_range[0]:
			return frame_range[0]
		else:
			return curFrame-(FPS/4)
	elif str == "load":
		Tk().withdraw()
		infile = askopenfilename(filetypes=[("H264 Video","*.h264")])
		
		if infile != '':
			cleanDir()
			font = pygame.font.SysFont("sanserif",72)
			font2 = pygame.font.SysFont("sanserif",24)
			screen.blit(pygame.image.load("Images/pic_temp.png"),(720-(480+10),10))
			label = font.render("CONVERTING",1,(255,255,255))
			label2 = font2.render("THIS WILL TAKE A MINUTE",1,(255,0,0))
			screen.blit(label,(310,300))
			screen.blit(label2,(370,355))
			pygame.display.update()
			os.system("mkdir pic_temp")
			frames = change_vid(infile, screen, font)
			screen.blit(pygame.image.load("Images/bg.png"),(0,0))
			screen.blit(pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png"),(0,0))
			screen.blit(pygame.image.load("Images/pic_temp.png"),(720-(480+10),10))
			return frames	
	elif str == "start":
		return frame_range[0]
	elif str == "end":
		return frame_range[1]
		
# Switches out for the new video once the user selects to load another	
def change_vid(infile, screen, font):
	#os.system("ffmpeg -i "+infile+" -ss 00:00:04.8 -t 00:00:03.6 -r 25 -f image2 pic_temp/%05d.jpg")
	# The program thinks the video is at 25 FPS so 1 second at 90 FPS is 3.6 seconds at 25 FPS
	os.system("avconv -i "+infile+" -ss 00:00:04.8 -t 00:00:03.6 -r 25 -f image2 pic_temp/%05d.jpg")
	path, dirs, files = os.walk("./pic_temp/").next()
	frames = []
	length = len(files)
	label = font.render("LOADING",1,(255,255,255))
	screen.blit(pygame.image.load("Images/pic_temp.png"),(720-(480+10),10))
	screen.blit(label,(365,300))
	bar = pygame.image.load("Images/loading.png")
	c = 0; v = 0
	files.sort()
	for i in files:
		frames.append(pygame.image.load("./pic_temp/"+i))
		while (v*100/length) > c:
			screen.blit(bar,(325+c*3,355))
			pygame.display.update()
			c += 1
		v += 1
	return frames

# Deletes the temp files placed in the directory and closes the program
def exitAndClean():
	cleanDir()
	pygame.quit()
	sys.exit()

# Deletes the temp files placed in the directory by the program
def cleanDir():
	os.system("rm -rf ./pic_temp")

# Loads the buttons into an array for easy access and processing	
def load_buttons(buttons, screen, screen_size):
	midx = screen_size[0] - 240; gap = 65; midy = 660; button_x = 50; button_y = 50; vertical = 150
	buttons.append(Button(screen,False,None,None,"Images/load.png","Images/load2.png","load",(15,vertical+10),(200,63)))
	buttons.append(Button(screen,False,None,None,"Images/start_frame.png","Images/start_frame2.png","set_start",(10,vertical+75),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/finish_frame.png","Images/finish_frame2.png","set_end",(120,vertical+75),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/reset.png","Images/reset2.png","reset",(15,vertical+145),(200,34)))
	buttons.append(Button(screen,True,"Images/hide.png","Images/hide2.png","Images/show.png","Images/show2.png","show",(10,vertical+185),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/clear.png","Images/clear2.png","clear",(120,vertical+185),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/end.png","Images/end2.png","end",(midx+(2*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/skipf.png","Images/skipf2.png","skipf",(midx+gap,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/stepf.png","Images/stepf2.png","stepf",(midx,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/stepb.png","Images/stepb2.png","stepb",(midx-gap,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/skipb.png","Images/skipb2.png","skipb",(midx-(2*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/start.png","Images/start2.png","start",(midx-(3*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/save.png","Images/save2.png","save",(15,650),(200,63)))
	
	return buttons

# Updates everything on the screen (except buttons)	
def update_all(screen, screen_size, frames, frame_loc, numberBox, curFrame, font):
	frame_num = font.render(str(curFrame),1,(255,255,255))
	screen.blit(pygame.image.load("Images/bg.png"),(0,0))
	screen.blit(pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png"),(0,0))
	screen.blit(numberBox[0],(10,265))
	screen.blit(numberBox[1],(120,265))
	update_pic(screen, screen_size, frames, frame_loc, curFrame, font)

# Updates the buttons if they are being hovered over with the mouse	
def update_buttons(screen, buttons):
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))

# Updates the video image and the frame number in the corner
def update_pic(screen, screen_size, frames, frame_loc, curFrame, font):
	frame_num = font.render(str(curFrame),1,(255,255,255))
	screen.blit(frames[curFrame],frame_loc)
	screen.blit(frame_num,(frame_loc[0]+5,frame_loc[1]+5))

# Plots all the points in the program
def show_all_points(screen, keyFrames, frame_range, frame_loc, curFrame, dotR, dotB):
	for i in range(frame_range[0], frame_range[1]+1):
		p = keyFrames[i]
		if p != (1000,1000):
			temp = p
			if i == curFrame:
				screen.blit(dotB,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
			else:
				screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))

# Deletes all the point by replacing them with (1000,1000) which can't happen on a 480x640 image
def clear_points(keyFrames):
	length = len(keyFrames)
	keyFrames = []
	for i in range(length):
		keyFrames.append((1000,1000))
	return keyFrames

# Saves a file assuming that all points in the range have been selected
def save_file(keyFrames, frame_range, curFrame, font):
	Tk().withdraw()
	savefile = asksaveasfilename(filetypes=[("Python Pickle","*.p")])
	message = False
	message_str = ""
	message_rect = pygame.Rect((0,0), (200,150))
	temp = []
	if savefile != "":
		for i in range(frame_range[0], frame_range[1]+1):
			p = keyFrames[i]
			if p != (1000,1000):
				temp.append((p,(float(i)-frame_range[0])*1/float(FPS)))
				#print temp
			else:
				message_str = "Frame "+str(i)+" missing data point"
				message = True
				curFrame = i
				break
		if not message:
			savefile = check_filename(savefile)
			pickle.dump(temp,open(savefile, "wb"))
			message = True
			message_str = ".p File Saved"
	
	message_area = render_textrect(message_str, font, message_rect, (255,0,0), (0,0,0), justification=1)
	return message_area, message, curFrame

# Checks to see if the user added the .p file extension. If not, this will add it to the end
def check_filename(filename):
	temp = filename.split(".")
	if temp[len(temp)-1] == 'p':
		return filename
	else:
		return filename+".p"
	
	
	
	
	
