import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Tile:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        self.neighbours = []
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self) -> bool:
        return self.color == RED
    
    def is_open(self) -> bool:
        return self.color == GREEN
    
    def is_barrier(self) -> bool:
        return self.color == BLACK
    
    def is_start(self) -> bool:
        return self.color == ORANGE
    
    def is_end(self) -> bool:
        return self.color == TURQUOISE
    
    def reset(self) -> None:
        self.color = WHITE
    
    def make_closed(self) -> None:
        self.color = RED
    
    def make_open(self) -> None:
        self.color = GREEN
    
    def make_barrier(self) -> None:
        self.color = BLACK

    def make_start(self) -> None:
        self.color = ORANGE
    
    def make_end(self) -> None:
        self.color = TURQUOISE
    
    def make_path(self) -> None:
        self.color = PURPLE
    
    def draw(self, win) -> None:
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, grid) -> None:
        self.neighbours = []
        
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
          self.neighbours.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])
        
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other) -> bool:
        return False

def a_star_pathfind(draw_grid, grid, start, end) -> bool:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {tile: float("inf") for row in grid for tile in row}
    g_score[start] = 0
    f_score = {tile: float("inf") for row in grid for tile in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw_grid)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        
        draw_grid()

        if current != start:
            current.make_closed()
    
    return False

def reconstruct_path(came_from, current, draw_grid):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_grid()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap, rows)
            grid[i].append(tile)
    
    return grid

def draw_grid_lines(win, rows, width) -> None:
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_grid(win, grid, rows, width) -> None:
    win.fill(WHITE)

    for row in grid:
        for tile in row:
            tile.draw(win)
            if tile.row == 0 or tile.row == tile.total_rows - 1 or tile.col == 0 or tile.col == tile.total_rows - 1:
                tile.make_barrier()
    
    draw_grid_lines(win, rows, width)
    pygame.display.update()

def get_clicked_position(mouse_pos, rows, width):
    gap = width // rows
    y, x = mouse_pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width) -> None:
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw_grid(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # LEFT MOUSE BUTTON
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                tile = grid[row][col]

                if not start and tile != end:
                    start = tile
                    start.make_start()
                
                elif not end and tile != start:
                    end = tile
                    tile.make_end()
                
                elif tile != end and tile != start:
                    tile.make_barrier()

            # RIGHT MOUSE BUTTON
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                tile = grid[row][col]
                tile.reset()

                if tile == start:
                    start = None
                
                elif tile == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for tile in row:
                            tile.update_neighbours(grid)
                    
                    a_star_pathfind(lambda: draw_grid(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    
    pygame.quit()

main(WIN, WIDTH)