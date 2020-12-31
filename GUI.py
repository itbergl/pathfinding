from numpy.lib.function_base import select
import pygame
from pygame.mixer import pause
import os
import numpy as np
import time

#hide default pygame message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()

#Screen
cell_size = 10
ncells = 100
line_colour = (200,200,200)
screen = pygame.display.set_mode((ncells*cell_size,ncells*cell_size))

#board
board = []
for r in range(ncells):
    row = []
    for c in range(ncells):
        row.append(True)
    board.append(row)

def drawCell(xcord, ycord, colour):
    #print box
    square = pygame.Rect((xcord*cell_size, ycord*cell_size, cell_size, cell_size)) 
    pygame.draw.rect(screen,colour,square)

def drawBoard(b):
    screen.fill((255,255,255))
    for r in range(ncells):
        
        for c in range(ncells): 
            if b[r][c]:
                colour = (255,255,255) 
            else:
                colour = (0,0,0) 
            drawCell(r,c, colour)

    for r in range(100):
        pygame.draw.line(screen,line_colour,(r*cell_size, 0), (r*cell_size, ncells*cell_size),1)
    for c in range(100):      
        pygame.draw.line(screen,line_colour,(0, c*cell_size), (ncells*cell_size, c*cell_size),1)

def selectCell(pos, fakeboard, draw):
    xpos = pos[0]
    ypos = pos[1]

    if board[xpos][ypos] == draw:
        fakeboard[xpos][ypos] = not draw

RUNNING = True
SELECTING = False
selectedCell = (-1,-1)
board_copy = np.copy(board)
draw = True
while RUNNING:
    

    for event in pygame.event.get():
        #close game
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1:
                SELECTING = False
                board = board_copy
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                SELECTING = True
                board_copy = np.copy(board)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                draw = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                draw = True
            

    if SELECTING:
        mouse_pos = pygame.mouse.get_pos()
        selected_cell = (int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
        selectCell(selected_cell, board_copy, draw)
    
    drawBoard(board_copy)
   
    
    

        
    pygame.display.update()