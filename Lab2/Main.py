import Pygame
import Pathfinder

def main():
    algorithm = "custom"
    running = True
    f = open("maps/Map2.txt", "r")

    # parse map file
    mapLines = f.readlines()
    map = [[] for _ in range(len(mapLines[0])-1)]

    for lines in mapLines:
        i = 0
        print(lines)
        
        for c in lines:
            if c == "\r":
                continue
            if c == "\n":
                break
            map[i].append(c)
            i += 1

    Pygame.init(map)
    Pygame.drawPath(Pathfinder.findPath(algorithm, map))

    while running is True:
        running = Pygame.update()


main()