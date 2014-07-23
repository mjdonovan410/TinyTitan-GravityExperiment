import pygame,sys,os,commands
sys.path.insert(0, '../lib/')
import RPi.GPIO as GPIO
from time import sleep,strftime
from button import *
from pygame.locals import *
from mpi4py import MPI

comm = MPI.COMM_WORLD

name = MPI.Get_processor_name()
rank = comm.rank
size = comm.size

#print rank,name,size

if rank == 0:
	pygame.init()
	clock = pygame.time.Clock()
	update_rate = 20
	screen_size = (450,200)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Experiment Recorder")
	button_str = ""

	buttons = []
	buttons.append(Button(screen,False,None,None,"Images/open.png","Images/open2.png","open",(10,50),(200,55)))
	buttons.append(Button(screen,False,None,None,"Images/close.png","Images/close2.png","close",(240,50),(200,55)))
	buttons.append(Button(screen,False,None,None,"Images/drop.png","Images/drop2.png","drop",(125,110),(200,55)))

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)
	p = GPIO.PWM(7,50)

	d0 = .6*100
	d150 = 2.2*100
	
	dc = 20
	p.start(d150/dc)
	sleep(1)

	screen.blit(pygame.image.load("Images/header.png"),(0,0))

	while True:
		x,y = pygame.mouse.get_pos()
		for i in buttons:
			i.mouseloc(x,y)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					button_str = 'drop'
				elif event.key == 27:
					pygame.quit()
					sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x,y = event.pos
				for i in buttons:
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
						if button_str == 'close':
							#print "Gripping"
							p.ChangeDutyCycle(d0/dc)
							sleep(1)
						elif button_str == 'open':
							#print "Releasing"
							p.ChangeDutyCycle(d150/dc)
							sleep(1)
		
		if button_str == 'drop':
			#print "Dropping"
			comm.send(button_str,dest=1)
			sleep(2)
			p.ChangeDutyCycle(d150/dc)
			sleep(1)
			break

		for i in buttons:
			screen.blit(i.getpicDisp(),(i.getx(),i.gety()))			
					
		pygame.display.update()
		button_str = ""
		clock.tick(update_rate)	
	
	p.stop()	
	pygame.quit()
	GPIO.cleanup()	

elif rank == 1:
	cmdReturn = commands.getoutput("df -h")
	temp = cmdReturn.split("\n")
	flashName = ""
	temp2 = []
	
	for i in temp:
		if "/media/" in i:
			temp3 = i.split("/media/")
			temp2.append(temp3[1])
	for i in temp2:
		if i != "SETTINGS":
			flashName = i

	if flashName == "":
		print "ERROR: NO FLASH DRIVE INSTALLED ON CAMERA PI"
	else:
		input = comm.recv(source=0)
		if input == "drop":
			cmd = "raspivid -fps 90 -h 640 -w 480 -t 3000 -o /media/"+flashName+"/vid.h264"
			os.system(cmd)

sys.exit()
