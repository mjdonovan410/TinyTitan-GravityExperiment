import pygame, sys
from pygame.locals import *

class Button:
	def __init__(self, screen, picpath1, picpath2, actionStr, loc, size):
		self.pic1 = pygame.image.load(picpath1).convert_alpha()
		self.pic2 = pygame.image.load(picpath2).convert_alpha()
		self.picDisp = self.pic1
		self.actionStr = actionStr
		self.loc = loc
		self.size = size

	def mouseloc(self,x,y):
		if x in range(self.loc[0],self.loc[0]+self.size[0]) and y in range(self.loc[1],self.loc[1]+self.size[1]):
			self.picDisp = self.pic2
			return 1
		else:
			self.picDisp = self.pic1
			return 0

	def getpicDisp(self):
		return self.picDisp
	def getactionStr(self):
		return self.actionStr
	def getx(self):
		return self.loc[0]
	def gety(self):
		return self.loc[1]

