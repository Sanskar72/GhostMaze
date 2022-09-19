from generateEnvironment import genWorld
import numpy as np
import random 
from collections import deque

    
def createGhost(grid, size = 51):
    """_summary_
        Using Random numbers get the index values for the ghost
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated
        size (int, optional): Order of the square maze used . Defaults to 51.

    Returns:
        _type_: Int values for indices of the ghost
    """
    ghostX = random.randrange(1, 50)
    ghostY = random.randrange(1, 50)
    return ghostX, ghostY


def fillGridWithGhosts(grid):
    """_summary_
        Get X,Y index of the ghosts and store it in a list for the maze
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated

    Returns:
        _type_: list of indices of the ghosts
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
        Function to track the movement of the ghosts
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated
        ghostGrid (_type_): _description_
        prevPosition (_type_): _description_

    Returns:
        _type_: _description_
    """
    prob = random.randrange(100)
    for i, pos in enumerate(ghostGrid):
        x, y = pos[0], pos[1]
        # Probability to move left
        if prob<25:
            if grid[x,y] == -1 and prob<13:
                continue
            ghostGrid[i] = [x-1, y]
           
        # Probability to move up
        elif prob<50:
            if grid[x,y] == -1 and prob<38:
                continue
            ghostGrid[i] = [x, y-1]
            
        # Probability to move right
        elif prob<75:
            if grid[x,y] == -1 and prob<63:
                continue
            ghostGrid[i] = [x+1, y]
        # Probability to move down
        else:
            if grid[x,y] == -1 and prob<88:
                continue
            ghostGrid[i] = [x, y+1]
       
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
        Function to save the maze values where the ghost is
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated
        ghostGrid (_type_): List of indices of the ghosts

    Returns:
        _type_: Dictionary of the location indices and the value at that location
    """
    prevPosition = {}
    for x,y in ghostGrid:
        prevPosition[(x,y)] = grid[x,y]
    return prevPosition
                
def initialiser():
    """_summary_
        Driver code to call the functions to generate maze, ghosts, and save the previous location value of the ghost location
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
    
    

