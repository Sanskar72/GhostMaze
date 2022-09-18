from generateEnvironment import genWorld
import numpy as np
import random 
from collections import deque

    
def createGhost(grid, size = 51):
    ghostX = random.randrange(1, 50)
    ghostY = random.randrange(1, 50)
    return ghostX, ghostY


def fillGridWithGhosts(grid):
    ghostGrid = []
    noOFGhosts = 10
    if grid.shape[0] == 51:
        for i in range(noOFGhosts):
            x, y = createGhost(grid)
            ghostGrid.append([x,y])
    else:
        ghostGrid.append("No World")
        
    return ghostGrid

def ghostMoves(grid, ghostPosition):
    
    prob = random.randrange(100)
    if prob<25:
        
        pass

def saveWorld(grid, ghostGrid):
    prevPosition = {}
    for x,y in ghostGrid:
        prevPosition[(x,y)] = grid[x,y]
    return prevPosition
                

grid = genWorld()[0]["grid"]
ghostGrid = fillGridWithGhosts(grid)
prevPosition = saveWorld(grid, ghostGrid)
for i in range(len(ghostGrid)):
    grid[ghostGrid[i]] = -1
    
''' ===FOR TESTING PURPOSES ONLY===
for key in prevPosition.keys():
    print(grid[key[0],key[1]])
    print(prevPosition[key])
    print("=====================")
'''