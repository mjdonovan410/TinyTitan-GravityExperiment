'''
Author:   Matthew Donovan
Created:  7/8/14
File:     exp.py
Purpose:  Provides a service to load a video created by the raspberry pi, and convert the visuals into data points to be used
in other programs.
'''	

import pygame, pickle
from functions import *
from button import *
from textrect import render_textrect
from pygame.locals import *

pygame.init()

# Screen and Basic Program Variables
clock = pygame.time.Clock()
screen_size = (720,720)
screen = pygame.display.set_mode(screen_size)
frame_range = [0,0]
frame_size = (480,640)
frame_loc = (screen_size[0]-(frame_size[0]+10),10)
frames = []
keyFrames = []
logo = pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png")
bg = pygame.image.load("Images/bg.png")
pic_temp = pygame.image.load("Images/pic_temp.png")
crosshairs = [pygame.image.load("Images/crosshairs_w.png"),pygame.image.load("Images/crosshairs_h.png")]
dotR = pygame.image.load("Images/dotr.png").convert_alpha()
dotB = pygame.image.load("Images/dotb.png").convert_alpha()
fontB = pygame.font.SysFont("sanserif",36)
fontL = pygame.font.SysFont("sanserif",24)
numberBox = [None,None]
number_rect = pygame.Rect((0,0), (100,40))
curFrame = 0
timer = 0
button_str = ""
message_str = ""
message_rect = pygame.Rect((0,0), (200,50))
showPoints = False
mouseOnPic = False
message = False

# Creates an array of Button objects the will provide data and blit the objects to the screen
buttons = []
buttons = load_buttons(buttons, screen, screen_size)

# Basic GUI Frame Setup
update_rate = 40
screen.blit(bg,(0,0))
screen.blit(logo,(0,0))
screen.blit(pic_temp,frame_loc)

