import Agents
import FogOfWar
import Map
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    )

gridSize = 10
agentSize = 5
screen = 0


workerColor = (0, 100, 150)
builderColor = (0, 130, 150)
explorerColor = (0, 160, 150)
soldierColor = (0, 190, 150)
mountainColor = (0, 26, 0)
swampColor = (77, 51, 0)
waterColor = (51, 153, 255)
groundColor = (180, 140, 102)
treeColor = (25, 77, 0)
startColor = (255, 128, 255)
mineralColor = (179, 191, 255)
fogColor = (0, 43, 51)


def init():
    map = Map.map
    fogOfWar = FogOfWar.fogOfWar
    # Set window size depending on amount of squares
    screenWidth = gridSize * len(map)
    screenHeight = gridSize * len(map[0])

    pygame.init()

    # Set up the drawing window
    global screen
    screen = pygame.display.set_mode([screenWidth, screenHeight])

    screen.fill(groundColor)
    drawMap(map, fogOfWar)
    update()

def drawMap():
    # Draw map
    mapList = Map.map
    fogOfWar = FogOfWar.fogOfWar
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            rect = pygame.Rect(x * gridSize, y * gridSize, gridSize, gridSize)
            if fogOfWar[x][y] == False:
                pygame.draw.rect(screen, fogColor, rect, 1)
                screen.fill(fogColor, rect, 0)
            else:
                if mapList[x][y] == "M":
                    pygame.draw.rect(screen, groundColor, rect, 1)
                    screen.fill(groundColor, rect, 0)
                elif mapList[x][y] == "B":
                    pygame.draw.rect(screen, mountainColor, rect, 1)
                    screen.fill(mountainColor, rect, 0)
                elif mapList[x][y] == "T":
                    pygame.draw.rect(screen, treeColor, rect, 1)
                    screen.fill(treeColor, rect, 0)
                elif mapList[x][y] == "G":
                    pygame.draw.rect(screen, swampColor, rect, 1)
                    screen.fill(swampColor, rect, 0)
                elif mapList[x][y] == "V":
                    pygame.draw.rect(screen, waterColor, rect, 1)
                    screen.fill(waterColor, rect, 0)
                elif mapList[x][y] == "I":
                    pygame.draw.rect(screen, mineralColor, rect, 1)
                    screen.fill(mineralColor, rect, 0)
                elif mapList[x][y] == "S":
                    pygame.draw.rect(screen, startColor, rect, 1)
                    screen.fill(startColor, rect, 0)
                else:
                    print("Map not formatted correctly!")
                    pygame.draw.rect(screen, (255, 0, 255), rect, 1)
                    screen.fill((255, 0, 255), rect, 0)

def drawAgents(agents):
    for agent in agents:
        pos = Agents.agent.getPos(agent)
        role = Agents.agent.getRole(agent)
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


