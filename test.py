from generateEnvironment import genWorld


N=5
M=5

class node:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.dirn=0
 
# maze of n*m matrix
n = N; m = M
 
# Coordinates of food
fx=0; fy=0
visited=[[True]*N for _ in range(M)]

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

def isReachable(maze):
    # Initially starting at (0, 0).
    i = 0; j = 0
    s=[]
    
    temp=node(i, j)
    
    s.append(temp)
    while s:
        
        # Pop the top node and move to the
        # left, right, top, down or retract
        # back according the value of node's
        # dirn variable.
        temp = s.pop()
        d = temp.dirn
        i = temp.x; j = temp.y
        # Increment the direction and
        # push the node in the stack again.
        temp.dirn+=1
        s.append(temp)
        # If we reach the Food coordinates
        # return true
        if (maze[i,j] == 10):
            return s
        # Checking the Up direction.
        if (d == 0):
            if (isValid(i-1, j, size, grid) and visited[i - 1][j]):
                temp1=node(i - 1, j)
                visited[i - 1][j] = False
                s.append(temp1)
        # Checking the left direction
        elif (d == 1):
            if(isValid(i, j-1, size, grid) and visited[i][j - 1]):
                temp1=node(i, j - 1)
                visited[i][j - 1] = False
                s.append(temp1)
        # Checking the down direction
        elif (d == 2):
            if(isValid(i+1, j, size, grid) and visited[i + 1][j]):
                temp1=node(i + 1, j)
                visited[i + 1][j] = False
                s.append(temp1)
        # Checking the right direction
        elif (d == 3):
            if (isValid(i, j+1, size, grid) and visited[i][j + 1]):
                temp1=node(i, j + 1)
                visited[i][j + 1] = False
                s.append(temp1)
        # If none of the direction can take
        # the rat to the Food, retract back
        # to the path where the rat came from.
        else:
            visited[temp.x][temp.y] = True
            s.pop()
    # If the stack is empty and
    # no path is found return false.
    return s
# Driver code
if __name__ == '__main__':
    # Initially setting the visited
    # array to true (unvisited)
    world, size = genWorld()
    grid = world[0]['grid']
    print(grid)
    s = isReachable(grid)
    for item in s:
        print(item.x, item.y)
