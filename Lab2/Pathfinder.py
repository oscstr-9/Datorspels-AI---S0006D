import copy
import time
import pygame
import Pygame

def findPath(algorithm, mapList):
    r = ((1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1))
    walls = []
    # separate coords from type
    for x in range(len(mapList)):
        for y in range(len(mapList[0])):
            if mapList[x][y] == "X":
                walls.append((x, y))
            elif mapList[x][y] == "S":
                start = (x, y)
            elif mapList[x][y] == "G":
                finish = (x, y)

    if algorithm == "astar" or algorithm == "a*":
        return aStar(start, finish, mapList, r)
    elif algorithm == "depthfirstsearch" or algorithm == "dfs":
        return depthFirstSearch(start, finish, walls, r)
    elif algorithm == "breadthfirstsearch" or algorithm == "bfs":
        return breadthFirstSearch(start, finish, mapList, r)
    elif algorithm == "custom":
        return custom(start, finish, mapList, r)


def heuristic(neighbour, finish, g, r):
    if r[0] == 0 or r[1] == 0:
        neighbour.append(g+1) # g
    else:
        neighbour.append(g+1.4)

    dx = abs(neighbour[0] - finish[0])
    dy = abs(neighbour[1] - finish[1])

    neighbour.append(dx + dy) # h
    neighbour.append(1 * (dx + dy) + (1.4 - 2 * 1) * min(dx, dy)) # f

    return neighbour

def addToOpen(openList, closedList, neighbour):
    for node in openList:
        if neighbour[0] == node[0] and neighbour[1] == node[1]:
            if neighbour[5] >= node[5]:
                return
            openList.remove(node)
            openList.append(neighbour)
            return

    for node in closedList:
        if neighbour[0] == node[0] and neighbour[1] == node[1]:
            if neighbour[5] >= node[5]:
                return
            closed.remove(node)
            openList.append(neighbour)
            return
    openList.append(neighbour)