while True:
	prevFrame = curFrame
	x,y = pygame.mouse.get_pos()
	
	#Checks if the mouse is hovering over the image so the crosshairs can be added and reduce updating frequency
	if x in range(frame_loc[0],frame_loc[0]+frame_size[0]) and y in range(frame_loc[1],frame_loc[1]+frame_size[1]):
		mouseOnPic = True
	else:
		mouseOnPic = False
		for i in buttons: # Checks if mouse is hovering over a button and changes the image accordingly
			i.mouseloc(x,y)
	
	# Checks for inputs whether it be a mouse click, key pressed, or the 'X' has been pressed in the corner
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exitAndClean()
		
		# Keyboard shortcuts for the action buttons
		elif event.type == KEYDOWN:
			if event.key == K_LEFT or event.key == K_a:
				curFrame = left_key(curFrame,frame_range)
			elif event.key == K_RIGHT or event.key == K_d:
				curFrame = right_key(curFrame,frame_range)
			elif event.key == K_s:
				frame_range[0] = curFrame
				button_str = "set_start"
			elif event.key == K_f:
				frame_range[1] = curFrame
				button_str = "set_end"
			elif event.key == K_c:
				frame_range = [0,len(frames)-1]
				button_str = "reset"
			elif event.key == 27:
				exitAndClean()
			elif event.key == K_q:
				curFrame = button_pressed(screen,curFrame,"skipb",frame_range)
			elif event.key == K_e:
				curFrame = button_pressed(screen,curFrame,"skipf",frame_range)
				
		# Used for both buttons being pressed or location of a data point
		elif event.type == MOUSEBUTTONDOWN:
			x,y = event.pos
			if mouseOnPic and frames != []:
				keyFrames[curFrame] = (x-screen_size[0]+(frame_size[0]+10),y-10)
			else:
				#Checks if a button has been pressed
				for i in buttons:
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
						temp = button_pressed(screen,curFrame,button_str,frame_range)
						
						# Loads a new video to the screen and clears the keyFrames from the previous video
						if button_str == 'load':
							if temp is not None:
								frames = temp
								frame_range = [0,len(frames)-1]
								keyFrames = []
								numberBox[0] = render_textrect(str(frame_range[0]), fontB, number_rect, (255,255,255), (0,0,0), justification=1)
								numberBox[1] = render_textrect(str(frame_range[1]), fontB, number_rect, (255,255,255), (0,0,0), justification=1)
								for p in range(len(frames)):
									keyFrames.append((1000,1000))
								update_all(screen, screen_size, frames, frame_loc, numberBox, curFrame, fontB)
								curFrame = 0
						
						# These functions only work when there are frames loaded
						if frames != []:
							if button_str in ['stepf','stepb','skipf','skipb','start','end']:
								curFrame = temp
							elif button_str == 'set_start':
								frame_range[0] = curFrame
							elif button_str == 'set_end':
								frame_range[1] = curFrame
							elif button_str == 'show':
								i.toggle_button()
								if showPoints:
									showPoints = False
								else:
									showPoints = True
								update_pic(screen, screen_size, frames, frame_loc, curFrame, fontB)
							
							# Saves a file to be used in another program for processing
							elif button_str == 'save':
								message_area, message, curFrame = save_file(keyFrames, frame_range, curFrame, fontL)
							
							# Clears all the data points from the frames
							elif button_str == 'clear':
								keyFrames = clear_points(keyFrames)
								update_pic(screen, screen_size, frames, frame_loc, curFrame, fontB)
								message_str = "Data Points Erased"
								message = True
								message_area = render_textrect(message_str, fontL, message_rect, (255,0,0), (0,0,0), justification=1)
							
							elif button_str == 'reset':
								frame_range = [0,len(frames)-1]								
	
	frame_num = fontB.render(str(curFrame),1,(255,255,255))
	
	# Updates the video frames on the right with the appropriate layering
	if prevFrame != curFrame and frames != []:
		update_pic(screen, screen_size, frames, frame_loc, curFrame, fontB)
		if keyFrames[curFrame] != (1000,1000):
			temp = keyFrames[curFrame]
			screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	# Updates the whole screen with the new start and end points
	if button_str in ["set_end","set_start","reset"] and frames != []:
		numberBox[0] = render_textrect(str(frame_range[0]), fontB, number_rect, (255,255,255), (0,0,0), justification=1)
		numberBox[1] = render_textrect(str(frame_range[1]), fontB, number_rect, (255,255,255), (0,0,0), justification=1)
		screen.blit(numberBox[0],(10,265))
		screen.blit(numberBox[1],(120,265))
		message = True
		if button_str == "set_end":
			message_str = "End Point set at Frame "+str(curFrame)
		elif button_str == "set_start":
			message_str = "Start Point set at Frame "+str(curFrame)
		else:
			message_str = "Start and End Points Reset"
		message_area = render_textrect(message_str, fontL, message_rect, (255,0,0), (0,0,0), justification=1)
	
	# Updates the button images if they are being hovered
	#update_buttons(screen, buttons)
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))
	
	# Adds crosshairs if the mouse is on the frame and there are frames
	if mouseOnPic and frames != []:
		crosshair_loc = fontB.render("("+str((x-screen_size[0]+(frame_size[0]+10)))+","+str(y-10)+")",1,(255,255,255))
		update_pic(screen, screen_size, frames, frame_loc, curFrame, fontB)
		screen.blit(crosshairs[1],(x,10))
		screen.blit(crosshairs[0],(screen_size[0]-(frame_size[0]+10),y))
		screen.blit(crosshair_loc,(screen_size[0]-(frame_size[0]),screen_size[1]-100))
	
	# Adds all the points to the screen
	if showPoints:
		show_all_points(screen, keyFrames, frame_range, frame_loc, curFrame, dotR, dotB)
	elif frames != [] and keyFrames[curFrame] != (1000,1000):
		temp = keyFrames[curFrame]
		screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	# Displays a message if there is one and then clears it after 2 seconds
	if message:
		screen.blit(message_area,(15,590))
		message_str = ""
		message = False
		timer = 0
	else:
		if timer == 2*update_rate:
			surface = pygame.Surface((200,40)) 
			surface.fill((0,0,0))
			screen.blit(surface,(15,590))
	
	button_str = ""
	pygame.display.update()
	clock.tick(update_rate)
	timer += 1

exitAndClean()
				
