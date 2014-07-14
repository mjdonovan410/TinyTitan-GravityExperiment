import pygame,sys
#import RPi.GPIO as GPIO
from time import sleep,strftime
from button import *
from pygame.locals import *
from mpi4py import MPI

comm = MPI.COMM_WORLD

rank = comm.rank
name = MPI.Get_processor_name()

if rank == 0:
	pygame.init()
	screen_size = (450,200)
	screen = pygame.display.set_mode(screen_size)
	button_str = ""

	buttons = []
	buttons.append(Button(screen,False,None,None,"Images/Record_pics/open.png","Images/Record_pics/open2.png","open",(10,50),(200,55)))
	buttons.append(Button(screen,False,None,None,"Images/Record_pics/close.png","Images/Record_pics/close2.png","close",(240,50),(200,55)))
	buttons.append(Button(screen,False,None,None,"Images/Record_pics/drop.png","Images/Record_pics/drop2.png","drop",(125,110),(200,55)))

	#GPIO.setmode(GPIO.BOARD)
	#GPIO.setup(7,GPIO.OUT)
	#p = GPIO.PWM(7,50)

	degree = []
	for i in range(19):
		x = round(i*10+60)
		degree.append(x)

	curDeg = 14
	dc = 20
	#p.start(degree[curDeg]/dc)
	#sleep(1)

	screen.blit(pygame.image.load("Images/Record_pics/header.png"),(0,0))

	while True:
		x,y = pygame.mouse.get_pos()
		for i in buttons:
			i.mouseloc(x,y)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					print "Dropping"
					curDeg = 14
					#p.ChangeDutyCycle(degree[curDeg]/dc)
				elif event.key == 27:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				x,y = event.pos
				for i in buttons:
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
						if button_str == 'close':
							print "Gripping"
							if curDeg > 1:
								curDeg -= 2
							#p.ChangeDutyCycle(degree[curDeg]/dc)
						elif button_str == 'open':
							print "Releasing"
							if curDeg < 17:
								curDeg += 2
							#p.ChangeDutyCycle(degree[curDeg]/dc)
						elif button_str == 'drop':
							print "Dropping"
							comm.send(data,dest=1)
							sleep(4)
							curDeg = 14
							#p.ChangeDutyCycle(degree[curDeg]/dc)				
				
		for i in buttons:
			screen.blit(i.getpicDisp(),(i.getx(),i.gety()))			
					
		pygame.display.update()	
		
	pygame.quit()

elif rank == 1:
	comm.recv(source=0)
	cmd = "raspivid -fps 90 -h 640 -w 480 -t 5000 -o vid_" + strftime("%X") + ".h264"
	os.system(cmd)
sys.exit()
#p.stop()
#GPIO.cleanup()
