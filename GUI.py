from os import path
from numpy.lib.function_base import select
import pygame
from pygame.mixer import pause
import os
import numpy as np
import time
import math
from pathfinding import pathfinding as pf
import sys

#hide default pygame message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()

#Screen
cell_size = 30
ncells = 30
line_colour = (200,200,200)
screen = pygame.display.set_mode((ncells*cell_size,ncells*cell_size))

#pathfinding class init
pathfinding = pf(ncells, (10,-10), (-1,-1))

#facade board
board_copy = np.copy(pathfinding.board)

# final path
final_path = []

def drawCell(xcord, ycord, colour):
    #print box
    square = pygame.Rect((xcord*cell_size, ycord*cell_size, cell_size, cell_size)) 
    pygame.draw.rect(screen,colour,square)

def drawBoard():
    screen.fill((255,255,255))
    for r in range(ncells):
        
        for c in range(ncells):           
                 
            #   PROBING
            if pathfinding.heuristic[r][c] != sys.maxsize:
                drawCell(r,c, (15,210,185))
                
            #   SEARCHED
            if (r,c) in pathfinding.explored:
                drawCell(r,c, (13,179,154))                    
            #   WALL
            if not board_copy[r][c]:
                drawCell(r,c, (0,0,0)) 
            #   DESTINATION
            if (r,c)==pathfinding.dest:
                drawCell(r,c, (255,0,0))
            #   START
            if (r,c)==pathfinding.origin:
                drawCell(r,c, (0,0,255)) 
            #   FINAL PATH
            if (r,c) in final_path:
                print(final_path)
                drawCell(r,c, (0,255,0)) 

    for r in range(100):
        pygame.draw.line(screen,line_colour,(r*cell_size, 0), (r*cell_size, ncells*cell_size),1)
    for c in range(100):      
        pygame.draw.line(screen,line_colour,(0, c*cell_size), (ncells*cell_size, c*cell_size),1)

def selectCell(prev, pos, draw):
    xpos = pos[0]
    ypos = pos[1]

    if board_copy[xpos][ypos] == draw:
        board_copy[xpos][ypos] = not draw
        
        #make it so fast mouse doesn't break

def pathFind():
    global RUNNING
    SIMULATING = True
    FINDING = True
    node = pathfinding.dest
    global final_path

    while RUNNING and SIMULATING:

        for event in pygame.event.get():
            #close game
            if event.type == pygame.QUIT:
                RUNNING = False

        if FINDING:
            FINDING = pathfinding.nextStep()
        else:
            node = pathfinding.addToPath(final_path, node)
            if node == pathfinding.origin:
                SIMULATING = False

        drawBoard()                
        pygame.display.update()



RUNNING = True
SELECTING = False
selectedCell = (-1,-1)

draw = True
while RUNNING:    

    for event in pygame.event.get():
        #close game
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONUP :
            if event.button == 2:
                SELECTING = False
                pathfinding.board = board_copy
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                SELECTING = True
                board_copy = np.copy(pathfinding.board)
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
                pathfinding.dest = selectedCell
            elif event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
                pathfinding.addOrigin(selectedCell)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                draw = False
            if event.key == pygame.K_SPACE:
                pathFind()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                draw = True
        
            

    if SELECTING:
        prev_selected_cell = selectedCell
        mouse_pos = pygame.mouse.get_pos()
        selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
        selectCell(prev_selected_cell, selectedCell, draw)
    
    drawBoard()  
    pygame.display.update()