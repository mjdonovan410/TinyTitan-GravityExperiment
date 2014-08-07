#----------------------------------------------------------------------------------
# Author: 	Matt Donovan
# Provider:	Oak Ridge National Lab
# Date: 	8/7/14
# File:		plot_Functions.py
# Purpose:	Provides a list of functions to clean up the code in plotting.py
#----------------------------------------------------------------------------------

import pickle,pygame,sys,time,matplotlib,pylab,math
from button import *
from plot_Functions import *
from textrect import render_textrect
from pygame.locals import *
import matplotlib.backends.backend_agg as agg
import tkSimpleDialog
from math import floor
from mpi4py import MPI

# Loads data from the file and adjusts to accordingly
def load_data(screen,infile,figure,axis,HEIGHT_IN_METERS):
	xCoord = []
	yCoord = []
	yCoordNew = []
	timing = []
	data = pickle.load(open(infile,'rb'))
	length = len(data)
	
	# Loops through the data and splits the data into separate arrays
	# The data is separated by ((xCoord,yCoord),Time)
	for i in range(length):
		temp = data[i]
		coord = temp[0]
		xCoord.append(coord[0])
		yCoord.append(coord[1])
		timing.append(temp[1])
	# Calculates the pixels per meter assuming the first and last data points are the full frame
	pxPerM = (max(yCoord)-min(yCoord))/HEIGHT_IN_METERS
	
	# Changes all of the yCoords to meters
	for i in range(len(yCoord)):
		yCoordNew.append(round((max(yCoord)-yCoord[i]-min(yCoord))/pxPerM,3))
	
	# If the smallest Y coordinate is less than 0, all of the coordinates will be bumped so the smallest number will be 0
	if min(yCoordNew) < 0:
		miny = min(yCoordNew)
		for i in range(length):
			yCoordNew[i] = yCoordNew[i] - miny
	
	# Plots data
	loading_plot(screen)		
	figure = pylab.figure(figsize=[6, 6],dpi=75,facecolor="0.1") # Makes the plot figure 450x450px
	axis = figure.gca(axisbg="0.0")
	axis = style_axis(axis,HEIGHT_IN_METERS)
	axis.plot(timing,yCoordNew,'b',label='Data',linewidth=2)
	axis.legend()	
	return xCoord, yCoordNew, timing, pxPerM, figure, axis

# Renders an image from the plot created to be loaded to the screen	
def create_graph(figure,plot_size):
	canvas = agg.FigureCanvasAgg(figure)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	graph = pygame.image.fromstring(raw_data, plot_size, "RGB")
	return graph

# Fits the data using the least squares algorithm and splitting the loop across all processors
def fit_data_basic(screen,yCoord,timing,HEIGHT_IN_METERS,figure,axis,comm):
	rank = comm.rank
	size = comm.size
	name = MPI.Get_processor_name()
	totRange = [7.5,11.5]
	gStep = 0.01
	viStep = 0.05
	
	# Using the rank and size provided from MPI, it will calculate the range that each processor will calculate
	gStart = floor(100*(totRange[0] + float(rank)*float((totRange[1]-totRange[0])/float(size))))/100 + 0.01
	gStop = floor(100*(gStart + float((totRange[1]-totRange[0])/float(size))))/100 - 0.01
	print rank, name, gStart, "--", gStop
	
	# Sets starting values and instantiates values for the loop
	gTmp = gStart
	viTemp = -0.50
	g = 0; vi = 0; diff = 0; lowestDiff = 0.5;
	fitGraph = []; idealGraph = []; temp = []
	
	# This will calculate the position of the ball in ideal conditions (no drag) and then compare it to the data collected.
	# Due to minor user error, the initial velocity also has to be calculated.
	while gTmp < gStop:
		while viTemp < 0.50:
			# Calculates and compares the data to the find the smallest difference
			for i in range(len(timing)):
				temp.append(HEIGHT_IN_METERS -(float(gTmp)*(timing[i]**2)/2) - viTemp*timing[i])
				diff += (yCoord[i]-temp[i])**2
			
			# If conditions are ideal, it will capture it for comparison on the plot
			if round(gTmp,2) == 9.81 and round(viTemp,2) == 0.00:
				idealGraph = temp
			
			# If it is smaller than the previous smallest, it will replace all the data with the new lowest
			if diff < lowestDiff:
				fitGraph = []
				g = gTmp
				vi = viTemp
				fitGraph = temp
				lowestDiff = diff
			
			# Reset for new iteration of initial velocity
			temp = []
			diff = 0
			viTemp = round(viTemp+viStep,2)
		
		# Reset for next iteration of gravity
		viTemp = -0.50
		gTmp += gStep
	
	# Collects all the data from all the other nodes to the head node
	data = comm.gather([lowestDiff,g,vi,None,fitGraph,idealGraph],root=0)
	
	if rank == 0:
		# The head node then calculates which one had the smallest difference and will return all the corresponding data
		g,vi,Cd,fitGraph,idealGraph = get_smallest(data)
		
		# Loads the plot for the data, the best fit, and the ideal conditions
		loading_plot(screen)		
		axis = figure.gca(axisbg="0.0")
		axis = style_axis(axis,HEIGHT_IN_METERS)
		axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
		axis.plot(timing,fitGraph,'g',label='Fit',linewidth=2) 
		axis.plot(timing,idealGraph,'r',label='Ideal',linewidth=2)
		axis.legend()
		return round(g,2), round(vi,2), figure, axis

