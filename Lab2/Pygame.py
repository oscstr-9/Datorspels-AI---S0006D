import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    )

gridSize = 20
agentSize = 5
screen = 0
agent = (0, 100, 150)
wall = (0, 0, 0)
path = (255, 255, 255)
start = (0, 255, 0)
finish = (255, 0, 0)

def init(map):
    # Set window size depending on amount of squares
    screenWidth = gridSize * len(map)
    screenHeight = gridSize * len(map[0])

    pygame.init()

    # Set up the drawing window
    global screen
    screen = pygame.display.set_mode([screenWidth, screenHeight])

    screen.fill(path)
    drawMap(map)
    update()

def drawMap(mapList):
    # Draw map
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            rect = pygame.Rect(x * gridSize, y * gridSize, gridSize, gridSize)
            if mapList[x][y] == "X":
                pygame.draw.rect(screen, wall, rect, 1)
                screen.fill(wall, rect, 0)
            elif mapList[x][y] == "0":
                pygame.draw.rect(screen, path, rect, 1)
                screen.fill(path, rect, 0)
            elif mapList[x][y] == "S":
                pygame.draw.rect(screen, start, rect, 1)
                screen.fill(start, rect, 0)
            elif mapList[x][y] == "G":
                pygame.draw.rect(screen, finish, rect, 1)
                screen.fill(finish, rect, 0)
            else:
                print("Map not formatted correctly!")
                pygame.draw.rect(screen, (255, 0, 255), rect, 1)
                screen.fill((255, 0, 255), rect, 0)


# Takes list of (x, y) tuples to print path
def drawPath(path, color):
    # Scales the path to fit the map
    scaledPath = []
    for tiles in path:
        scaledPath.append(((tiles[0] * gridSize) + gridSize // 2, (tiles[1] * gridSize) + gridSize // 2))
    pygame.draw.lines(screen, color, False, scaledPath, 5)

def update():
    pygame.display.flip()
    # Has the ESCAPE key been pressed?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Done! Time to quit.
                pygame.quit()
                return False

    return True


