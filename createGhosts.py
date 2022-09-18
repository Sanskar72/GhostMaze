from generateEnvironment import genWorld
import numpy as np
import random 
from collections import deque

    
def createGhost(grid, size = 51):
    """_summary_

    Args:
        grid (_type_): _description_
        size (int, optional): _description_. Defaults to 51.

    Returns:
        _type_: _description_
    """
    ghostX = random.randrange(1, 50)
    ghostY = random.randrange(1, 50)
    return ghostX, ghostY


def fillGridWithGhosts(grid):
    """_summary_

    Args:
        grid (_type_): _description_

    Returns:
        _type_: _description_
    """
    ghostGrid = []
    noOFGhosts = 10
    if grid.shape[0] == 51:
        for i in range(noOFGhosts):
            x, y = createGhost(grid)
            ghostGrid.append([x,y])
    else:
        ghostGrid.append("No World")
        
    return ghostGrid

def ghostMoves(grid, ghostGrid, prevPosition):
    """_summary_

    Args:
        grid (_type_): _description_
        ghostGrid (_type_): _description_
        prevPosition (_type_): _description_

    Returns:
        _type_: _description_
    """
    prob = random.randrange(100)
    for i, pos in enumerate(ghostGrid):
        x, y = pos[0], pos[1]
        if prob<25:
            if grid[x,y] == -1 and prob<13:
                continue
            ghostGrid[i] = [x-1, y]
            #left
        elif prob<50:
            if grid[x,y] == -1 and prob<38:
                continue
            ghostGrid[i] = [x, y-1]
            #up
        elif prob<75:
            if grid[x,y] == -1 and prob<63:
                continue
            ghostGrid[i] = [x+1, y]
            #right
        else:
            if grid[x,y] == -1 and prob<88:
                continue
            ghostGrid[i] = [x, y+1]
            #down
    #update grid w prev prev position
    for key in prevPosition.keys():
        grid[key[0],key[1]] = prevPosition[key]
    
    #update new prev prosition
    NEWprevPosition = saveWorld(grid, ghostGrid)
    
    #update grid w ghost pos = -1
    for x,y in ghostGrid:
        grid[x,y] = -1
        
    return grid, ghostGrid, NEWprevPosition
            

def saveWorld(grid, ghostGrid):
    """_summary_

    Args:
        grid (_type_): _description_
        ghostGrid (_type_): _description_

    Returns:
        _type_: _description_
    """
    prevPosition = {}
    for x,y in ghostGrid:
        prevPosition[(x,y)] = grid[x,y]
    return prevPosition
                
def initialiser():
    """_summary_
    """
    grid = genWorld()[0]["grid"]
    ghostGrid = fillGridWithGhosts(grid)
    prevPosition = saveWorld(grid, ghostGrid)
    for i in range(len(ghostGrid)):
        grid[ghostGrid[i]] = -1
    '''
    for key in prevPosition.keys():
        print(grid[key[0],key[1]])
        print(prevPosition[key])
        print("=====================")
    '''
    grid, ghostGrid, NEWprevPosition = ghostMoves(grid, ghostGrid, prevPosition)
    '''
    # ===FOR TESTING PURPOSES ONLY===
    print("############################")
    for key in prevPosition.keys():
        print(grid[key[0],key[1]])
        print(prevPosition[key])
        print("=====================")
    '''
        
#DRIVER
initialiser()
    
    