# Loops through the data given and calculates the best fit for the data		
def get_smallest(data):
	diffTemp = 100
	bestFit = []
	idealGraph = None
	
	# If the difference is smaller than the previous smallest difference, the best fit will update to the new smallest difference
	for i in data:
		if i[0] < diffTemp:
			diffTemp = i[0]
			bestFit = i
		if i[5] != []:
			idealGraph = i[5]
	g = bestFit[1]
	vi = bestFit[2]
	Cd = bestFit[3]
	fitGraph = bestFit[4]
	return g,vi,Cd,fitGraph,idealGraph


def fit_data_advanced(screen,yCoord,timing,mass,csArea,airD,HEIGHT_IN_METERS,figure,axis,comm):
	rank = comm.rank
	size = comm.size
	name = MPI.Get_processor_name()
	totRange = [9.0,10.5]
	viRange = [-0.30,0.30]
	CdRange = [0.45,0.65]
	gStep = 0.01
	viStep = 0.05
	CdStep = 0.01
	
	# Using the rank and size provided from MPI, it will calculate the range that each processor will calculate
	gStart = floor(100*(totRange[0] + float(rank)*float((totRange[1]-totRange[0])/float(size))))/100 + 0.01
	gStop = floor(100*(gStart + float((totRange[1]-totRange[0])/float(size))))/100 - 0.01
	print rank, name, gStart, "--", gStop
	
	# Sets starting values and instantiates values for the loop
	gTemp = gStart
	viTemp = viRange[0]
	CdTemp = CdRange[0]
	g = 0; vi = 0; diff = 0; Cd = 0; lowestDiff = 1
	fitGraph = []; idealGraph = []; temp = []
	
	# Calculates the position taking into account drag and then compares it to the data using the least squares algorithm.
	while gTemp < gStop:
		while viTemp < viRange[1]:
			while CdTemp < CdRange[1]:
				# Using the crazy equation for position with drag, this calculates the position and compares it to see which has the least difference from the data provided
				for i in range(len(timing)):
					a = math.sqrt(2*mass*gTemp/(airD*csArea*CdTemp))
					b = math.sqrt(gTemp*airD*CdTemp*csArea/(2*mass))
					temp.append(HEIGHT_IN_METERS - (a*math.log(math.cosh(b*timing[i])))/b - viTemp*timing[i])
					diff += (yCoord[i]-temp[i])**2
				
				# If perfect conditions, the data will be captured for plotting
				if round(CdTemp,2) == 0.47 and round(gTemp,2) == 9.81 and round(viTemp,2) == 0.00:
					idealGraph = temp
				
				# If the difference is lower, then the new lowest is saved to all the variables
				if diff < lowestDiff:
					g = gTemp
					vi = viTemp
					Cd = CdTemp
					lowestDiff = diff
					fitGraph = temp
				
				# Reset for next iteration of drag coefficient
				temp = []
				diff = 0
				CdTemp += CdStep
			
			# Reset for next iteration of initial velocity
			CdTemp = CdRange[0]
			viTemp += viStep
		
		# Reset for next iteration of gravity
		viTemp = viRange[0]
		gTemp += gStep
	
	# Collects all the data from all the other nodes to the head node
	data = comm.gather([lowestDiff,g,vi,Cd,fitGraph,idealGraph],root=0)
	
	if rank == 0:
		# The head node then calculates which one had the smallest difference and will return all the corresponding data
		g,vi,Cd,fitGraph,idealGraph = get_smallest(data)
		
		# Loads the plot for the data, the best fit, and the ideal conditions
		loading_plot(screen)
		axis = figure.gca(axisbg="0.0")
		axis = style_axis(axis,HEIGHT_IN_METERS)
		axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
		axis.plot(timing,fitGraph,'g',label='Fit',linewidth=2) 
		axis.plot(timing,idealGraph,'r',label='Ideal',linewidth=2)
		axis.legend()
		return round(g,2), round(vi,2), round(Cd,2), figure, axis

