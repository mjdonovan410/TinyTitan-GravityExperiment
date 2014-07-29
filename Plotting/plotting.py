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

comm = MPI.COMM_WORLD

name = MPI.Get_processor_name()
rank = comm.rank
size = comm.size
print rank, name, size

HEIGHT_IN_METERS = 6*0.3048 # 6ft conversion to meters
pygame.init()

font = pygame.font.SysFont("sanserif",30)
button_str = ""
data_rect = pygame.Rect((0,0), (200,30))
timing = []
xCoord = []
yCoord = []
pxPerM = 1000
yFit = []
vi = 0.00
fitResults = [None,None,None]
figure = None
axis = None
g = 0
Cd = 0
vi = 0

if rank == 0:
	clock = pygame.time.Clock()
	screen_size = (700,480)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Experiment Plotting")
	plot_size = (450,450)
	plot_loc = (235,15)
	logo = pygame.image.load("Images/ORNL_Images/ORNL_Stacked_white_banner.png")
	plotTemp = pygame.image.load("Images/plot_temp.png")
	
	# Creates an array of Button objects the will provide data and blit the objects to the screen
	buttons = []
	buttons.append(ImgButton(screen,False,None,None,"Images/load.png","Images/load2.png","load",(15,140),(200,49)))
	buttons.append(ImgButton(screen,False,None,None,"Images/fit.png","Images/fit2.png","fit",(15,365),(200,49)))
	buttons.append(ImgButton(screen,False,None,None,"Images/advanced.png","Images/advanced2.png","afit",(15,420),(200,49)))

	# Basic GUI Frame Setup
	update_rate = 20
	screen.blit(logo,(0,0))
	screen.blit(plotTemp,plot_loc)

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
						g = 0
						Cd = 0
						vi = 0
						xCoord, yCoord, timing, pxPerM, figure, axis = load_data(infile,figure,axis,HEIGHT_IN_METERS)
						graph = create_graph(figure, plot_size)
						screen.blit(graph, plot_loc)
						screen,fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 0)
						pyplot.clf()
				
				elif button_str == "fit":
					if yCoord != []:
						comm.bcast([yCoord,timing],root=0)
						g, vi, figure, axis = fit_data_basic(yCoord,timing,HEIGHT_IN_METERS,figure,axis,comm,size,rank)
						graph = create_graph(figure, plot_size)
						screen,fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 1)
						screen.blit(graph, plot_loc)
						pyplot.ylim((0,HEIGHT_IN_METERS))
						pyplot.clf()
				
				elif button_str == "afit":
					if yCoord != []:
						mass, csArea, airD = get_constants()
						if None not in [mass,csArea,airD]:
							g, vi, Cd, figure, axis = fit_data_advanced(yCoord,timing,pxPerM,mass,csArea,airD,HEIGHT_IN_METERS,figure,axis,comm,size,rank)
							graph = create_graph(figure, plot_size)
							screen,fitResults = load_results(screen, fitResults, font, data_rect, g, vi, Cd, 2)
							screen.blit(graph, plot_loc)
							pyplot.ylim((0,HEIGHT_IN_METERS))
							pyplot.clf()
					
		for i in buttons:
			screen.blit(i.getpicDisp(),(i.getx(),i.gety()))
		
		button_str = ""
		pygame.display.update()
		clock.tick(update_rate)
else:
	data = comm.bcast(None,root=0)
	yCoord = data[0]
	timing = data[1]
	if input == "fit":
		g, vi, figure, axis = fit_data_basic(yCoord,timing,HEIGHT_IN_METERS,figure,axis,comm,size,rank)
		comm.send([g,vi],dest=0)
	elif input == "afit":
		g, vi, Cd, figure, axis = fit_data_advanced(yCoord,timing,pxPerM,mass,csArea,airD,HEIGHT_IN_METERS,figure,axis,comm,size,rank)
		comm.send([g,vi,Cd],dest=0)