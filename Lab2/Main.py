import pygame
from pygame.locals import(
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )

screenWidth = 500
screenHeight = 500
wall = (0,0,0)
path = (255,255,255)
start = (0,255,0)
finish = (255,0,0)
        
def main():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([screenWidth, screenHeight])

    screen.fill(path)

    map1 = [[]]
    j = 0
    f = open("map2.txt", "r")
    mapLines = f.readlines()
    map1 = [[] for _ in range(len(mapLines))]
    for lines in mapLines:
        i = 0
        print(lines)
        
        for c in lines:
            if c == "\n":
                break
            map1[i].append(c)
            
            i += 1
        j += 1
        
    print(f.read())
    # Run until the user asks to quit
    running = True
    while running:

        #Has the ESCAPE key been pressed?
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        drawMap(map1, screen)
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


def drawMap(mapList, screen):
    gridSize = screenHeight // len(mapList)
     
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            rect = pygame.Rect(x*gridSize, y*gridSize, gridSize, gridSize)
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
                print("broken")
   
main()
