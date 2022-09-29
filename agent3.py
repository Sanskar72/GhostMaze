from distutils.command.clean import clean
from createGhosts import ghostMoves, initializer, saveWorld
from collections import deque
import numpy as np
import time

def cleanPath(path):
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
    if grid[a, b] == -1:
        return False
    
    #Otherwise
    return True

def measureDist(x1, y1, grid, ghostGrid, size):
    #print("IN DIST VALA FN")
    dir = list()
    dist = list()
    for ghost in ghostGrid:
        dir.append([ghost[0]-x1, ghost[1]-y1])
        dist.append(np.sqrt((ghost[0]-x1)**2 + (ghost[1]-y1)**2))
        
    ind = np.argmin(dist)
    #print("dist", dist)
    #print("dir", dir)
    pos = dir[ind]
    if np.abs(pos[0])<=np.abs(pos[1]):
        if pos[0]>0 and isValid(x1-1, y1, size, grid):
            x1 -= 1
        elif isValid(x1+1, y1, size, grid):
            x1 += 1
    if np.abs(pos[0])>np.abs(pos[1]):
        if pos[1]>0 and isValid(x1, y1-1, size, grid):
            y1 -= 1
        elif isValid(x1, y1+1, size, grid):
            y1 += 1
            
        
    
    return x1, y1

def getClosestGhost(x1, y1, ghostGrid):
    dist = list()
    for ghost in ghostGrid:
        dist.append(np.sqrt((ghost[0]-x1)**2 + (ghost[1]-y1)**2))

    return np.argmin(dist)


def planBFS(grid, i, j, visited, size):
    # Initially starting at (0, 0).
    s=[]
    
    temp = {
        "x":i,
        "y":j,
        "dirn":0
    }    
    s.append(temp)
    while s:
        
        # Pop the top node and move to the
        # left, right, top, down or retract
        # back according the value of node's
        # dirn variable.
        temp = s.pop()
        d = temp["dirn"]
        i = temp["x"]; j = temp["y"]
        # Increment the direction and
        # push the node in the stack again.
        temp["dirn"] += 1
        s.append(temp)
        # If we reach the Food coordinates
        # return true
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
        # If none of the direction can take
        # the rat to the Food, retract back
        # to the path where the rat came from.
        else:
            visited[temp["x"]][temp["y"]] = True
            s.pop()
    # If the stack is empty and
    # no path is found return false.
    return {"statusCode":400, "path":s}

