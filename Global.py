#coding: utf8
#Imports
import pygame, sys, math
import pygame.gfxdraw
import random as rn
import numpy as np
import ast
from pygame.locals import *

#global variables
WIDTH = 640
HEIGHT = 640
GAME_NAME = "SQUARE ESCAPE"

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = Color(255, 0, 0, 100)
GREEN = (0, 255, 0)
BLUE = Color(0, 0, 255,200)
GRAY_BLUE = (108, 159, 126)

#Delay values
DELAY = np.arange(1,20.1, 0.1)
DELAY = 1/DELAY * 1000

#USER EVENTS
SCOREEVENT = USEREVENT + 1
INVEVENT = USEREVENT + 2

#SCORES
#Importe le fichier des scores
path_Scores = 'Scores.txt'
with open(path_Scores, 'r') as f:
	HIGH_SCORES = f.read()
#Converti en liste de int
HIGH_SCORES = ast.literal_eval(HIGH_SCORES)



#Detect if a rectangle and a circle are intersecting
def collision(cx, cy, radius, x, y, width, height):
	p1 = (x,y)
	p2 = (x+width, y)
	p3 = (x, y+height)
	p4 = (x+width, y+height)
	
	for p in [p1,p2,p3,p4]:
		if math.hypot(cx - p[0], cy - p[1]) < radius:
			return True
	return False
	
