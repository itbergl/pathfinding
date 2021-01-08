#CUMS
from os import path
from typing import Final
from numpy.lib.function_base import select
import pygame
import time
from pygame.mixer import pause
import os
import numpy as np
import time
from pathfinding import pathfinding as pf
import sys

#hide default pygame message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()
start = 0
end = 0

#Icon
pygame.display.set_caption("Path Finder")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

#Screen

ncells = 50
cell_size = int(1000/ncells)

line_colour = (255,255,255)
screen = pygame.display.set_mode((ncells*cell_size,ncells*cell_size))
# screen.set_alpha(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])

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
    
    screen.fill((220,220,220))
    for r in range(ncells):
        
        for c in range(ncells):  
            #   WALL 
            if not board_copy[r][c]:
                drawCell(r,c, (75,75,75)) 
            #   START
            elif (r,c)==pathfinding.origin:
                drawCell(r,c, (102,102,255))   
            #   DESTINATION
            elif (r,c)==pathfinding.dest:
                drawCell(r,c, (255,153,153))
            #   FINAL PATH
            # elif (r,c) in final_path:
            #     drawCell(r,c, (0,255,0)) 
            #   PROBE
            # if (r,c) == pathfinding.probe:
            #     drawCell(r,c, (0,255,255))  
            #   SEARHCED
            elif pathfinding.heuristicSum[r][c] == -1:
                drawCell(r,c, (111,195,195))    
            #   PROBING
            elif pathfinding.heuristicSum[r][c] != sys.maxsize:
                drawCell(r,c, (130,222,222))              

    if len(final_path) > 2:
        pygame.draw.lines(screen, (100,255,0), False, final_path, 4)       

    for r in range(ncells):
        pygame.draw.line(screen,line_colour,(r*cell_size, 0), (r*cell_size, ncells*cell_size),1)
    for c in range(ncells):      
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
    global final_path
    global start
    global end
    ONCE = True
    start = time.time()

    while RUNNING and SIMULATING:
        # wait()

        if not pathfinding.nextStep() and ONCE:
                ONCE = False
                end = time.time()
                tracePath()

        for event in pygame.event.get():
            #close game
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    final_path = []
                    pathfinding.reset(False)
                    SIMULATING = False
        drawBoard()                
        pygame.display.update()

def tracePath():
    global RUNNING
    TRACING = True
    global final_path

    final_path_full = pathfinding.getFinalPath()
    index = len(final_path_full)-1
    while RUNNING and TRACING:
        # wait()
        for event in pygame.event.get():
            #close game
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    final_path = []
                    pathfinding.reset(False)
                    TRACING = False
        if index > -1:
            node_to_add = final_path_full[index]
            final_path.append(((node_to_add[0]+0.5)*cell_size, (node_to_add[1]+0.5)*cell_size))

            index -= 1

            drawBoard()                
            pygame.display.update()
        else: 
            print("Time taken: " + str(int(1000*(end - start))) + " ms")
            endx = pathfinding.dest[0]
            endy = pathfinding.dest[1]
            print("Path Length: " + str(round(pathfinding.dist_from_start[endx][endy],3)))
            TRACING = False

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                selectedCell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
                pathfinding.addDest(selectedCell)
            
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or pygame.mouse.get_focused() == 0 :               
                SELECTING = False
                # wallMode = False
                pathfinding.board = np.copy(board_copy)

                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                draw = False
                wallMode = True
            if event.key == pygame.K_SPACE:
                if pathfinding.origin != (-1,-1) and pathfinding.dest != (-1,-1):
                    wallMode = False
                    pathfinding.board = np.copy(board_copy)
                    pathFind()       
            if event.key == pygame.K_LSHIFT:
                wallMode = True
            if event.key == pygame.K_ESCAPE:
                final_path = []
                pathfinding.reset(True)
                board_copy = np.copy(pathfinding.board)
                
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