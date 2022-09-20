from createGhosts import saveWorld, ghostMoves, initializer
from collections import deque
import numpy as np

def planBFS(grid, startX, startY, size = 51):
    """_summary_
        Performing Breadth First Search to reach to the goal block location
    Args:
        grid (_type_): The different combinations of 51x51 square matrix/maze generated
        size (int, optional): Order of the matrix/maze used. Defaults to 51.

    Returns: StatusCode if there is a successful way for the agent to reach its goal/ bottom-right node
        _type_: json
    """
    # Stores indices of the location of the maze cells
    visited = np.array([[False]*size]*size)
    childRow = [-1, 0, 1, 0]
    childCol = [0, 1, 0 ,-1]
    
    startQ = deque()
    path = list()
    
    # Mark the starting cell as visited and push it into the goal queue
    startQ.append([startX,startY])
    visited[startX, startY] = True
    #goalQ.append(grid[goalX, goalY])
    
    # Iterate while the queue is not empty
    while startQ:
        x1,y1 = startQ.popleft()
        path.append([x1,y1])
        if grid[x1,y1] == 10:
            return {"statusCode":200, "path":path}
        # Go to the adjacent blocks on the maze
        for i in range(4):
            childX = x1 + childRow[i]
            childY = y1 + childCol[i]
            if isValid(childX, childY, size, visited, grid):
                startQ.append([childX, childY])  
                visited[childX, childY] = True
                
    return {"statusCode": 400, "path":path}

# Function to check if a cell is to be visited or not      
def isValid(a, b, size, visited, grid):
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

    # If the cell is already visited
    if visited[a, b] or grid[a, b] == -1:
        return False
    
    #Otherwise
    return True

def executeBFS(grid, size, ghostGrid, prevPosition):
    # Stores indices of the location of the maze cells
    #visited = np.array([[False]*size]*size)
    #childRow = [-1, 0, 1, 0]
    #childCol = [0, 1, 0 ,-1]
    
    #goalQ.append(grid[goalX, goalY])
    startX, startY = 0, 0
    dictBFS = planBFS(grid, startX, startY, size = size)
    statusCode, path = dictBFS.get("statusCode"), dictBFS.get("path")
    pos = path[0]
    x1, y1 = pos[0], pos[1]
    finalPath = list()

    # Iterate while the queue is not empty
    while [x1,y1] not in ghostGrid:
        print(grid)
        if grid[x1,y1] == 10:
            return {"statusCode":200, "path":finalPath}
        
        #BFS PLAN
        dictBFS = planBFS(grid, x1, y1, size = size)
        statusCode, path = dictBFS.get("statusCode"), dictBFS.get("path")
        

        #AGENT MOVE
        if statusCode == 200:
            pos = path[1]
            x1, y1 = pos[0], pos[1]
            finalPath.append([x1,y1])
            
        elif statusCode == 400: #MOVE AGENT AWAY FROM CLOSEST GHOST
            finalPath.append([x1,y1])
            
        #GHOST MOVE
        grid, ghostGrid, prevPosition = ghostMoves(grid, ghostGrid, prevPosition)
        print("agent: ",x1,y1)
        print("ghost: ",ghostGrid)
        print("=============================")
        
        
    return {"statusCode":400, "path":finalPath}

def agent2init():
    ghostGrid, grid, prevPosition, size = initializer()
    print(executeBFS(grid, size, ghostGrid, prevPosition))

agent2init()






