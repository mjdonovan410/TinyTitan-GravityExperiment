import pygame, pickle
from functions import *
from button import *
from pygame.locals import *

pygame.init()

# Screen and System Variables
clock = pygame.time.Clock()
screen_size = (720,720)
screen = pygame.display.set_mode(screen_size)
frame_range = [0,0]
frame_size = (480,640)
frame_loc = (screen_size[0]-(frame_size[0]+10),10)
frames = []
logo = pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png")
bg = pygame.image.load("Images/bg.png")
pic_temp = pygame.image.load("Images/pic_temp.png")
crosshairs = [pygame.image.load("Images/crosshairs_w.png"),pygame.image.load("Images/crosshairs_h.png")]
dotR = pygame.image.load("Images/dotr.png").convert_alpha()
dotB = pygame.image.load("Images/dotb.png").convert_alpha()
font = pygame.font.SysFont("sanserif",36)
font2 = pygame.font.SysFont("sanserif",24)
curFrame = 0
timer = 0
keyFrames = []
button_str = ""
message_str = ""
message_rect = pygame.Rect((0,0), (200,150))
showPoints = False
mouseOnPic = False
message = False

# Buttons for rendering
buttons = []
buttons = load_buttons(buttons, screen, screen_size)

# Video Frame Setup
update_rate = 25
screen.blit(bg,(0,0))
screen.blit(logo,(0,0))
screen.blit(pic_temp,frame_loc)

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
								frame_range[1] = curFrame
							elif button_str == 'show':
								i.toggle_button()
								if showPoints:
									showPoints = False
								else:
									showPoints = True
								update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
							elif button_str == 'save':
								message_area, message, curFrame = save_file(keyFrames, frame_range, curFrame, font2)
									
							elif button_str == 'clear':
								keyFrames = clear_points(keyFrames)
								update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
								message_str = "Data Points Erased"
								message = True
								message_area = render_textrect(message_str, font2, message_rect, (255,0,0), (0,0,0), justification=1)
								
	
	frame_num = font.render(str(curFrame),1,(255,255,255))
	
	if prevFrame != curFrame and frames != []:
		update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
		if keyFrames[curFrame] != (1000,1000):
			temp = keyFrames[curFrame]
			screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	if button_str in ["set_end","set_start"] and frames != []:
		update_all(screen, screen_size, frames, frame_loc, frame_range, curFrame, font)
		message = True
		if button_str == "set_end":
			message_str = "End Point set at Frame "+str(curFrame)
		else:
			message_str = "Start Point set at Frame "+str(curFrame)
		message_area = render_textrect(message_str, font2, message_rect, (255,0,0), (0,0,0), justification=1)
		
	update_buttons(screen, buttons)
	
	if mouseOnPic:
		if frames != []:
			crosshair_loc = font.render("("+str((x-screen_size[0]+(frame_size[0]+10)))+","+str(y-10)+")",1,(255,255,255))
			update_pic(screen, screen_size, frames, frame_loc, curFrame, font)
			screen.blit(crosshairs[1],(x,10))
			screen.blit(crosshairs[0],(screen_size[0]-(frame_size[0]+10),y))
			screen.blit(crosshair_loc,(screen_size[0]-(frame_size[0]),screen_size[1]-100))
	
	if showPoints:
		show_all_points(screen, keyFrames, frame_range, frame_loc, curFrame, dotR, dotB)
	elif frames != [] and keyFrames[curFrame] != (1000,1000):
		temp = keyFrames[curFrame]
		screen.blit(dotR,(frame_loc[0]-5+temp[0],frame_loc[1]-5+temp[1]))
	
	if message:
		screen.blit(message_area,(15,600))
		message_str = ""
		message = False
		timer = 0
	else:
		if timer == 2*update_rate:
			surface = pygame.Surface((200,40)) 
			surface.fill((0,0,0))
			screen.blit(surface,(15,600))
	
	button_str = ""
	pygame.display.update()
	clock.tick(update_rate)
	timer += 1

exitAndClean()
				