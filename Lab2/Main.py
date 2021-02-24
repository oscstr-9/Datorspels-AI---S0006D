import Pygame
import Pathfinder

def main():
    running = True
    algorithm = input("What algorithm should be checked?: ")
    if algorithm == "all":
        checks = int(input("how many times should the algorithms be checked?: "))
        for mapNr in range(3):
            testAlgs(makeMap(mapNr+1), mapNr + 1, checks)
            Pygame.update()

    else:
        mapNr = int(input("What map should be tested? (1-3): "))
        map = makeMap(mapNr)
        Pygame.init(map)

        if algorithm == "dfs" or algorithm == "depthfirstsearch":
            result = Pathfinder.findPath("dfs", map)
            Pygame.drawPath(result[0], (255, 255, 0))

        elif algorithm == "bfs" or algorithm == "breadthfirstsearch":
            result = Pathfinder.findPath("bfs", map)
            Pygame.drawPath(result[0], (0, 150, 140))

        elif algorithm == "astar" or algorithm == "a*":
            result = Pathfinder.findPath("a*", map)
            Pygame.drawPath(result[0], (0, 50, 100))

        elif algorithm == "custom":
            result = Pathfinder.findPath("custom", map)
            Pygame.drawPath(result[0], (120, 0, 255))

    while running is True:
        running = Pygame.update()


def makeMap(mapNr):
    f = open("maps/Map" + str(mapNr) + ".txt", "r")

    # parse map file
    mapLines = f.readlines()
    map = [[] for _ in range(len(mapLines[0]) - 1)]

    for lines in mapLines:
        i = 0
        for c in lines:
            if c == "\r":
                continue
            if c == "\n":
                break
            map[i].append(c)
            i += 1

    return map


def testAlgs(map, mapNr, checks):
    dfsDiff = 0
    bfsDiff = 0
    astarDiff = 0
    customDiff = 0

    Pygame.init(map)

    for i in range(checks):
        result = Pathfinder.findPath("dfs", map)
        Pygame.drawPath(result[0], (255, 255, 0))
        dfsDiff += result[1]

    for j in range(checks):
        result = Pathfinder.findPath("bfs", map)
        Pygame.drawPath(result[0], (0, 150, 140))
        bfsDiff += result[1]

    for k in range(checks):
        result = Pathfinder.findPath("a*", map)
        Pygame.drawPath(result[0], (0, 50, 100))
        astarDiff += result[1]

    for l in range(checks):
        result = Pathfinder.findPath("custom", map)
        Pygame.drawPath(result[0], (120, 0, 255))
        customDiff += result[1]

    print("\n")

    print("|>------------------------------<|")
    print("Average time for dfs test on map" + str(mapNr) + ":")
    print(dfsDiff / checks)

    print("|>------------------------------<|")
    print("Average time for bfs test on map" + str(mapNr) + ":")
    print(bfsDiff / checks)

    print("|>------------------------------<|")
    print("Average time for astar test on map" + str(mapNr) + ":")
    print(astarDiff / checks)

    print("|>------------------------------<|")
    print("Average time for custom alg test on map" + str(mapNr) + ":")
    print(customDiff / checks)

main()