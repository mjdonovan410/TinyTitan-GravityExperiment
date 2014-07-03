import pygame
from functions import *
from button import *
from pygame.locals import *
import os, sys

os.environ['SDL_VIDEO_WINDOW_POS'] = str(75) + "," + str(30)
pygame.init()

# Screen and System Variables
screen_h = 720
screen_w = screen_h
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_w,screen_h))
font = pygame.font.SysFont("sanserif",36)
frame_range = [0,0]
curFrame = 0
pic_size = (480,640)
frames = []
mouseOnPic = False
crosshairs = [pygame.image.load("Images/crosshairs_w.png"),pygame.image.load("Images/crosshairs_h.png")]
keyFrames = []

# Buttons for rendering
buttons = []
midx = screen_w - 240; gap = 65; midy = 660; button_x = 50; button_y = 50
buttons.append(Button(screen,"Images/load.png","Images/load2.png","load",(10,20),(200,63)))
buttons.append(Button(screen,"Images/save.png","Images/save2.png","load",(10,100),(200,63)))
buttons.append(Button(screen,"Images/end.png","Images/end2.png","end",(midx+(2*gap),midy),(button_x,button_y)))
buttons.append(Button(screen,"Images/skipf.png","Images/skipf2.png","skipf",(midx+gap,midy),(button_x,button_y)))
buttons.append(Button(screen,"Images/stepf.png","Images/stepf2.png","stepf",(midx,midy),(button_x,button_y)))
buttons.append(Button(screen,"Images/stepb.png","Images/stepb2.png","stepb",(midx-gap,midy),(button_x,button_y)))
buttons.append(Button(screen,"Images/skipb.png","Images/skipb2.png","skipb",(midx-(2*gap),midy),(button_x,button_y)))
buttons.append(Button(screen,"Images/start.png","Images/start2.png","start",(midx-(3*gap),midy),(button_x,button_y)))

# Video Frame Setup
FPS = 90
screen.blit(pygame.image.load("Images/bg.png"),(0,0))
screen.blit(pygame.image.load("Images/pic_temp.png"),(screen_w-(pic_size[0]+10),10))

while True:
	prevFrame = curFrame
	x,y = pygame.mouse.get_pos()
	if x in range(screen_w-(pic_size[0]+10),screen_w-10) and y in range(10,10+pic_size[1]):
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
			elif event.key == K_f:
				if frame_range[0] < curFrame:
					frame_range[1] = curFrame
			elif event.key == K_c:
				frame_range = [0,len(frames)-1]
			elif event.key == 27:
				exitAndClean()
		elif event.type == MOUSEBUTTONDOWN:
			x,y = event.pos
			for i in buttons:
				if i.mouseloc(x,y):
					buttstr = i.getactionStr()
					temp = button_pressed(screen,curFrame,buttstr,frame_range)
					if buttstr == 'load':
						if temp != None:
							frames = temp
							frame_range[1] = len(frames)-1
							for p in range(len(frames)):
								keyFrames.append((1000,1000))
							label = font.render(str(curFrame),1,(255,255,255))
							screen.blit(frames[curFrame],(screen_w-(pic_size[0]+10),10))
							screen.blit(label,(screen_w-(pic_size[0]+5),15))
							curFrame = 0
					if buttstr in ['stepf','stepb','skipf','skipb','start','end']:
						curFrame = temp
				
	label = font.render(str(curFrame),1,(255,255,255))
	
	if prevFrame != curFrame and frames != []:
		screen.blit(frames[curFrame],(screen_w-(pic_size[0]+10),10))
		screen.blit(label,(screen_w-(pic_size[0]+5),15))
		
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))
	
	if mouseOnPic:
		if frames != []:
			screen.blit(frames[curFrame],(screen_w-(pic_size[0]+10),10))
			screen.blit(label,(screen_w-(pic_size[0]+5),15))
			screen.blit(crosshairs[1],(x,10))
			screen.blit(crosshairs[0],(screen_w-(pic_size[0]+10),y))
	
	pygame.display.update()
	clock.tick(FPS)

exitAndClean()
				