import numpy as np
from collections import deque 

size = 51
def generateMap(size = 51):
    """_summary_

    Args:
        size (int, optional): side of the square matrix to be made into a grid. Defaults to 51.

    Returns: statusCode if grid was generated sucessfully along w the grid
        _type_: JSON
    """
    grid = np.random.randint(100, size = (size, size))
    for i1, col in enumerate(grid):
        for i2, cell in enumerate(col):
            if cell<72:
                grid[i1,i2] = 0
            else:
                grid[i1, i2] = -1
    grid[0,0], grid[-1,-1] = 0, 10
    return {"statusCode": 200, "grid": grid}
        
def isValid(a, b, size, visited, grid):
    """_summary_

    Args:
        a (_type_): _description_
        b (_type_): _description_
        size (_type_): _description_
        visited (_type_): _description_
        grid (_type_): _description_

    Returns:
        _type_: _description_
    """
    if (a < 0 or a > size-1) or (b < 0 or b > size-1):
        return False
    
    if visited[a, b] or grid[a, b] == -1:
        return False
    
    return True

def BFS(grid, size = 51):
    """_summary_

    Args:
        grid (_type_): _description_
        size (int, optional): _description_. Defaults to 51.

    Returns:
        _type_: _description_
    """
    visited = np.array([[False]*size]*size)
    childRow = [-1, 0, 1, 0]
    childCol = [0, 1, 0 ,-1]
    
    startQ = deque()
    path = deque()
    startX, startY = 0, 0
    goalX, goalY = size - 1, size - 1
    
    startQ.append([startX,startY])
    visited[startX, startY] = True
    #goalQ.append(grid[goalX, goalY])
    
    while startQ:
        x1,y1 = startQ.popleft()
        path.append([x1,y1])
        if grid[x1,y1] == 10:
            return {"statusCode":200, "path":path}
        for i in range(4):
            childX = x1 + childRow[i]
            childY = y1 + childCol[i]
            if isValid(childX, childY, size, visited, grid):
                startQ.append([childX, childY])  
                visited[childX, childY] = True
                
    return {"statusCode": 400, "path":"route DNE"}

def isMapValid(grid):
    """_summary_

    Args:
        grid (_type_): _description_

    Returns:
        _type_: _description_
    """
    if BFS(grid)["statusCode"] == 200:
        return True
    elif BFS(grid)["statusCode"] == 400:
        return False

def checkWorlds():
    """_summary_
    """
    world = list()        
    for i in range(10):
        grid = generateMap()["grid"]
        world.append(grid)
        print(world[-1], grid.shape)
        print(BFS(world[-1])["statusCode"])
        
#checkWorlds()
    

