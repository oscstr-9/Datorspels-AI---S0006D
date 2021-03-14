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
        "t": (75, 0, 25),
        "G": (77, 51, 0),
        "V": (51, 153, 255),
        "I": (179, 191, 255),
        "S": (255, 128, 255),
        "CF": (192, 192, 192),
        "SM": (255, 128, 0),
        "BS": (255, 0, 0),
        "TC": (255, 153, 153),
        "construction": (255, 255, 255)
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
    colorDict = {
        "worker": (0, 100, 150),
        "explorer": (160, 90, 25),
        "builder": (255, 0, 0),
        "coalWorker": (0, 255, 0),
        "weaponSmith": (240, 240, 170),
        "smelteryWorker": (240, 170, 240),
        "soldier": (0, 190, 150)
    }
    for agent in agents:
        pos = agent.getPos()
        rect = pygame.Rect(pos[0] * gridSize + gridSize//2 - agentSize//2, pos[1] * gridSize + gridSize//2 - agentSize//2, agentSize, agentSize)

        pygame.draw.rect(screen, colorDict[agent.getRole()], rect, 1)
        screen.fill(colorDict[agent.getRole()], rect, 0)

# updates the display and allows for ESC to quit
def update():
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

            if event.key == K_ESCAPE:
                # Done! Time to quit.
                pygame.quit()
                return False
    pygame.display.update()
    drawMap()

    return True