def aStar(startPos, finishPos, mapList, r):
    i = 0
    openList = []
    closedList = []
    nodes = []
    start = [startPos[0], startPos[1], -1, 0, 0, 0]
    finish = [finishPos[0], finishPos[1], 0, 0, 0, 0]
    openList.append(start)

    while len(openList) > 0:
        #sort list
        openList.sort(key=lambda x: x[5])
        #pop lowest cost
        currentPos = openList.pop(0)
        nodes.append(currentPos)
        closedList.append(currentPos)
        if currentPos[0] == finish[0] and currentPos[1] == finish[1]:
            path = []
            while currentPos[2] != -1:
                path.append((currentPos[0], currentPos[1]))
                currentPos = nodes[currentPos[2]]
            path.append((start[0], start[1]))
            return path[::-1]

        for next in r:
            if mapList[next[0] + currentPos[0]][next[1] + currentPos[1]] == "X":
                continue

            elif next == (1, 1):
                if mapList[currentPos[0]][currentPos[1] + 1] == "X" or mapList[currentPos[0] + 1][currentPos[1]] == "X":
                    continue
            elif next == (-1, 1):
                if mapList[currentPos[0]][currentPos[1] + 1] == "X" or mapList[currentPos[0] + -1][currentPos[1]] == "X":
                    continue
            elif next == (1, -1):
                if mapList[currentPos[0]][currentPos[1] + -1] == "X" or mapList[currentPos[0] + 1][currentPos[1]] == "X":
                    continue
            elif next == (-1, -1):
                if mapList[currentPos[0]][currentPos[1] + -1] == "X" or mapList[currentPos[0] + -1][currentPos[1]] == "X":
                    continue

            neighbour = [next[0] + currentPos[0], next[1] + currentPos[1], i]
            heuristic(neighbour, finish, currentPos[3], r)

            for x in closedList:
                if neighbour[0] == x[0] and neighbour[1] == x[1]:
                    continue

            addToOpen(openList, closedList, neighbour)
        i += 1

        Pygame.drawMap(mapList)
        for node in openList:
            pygame.draw.rect(Pygame.screen, Pygame.agent, pygame.Rect(node[0]*Pygame.gridSize+Pygame.gridSize//2,node[1]*Pygame.gridSize+Pygame.gridSize//2,5,5))
            pygame.draw.line(Pygame.screen, (100, 255, 255), (node[0]*Pygame.gridSize+Pygame.gridSize//2,node[1]*Pygame.gridSize+Pygame.gridSize//2), (nodes[node[2]][0]*Pygame.gridSize+Pygame.gridSize//2,nodes[node[2]][1]*Pygame.gridSize+Pygame.gridSize//2),5)
        for node in closedList:
            pygame.draw.rect(Pygame.screen, (100, 0, 75), pygame.Rect(node[0]*Pygame.gridSize+Pygame.gridSize//2,node[1]*Pygame.gridSize+Pygame.gridSize//2,5,5))
            pygame.draw.line(Pygame.screen, (100, 255, 255), (node[0]*Pygame.gridSize+Pygame.gridSize//2,node[1]*Pygame.gridSize+Pygame.gridSize//2), (nodes[node[2]][0]*Pygame.gridSize+Pygame.gridSize//2,nodes[node[2]][1]*Pygame.gridSize+Pygame.gridSize//2),5)

        Pygame.update()
        time.sleep(0.05)


def depthFirstSearch(currentPos, finish, walls, r):
    # All directions
    # Is finished
    if currentPos == finish:
        return [currentPos]
    if currentPos not in walls:
        walls.append(currentPos)

        for i in r:
            neighbour = (currentPos[0] + i[0], currentPos[1] + i[1])
            if i == (1, 1):
                if (currentPos[0], currentPos[1] + 1) in walls or (currentPos[0] + 1, currentPos[1]) in walls:
                    continue
            elif i == (-1, 1):
                if (currentPos[0], currentPos[1] + 1) in walls or (currentPos[0] + -1, currentPos[1]) in walls:
                    continue
            elif i == (1, -1):
                if (currentPos[0], currentPos[1] + -1) in walls or (currentPos[0] + 1, currentPos[1]) in walls:
                    continue
            elif i == (-1, -1):
                if (currentPos[0], currentPos[1] + -1) in walls or (currentPos[0] + -1, currentPos[1]) in walls:
                    continue

            # Save and check if we ever got stuck during search
            print(neighbour)
            path = depthFirstSearch(neighbour, finish, walls, r)
            if not path == []:
                return [currentPos] + path
        return []
    return []


def breadthFirstSearch(currentPos,finish,mapList,r):
    searching = True
    graph = copy.deepcopy(mapList)

    for x in range(len(graph)):
        for y in range(len(graph[0])):
            if graph[x][y] == "X":
                graph[x][y] = False
            else:
                graph[x][y] = True

    queue = []
    path = []
    i = 0
    # Add start pos to walls and queue
    queue.append((currentPos[0], currentPos[1], -1))
    graph[currentPos[0]][currentPos[1]] = False

    while searching:
        currentPos = queue[i]
        for neighbour in r:

            if neighbour == (1, 1):
                if graph[currentPos[0]][currentPos[1] + 1] == False or graph[currentPos[0] + 1][currentPos[1]] == False:
                    continue
            elif neighbour == (-1, 1):
                if graph[currentPos[0]][currentPos[1] + 1] == False or graph[currentPos[0] + -1][currentPos[1]] == False:
                    continue
            elif neighbour == (1, -1):
                if graph[currentPos[0]][currentPos[1] + -1] == False or graph[currentPos[0] + 1][currentPos[1]] == False:
                    continue
            elif neighbour == (-1, -1):
                if graph[currentPos[0]][currentPos[1] + -1] == False or graph[currentPos[0] + -1][currentPos[1]] == False:
                    continue

            if graph[neighbour[0]+currentPos[0]][neighbour[1]+currentPos[1]] == True:
                graph[neighbour[0]+currentPos[0]][neighbour[1]+currentPos[1]] = False
                queue.append((neighbour[0]+currentPos[0], neighbour[1]+currentPos[1], i))

                if neighbour[0]+currentPos[0] == finish[0] and neighbour[1]+currentPos[1] == finish[1]:
                    path.append((neighbour[0]+currentPos[0], neighbour[1]+currentPos[1]))

                    searching = False
                    while currentPos[2] != -1:
                        path.append(currentPos)
                        currentPos = queue[currentPos[2]]
                    path.append(currentPos)

        i += 1
    return path

def custom(start, finish, mapList, r):
    startFound = False
    runningStart = True
    runningfinish = True
    i = 0
    centerX = len(mapList)//2
    centerY = len(mapList[0])//2

    startPath = []
    finishPath = []

    graphMap = copy.deepcopy(mapList)
    for x in range(len(graphMap)):
        for y in range(len(graphMap[0])):
            if mapList[x][y] == "X":
                graphMap[x][y] = False
            else:
                graphMap[x][y] = True

    if mapList[centerX][centerY] == "X":

        searchCenter = [centerX, centerY, -1]
        graph = copy.deepcopy(mapList)

        for x in range(len(graph)):
            for y in range(len(graph[0])):
                if graph[x][y] == "X":
                    graph[x][y] = 0
                else:
                    graph[x][y] = 1
        queue = []

        queue.append((searchCenter[0], searchCenter[1], -1))
        graph[searchCenter[0]][searchCenter[1]] = False
        while startFound is False:
            searchStart = queue[i]
            for neighbour in r:
                if graph[neighbour[0] + searchCenter[0]][neighbour[1] + searchCenter[1]] == 0:
                    graph[neighbour[0] + searchCenter[0]][neighbour[1] + searchCenter[1]] = 2
                    queue.append((neighbour[0] + searchCenter[0], neighbour[1] + searchCenter[1], i))

                elif graph[neighbour[0] + searchCenter[0]][neighbour[1] + searchCenter[1]] == 1:
                    centerX = neighbour[0] + searchCenter[0]
                    centerY = neighbour[1] + searchCenter[1]
                    searchCenter[0] = centerX
                    searchCenter[1] = centerY
                    startFound = True
            i+= 1

    currentPos = [centerX, centerY]
    startPath.append(currentPos)
    revR = r[::-1]
    while runningStart:
        print(currentPos)
        currentPos = startPath[len(startPath)-1]
        print(currentPos)


        if currentPos[0] == start[0] and currentPos[1] == start[1]:
            runningStart = False
            break
        i = 0
        for next in revR:
            neighbour = (currentPos[0] + next[0], currentPos[1] + next[1])
            if next == (1, 1):
                if graphMap[currentPos[0]][currentPos[1] + 1] == False or graphMap[currentPos[0] + 1][currentPos[1]] == False:
                    continue
            elif next == (-1, 1):
                if graphMap[currentPos[0]][currentPos[1] + 1] == False or graphMap[currentPos[0] + -1][currentPos[1]] == False:
                    continue
            elif next == (1, -1):
                if graphMap[currentPos[0]][currentPos[1] + -1] == False or graphMap[currentPos[0] + 1][currentPos[1]] == False:
                    continue
            elif next == (-1, -1):
                if graphMap[currentPos[0]][currentPos[1] + -1] == False or graphMap[currentPos[0] + -1][currentPos[1]] == False:
                    continue

            if graphMap[neighbour[0]][neighbour[1]]:
                startPath.append(neighbour)
                break
            i += 1
        if neighbour == startPath[len(startPath)-1] and i == 8:
            startPath.remove(neighbour)

            Pygame.drawMap(mapList)
            for node in startPath:
                pygame.draw.rect(Pygame.screen, Pygame.agent,
                                 pygame.Rect(node[0] * Pygame.gridSize + Pygame.gridSize // 2,
                                             node[1] * Pygame.gridSize + Pygame.gridSize // 2, 5, 5))
                pygame.draw.line(Pygame.screen, (100, 255, 255), (
                    node[0] * Pygame.gridSize + Pygame.gridSize // 2, node[1] * Pygame.gridSize + Pygame.gridSize // 2),
                                 (startPath[len(startPath)-2][0] * Pygame.gridSize + Pygame.gridSize // 2,
                                  startPath[len(startPath)-2][1] * Pygame.gridSize + Pygame.gridSize // 2), 5)
            Pygame.update()
            time.sleep(0.05)


    for x in range(len(graphMap)):
        for y in range(len(graphMap[0])):
            if mapList[x][y] == "X":
                graphMap[x][y] = False
            else:
                graphMap[x][y] = True
    currentPos = [centerX, centerY, -1]
    k = 0
    while runningFinish:
        finishPath.append(currentPos)
        currentPos = startPath[len(startPath) - 1]

        if currentPos[0] == finish[0] and currentPos[1] == finish[1]:
            runningFinish = False
            break

            i = 0
            for next in r:
                neighbour = (currentPos[0] + next[0], currentPos[1] + next[1])
                if next == (1, 1):
                    if graphMap[currentPos[0]][currentPos[1] + 1] == False or graphMap[currentPos[0] + 1][currentPos[1]] == False:
                        continue
                elif next == (-1, 1):
                    if graphMap[currentPos[0]][currentPos[1] + 1] == False or graphMap[currentPos[0] + -1][currentPos[1]] == False:
                        continue
                elif next == (1, -1):
                    if graphMap[currentPos[0]][currentPos[1] + -1] == False or graphMap[currentPos[0] + 1][currentPos[1]] == False:
                        continue
                elif next == (-1, -1):
                    if graphMap[currentPos[0]][currentPos[1] + -1] == False or graphMap[currentPos[0] + -1][currentPos[1]] == False:
                        continue

                if graphMap[neighbour[0]][neighbour[1]]:
                    finishPath.append(neighbour)
                    break
                i += 1
            if neighbour == startPath[len(startPath - 1)]:
                finishPath.remove(neighbour)

            Pygame.drawMap(mapList)
            for node in finishPath:
                pygame.draw.rect(Pygame.screen, Pygame.agent,
                                 pygame.Rect(node[0] * Pygame.gridSize + Pygame.gridSize // 2,
                                             node[1] * Pygame.gridSize + Pygame.gridSize // 2, 5, 5))
                pygame.draw.line(Pygame.screen, (100, 255, 255), (
                    node[0] * Pygame.gridSize + Pygame.gridSize // 2, node[1] * Pygame.gridSize + Pygame.gridSize // 2),
                                 (finishPath[len(startPath)-2][0] * Pygame.gridSize + Pygame.gridSize // 2,
                                  finishPath[len(startPath)-2][1] * Pygame.gridSize + Pygame.gridSize // 2), 5)

            Pygame.update()
            time.sleep(0.05)

    return startPath + finish