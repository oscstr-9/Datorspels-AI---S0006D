import copy

def findPath(algorithm, allNodes, mapList):
    r = ((1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))
    walls = []
    walkables = []
    # separate coords from type
    for nodes in allNodes:
        if nodes[2] == "X":
            walls.append((nodes[0], nodes[1]))
        elif nodes[2] == "S":
            start = (nodes[0], nodes[1])
        elif nodes[2] == "G":
            finish = (nodes[0], nodes[1])
        if nodes[2] == "0" or nodes[2] == "S" or nodes[2] == "G":
            walkables.append((nodes[0], nodes[1]))

    if algorithm == "astar" or algorithm == "a*":
        return aStar(start, finish, mapList, r)
    elif algorithm == "depthfirstsearch" or algorithm == "dfs":
        return depthFirstSearch(start, finish, walls, r)
    elif algorithm == "breadthfirstsearch" or algorithm == "bfs":
        return breadthFirstSearch(start, finish, mapList, r)
    elif algorithm == "custom":
        return custom(start, finish)

def heuristic(neighbour, start, finish):
    neighbour.append(abs(neighbour[0] - start[0]) + abs(neighbour[1] - start[1]))
    neighbour.append(abs(neighbour[0] - finish[0]) + abs(neighbour[1] - finish[1]))
    neighbour.append(neighbour[3] + neighbour[4])

    return neighbour

def addToOpen(openList, closedList, neighbour):
    for node in openList:
        if neighbour[0] == node[0] and neighbour[1] == node[1] and neighbour[5] >= node[5]:
            return False
        elif neighbour[0] == node[0] and neighbour[1] == node[1] and neighbour[5] <= node[5]:
            closedList.append(node)
            openList.pop(node)
    return True

def aStar(startPos, finishPos, mapList, r):
    i = 0
    openList = []
    closedList = []
    nodes = []
    start = [startPos[0], startPos[1], 0, 0, 0, 0]
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
            while currentPos[0] != start[0] and currentPos[1] != start[1]:
                path.append((currentPos[0], currentPos[1]))
                currentPos = nodes[currentPos[2]]
            path.append((start[0], start[1]))
            return path[::-1]

        for next in r:


            if mapList[next[0] + currentPos[0]][next[1] + currentPos[1]] == "X":
                continue

            neighbour = [next[0] + currentPos[0], next[1] + currentPos[1], i]
            heuristic(neighbour, start, finish)


            for x in closedList:
                if neighbour[0] == x[0] and neighbour[1] == x[1]:
                    continue

            if addToOpen(openList, closedList, neighbour) == True:
                openList.append(neighbour)
        i += 1



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
    print(finish)

    for x in range(len(graph)):
        for y in range(len(graph[0])):
            if graph[x][y] == "X":
                graph[x][y] = False
            else:
                graph[x][y] = True

    queue = []
    path = []
    i = 0
    j = 0
    # Add start pos to walls and queue
    queue.append((currentPos[0], currentPos[1], -1))
    graph[currentPos[0]][currentPos[1]] = False

    while searching:
        print(i)
        print(currentPos)
        print(finish)
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

def custom(start, finish):
    zxc