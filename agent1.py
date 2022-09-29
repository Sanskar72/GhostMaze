# Import all the packages and required Functions
from createGhosts import ghostMoves, initializer
from collections import deque
import numpy as np
import time

def cleanPath(path):
    """_summary_
        Calculate a cleaner and direct path removing the backtrack and loop iterations
    Args:
        path (_type_): The path followed by the agent to reach the goal

    Returns:
        _type_: A list with a cleaner and direct path removing the backtrack
    """
    q = deque()
    finalPath = list()
    flag = -1
    for ele in path:
        x,y = ele[0], ele[1]
        if [x,y] not in q:
            q.append([x,y])
        else:
            flag = 1
            while(q):
                popped = q.popleft()
                if popped == [x,y]:
                    q.clear()
                else:
                    finalPath.append([popped[0], popped[1]])
            finalPath.append([x,y])      
    if flag == -1:
        return path
    while q:
        popped = q.popleft()
        finalPath.append([popped[0], popped[1]])
                
    return finalPath


def isValid(a, b, size, grid):
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

    # If the cell is already visited
    if grid[a, b] == -1:
        return False
    
    #Otherwise
    return True

def measureDist(x1, y1, grid, ghostGrid, size):
    """_summary_
        Function measure the distance between the agent and the closest ghost to increase survivability
    Args:
        x1 (int): x index position of the agent on the maze
        y1 (int): y index position of the agent on the maze
        grid (2D List): The maze with blocked and unblocked cells along with the ghost spawns
        ghostGrid (2D List): Positions pf the ghosts in the maze
        size (int): Size of the maze

    Returns: Updated Co-ordinates using Distance from agent to the closest ghost.
        _type_: int 
    """
    dir = list()
    dist = list()
    for ghost in ghostGrid:
        # Manhattan Distance
        dir.append([ghost[0]-x1, ghost[1]-y1])
        # Euclidean Distance
        dist.append(np.sqrt((ghost[0]-x1)**2 + (ghost[1]-y1)**2))
        
    ind = np.argmin(dist)
    #print("dist", dist)
    #print("dir", dir)
    pos = dir[ind]

    # Compare Manhattan Distance to determine the direction to move to (Up or Down)
    if np.abs(pos[0])<=np.abs(pos[1]):
        if pos[0]>0 and isValid(x1-1, y1, size, grid):
            x1 -= 1
        elif isValid(x1+1, y1, size, grid):
            x1 += 1
    # Compare Manhattan Distance to determine the direction to move to (Left or Right)
    if np.abs(pos[0])>np.abs(pos[1]):
        if pos[1]>0 and isValid(x1, y1-1, size, grid):
            y1 -= 1
        elif isValid(x1, y1+1, size, grid):
            y1 += 1
            
    return x1, y1