# This function is only used to make the plot look the way it does. Aesthetics only
def style_axis(axis,HEIGHT_IN_METERS):
	axis.set_xlabel('Time(s)')
	axis.set_ylabel('Height(m)')
	axis.xaxis.label.set_color('white')
	axis.yaxis.label.set_color('white')
	axis.tick_params(axis='x', colors='white')
	axis.tick_params(axis='y', colors='white')
	pylab.ylim([0,math.ceil(HEIGHT_IN_METERS)])
	for i in axis.get_children():
		if isinstance(i, matplotlib.spines.Spine):
			i.set_color('#000000')
	return axis

# This loads the presets and allows the user to add new presets	
def get_constants():
	mass = None
	csArea = None
	airD = None
	
	# Loads the presets from the file
	data = pickle.load(open("constants.p", "rb"))
	pNames = [str(i[0]) for i in data]
	
	# Prompt for preset or new preset
	preset = tkSimpleDialog.askstring("Load Preset", "Please type a preset name or new")
	if preset == 'new':
		# Prompts for the object's mass
		mass = tkSimpleDialog.askstring("Mass", "Type value of the object's mass(kg)")
		if mass != None:
			# Prompts for the object's Cross-Sectional Area
			csArea = tkSimpleDialog.askstring("Cross-Sectional Area", "Type value of the object's cross-sectional area(m^2)")
			if csArea != None:
				# Prompts for the room's air density
				airD = tkSimpleDialog.askstring("Air Density", "Type value of the room's Air Density(kg/m^3)")
				if airD != None:
					try: # If any of the data entered was not a number, it will throw an error
						mass = float(mass)
						csArea = float(csArea)
						airD = float(airD)
						
						# Asks for a name for the preset. If no name is entered, it will assign it "Temp"
						name = tkSimpleDialog.askstring("Name New Preset", "What would you like to name the new preset?")
						if name == None:
							name = "Temp"
						
						# If the name is already in the file, it will overwrite it
						if name in pNames:
							temp = pNames.index(name)
							data.pop(temp)
							
						# Adds the new preset and rewrites the file
						data.append((name,[mass,csArea,airD]))
						file = open("constants.p", "wb")
						pickle.dump(data, file)
						file.close()
					except ValueError:
						mass = None
						print "ERROR: Values entered invalid"
	else:
		# If it is a preset, it will load the constants. Otherwise, it will throw an error.
		if preset in pNames:
			temp = data[pNames.index(preset)]
			temp2 = temp[1]
			mass = temp2[0]
			csArea = temp2[1]
			airD = temp2[2]
		else:
			if preset != None:
				print "ERROR: ",preset,"has not been defined as a preset"
	return mass, csArea, airD

# This simply takes the results and places makes them look nice to display. Aesthetics only.
def load_results(screen, fitResults, font, data_rect, g, vi, Cd, state):
	# There are 3 possible states: loading = 0, fit data = 1, and advanced = 2
	if state == 0:
		fitResults[0] = render_textrect("", font, data_rect, (255,0,0), (0,0,0), justification=1)
		screen.blit(fitResults[0],(15,210))
		screen.blit(fitResults[0],(15,240))
		screen.blit(fitResults[0],(15,270))
	elif state in [1,2]:
		fitResults[0] = render_textrect("g = "+str(g)+" m/s^2", font, data_rect, (255,0,0), (0,0,0), justification=1)
		fitResults[1] = render_textrect("vi = "+str(vi)+" m/s", font, data_rect, (255,0,0), (0,0,0), justification=1)
		fitResults[2] = render_textrect("", font, data_rect, (255,0,0), (0,0,0), justification=1)
		screen.blit(fitResults[0],(15,210))
		screen.blit(fitResults[1],(15,240))
		screen.blit(fitResults[2],(15,270))
	if state == 2:
		fitResults[2] = render_textrect("Cd = "+str(Cd), font, data_rect, (255,0,0), (0,0,0), justification=1)
		screen.blit(fitResults[2],(15,270))
	
	return fitResults

# This just prints to the screen saying that the plot is loading because generating the plots take about 5 seconds on the Pis
def loading_plot(screen):
	font = pygame.font.SysFont("sanserif",48)
	label = font.render("CREATING PLOT",1,(255,0,0))
	screen.blit(label,(330,220))
	pygame.display.update()