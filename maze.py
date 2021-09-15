import pygame
import math
from queue import PriorityQueue
import numpy as np


WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Runner")

#RGB Colors

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node class
# Node class represents a square on the grid
#

class Node():
    def __init__(self, row, col, width, total_rows):
        self.width = width
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.color = WHITE
        self.total_rows = total_rows
        self.prev = None
        self.visited = False
        self.g = np.inf
        self.f = np.inf


    def get_pos(self):
        return self.row,self.col

    def get_prev(self):
        return self.prev

    def get_visited(self):
        return self.visited

    def get_neighbors(self):
        return self.neighbors

    def visit(self):
        self.visited = True

    def unvisit(self):
        self.visited = False

    def add_neighbor(self,n):
        self.neighbors.append(n)

    def clear_neighbors(self):
        self.neighbors.clear()

    def set_parent(self,p):
        self.prev = p

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == YELLOW

    def is_empty(self):
        return self.color == WHITE

    def is_path(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_start(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def make_end(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        pass

    def __lt__(self, other):
        return False

# heuristic function for a star search
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2

    xDist = abs(x2 - x1)
    yDist = abs(y2 - y1)

    dist = xDist + yDist

    return dist

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i,j,gap,rows))

    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i * gap), (width,i * gap))

    for j in range(rows):
        pygame.draw.line(win,GREY,(j * gap,0), (j *gap,width ))

def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row, col

def in_bounds(x,y,rows):
    if x < 0 or x >= rows:
        return False
    if y < 0 or y >= rows:
        return False
    return True



# function to setup the neighbors array of each node
def initalize_search(rows,grid):
    # loop through each square in the grid
    for i in range(rows):
        for j in range(rows):
            current = grid[i][j]
            location = current.get_pos() #(y,x)
            if current.is_barrier(): # no need to fill neighbors for barriers
                continue
            else:
                # get the grid locations of each of its neighbors
                upper = (location[0] - 1, location[1])
                lower = (location[0] + 1, location[1])
                left = (location[0],location[1] - 1)
                right = (location[0],location[1] + 1)
                neighborhood = [upper,lower,left,right]
                # if the neighbor is in the grid and not a barrier add it to the current nodes neighbors list
                for neighbor in neighborhood:
                    if in_bounds(neighbor[1],neighbor[0],rows):
                        if(not grid[neighbor[0]][neighbor[1]].is_barrier()):
                            current.add_neighbor(grid[neighbor[0]][neighbor[1]])


# perform breadth first search on the maze
# if bfs returns true a path was found otherwise false is returned
def bfs(start,end,win,grid,rows,width):
    initalize_search(rows, grid)  # get all the neighbors set-up
    start.visit()
    q = [start]  # queue to do breadth first search with
    while len(q) > 0:
        curr = q.pop(0)
        if curr == end:
            return True
        elif curr == None:
            return False
        for neighbor in curr.get_neighbors():
            if (not neighbor.get_visited()):  # current neighbor has not been visited
                neighbor.visit()  # visit the neighbor
                neighbor.set_parent(curr)
                if (neighbor != end):
                    neighbor.make_closed()  # turn the node red
                q.append(neighbor)
        draw(win, grid, rows, width)

def aStar(start,end,win,grid,rows,width):
    initalize_search(rows,grid)
    start.g = 0
    start.f = h(start.get_pos(),end.get_pos())
    openSet = [start]
    closedSet = []

    while len(openSet) > 0:
         # Get the current node with the lowest f score
        current = openSet[0]
        current_index = 0
        for index, item in enumerate(openSet):
            if item.f < current.f:
                current = item
                current_index = index

        # Pop current off open list, add to closed list
        openSet.pop(current_index)
        closedSet.append(current)
        if current != start and current != end:
            current.make_closed()

        if current == end:
            return True

        for child in current.get_neighbors():
            if child in closedSet:
                continue

            child.g = current.g + 1
            child.f = child.g + h(child.get_pos(),end.get_pos())

            # Child is already in the open list
            if child in openSet:
                continue

            child.set_parent(current)
            openSet.append(child)
        draw(win, grid, rows, width)

    return False





# perform depth first search on the maze
# if dfs returns true a path was found otherwise false is returned
def dfs(start,end,win,grid,rows,width):
    initalize_search(rows, grid)  # get all the neighbors set-up
    start.visit()
    q = [start]  # queue to do breadth first search with
    while len(q) > 0:
        curr = q.pop(0)
        if curr == end:
            return True
        elif curr == None:
            return False
        for neighbor in curr.get_neighbors():
            if (not neighbor.get_visited()):  # current neighbor has not been visited
                neighbor.visit()  # visit the neighbor
                neighbor.set_parent(curr)
                if (neighbor != end):
                    neighbor.make_closed()  # turn the node red
                q.insert(0,neighbor)
        draw(win, grid, rows, width)

# traces a solution path after search algorithm has been executed
def trace_path(start,end,win,grid,rows,width):
    # now we retrace our path back to the start
    x = end.get_prev()
    while x != start:
        x.make_path()
        x = x.get_prev()
        draw(win, grid, rows, width)

# resets the grid after a search allowing the user to go back to editing it
def reset(grid,rows):
    for i in range(rows):
        for j in range(rows):
            curr = grid[i][j]
            curr.unvisit()
            curr.set_parent(None)
            curr.clear_neighbors()
            curr.g = np.inf
            curr.f = np.inf
            if curr.is_closed() or curr.is_path():
                curr.reset()


def main(win,width):
    ROWS = 20 # define the number of rows and columns for the grid
    grid = make_grid(ROWS,width)

    # start and end represent the start and goal of the maze
    start = None
    end = None

    run = True
    started = False



    while run:
        # each iteration we draw the grid
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user presses x button in the upper right corner
                run = False

            if started: # algorithm has been run
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # user presses c means clear the map and reset
                        # reset everything to default states
                        grid = make_grid(ROWS, width)

                        start = None
                        end = None

                        started = False
                    if event.key == pygame.K_r: # pressing r will undo the search and allow the user to modify the maze
                        reset(grid,ROWS)
                        started = False
                break

            if pygame.mouse.get_pressed()[0]: # left mouse click
                # collect the location of the mouse click and identify which square on the grid the user clicked
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]

                # don't allow user to place on top of existing placements
                if not spot.is_empty():
                    continue

                # if the start has not been placed the left click places the start
                if not start:
                    start = spot
                    spot.make_start()

                #if the goal has not been placed and the start has place the goal
                elif not end:
                    end = spot
                    spot.make_end()

                else:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # right mouse click
                # collect the location of the mouse click and identify which square on the grid the user clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                # user clears start position
                if spot == start:
                    spot.reset()
                    start = None

                # user clears goal
                elif spot == end:
                    spot.reset()
                    end = None

                elif spot.is_barrier():
                    spot.reset()

            elif event.type == pygame.KEYDOWN: # user presses a key
                if start and end:
                    started = True
                    pathFound = None
                    if event.key == pygame.K_b: # if the user presses the letter b
                        pathFound = bfs(start, end, win, grid, ROWS, width)
                    elif event.key == pygame.K_d: # if the user presses the letter b
                        pathFound = dfs(start, end, win, grid, ROWS, width)
                    elif event.key == pygame.K_a: # if the user presses the letter b
                        pathfound = aStar(start, end, win, grid, ROWS, width)
                    if pathfound:
                        trace_path(start,end,win,grid,ROWS,width)
                    else:
                        pass
    pygame.quit()

main(WIN,WIDTH)