def executeBFS(grid, size, ghostGrid, prevPosition):
    x1, y1 = 0, 0
    counter = 0
    finalPath = [[0,0]]
    while(counter<500 and [x1,y1] not in ghostGrid):
        if grid[x1,y1] == 10:
            return {"statusCode":200, "path":finalPath}

        #START SIMULATION
        maxVal = 1000000
        finalDict = {"pathLen": maxVal, "nextStep": [x1,y1]}
        visited=[[True]*size for _ in range(size)]
        if isValid(x1+1, y1, size, grid):#AGENT MOVES DOWN
            dictBFS = planBFS(grid, x1+1, y1, visited, size)
            if dictBFS["statusCode"] == 200:
                path = dictBFS["path"]
                path = cleanPath(path)
                #SIMULATE  CLOSEST GHOST MOVEMENT
                closestGhost = getClosestGhost(x1+1, y1, ghostGrid)
                ghostX, ghostY = ghostGrid[closestGhost][0], ghostGrid[closestGhost][1]
                if ghostX+1<size:#GHOST MOVE DOWN
                    prevGhostMovementVal = grid[ghostX+1][ghostY]
                    grid[ghostX+1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1+1, y1, visited, size)
                    grid[ghostX+1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1+1,y1]

                if ghostX-1>=0:#GHOST MOVE UP
                    prevGhostMovementVal = grid[ghostX-1][ghostY]
                    grid[ghostX-1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1+1, y1, visited, size)
                    grid[ghostX-1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1+1,y1]

                if ghostY+1<size:#GHOST MOVE RIGHT
                    prevGhostMovementVal = grid[ghostX][ghostY+1]
                    grid[ghostX][ghostY+1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1+1, y1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1+1,y1]

                if ghostY-1>=0:#GHOST MOVE LEFT
                    prevGhostMovementVal = grid[ghostX][ghostY-1]
                    grid[ghostX][ghostY-1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1+1, y1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1+1,y1]

        elif isValid(x1, y1+1, size, grid):#AGENT MOVES RIGHT
            dictBFS = planBFS(grid, x1, y1+1, visited, size)
            if dictBFS["statusCode"] == 200:
                path = dictBFS["path"]
                path = cleanPath(path)
                #SIMULATE  CLOSEST GHOST MOVEMENT
                closestGhost = getClosestGhost(x1, y1+1, ghostGrid)
                ghostX, ghostY = ghostGrid[closestGhost][0], ghostGrid[closestGhost][1]
                if ghostX+1<size:#GHOST MOVE DOWN
                    prevGhostMovementVal = grid[ghostX+1][ghostY]
                    grid[ghostX+1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1+1, visited, size)
                    grid[ghostX+1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1+1]

                if ghostX-1>=0:#GHOST MOVE UP
                    prevGhostMovementVal = grid[ghostX-1][ghostY]
                    grid[ghostX-1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1+1, visited, size)
                    grid[ghostX-1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1+1]

                if ghostY+1<size:#GHOST MOVE RIGHT
                    prevGhostMovementVal = grid[ghostX][ghostY+1]
                    grid[ghostX][ghostY+1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1+1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1+1]

                if ghostY-1>=0:#GHOST MOVE LEFT
                    prevGhostMovementVal = grid[ghostX][ghostY-1]
                    grid[ghostX][ghostY-1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1+1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1+1]



        elif isValid(x1-1, y1, size, grid):#AGENT MOVES UP
            dictBFS = planBFS(grid, x1-1, y1, visited, size)
            if dictBFS["statusCode"] == 200:
                path = dictBFS["path"]
                path = cleanPath(path)
                #SIMULATE  CLOSEST GHOST MOVEMENT
                closestGhost = getClosestGhost(x1-1, y1, ghostGrid)
                ghostX, ghostY = ghostGrid[closestGhost][0], ghostGrid[closestGhost][1]
                if ghostX+1<size:#GHOST MOVE DOWN
                    prevGhostMovementVal = grid[ghostX+1][ghostY]
                    grid[ghostX+1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1-1, y1, visited, size)
                    grid[ghostX+1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1-1,y1]

                if ghostX-1>=0:#GHOST MOVE UP
                    prevGhostMovementVal = grid[ghostX-1][ghostY]
                    grid[ghostX-1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1-1, y1, visited, size)
                    grid[ghostX-1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1-1,y1]

                if ghostY+1<size:#GHOST MOVE RIGHT
                    prevGhostMovementVal = grid[ghostX][ghostY+1]
                    grid[ghostX][ghostY+1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1-1, y1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1-1,y1]

                if ghostY-1>=0:#GHOST MOVE LEFT
                    prevGhostMovementVal = grid[ghostX][ghostY-1]
                    grid[ghostX][ghostY-1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1-1, y1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1-1,y1]



        elif isValid(x1, y1-1, size, grid):#AGENT MOVES LEFT
            dictBFS = planBFS(grid, x1, y1-1, visited, size)
            if dictBFS["statusCode"] == 200:
                path = dictBFS["path"]
                path = cleanPath(path)
                #SIMULATE  CLOSEST GHOST MOVEMENT
                closestGhost = getClosestGhost(x1, y1-1, ghostGrid)
                ghostX, ghostY = ghostGrid[closestGhost][0], ghostGrid[closestGhost][1]
                if ghostX+1<size:#GHOST MOVE DOWN
                    prevGhostMovementVal = grid[ghostX+1][ghostY]
                    grid[ghostX+1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1-1, visited, size)
                    grid[ghostX+1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1-1]

                if ghostX-1>=0:#GHOST MOVE UP
                    prevGhostMovementVal = grid[ghostX-1][ghostY]
                    grid[ghostX-1][ghostY] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1-1, visited, size)
                    grid[ghostX-1][ghostY] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1-1]

                if ghostY+1<size:#GHOST MOVE RIGHT
                    prevGhostMovementVal = grid[ghostX][ghostY+1]
                    grid[ghostX][ghostY+1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1-1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1-1]

                if ghostY-1>=0:#GHOST MOVE LEFT
                    prevGhostMovementVal = grid[ghostX][ghostY-1]
                    grid[ghostX][ghostY-1] = -1
                    visited=[[True]*size for _ in range(size)]
                    dictBFS = planBFS(grid, x1, y1-1, visited, size)
                    grid[ghostX][ghostY-1] = prevGhostMovementVal
                    if dictBFS["statusCode"] == 200 and len(path)<finalDict["pathLen"]:
                        finalDict["pathLen"], finalDict["nextStep"] = len(path), [x1,y1-1]


        x1, y1 = finalDict["nextStep"][0], finalDict["nextStep"][1]
        finalPath.append([x1,y1])

        #MOVE GHOSTS
        grid, ghostGrid, prevPosition = ghostMoves(grid, ghostGrid, prevPosition)
        counter += 1

        print("===================================")
        print("counter:",counter)
        print("Ghost: ", ghostGrid)
        print("Agent: ", x1,y1)

    print("===================================")
    print("counter:",counter)
    print("Ghost: ", ghostGrid)
    print("Agent: ", x1,y1)
    return {"statusCode":400, "path":finalPath}


def agent3init():
    ghostGrid, grid, prevPosition, size = initializer(noOfGhosts=1)
    OGgrid = grid
    agent3_data = executeBFS(grid, size, ghostGrid, prevPosition)
    agent3_data["steps"] = len(agent3_data["path"])
    print("Final grid: \n",grid)
    print("OG grid: \n",OGgrid)
    print("SC: ",agent3_data["statusCode"], "STEPS: ", agent3_data["steps"])
    
for i in range(1):
    tic = time.perf_counter()
    agent3init()
    print("=======================================================")
    toc = time.perf_counter()
    print("time: ",toc-tic)
    print("=======================================================")






