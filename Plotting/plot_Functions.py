import pickle,pygame,sys,time,matplotlib,pylab,math
from button import *
from plot_Functions import *
from textrect import render_textrect
from pygame.locals import *
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import matplotlib.backends.backend_agg as agg
from scipy.optimize import curve_fit
import numpy as np

global constGUI
global m
global rho
global A

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
	gTmp = 7.0
	viTemp = -1.50
	g = 0; vi = 0; diff = 0
	fitGraph = []; idealGraph = []; yFit = []; temp = []
	
	while gTmp < 12.0:
		while viTemp < 1.50:
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
		viTemp = -1.50
		gTmp += 0.05
	axis = figure.gca(axisbg="0.0")
	axis = style_axis(axis,HEIGHT_IN_METERS)
	axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
	axis.plot(timing,fitGraph,'g',label='Fit',linewidth=2) 
	axis.plot(timing,idealGraph,'r',label='Ideal',linewidth=2)
	axis.legend()
	return g, vi, figure, axis
	
def fit_data_advanced(yCoord,timing,pxPerM,HEIGHT_IN_METERS,figure,axis):
	gTmp = 7.0
	viTemp = -1.50
	g = 0; vi = 0; diff = 0; Cd = 0
	fitGraph = []; idealGraph = []; yFit = []; temp = []
	m = .057
	CdTemp = .3
	rho = 1.225
	A = 0.00335978
	
	while gTmp < 12.0:
		while viTemp < 1.50:
			while CdTemp < .8:
				for i in range(len(timing)):
					a = math.sqrt(2*m*gTmp/(rho*A*CdTemp))
					b = math.sqrt(gTmp*rho*CdTemp*A/(2*m))
					temp.append(HEIGHT_IN_METERS - (a*math.log(math.cosh(b*timing[i])))/b - viTemp*timing[i])
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
					Cd = CdTemp
				temp = []
				diff = 0
				viTemp = round(viTemp+0.05,2)
				CdTemp += .01
			CdTemp = .3
		viTemp = -1.50
		gTmp += 0.05
	axis = figure.gca(axisbg="0.0")
	axis = style_axis(axis,HEIGHT_IN_METERS)
	axis.plot(timing,yCoord,'b',label='Data',linewidth=2)
	axis.plot(timing,fitGraph,'g',label='Fit',linewidth=2) 
	axis.plot(timing,idealGraph,'r',label='Ideal',linewidth=2)
	axis.legend()
	print Cd
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
	
def get_constants():	
	global constGUI
	global m
	global rho
	global A
	
	m = 0
	rho = 0
	A = 0
	area = StringVar()
	mass = StringVar()
	air = StringVar()
	
	constGUI = Tk()
	constGUI.geometry("300x175+100+100")
	l1 = Label(constGUI,text="Advanced Fitting Options",font=("sanserif", 16)).pack()
	l2 = Label(constGUI,text="Object's Mass(kg)").place(x=15,y=40)
	l3 = Label(constGUI,text="Air Density(kg/m^3)").place(x=15,y=70)
	l4 = Label(constGUI,text="Object's Area(m^2)").place(x=15,y=100)
	b1 = Button(constGUI,text="OK",command=lambda:save_constants(mass.get(),air.get(),area.get())).place(x=120,y=130)
	b2 = Button(constGUI,text="Cancel",command=save_constants).place(x=150,y=130)
	e1 = Entry(constGUI,textvariable=mass).place(x=155,y=40)
	e2 = Entry(constGUI,textvariable=air).place(x=155,y=70)
	e3 = Entry(constGUI,textvariable=area).place(x=155,y=100)
	constGUI.mainloop()
	return m, rho, A

def save_constants(mass,air,area):
	global constGUI
	global m
	global rho
	global A
	m = mass
	rho = air
	A = area
	constGUI.destroy()
	constGUI.quit()
	return
	
def getY(timing, g, Cd, vi):
	HEIGHT_IN_METERS = 6*0.3048
	m = 0.057
	rho = 1.225
	A =  0.00335978
	a = np.sqrt(2*m*abs(g)/(rho*A*abs(Cd)))
	b = np.sqrt(abs(g)*rho*abs(Cd)*A/(2*m))
	return (HEIGHT_IN_METERS - (a*np.log(np.cosh(b*timing)))/b - vi*timing)