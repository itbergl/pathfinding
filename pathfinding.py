import math
import numpy as np
import sys

class pathfinding:

    # data structures
    dist_from_goal = []
    dist_from_start = []
    heuristic = []
    board = []
    explored = []
    inprogress = []
    node_from = []

    # nodes
    probe = (-1,-1)
    dest = (-1,-1)
    origin = (-1,-1)

    def __init__(self, ncells, dest, origin):
        self.dest = dest
        self.origin = origin
        self.probe = origin
    
        for r in range(ncells+1):
            bool = []
            integer = []
            infinity = []  
            node = []
            for c in range(ncells+1):
                bool.append(True)   
                integer.append(0)
                infinity.append(sys.maxsize)
                node.append((-1,-1))    
            self.board.append(bool)
            self.dist_from_goal.append(integer)
            self.dist_from_start.append(integer)
            self.heuristic.append(infinity)      
            self.node_from.append(node)    
    
    def selectPromising(self):
        MIN = sys.maxsize
        best = self.origin
        for (r,c) in self.inprogress:
            
            if self.heuristic[r][c] < MIN:
                MIN = self.heuristic[r][c]
                best = (r,c)
        self.probe = best
        return best
    
    def updateNeighbours(self):
        direcitons = [(-1,0), (1,0), (0,-1), (0, 1)]

        nodex = self.probe[0]
        nodey = self.probe[1]

        destx = self.dest[0]
        desty = self.dest[1]

        for (v,h) in direcitons:          
            self.dist_from_goal[v+nodex][h+nodey] = math.hypot(nodex+v-destx, nodey+h-desty)
            dist_to = self.dist_from_start[nodex][nodey] + 1
            potential = dist_to + self.dist_from_goal[v+nodex][h+nodey]

            if  (v+nodex, h+nodey) not in self.explored and potential < self.heuristic[v+nodex][h+nodey] and self.board[v+nodex][h+nodey]:
                self.heuristic[v+nodex][h+nodey] = potential
                self.dist_from_start[v+nodex][h+nodey] = self.dist_from_start[nodex][nodey] + 1
                self.node_from[v+nodex][h+nodey] = self.probe
                self.inprogress.append((v+nodex, h+nodey))


        self.explored.append(self.probe)

        index = 0
        for (x,y) in self.inprogress:                
            if x == self.probe[0] and y == self.probe[1]:
                self.inprogress.pop(index)

            index += 1   
        

    def nextStep(self):
        if self.dest not in self.inprogress:
            
            self.selectPromising()

            self.updateNeighbours()
            return True
        
        return False
    
    def addOrigin(self, node):
        self.origin = node
        self.inprogress.append(node)

    def addToPath(self, list, node):
        prev_node = self.node_from[node[0]][node[1]]
        if prev_node != self.origin:
            list.append(prev_node)
        return prev_node

    

