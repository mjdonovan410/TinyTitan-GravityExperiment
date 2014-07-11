import pygame,sys
#import RPi.GPIO as GPIO
from time import sleep
from pygame.locals import *
from subprocess import Popen

pygame.init()
screen = pygame.display.set_mode((200,200))
record = "raspivid -t 5000 -h 640 -w 480 -fps 90 -o "

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7,GPIO.OUT)
#p = GPIO.PWM(7,50)

degree = []
for i in range(19):
	x = round(float(i)/10+.6,1)
	degree.append(x)

curDeg = 14
dc = 20
#p.start(degree[curDeg]/dc)
sleep(1)
try:
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_g:
					print "Gripping"
					if curDeg > 1:
						curDeg -= 2
					sleep(1)
					#p.ChangeDutyCycle(degree[curDeg]/dc)
				elif event.key == K_r:
					print "Releasing"
					if curDeg < 17:
						curDeg += 2
					sleep(1)
					#p.ChangeDutyCycle(degree[curDeg]/dc)
				elif event.key == K_d:
					print "Dropping"
					
					#p.ChangeDutyCycle(14/dc)
				elif event.key == 27:
					pygame.quit()
					sys.exit()
	pygame.display.update()
except KeyboardInterrupt:		
	pygame.quit()
	sys.exit()
	#p.stop()
	#GPIO.cleanup()
#p.stop()
#GPIO.cleanup()
