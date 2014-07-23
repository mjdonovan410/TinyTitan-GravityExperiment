import pickle,pygame,sys,time,matplotlib,pylab,math
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
		temp = data[i]
		coord = temp[0]
		xCoord.append(coord[0])
		yCoord.append(coord[1])
		timing.append(temp[1])
	pxPerM = (max(yCoord)-min(yCoord))/HEIGHT_IN_METERS
	for i in range(len(yCoord)):
		yCoord[i] = round((max(yCoord)-yCoord[i]-min(yCoord))/pxPerM,3)
	figure = pylab.figure(figsize=[6, 6],dpi=75,facecolor="0.1")
	axis = figure.gca(axisbg="0.0")
	axis = style_axis(axis,HEIGHT_IN_METERS)
	axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
	axis.legend()
	
	return xCoord, yCoord, timing, pxPerM, figure, axis
	
def create_graph(figure,plot_size):
	canvas = agg.FigureCanvasAgg(figure)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()
	graph = pygame.image.fromstring(raw_data, plot_size, "RGB")
	return graph
	
def fit_data_basic(yCoord,timing,HEIGHT_IN_METERS,figure,axis):
	gTmp = 8.0
	viTemp = -1.00
	g = 0
	fitGraph = []
	idealGraph = []
	yFit = []
	diff = 0
	temp = []
	vi = 0
	while gTmp < 11.0:
		while viTemp < 1.00:
			for i in range(len(timing)):
				temp.append(HEIGHT_IN_METERS -(float(gTmp)*(timing[i]**2)/2) - viTemp*timing[i])
				diff += (yCoord[i]-temp[i])**2
			yFit.append(diff)
			if round(gTmp,1) == 9.8 and round(viTemp,2) == 0.00:
				idealGraph = temp
			if diff == min(yFit):
				fitGraph = []
				yFit = []
				yFit.append(diff)
				g = gTmp
				vi = viTemp
				fitGraph = temp
			temp = []
			diff = 0
			viTemp = round(viTemp+0.05,2)
		viTemp = -1.00
		gTmp += 0.05
	axis = figure.gca(axisbg="0.0")
	axis = style_axis(axis,HEIGHT_IN_METERS)
	axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
	axis.plot(timing,fitGraph,'g',label='Fit',linewidth=2) 
	axis.plot(timing,idealGraph,'r',label='Ideal',linewidth=2)
	axis.legend()
	return g, vi, figure, axis

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