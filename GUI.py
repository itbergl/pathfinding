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

#Icon
pygame.display.set_caption("Path Finder")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

#Screen
cell_size = 20
ncells = 30
line_colour = (200,200,200)
screen = pygame.display.set_mode((ncells*cell_size,ncells*cell_size))

#pathfinding class init
pathfinding = pf(ncells)

#facade board
board_copy = np.copy(pathfinding.board)

# final path
final_path = []

def drawCell(xcord, ycord, colour):
    #print box
    square = pygame.Rect((xcord*cell_size, ycord*cell_size, cell_size, cell_size)) 
    pygame.draw.rect(screen,colour,square)

    # #print heuristic
    # num_font = pygame.font.Font('freesansbold.ttf', 10)
    # static_num_dsp = num_font.render(str("est " + str(int(pathfinding.heuristic[xcord][ycord]*100)/100)), True, (0,0,0))
    # screen.blit(static_num_dsp, ((xcord+0.1)*cell_size, (ycord+0.15)*cell_size))

    # static_num_dsp = num_font.render(str("path " + str(int(pathfinding.dist_from_start[xcord][ycord]*100)/100)), True, (0,0,0))
    # # print("printing " + str((xcord, ycord)) + "  " + str(pathfinding.heuristic[xcord][ycord]))
    # screen.blit(static_num_dsp, ((xcord+0.1)*cell_size, (ycord+0.4)*cell_size))

    # static_num_dsp = num_font.render(str("tot " + str(int(pathfinding.heuristicSum[xcord][ycord]*100)/100)), True, (0,0,0))
    # # print("printing " + str((xcord, ycord)) + "  " + str(pathfinding.heuristic[xcord][ycord]))
    # screen.blit(static_num_dsp, ((xcord+0.1)*cell_size, (ycord+0.65)*cell_size))

def drawBoard():
    screen.fill((255,255,255))
    for r in range(ncells):
        
        for c in range(ncells):           
            #   PROBING
            if pathfinding.heuristicSum[r][c] != 999:
                drawCell(r,c, (15,210,185))              
            #   SEARCHED
            if (r,c) in pathfinding.explored:
                drawCell(r,c, (13,179,154)) 
            #   PROBE
            if (r,c) == pathfinding.probe:
                drawCell(r,c, (0,255,255))                    
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
        # wait()
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

def wait():
    print("--------")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print(pathfinding.heuristic)
                return
    

RUNNING = True
SELECTING = False
selectedCell = (-1,-1)

draw = True
wallMode = False
while RUNNING:    

    for event in pygame.event.get():
        #close game
        if event.type == pygame.QUIT:
            RUNNING = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if wallMode:
                    SELECTING = True
                    board_copy = np.copy(pathfinding.board)      
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
                    pathfinding.addOrigin(selectedCell)
                    print(pathfinding.origin)
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
                pathfinding.addDest(selectedCell)
            
        
        if event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1 and wallMode:
                SELECTING = False
                wallMode = False
                pathfinding.board = np.copy(board_copy)

                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                draw = False
                wallMode = True
            if event.key == pygame.K_SPACE:
                pathFind()
            if event.key == pygame.K_LSHIFT:
                wallMode = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                draw = True
                wallMode = False
            if event.key == pygame.K_LSHIFT:
                wallMode = False
        
            

    if SELECTING and wallMode:
        prev_selected_cell = selectedCell
        mouse_pos = pygame.mouse.get_pos()
        selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
        selectCell(prev_selected_cell, selectedCell, draw)
    
    drawBoard()  
    pygame.display.update()