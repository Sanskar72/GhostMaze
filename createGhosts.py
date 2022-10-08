# Import Packages and Functions
from generateEnvironment import genWorld
import numpy as np
import random 
from collections import deque

    
def createGhost(size):
    """_summary_
        Using Random numbers get the index values for the ghost
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated
        size (int, optional): Order of the square maze used . Defaults to 51.

    Returns:
        _type_: Int values for indices of the ghost
    """
    ghostX = random.randrange(3, 48)
    ghostY = random.randrange(3, 48)
    return ghostX, ghostY


def fillGridWithGhosts(grid, noOFGhosts, size):
    """_summary_
        Get X,Y index of the ghosts and store it in a list for the maze
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated

    Returns:
        _type_: list of indices of the ghosts
    """
    ghostGrid = []
    if grid.shape[0] == size:
        for i in range(noOFGhosts):
            x, y = createGhost(size)
            ghostGrid.append([x,y])
    else:
        ghostGrid.append("No World")
        
    return ghostGrid

def isGhostValid(a, b, size):
    """_summary_
        Checking for boundary conditions and overall validity
    Args:
        a (_type_): Integer index declaration
        b (_type_): Integer index declaration
        size (_type_): Order of the square matrix used for traversal.
        visited (_type_): A list to append the visited Locations of the maze
        grid (_type_): The different combinations of 51x51 square matrix/maze generated

    Returns: False based on the condition satisfaction of the degree of the maze & True if the location is visited or blocked
        _type_: Boolean
    """
    # If the cell lies out of bounds
    if (a < 0 or a > size-1) or (b < 0 or b > size-1):
        return False
    
    #Otherwise
    return True


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
    
   
    for i, pos in enumerate(ghostGrid):
        bound=[0,grid.shape[0]-1]
        x, y = pos[0], pos[1]


        # Probability that the Ghost is in the middle region of the maze
        if pos[0] not in bound and pos[1] not in bound:
            prob = random.randrange(100)
            #print("1",x, y, prob)

        # Computation for Ghost Movement when its in the upper corners or 1st row
        elif pos[0]==0:
            if pos[0]==0 and pos[1]==0:
                prob = random.randrange(51,100)
                #print("2",x, y, prob)
            elif pos[0]==0 and pos[1]==grid.shape[0]-1:
                range=random.choice([[0,25],[76,100]])
                prob= random.randrange(range[0],range[1])
                #print("3",x, y, prob)
            else:
                range=random.choice([[0,25],[51,100]])
                prob= random.randrange(range[0],range[1])
                #print("4",x, y, prob)


        # Computation for Ghost Movement when its in the bottom corners or last row
        elif pos[0]==grid.shape[0]-1:
            if pos[0]==grid.shape[0]-1 and pos[1]==0:
                prob=random.randrange(26,75)
                #print("5",x, y, prob)
            elif pos[0]==grid.shape[0]-1 and pos[1]==grid.shape[0]-1:
                prob=random.randrange(0,50)
                #print("6",x, y, prob)
            else:
                prob=random.randrange(75)
                #print("7",x, y, prob)

        # Computation for Ghost Movement when its in the left most column
        elif pos[1]==0:
            prob = random.randrange(26,100) 
            #print("8",x, y, prob)

        # Computation for Ghost Movement when its in the right most column
        elif pos[1]==grid.shape[0]-1:
            range=random.choice([[1,50],[76,100]])
            prob = random.randrange(range[0],range[1])
            #print("9",x, y, prob)

        # elif pos[0]==0 and pos[1]==0:
        #     prob = random.randrange(51,100)
        # elif pos[0]==0 and pos[1]==grid.shape-1:
        #     prob=random.choice([[1,25],[76,100]])
        # elif pos[0]==grid.shape() and pos[1]==0:
        #     prob=random.randrange(26,75)
        # elif pos[0]==grid.shape() and pos[1]==grid.shape():
        #     prob=random.randrange(1,50)
        #print('Prob:',prob)


        # Probability to move left
        if prob<25:
            if grid[x, y-1] == -1 and prob<13:
                continue
            ghostGrid[i] = [x, y-1]
           
        # Probability to move up
        elif prob<50:
            if grid[x-1, y] == -1 and prob<38:
                continue
            ghostGrid[i] = [x-1, y]
            
        # Probability to move right
        elif prob<75:
            if grid[x, y+1] == -1 and prob<63:
                continue
            ghostGrid[i] = [x, y+1]
        # Probability to move down
        else:
            if grid[x+1, y] == -1 and prob<88:
                continue
            ghostGrid[i] = [x+1, y]
       
    #update grid w prev prev position
    for key in prevPosition.keys():
        grid[key[0],key[1]] = prevPosition[key]
    
    #update new prev position
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

                
def initializer(noOfGhosts):
    """_summary_
        Driver code to call the functions to generate maze, ghosts, and save the previous location value of the ghost location
    """
    world, size = genWorld()
    grid = world[0]["grid"]

    # print('Before Adding GHosts:\n',grid)
    
    ghostGrid = fillGridWithGhosts(grid,  noOFGhosts =  noOfGhosts, size=size)
    prevPosition = saveWorld(grid, ghostGrid)
    for i in range(len(ghostGrid)):
        grid[ghostGrid[i][0], ghostGrid[i][1]] = -1
    '''
    for key in prevPosition.keys():
        print(grid[key[0],key[1]])
        print(prevPosition[key])
        print("=====================")
    '''
    # print(grid)
    # # print(ghostGrid)
    # grid, ghostGrid, NEWprevPosition = ghostMoves(grid, ghostGrid, prevPosition)
    '''
    # ===FOR TESTING PURPOSES ONLY===
    print("############################")
    for key in prevPosition.keys():
        print(grid[key[0],key[1]])
        print(prevPosition[key])
        print("=====================")
    '''
    # print(grid)
    # print(ghostGrid)
    return ghostGrid, grid, prevPosition, size


        
#DRIVER
#initializer()
    
    

