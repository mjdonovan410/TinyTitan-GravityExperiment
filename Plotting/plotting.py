import pickle,pygame,sys,time,matplotlib,pylab
from button import *
from plot_Functions import *
from textrect import render_textrect
from pygame.locals import *
from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfilename
import matplotlib.backends.backend_agg as agg

HEIGHT_IN_METERS = 6*0.3048 # 6ft conversion to meters

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
timer = 0
button_str = ""
message_str = ""
message_rect = pygame.Rect((0,0), (200,30))
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
iV = 0.00
fitResults = [None,None]
figure = None
axis = None

while True:
	x,y = pygame.mouse.get_pos()
	
	for i in buttons: 
		i.mouseloc(x,y)
			
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == 27:
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
					xCoord, yCoord, timing, pxPerM, figure, axis = load_data(infile,figure,axis,HEIGHT_IN_METERS)
					graph = create_graph(figure)
					screen.blit(graph, plot_loc)
					figure.clf
			
			elif button_str == "fit":
				g, iV, figure, axis = fit_data_basic(yCoord,timing,HEIGHT_IN_METERS,figure,axis)
				fitResults[0] = render_textrect("G = "+str(g)+" m/s^2", font, message_rect, (255,0,0), (0,0,0), justification=1)
				fitResults[1] = render_textrect("iV = "+str(iV)+" m/s", font, message_rect, (255,0,0), (0,0,0), justification=1)
				graph = create_graph(figure)
				screen.blit(fitResults[0],(15,220))
				screen.blit(fitResults[1],(15,250))
				screen.blit(graph, plot_loc)
				figure.clf
			
			elif button_str == "afit":
				print "UNDER CONSTRUCTION"
				
				
	for i in buttons:
		screen.blit(i.getpicDisp(),(i.getx(),i.gety()))
	
	button_str = ""
	pygame.display.update()
	clock.tick(update_rate)