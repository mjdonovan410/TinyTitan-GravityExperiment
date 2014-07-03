import pygame, os, sys, pickle
from functions import *
from button import *
from pygame.locals import *

os.environ['SDL_VIDEO_WINDOW_POS'] = str(75) + "," + str(30)
pygame.init()

# Screen and System Variables
clock = pygame.time.Clock()
screen_size = (720,720)
screen = pygame.display.set_mode(screen_size)
frame_range = [0,0]
frame_size = (480,640)
frame_loc = (screen_size[0]-(frame_size[0]+10),10)
frames = []
crosshairs = [pygame.image.load("Images/crosshairs_w.png"),pygame.image.load("Images/crosshairs_h.png")]
dot = pygame.image.load("Images/dotr.png").convert_alpha()
dot2 = pygame.image.load("Images/dotb.png").convert_alpha()
font = pygame.font.SysFont("sanserif",36)
curFrame = 0
keyFrames = []
button_str = ""
message_str = ""
showPoints = False
mouseOnPic = False
message = False

# Buttons for rendering
buttons = []
buttons = load_buttons(buttons, screen, screen_size)

# Video Frame Setup
FPS = 90
screen.blit(pygame.image.load("Images/bg.png"),(0,0))
screen.blit(pygame.image.load("Images/pic_temp.png"),frame_loc)

while True:
	prevFrame = curFrame
	x,y = pygame.mouse.get_pos()
	if x in range(frame_loc[0],frame_loc[0]+frame_size[0]) and y in range(frame_loc[1],frame_loc[1]+frame_size[1]):
		mouseOnPic = True
	else:
		mouseOnPic = False
		
	for i in buttons:
		i.mouseloc(x,y)
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exitAndClean()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				curFrame = left_key(curFrame,frame_range)
			elif event.key == K_RIGHT:
				curFrame = right_key(curFrame,frame_range)
			elif event.key == K_s:
				frame_range[0] = curFrame
				button_str = "set_start"
			elif event.key == K_f:
				if frame_range[0] < curFrame:
					frame_range[1] = curFrame
					button_str = "set_end"
			elif event.key == K_c:
				frame_range = [0,len(frames)-1]
			elif event.key == 27:
				exitAndClean()
		elif event.type == MOUSEBUTTONDOWN:
			x,y = event.pos
			if mouseOnPic and frames != []:
				keyFrames[curFrame] = (x-screen_size[0]+(frame_size[0]+10),y-10)
			else:
				for i in buttons:
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
						temp = button_pressed(screen,curFrame,button_str,frame_range)
						if button_str == 'load':
							if temp != None:
								frames = temp
								frame_range[1] = len(frames)-1
								for p in range(len(frames)):
									keyFrames.append((1000,1000))
								update_all(screen, screen_size, frames, frame_loc, frame_range, curFrame, font)
								curFrame = 0
						if frames != []:
							if button_str in ['stepf','stepb','skipf','skipb','start','end']:
								curFrame = temp
							elif button_str == 'set_start':
								frame_range[0] = curFrame
							elif button_str == 'set_end':
								if frame_range[0] < curFrame:
									frame_range[1] = curFrame
							elif button_str == 'show':
								i.toggle_button()
								if showPoints:
									showPoints = False
								else:
									showPoints = True
							elif button_str == 'save':
								temp = []
								for i in range(frame_range[0], frame_range[1]):
									p = keyFrames[i]
									if p != (1000,1000):
										temp.append((p,i*1/90))
									else:
										message_str = "Frame "+str(i)+" missing data point"
										message = True
										curFrame = i
										break
								if not message:
									pickle.dump(temp,open("save.p", "wb"))
									message = True
									filename = "file.p"
									message_str = "File "+filename+" successfully saved"
									
							elif button_str == 'clear':
								for p in keyFrames:
									p = (1000,1000)
	
	frame_num = font.render(str(curFrame),1,(255,255,255))
	
	if prevFrame != curFrame and frames != []:
		update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
		if keyFrames[curFrame] != (1000,1000):
			temp = keyFrames[curFrame]
			screen.blit(dot,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	if button_str in ["set_end","set_start"] and frames != []:
		update_all(screen, screen_size, frames, frame_loc, frame_range, curFrame, font)
		
	update_buttons(screen, buttons)

	if mouseOnPic:
		if frames != []:
			update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
			screen.blit(crosshairs[1],(x,10))
			screen.blit(crosshairs[0],(screen_size[0]-(frame_size[0]+10),y))
	
	if showPoints:
		show_all_points(screen, keyFrames, frame_range, frame_loc, curFrame, dot, dot2)
	elif frames != [] and keyFrames[curFrame] != (1000,1000):
		temp = keyFrames[curFrame]
		screen.blit(dot,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	if message:
		message_convert = font.render(message_str,1,(255,0,0))
		screen.blit(message_convert,(frame_loc[0]+75,300))
		message_str = ""
		message = False
	
	pygame.display.update()
	clock.tick(FPS)

exitAndClean()
				