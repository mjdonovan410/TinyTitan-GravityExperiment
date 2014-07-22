import pickle,pygame,sys,time
from button import *
from textrect import render_textrect
from pygame.locals import *
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

HEIGHT_IN_METERS = 6*0.3048 # 6ft conversion

pygame.init()

clock = pygame.time.Clock()
screen_size = (700,480)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Experiment Plotting")
plot_size = (450,450)
plot_loc = (235,15)
logo = pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png")
plotTemp = pygame.image.load("Images/plot_temp.png")
fontB = pygame.font.SysFont("sanserif",36)
fontL = pygame.font.SysFont("sanserif",24)
timer = 0
button_str = ""
message_str = ""
message_rect = pygame.Rect((0,0), (200,50))
message = False

# Creates an array of Button objects the will provide data and blit the objects to the screen
buttons = []
buttons.append(Button(screen,False,None,None,"Images/load.png","Images/load2.png","load",(15,140),(200,49)))
buttons.append(Button(screen,False,None,None,"Images/fit.png","Images/fit2.png","fit",(15,365),(200,49)))
buttons.append(Button(screen,False,None,None,"Images/advanced.png","Images/advanced2.png","afit",(15,420),(200,49)))

# Basic GUI Frame Setup
update_rate = 20
screen.blit(logo,(0,0))
screen.blit(plotTemp,plot_loc)
timing = []
xCoord = []
yCoord = []
pxPerM = 1000
yFit = []

while True:
	x,y = pygame.mouse.get_pos()
	
	for i in buttons: 
		i.mouseloc(x,y)
			
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			x,y = event.pos
			for i in buttons:
				if i.mouseloc(x,y):
					button_str = i.getactionStr()
			
			if button_str == "load":
				Tk().withdraw()
				infile = askopenfilename(filetypes=[("Python Pickle","*.p")])
		
				if infile != '':
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
					#print yCoord
					 
					canvas = agg.FigureCanvasAgg(figure)
					canvas.draw()
					renderer = canvas.get_renderer()
					raw_data = renderer.tostring_rgb()
					graph = pygame.image.fromstring(raw_data, (450,450), "RGB")
					screen.blit(graph, plot_loc)
			
			elif button_str == "fit":
				g = 6.0
				gVal = 0
				fitGraph = []
				idealGraph = []
				yFit = []
				diff = 0
				temp = []
				while g < 13.0:
					for i in range(len(timing)):
						temp.append(HEIGHT_IN_METERS -(float(g)*(timing[i]**2)/2))
						diff += (yCoord[i]-temp[i])**2
					
					yFit.append(diff)
					if str(g) == "9.8":
						idealGraph = temp
					if diff == min(yFit):
						fitGraph = []
						gVal = g
						fitGraph = temp
					
					temp = []
					diff = 0
					g += 0.1
				#print yFit
				print "------",gVal,"-------"
				figure = pylab.figure(figsize=[4.5, 4.5],dpi=100)
				axis = figure.gca()
				axis.plot(timing,yCoord)
				axis.plot(timing,fitGraph) 
				axis.plot(timing,idealGraph) 
				canvas = agg.FigureCanvasAgg(figure)
				canvas.draw()
				renderer = canvas.get_renderer()
				raw_data = renderer.tostring_rgb()
				graph = pygame.image.fromstring(raw_data, (450,450), "RGB")
				screen.blit(graph, plot_loc)
				figure.clf
				
				
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))
	
	button_str = ""
	pygame.display.update()
	clock.tick(update_rate)