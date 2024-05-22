import pygame, sys
from collections import deque

# Initialize pygame and constants
pygame.init()
size = (width, height) = 640, 480
win = pygame.display.set_mode(size)
pygame.display.set_caption("Enhanced Dijkstra Visualizer")
clock = pygame.time.Clock()
cols, rows = 32, 24
w = width // cols
h = height // rows
board = []
queue, visited = deque(), []
final = []

class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.neighbours = []
        self.prev = None
        self.wall = False
        self.visited = False
        self.f, self.g, self.h = 0, 0, 0

    def show(self, win, color, shape=1):
        if self.wall:
            color = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, color, (self.r * w, self.c * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, color, (self.r * w + w // 2, self.c * h + h // 2), w // 3)

    def add_neighbours(self, grid):
        if self.r < cols - 1: self.neighbours.append(grid[self.r + 1][self.c])
        if self.r > 0: self.neighbours.append(grid[self.r - 1][self.c])
        if self.c < rows - 1: self.neighbours.append(grid[self.r][self.c + 1])
        if self.c > 0: self.neighbours.append(grid[self.r][self.c - 1])

def create_grid():
    for i in range(cols):
        array = []
        for j in range(rows):
            array.append(Cell(i, j))
        board.append(array)
    for i in range(cols):
        for j in range(rows):
            board[i][j].add_neighbours(board)

def select_wall(pos, status):
    x, y = pos[0] // w, pos[1] // h
    board[x][y].wall = status

def display_instructions():
    font = pygame.font.SysFont("Arial", 18)
    instructions = [
        "Left Click: Add Wall",
        "Right Click: Remove Wall",
        "Enter: Start Visualization",
        "Esc: Reset"
    ]
    for i, text in enumerate(instructions):
        render = font.render(text, True, (255, 255, 255))
        win.blit(render, (10, 10 + 20 * i))

def reset_grid():
    global queue, final, started
    for row in board:
        for cell in row:
            cell.visited = False
            cell.prev = None
            cell.wall = False  # Clear the walls as well
    queue.clear()
    final.clear()
    started = False

def display_message(message):
    font = pygame.font.SysFont("Arial", 36)
    text = font.render(message, True, (255, 0, 0))
    win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    create_grid()
    global start, end, started
    start, end = board[3][12], board[28][12]

    start.wall, end.wall = False, False

    running, started = True, False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    select_wall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    select_wall(pygame.mouse.get_pos(), False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not started:
                        started = True
                        queue.append(start)  # Ensure the start is in the queue
                        start.visited = True
                if event.key == pygame.K_ESCAPE:
                    reset_grid()

        if started:
            if queue:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        final.append(temp.prev)
                        temp = temp.prev
                    started = False
                    continue
                for neighbor in current.neighbours:
                    if not neighbor.visited and not neighbor.wall:
                        neighbor.visited = True
                        neighbor.prev = current
                        queue.append(neighbor)
            else:
                if started:
                    display_message("No Solution")
                    reset_grid()

        win.fill((0, 20, 20))
        for row in board:
            for cell in row:
                cell.show(win, (44, 62, 80))
                if cell in final:
                    cell.show(win, (192, 57, 43))
                elif cell.visited:
                    cell.show(win, (39, 174, 96))
                if cell == start:
                    cell.show(win, (0, 255, 200))
                if cell == end:
                    cell.show(win, (39, 120, 255))
        display_instructions()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
