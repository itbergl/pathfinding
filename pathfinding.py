import math
import numpy as np
import sys

class pathfinding:

    # data structures
    heuristic = []
    dist_from_start = []
    heuristicSum = []
    board = []
    explored = []
    inprogress = []
    node_from = []

    # nodes
    probe = (-1,-1)
    dest = (-1,-1)
    origin = (-1,-1)

    ncells = 0

    # const
    sqrt2 = math.sqrt(2)

    def __init__(self, ncells):
        self.ncells = ncells
        for r in range(ncells+1):
            bool = []
            integer1 = []
            integer2 = []
            infinity = []  
            node = []
            for c in range(ncells+1):
                if c%2 == 0:
                    bool.append(True)   
                else:
                    bool.append(False)
                integer1.append(0)
                integer2.append(0)
                infinity.append(999)
                node.append((-1,-1))
                 
            self.board.append(bool)
            self.heuristic.append(integer1)
            self.dist_from_start.append(integer2)
            self.heuristicSum.append(infinity)      
            self.node_from.append(node) 


    
    def selectPromising(self):
        MIN = sys.maxsize
        best = self.origin
        for (x,y) in self.inprogress:           
            if self.heuristicSum[x][y] < MIN:
                MIN = self.heuristicSum[x][y]
                best = (x,y)
        self.probe = best
        return best
    
    def getNeighbours(self, node):
        direcitons = []

        for i in range (-1,2):
            for j in range (-1,2):
                if i!=0 or j!=0:
                    direcitons.append((i,j))

        ret = []
        
        nodex = node[0]
        nodey = node[1]

        for (x,y) in direcitons:
            expx = nodex + x
            expy = nodey + y

            inboard = expx in range(0, self.ncells) and expy in range(0, self.ncells)

            noWall = True
            if x != 0 and y != 0:
                if not self.board[expx][nodey] and not self.board[nodex][expy]:
                    noWall = False
            
            if inboard and noWall and self.board[expx][expy]:
                ret.append((expx,expy))
        return ret
            
            
    
    def updateNeighbours(self):

        neighbours = self.getNeighbours(self.probe)

        nodex = self.probe[0]
        nodey = self.probe[1]

        destx = self.dest[0]
        desty = self.dest[1]

        for (x,y) in neighbours:          
            if (x, y) not in self.explored:             
                step = 1
                if x != nodex and y != nodey:
                    step = self.sqrt2

                if (x, y) not in self.inprogress:
                    self.inprogress.append((x, y))  
                    self.node_from[x][y] = self.probe
    
                    self.heuristic[x][y] = math.hypot(x-destx, y-desty)
                    
                    # print(math.hypot(expx-destx, expy-desty))
                    # print(str((expx, expy)) + "-> " + str(self.heuristic[expx][expy]))
                    self.dist_from_start[x][y] = float(self.dist_from_start[nodex][nodey]) + float(step)
                    self.heuristicSum[x][y] = float(self.heuristic[x][y]) + float(self.dist_from_start[x][y])
                else:
                    estimate = float(self.dist_from_start[nodex][nodey]) + float(step) + float(self.heuristic[x][y])
                    if self.heuristicSum[x][y] > estimate:
                        self.heuristicSum[x][y] = float(estimate)
                        self.dist_from_start[x][y] = float(self.dist_from_start[nodex][nodey]) + float(step)
                        self.node_from[x][y] = self.probe

        self.explored.append(self.probe)

        index = 0
        for (x,y) in self.inprogress:                
            if x == self.probe[0] and y == self.probe[1]:
                self.inprogress.pop(index)
            index += 1   
    
    def reset(self, fullreset):

        self.heuristic = []
        self.dist_from_start = []
        self.heuristicSum = []
        self.node_from = []
        self.explored = []
        self.probe = self.origin
        self.inprogress = []
        if fullreset:
            self.board = []
        for r in range(self.ncells+1):
            integer1 = []
            integer2 = []
            infinity = []  
            node = []
            bool = []
            for c in range(self.ncells+1):
                bool.append(True)
                integer1.append(0)
                integer2.append(0)
                infinity.append(999)
                node.append((-1,-1))                
            self.heuristic.append(integer1)
            self.dist_from_start.append(integer2)
            self.heuristicSum.append(infinity)      
            self.node_from.append(node) 
            if fullreset:
                self.board.append(bool)
    


    def nextStep(self):
        
        if self.probe != self.dest:
            
            self.selectPromising()
            self.updateNeighbours()
            return True
        return False
        
    def getFinalPath(self):
        n = self.dest
        list = []
        while n != (self.origin):
            list.append(n)
            n = self.node_from[n[0]][n[1]]
        return list



    def addOrigin(self, node):
        self.origin = node
        self.probe = node
        self.inprogress = []
        self.inprogress.append(node)
    
    def addDest(self, node):
        self.dest = node
        # self.dest_nodes = self.getNeighbours(self.dest)

    def addToPath(self, list, node):
        prev_node = self.node_from[node[0]][node[1]]
        if prev_node != self.origin:
            list.append(prev_node)
        return prev_node

    

