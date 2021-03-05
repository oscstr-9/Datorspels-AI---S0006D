import Agents
import FogOfWar
import Map
import TimeMultiplier
import pygame
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    K_LSHIFT,
    KEYDOWN,
    )

gridSize = 10
agentSize = 5
screen = 0
localTimeMultiplier = 1


workerColor = (0, 100, 150)
builderColor = (0, 130, 150)
explorerColor = (0, 160, 150)
soldierColor = (0, 190, 150)

# Initializes base data
def init():
    map = Map.map
    # Set window size depending on amount of squares
    screenWidth = gridSize * len(map)
    screenHeight = gridSize * len(map[0])

    pygame.init()

    # Set up the drawing window
    global screen
    screen = pygame.display.set_mode([screenWidth, screenHeight])

    screen.fill((180, 140, 102))
    drawMap()
    update()

# Draws the map onto the display
def drawMap():
    # Draw map
    colorDict = {
        "M": (180, 140, 102),
        "B": (0, 26, 0),
        "T": (25, 77, 0),
        "t": (51, 0, 25),
        "G": (77, 51, 0),
        "V": (51, 153, 255),
        "I": (179, 191, 255),
        "S": (255, 128, 255),
        "CF": (192, 192, 192),
        "SM": (255, 128, 0),
        "BS": (255, 0, 0),
        "TC": (255, 153, 153)
    }
    fogColor = (0, 43, 51)
    mapList = Map.map
    fogOfWar = FogOfWar.fogOfWar
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            rect = pygame.Rect(x * gridSize, y * gridSize, gridSize, gridSize)
            if fogOfWar[x][y] == False:
                pygame.draw.rect(screen, fogColor, rect, 1)
                screen.fill(fogColor, rect, 0)
            else:
                color = colorDict[mapList[x][y]]
                pygame.draw.rect(screen, color, rect, 1)
                screen.fill(color, rect, 0)

# Draws agents onto display
def drawAgents(agents):
    for agent in agents:
        pos = agent.getPos()
        role = agent.getRole()
        rect = pygame.Rect(pos[0] * gridSize + gridSize//2 - agentSize//2, pos[1] * gridSize + gridSize//2 - agentSize//2, agentSize, agentSize)
        if role == "worker":
            pygame.draw.rect(screen, workerColor, rect, 1)
            screen.fill(workerColor, rect, 0)
        elif role == "builder":
            pygame.draw.rect(screen, builderColor, rect, 1)
            screen.fill(builderColor, rect, 0)
        elif role == "explorer":
            pygame.draw.rect(screen, explorerColor, rect, 1)
            screen.fill(explorerColor, rect, 0)
        elif role == "soldier":
            pygame.draw.rect(screen, soldierColor, rect, 1)
            screen.fill(soldierColor, rect, 0)

# updates the display and allows for ESC to quit
def update():
    pygame.display.flip()
    # Has the ESCAPE key been pressed?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            global localTimeMultiplier
            if event.key == K_SPACE:
                if TimeMultiplier.timeMultiplier > 0:
                    localTimeMultiplier = TimeMultiplier.timeMultiplier
                    TimeMultiplier.setTimeMultiplier(0)
                else:
                    TimeMultiplier.setTimeMultiplier(localTimeMultiplier)

            if event.key == K_LSHIFT:
                localTimeMultiplier = abs(input())
                TimeMultiplier.setTimeMultiplier(localTimeMultiplier)

            if event.key == K_ESCAPE:
                # Done! Time to quit.
                pygame.quit()
                return False

    return True


