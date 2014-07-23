import pickle,pygame,sys,time,matplotlib,pylab
from button import *
from plot_Functions import *
from textrect import render_textrect
from pygame.locals import *
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename
import matplotlib.backends.backend_agg as agg

def load_data(infile,figure,axis,HEIGHT_IN_METERS):
	xCoord = []
	yCoord = []
	timing = []
	data = pickle.load(open(infile,'rb'))
	length = len(data)
	for i in range(length):
		timing.append(float(i)*1/90)
	for i in range(length):
		temp = data[i]
		coord = temp[0]
		xCoord.append(coord[0])
		yCoord.append(coord[1])
		#timing.append(temp[1])
	pxPerM = (max(yCoord)-min(yCoord))/HEIGHT_IN_METERS
	for i in range(len(yCoord)):
		yCoord[i] = round((max(yCoord)-yCoord[i]-min(yCoord))/pxPerM,3)
	figure = pylab.figure(figsize=[4.5, 4.5],dpi=100)
	axis = figure.gca()
	axis.plot(timing,yCoord)
	
	return xCoord, yCoord, timing, pxPerM, figure, axis
	
def create_graph(figure):
	canvas = agg.FigureCanvasAgg(figure)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	graph = pygame.image.fromstring(raw_data, (450,450), "RGB")
	return graph
	
def fit_data_basic(yCoord,timing,HEIGHT_IN_METERS,figure,axis):
	gTmp = 8.0
	iVTemp = -1.00
	g = 0
	fitGraph = []
	idealGraph = []
	yFit = []
	diff = 0
	temp = []
	iV = 0
	while gTmp < 11.0:
		while iVTemp < 1.00:
			for i in range(len(timing)):
				temp.append(HEIGHT_IN_METERS -(float(gTmp)*(timing[i]**2)/2) - iVTemp*timing[i])
				diff += (yCoord[i]-temp[i])**2
			yFit.append(diff)
			if round(gTmp,1) == 9.8 and round(iVTemp,2) == 0.00:
				idealGraph = temp
			if diff == min(yFit):
				fitGraph = []
				yFit = []
				yFit.append(diff)
				g = gTmp
				iV = iVTemp
				fitGraph = temp
			#print iVTemp,"/",round(diff,3)
			temp = []
			diff = 0
			iVTemp = round(iVTemp+0.05,2)
		iVTemp = -1.00
		gTmp += 0.05
		#print "-----------------------",gTmp
		
	#print "------",g,"/",iV,"------"
	figure = pylab.figure(figsize=[4.5, 4.5],dpi=100)
	axis = figure.gca()
	axis.plot(timing,yCoord)
	axis.plot(timing,fitGraph) 
	axis.plot(timing,idealGraph)
	return g, iV, figure, axis