def planBFS(grid, i, j, visited, size):
    """_summary_
        Run the BFS to find a path from agent to goal to plan if the survival is possible
    Args:
        grid (2D List): _description_The maze with blocked and unblocked cells along with the ghost spawns
        i (int): X coordinate
        j (int): Y coordinate
        visited (list): List of visited locations
        size (int): Size of the maze

    Returns:
        _type_: Json
    """
    # Initially starting at (0, 0).
    s=[]
    
    temp = {
        "x":i,
        "y":j,
        "dirn":0
    }    
    s.append(temp)
    while s:
        # Pop the top node and move to the left, right, top, down or retract back according the value of node's dirn variable.
        temp = s.pop()
        d = temp["dirn"]
        i = temp["x"]; j = temp["y"]
        # Increment the direction and push the node in the stack again.
        temp["dirn"] += 1
        s.append(temp)
        # If we reach the goal state return the final path
        if (grid[i,j] == 10):
            path = list()
            for dict in s:
                path.append([dict["x"],dict["y"]])
                
            return {"statusCode":200, "path":path}
        # Checking the Up direction.
        if (d == 0):
            if (isValid(i-1, j, size, grid) and visited[i - 1][j]):
                temp1={ "x":i-1,
                        "y":j,
                        "dirn":0}
                
                visited[i - 1][j] = False
                s.append(temp1)
        # Checking the left direction
        elif (d == 1):
            if(isValid(i, j-1, size, grid) and visited[i][j - 1]):
                temp1={ "x":i,
                        "y":j-1,
                        "dirn":0}
                visited[i][j - 1] = False
                s.append(temp1)
        # Checking the down direction
        elif (d == 2):
            if(isValid(i+1, j, size, grid) and visited[i + 1][j]):
                temp1={ "x":i+1,
                        "y":j,
                        "dirn":0}
                visited[i + 1][j] = False
                s.append(temp1)
        # Checking the right direction
        elif (d == 3):
            if (isValid(i, j+1, size, grid) and visited[i][j + 1]):
                temp1={ "x":i,
                        "y":j+1,
                        "dirn":0}
                visited[i][j + 1] = False
                s.append(temp1)
        # If none of the direction can take the agent to the goal, retract back to the last step.
        else:
            visited[temp["x"]][temp["y"]] = True
            s.pop()
    # If the stack is empty and no path is found return statusCode 400.
    return {"statusCode":400, "path":s}

def executeBFS(grid, size, ghostGrid, prevPosition):
    """_summary_
        Implement the path returned by the plan BFS Function
    Args:
        grid (2D List): _description_The maze with blocked and unblocked cells along with the ghost spawns
        size (int): Shape of the maze
        ghostGrid (list): list of ghost positions on the maze
        prevPosition (list): Stores the data of the cell being occupied by the ghost whether it is blocked or not

    Returns: The path followed by the agent towards the goal
        _type_: list
    """
    # Stores indices of the location of the maze cells
    #visited = np.array([[False]*size]*size)
    #childRow = [-1, 0, 1, 0]
    #childCol = [0, 1, 0 ,-1]
    
    #goalQ.append(grid[goalX, goalY])
    startX, startY = 0, 0
    visited=[[True]*size for _ in range(size)]
    dictBFS = planBFS(grid, startX, startY, visited, size = size)
    statusCode, path = dictBFS.get("statusCode"), dictBFS.get("path")
    path = cleanPath(path)
    if len(path)>0:
        pos = path[0]
        x1, y1 = pos[0], pos[1]
    else:
        x1, y1 = 0, 0
    route = 1
    counter = 0
    print(grid)

    # Iterate while the queue is not empty
    while [x1,y1] not in ghostGrid and counter<1200:
        if grid[x1,y1] == 10:
            return {"statusCode":200, "path":path}
        
        #AGENT MOVE
        if statusCode == 200:
            path = cleanPath(path)
            # for item in path:
            #     print(item["x"], item["y"])
            pos = path[route]
            x1, y1 = pos[0], pos[1]
            route += 1
        
        grid, ghostGrid, prevPosition = ghostMoves(grid, ghostGrid, prevPosition)
        counter += 1
        # if counter%30==0:
            # print("counter:",counter)
            # print("Ghost: ", ghostGrid)
            # print("Agent: ", x1,y1)
            # print("==================================")
    print("counter:",counter)
    print("Ghost: ", ghostGrid)
    print("Agent: ", x1,y1)
    return {"statusCode":400, "path":path}

def agent1init():
    """_summary_
        Initializer for the Agent1
    """
    ghostGrid, grid, prevPosition, size = initializer(noOfGhosts=1)
    agent1_data = executeBFS(grid, size, ghostGrid, prevPosition)
    agent1_data["steps"] = len(agent1_data["path"])
    print("SC: ",agent1_data["statusCode"], "STEPS: ", agent1_data["steps"])
    
for i in range(5):
    tic = time.perf_counter()
    agent1init()
    print("=======================================================")
    toc = time.perf_counter()
    print("time: ",toc-tic)
    print("=======================================================")
    







