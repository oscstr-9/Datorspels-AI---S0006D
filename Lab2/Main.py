import pygame
import Pathfinder
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
algorithm = "a*"


def main():
    f = open("Map1.txt", "r")


    
    # parse map file
    mapLines = f.readlines()
    map1 = [[] for _ in range(len(mapLines[0])-1)]

    for lines in mapLines:
        i = 0
        print(lines)
        
        for c in lines:
            if c == "\r":
                continue
            if c == "\n":
                break
            map1[i].append(c)
            i += 1

        
    print(f.read())

    drawMap(map1)
    
    # Run until the user asks to quit
    running = True
    while running:

        # Has the ESCAPE key been pressed?
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


def drawMap(mapList):
    # Set window size depending on amount of squares
    screenWidth = gridSize * len(mapList)
    screenHeight = gridSize * len(mapList[0])
    nodes = []
    
    pygame.init()

    # Set up the drawing window
    global screen
    screen = pygame.display.set_mode([screenWidth, screenHeight])

    screen.fill(path)

    # Draw map
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            rect = pygame.Rect(x*gridSize, y*gridSize, gridSize, gridSize)
            if mapList[x][y] == "X":
                pygame.draw.rect(screen, wall, rect, 1)
                screen.fill(wall, rect, 0)
                nodes.append((x, y, "X"))
            elif mapList[x][y] == "0":
                pygame.draw.rect(screen, path, rect, 1)
                screen.fill(path, rect, 0)
                nodes.append((x, y, "0"))
            elif mapList[x][y] == "S":
                pygame.draw.rect(screen, start, rect, 1)
                screen.fill(start, rect, 0)
                nodes.append((x, y, "S"))
            elif mapList[x][y] == "G":
                pygame.draw.rect(screen, finish, rect, 1)
                screen.fill(finish, rect, 0)
                nodes.append((x, y, "G"))
            else:
                print("Map not formatted correctly!")
                pygame.draw.rect(screen, (255, 0, 255), rect, 1)
                screen.fill((255, 0, 255), rect, 0)

    drawPath(Pathfinder.findPath(algorithm, nodes, mapList))

# Takes list of (x, y) tuples to print path
def drawPath(path):
    # Scales the path to fit the map
    scaledPath = []
    for tiles in path:
        scaledPath.append(((tiles[0] * gridSize) + gridSize//2, (tiles[1] * gridSize) + gridSize//2))
    pygame.draw.lines(screen, agent, False, scaledPath, 5)

main()
