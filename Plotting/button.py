'''
Author:   Matthew Donovan
Created:  7/8/14
File:     button.py
Purpose:  Provide a simple way to add buttons with ease to a program
'''	

import pygame, sys
from pygame.locals import *

# Takes the image paths and loads the images as variables so it can switch between the two on hover
# If it is a toggle button, it will switch to the next two images when clicked
class Button:
	def __init__(self, screen, toggle, picpath1, picpath2, picpath3, picpath4, actionStr, loc, size):
		if toggle:
			self.pic1 = pygame.image.load(picpath1).convert_alpha()
			self.pic2 = pygame.image.load(picpath2).convert_alpha()
		else:
			self.pic1 = None
			self.pic2 = None
		self.pic3 = pygame.image.load(picpath3).convert_alpha()
		self.pic4 = pygame.image.load(picpath4).convert_alpha()
		self.picDisp = self.pic3
		self.actionStr = actionStr
		self.loc = loc
		self.size = size
		self.toggle = toggle
		self.switch = False
	
	# Switches images when hovered over depending on which images it was previously when toggle button
	def mouseloc(self,x,y):
		if self.switch:
			if x in range(self.loc[0],self.loc[0]+self.size[0]) and y in range(self.loc[1],self.loc[1]+self.size[1]):
				self.picDisp = self.pic2
				return 1
			else:
				self.picDisp = self.pic1
				return 0
		else:
			if x in range(self.loc[0],self.loc[0]+self.size[0]) and y in range(self.loc[1],self.loc[1]+self.size[1]):
				self.picDisp = self.pic4
				return 1
			else:
				self.picDisp = self.pic3
				return 0

	def getpicDisp(self):
		return self.picDisp
	def getactionStr(self):
		return self.actionStr
	def getx(self):
		return self.loc[0]
	def gety(self):
		return self.loc[1]
	def toggle_button(self):
		if self.toggle:
			if self.switch:
				self.switch = False
			else:
				self.switch = True

