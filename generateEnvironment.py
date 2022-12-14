# Import the necessary libraries
import numpy as np
from collections import deque 
import time

# 51X51 Maze Size
size = 51
def generateMap(size):
    """_summary_
        Generate the size=51x51 block grid with 72% unblocked and 28% blocked cells
    Args:
        size (int, optional): Order of the square matrix to be made into a grid. Defaults to 51.

    Returns: StatusCode if grid was generated successfully along w the grid
        _type_: JSON
    """
    # Initialize a 51x51 maze with random numbers
    grid = np.random.randint(100, size = (size, size))
    for i1, col in enumerate(grid):
        for i2, cell in enumerate(col):
            # Set the block as unblocked for 72% blocks
            if cell<72:
                grid[i1,i2] = 0
            # For the rest 28% set the block as blocked
            else:
                grid[i1, i2] = -1
    # Set values for the root and Goal node separately
    grid[0,0], grid[-1,-1] = 0, 10
    return {"statusCode": 200, "grid": grid}

# Function to check if a cell is to be visited or not      
def isValid(a, b, size, visited, grid):
    """_summary_
        Checking for boundary conditions and overall validity
    Args:
        a (int): Integer index declaration
        b (int): Integer index declaration
        size (int): Order of the square matrix used for traversal.
        visited (list): A list to append the visited Locations of the maze
        grid (2D List): The different combinations of 51x51 square matrix/maze generated

    Returns: False based on the condition satisfaction of the degree of the maze & True if the location is visited or blocked
        _type_: Boolean
    """
    # If the cell lies out of bounds
    if (a < 0 or a > size-1) or (b < 0 or b > size-1):
        return False

    # If the cell is blocked
    if visited[a, b] or grid[a, b] == -1:
        return False
    
    #Otherwise
    return True

def DFS(grid, size = 51):
    """_summary_
        Performing Breadth First Search to reach to the goal block location
    Args:
        grid (2D List): The different combinations of 51x51 square matrix/maze generated
        size (int, optional): Order of the matrix/maze used. Defaults to 51.

    Returns: StatusCode if there is a successful way for the agent to reach its goal/ bottom-right node
        _type_: json
    """
    # Stores indices of the location of the maze cells
    visited = np.array([[False]*size]*size)
    childRow = [-1, 0, 1, 0]
    childCol = [0, 1, 0 ,-1]
    
    startQ = deque()
    path = deque()
    startX, startY = 0, 0
    
    # Mark the starting cell as visited and push it into the goal queue
    startQ.append([startX,startY])
    visited[startX, startY] = True
    #goalQ.append(grid[goalX, goalY])
    
    # Iterate while the queue is not empty
    while startQ:
        x1,y1 = startQ.pop()
        if grid[x1,y1] == 10:
            return {"statusCode":200}
        # Go to the adjacent blocks on the maze
        for i in range(4):
            childX = x1 + childRow[i]
            childY = y1 + childCol[i]
            if isValid(childX, childY, size, visited, grid):
                startQ.append([childX, childY])  
                visited[childX, childY] = True
                
    return {"statusCode": 400}



def genWorld():
    """_summary_
        Generate multiple combinations of 51x51 block maze and verify if there is a possible route to reach the goal node for the agent  
    Returns:
        _type_: List of 2-D Arrays
    """
    world = list()
    noOfGrids = 7
    for i in range(noOfGrids):
        temp = {}
        grid = generateMap(size=size)["grid"]
        if DFS(grid, size=size)["statusCode"] == 200:
            temp["grid"] = grid
            temp["BFS"] = DFS(grid, size=size)
            world.append(temp)
    return world, size


