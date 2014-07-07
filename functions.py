import pygame, os, sys, pickle
from pygame.locals import *
from button import *
from Tkinter import Tk
from tkFileDialog import askopenfilename

global FPS
FPS = 90

def left_key(curFrame,frame_range):
	if curFrame > frame_range[0]:
		curFrame -= 1
	return curFrame

def right_key(curFrame,frame_range):
	if curFrame < frame_range[1]:
		curFrame += 1
	return curFrame
	
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
			label = font.render("LOADING",1,(255,0,0))
			screen.blit(label,(350,300))
			pygame.display.update()
			os.system("mkdir ffmpeg_temp")
			frames = change_vid(infile, screen)
			screen.blit(pygame.image.load("Images/bg.png"),(0,0))
			screen.blit(pygame.image.load("Images/pic_temp.png"),(720-(480+10),10))
			return frames	
	elif str == "start":
		return frame_range[0]
	elif str == "end":
		return frame_range[1]
		
		
def change_vid(infile, screen):
	os.system("ffmpeg -i "+infile+" -r 25 -f image2 ffmpeg_temp/%05d.jpg")
	path, dirs, files = os.walk("./ffmpeg_temp/").next()
	frames = []
	length = len(files)
	bar = pygame.image.load("Images/loading.png")
	c = 1; v = 0
	files.sort()
	for i in files:
		frames.append(pygame.image.load("./ffmpeg_temp/"+i))
		if (v*100/length) > c:
			screen.blit(bar,(310+c*3,350))
			pygame.display.update()
			c += 1
		v += 1
	return frames
	
def exitAndClean():
	pygame.quit()
	sys.exit()
	
def cleanDir():
	os.system("rm ./ffmpeg_temp/*.jpg")
	os.system("rmdir ./ffmpeg_temp")
	
def load_buttons(buttons, screen, screen_size):
	midx = screen_size[0] - 240; gap = 65; midy = 660; button_x = 50; button_y = 50
	buttons.append(Button(screen,False,None,None,"Images/load.png","Images/load2.png","load",(15,20),(200,63)))
	buttons.append(Button(screen,False,None,None,"Images/start_frame.png","Images/start_frame2.png","set_start",(10,90),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/finish_frame.png","Images/finish_frame2.png","set_end",(120,90),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/end.png","Images/end2.png","end",(midx+(2*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/skipf.png","Images/skipf2.png","skipf",(midx+gap,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/stepf.png","Images/stepf2.png","stepf",(midx,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/stepb.png","Images/stepb2.png","stepb",(midx-gap,midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/skipb.png","Images/skipb2.png","skipb",(midx-(2*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/start.png","Images/start2.png","start",(midx-(3*gap),midy),(button_x,button_y)))
	buttons.append(Button(screen,False,None,None,"Images/save.png","Images/save2.png","save",(15,650),(200,63)))
	buttons.append(Button(screen,True,"Images/hide.png","Images/hide2.png","Images/show.png","Images/show2.png","show",(10,160),(100,38)))
	buttons.append(Button(screen,False,None,None,"Images/clear.png","Images/clear2.png","clear",(120,160),(100,38)))
	return buttons
	
def update_all(screen, screen_size, frames, frame_loc, frame_range, curFrame, font):
	frame_num = font.render(str(curFrame),1,(255,255,255))
	start_frame = font.render(str(frame_range[0]),1,(255,255,255))
	end_frame = font.render(str(frame_range[1]),1,(255,255,255))
	screen.blit(pygame.image.load("Images/bg.png"),(0,0))
	screen.blit(start_frame,(50,130))
	screen.blit(end_frame,(155,130))
	update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
	
def update_buttons(screen, buttons):
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))

def update_pic(screen, screen_size, frames, frame_loc, curFrame, font):
	frame_num = font.render(str(curFrame),1,(255,255,255))
	screen.blit(frames[curFrame],frame_loc)
	screen.blit(frame_num,(frame_loc[0]+5,frame_loc[1]+5))
	
def show_all_points(screen, keyFrames, frame_range, frame_loc, curFrame, dotR, dotB):
	for i in range(frame_range[0], frame_range[1]):
		p = keyFrames[i]
		if p != (1000,1000):
			temp = p
			if i == curFrame:
				screen.blit(dotB,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
			else:
				screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
def clear_points(keyFrames):
	length = len(keyFrames)
	keyFrames = []
	for i in range(length):
		keyFrames.append((1000,1000))
	return keyFrames
	
	
	
	
	
	
	
	
	
	
	