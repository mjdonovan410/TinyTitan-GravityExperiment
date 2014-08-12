#-------------------------------------------------------------------------------
# Author: 	Matt Donovan
# Provider:	Oak Ridge National Lab 
# Date: 	8/7/14
# File:		record.py
# Purpose:	Creates a simplistic GUI for the recording of a ball dropping.
#-------------------------------------------------------------------------------

import pygame,sys,os,commands
sys.path.insert(0, '../lib/')
from time import sleep,strftime
from button import *
from pygame.locals import *
from mpi4py import MPI

# References the MPI link between the two Pis
comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
#name = MPI.Get_processor_name()

# If it is the first Pi on the list in nodes.txt, it will control the servo and GUI. If it is the second, it will wait until the the first Pi tells it to record.
if rank == 0:
	# Start driver for ServoBlaster and preps pygame window
	os.system('sudo /home/pi/PiBits/ServoBlaster/user/servod')
	pygame.init()
	clock = pygame.time.Clock()
	update_rate = 20
	screen_size = (450,200)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Experiment Recorder")
	screen.blit(pygame.image.load("Images/header.png"),(0,0))
	button_str = ""
	
	# Creates a list of buttons to make things easier and more organized later
	buttons = []
	buttons.append(ImgButton(screen,False,None,None,"Images/open.png","Images/open2.png","open",(10,50),(200,55)))
	buttons.append(ImgButton(screen,False,None,None,"Images/close.png","Images/close2.png","close",(240,50),(200,55)))
	buttons.append(ImgButton(screen,False,None,None,"Images/drop.png","Images/drop2.png","drop",(125,110),(200,55)))
	
	# Sets a starting position for the claw to be open
	os.system('echo 0=240 > /dev/servoblaster')

	while True:
		# Checks if the mouse is hovering over any buttons. If it is, the button will switch images, otherwise it will switch back to its original state
		x,y = pygame.mouse.get_pos()
		for i in buttons:
			i.mouseloc(x,y)
		
		for event in pygame.event.get():
			# Quits if the 'X' in the corner has been pressed
			if event.type == QUIT:
				if size < 1:
					comm.send("quit",dest=1)
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE: 
					button_str = 'drop'
				elif event.key == K_LEFT: # Opens the Claw
					os.system('echo 0=240 > /dev/servoblaster')
					sleep(0.1)
				elif event.key == K_RIGHT: # Closes the Claw
					os.system('echo 0=50 > /dev/servoblaster')
					sleep(0.1)
				elif event.key == 27: # Quits if ESC is pressed
					if size > 1:
						comm.send("quit",dest=1)
					pygame.quit()
					sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x,y = event.pos
				for i in buttons: # Checks if a button has been pressed
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
						if button_str == 'close': # Closes the Claw
							os.system('echo 0=50 > /dev/servoblaster')
						elif button_str == 'open': # Opens the Claw
							os.system('echo 0=240 > /dev/servoblaster')
		
		# This sends a command to the camera to start recording for 3 secs then the claw will open.
		# This helps the camera warm up so it can record 90 FPS.
		if button_str == 'drop':
			if size > 1:
				comm.send(button_str,dest=1)
			sleep(3)
			os.system('echo 0=240 > /dev/servoblaster')
			sleep(1)
			break

		# Loads the buttons to the screen
		for i in buttons:
			screen.blit(i.getpicDisp(),i.getLoc())			
					
		pygame.display.update()
		button_str = ""
		clock.tick(update_rate)	
		
	pygame.quit()
	os.system('sudo killall servod') # Turns off the ServoBlaster driver
else:
	flashName = ""
	
	# Checks the media folder to see if a flash drive is plugged in
	cmdReturn = commands.getoutput("ls /media")
	devices = cmdReturn.split("\n")
	
	# If there is a media device that isn't the default "SETTINGS" that is already in the folder, it assumes it is a flash drive
	for i in devices:
		if i != 'SETTINGS':
			flashName = i
	
	# If no media device was found, it will prompt this error, otherwise it will record normally. It names the file vid[Date]_[Time].h264
	if flashName == "":
		print "ERROR: NO FLASH DRIVE INSTALLED ON CAMERA PI"
		input = comm.recv(source=0)
		print "ERROR: NO VIDEO FILE HAS BEEN CREATED"
	else:
		input = comm.recv(source=0)		
		if input == "drop":
			fileName = "vid"+strftime("%m-%d_%H%M%S")+".h264"
			cmd = "raspivid -fps 90 -h 640 -w 480 -t 4000 -o /media/"+flashName+"/"+fileName
			os.system(cmd)

sys.exit()