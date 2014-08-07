#----------------------------------------------------------------------------------
# Author: 	Matt Donovan
# Provider:	Oak Ridge National Lab
# Date: 	8/7/14
# File:		plotting.py
# Purpose:	Creates a user friendly GUI to plot data recorded from coordinates
#			from the ball dropping. This program uses matplotlib and its
#			dependencies, pygame, mpi4py, standard libraries, and some homebrewed
#			files located in lib.
#----------------------------------------------------------------------------------

import pickle,pygame,sys,time,matplotlib,pylab
sys.path.insert(0, '../lib/')
from button import *
from plot_Functions import *
from textrect import render_textrect
from pygame.locals import *
from Tkinter import Tk
from tkFileDialog import askopenfilename
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as pyplot
from mpi4py import MPI

# References the MPI connection between the Pis
comm = MPI.COMM_WORLD
rank = comm.rank
#name = MPI.Get_processor_name()
#size = comm.size

HEIGHT_IN_METERS = 6*0.3048 # 6ft conversion to meters

# Instantiates variables required by all processors running the program 
timing = []
xCoord = []
yCoord = []
pxPerM = 1000
yFit = []
fitResults = [None,None,None]
figure = None
axis = None
g = 0
Cd = 0
vi = 0

# If it is the head node in nodes.txt, it will run the GUI and plotting
if rank == 0:
	# Setup pygame window and prep variables required for window
	pygame.init()
	clock = pygame.time.Clock()
	screen_size = (700,480)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Experiment Plotting")
	plot_size = (450,450)
	plot_loc = (235,15)
	logo = pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png")
	plotTemp = pygame.image.load("Images/plot_temp.png")
	font = pygame.font.SysFont("sanserif",30)
	button_str = ""
	data_rect = pygame.Rect((0,0), (200,30))

	# Creates a list of buttons to keep organized and makes things easier to reference later
	buttons = []
	buttons.append(ImgButton(screen,False,None,None,"Images/load.png","Images/load2.png","load",(15,140),(200,49)))
	buttons.append(ImgButton(screen,False,None,None,"Images/fit.png","Images/fit2.png","fit",(15,365),(200,49)))
	buttons.append(ImgButton(screen,False,None,None,"Images/advanced.png","Images/advanced2.png","afit",(15,420),(200,49)))

	# Basic GUI Frame Setup
	update_rate = 20
	screen.blit(logo,(0,0))
	screen.blit(plotTemp,plot_loc)

	while True:
		# Checks if a button is currently being hovered over with the mouse. If it is, the button will switch images
		x,y = pygame.mouse.get_pos()
		for i in buttons: 
			i.mouseloc(x,y)
				
		for event in pygame.event.get():
			# If the "X" in the corner is hit, it will stop the program on all Pis
			if event.type == pygame.QUIT:
				comm.bcast(['quit',None,None],root=0)
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == 27: # If ESC is hit, it will stop the program on all Pis
					comm.bcast(['quit',None,None],root=0)
					pygame.quit()
					sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x,y = event.pos
				for i in buttons: # If a button is pressed, it will return its string which will be used to decipher which button was pressed
					if i.mouseloc(x,y):
						button_str = i.getactionStr()
				
				# If the load button is pressed, a window will come up asking the user to load a Python Pickle file.
				# Once the user selects, the program will load the data, convert the pixels to meters and then plot the data
				if button_str == "load":
					Tk().withdraw()
					infile = askopenfilename(filetypes=[("Python Pickle","*.p")])
					if infile != '':
						g = 0; Cd = 0; vi = 0
						xCoord, yCoord, timing, pxPerM, figure, axis = load_data(screen,infile,figure,axis,HEIGHT_IN_METERS)
						graph = create_graph(figure, plot_size)
						screen.blit(graph, plot_loc)
						fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 0)
						pyplot.clf()
				
				# If the user selects "Fit Data", the program will split a nested while loop and using the least squares algorithm,
				# will calculate which one best fits the data. Then it will plot the data, best fit, and the ideal fit.
				elif button_str == "fit":
					if yCoord != []:
						comm.bcast([button_str,yCoord,timing],root=0) # Sends the data required for the loop to all the nodes
						g, vi, figure, axis = fit_data_basic(screen,yCoord,timing,HEIGHT_IN_METERS,figure,axis,comm)
						graph = create_graph(figure, plot_size)
						fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 1)
						screen.blit(graph, plot_loc)
						pyplot.ylim((0,HEIGHT_IN_METERS))
						pyplot.clf()
				
				# If the user selects "Advanced", the program will prompt the user for either a preset or if the preset isn't already in the program,
				# the user can add a new one. It will ask for mass, cross-sectional area, and the air density. Then the program will do similar to the
				# fit by splitting the loop up into chunks and calculate the best fit taking drag into affect.
				elif button_str == "afit":
					if yCoord != []:
						mass, csArea, airD = get_constants()
						if None not in [mass,csArea,airD]:
							comm.bcast([button_str,yCoord,timing,mass,csArea,airD],root=0) # Sends the data required for the loop to all the nodes
							g, vi, Cd, figure, axis = fit_data_advanced(screen,yCoord,timing,mass,csArea,airD,HEIGHT_IN_METERS,figure,axis,comm)
							graph = create_graph(figure, plot_size)
							fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 2)
							screen.blit(graph, plot_loc)
							pyplot.ylim((0,HEIGHT_IN_METERS))
							pyplot.clf()
					
		# Loads the buttons to the screen			
		for i in buttons:
			screen.blit(i.getpicDisp(),i.getLoc())
		
		button_str = ""
		pygame.display.update()
		clock.tick(update_rate)
else:
	while True:
		data = comm.bcast(None,root=0) # Waits until the data is sent from the head node for the loop.
		button_str = data[0]; yCoord = data[1]; timing = data[2]
		
		# Depending on what the user selected, it will either quit, do a normal fit, or do an advanced fit.
		if button_str == 'fit':
			fit_data_basic(None,yCoord,timing,HEIGHT_IN_METERS,figure,axis,comm)
		elif button_str == 'afit':
			mass = data[3]; csArea = data[4]; airD = data[5]
			fit_data_advanced(None,yCoord,timing,mass,csArea,airD,HEIGHT_IN_METERS,figure,axis,comm)
		elif button_str == 'quit':
			sys.exit()
			break