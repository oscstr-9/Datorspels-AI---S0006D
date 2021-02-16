import copy

def findPath(algorithm, allNodes, mapList):
    walls = []
    walkables = []
    # separate coords from type
    for nodes in allNodes:
        if nodes[0] == "X":
            walls.append((nodes[1], nodes[2]))
        elif nodes[0] == "S":
            start = (nodes[1], nodes[2])
        elif nodes[0] == "G":
            finish = (nodes[1], nodes[2])
        if nodes[0] == "0" or nodes[0] == "S" or nodes[0] == "G":
            walkables.append((nodes[1], nodes[2]))

    if algorithm == "astar" or algorithm == "a*":
        return aStar(start, finish)
    elif algorithm == "depthfirstsearch" or algorithm == "dfs":
        return depthFirstSearch(start, finish, walls)
    elif algorithm == "breadthfirstsearch" or algorithm == "bfs":
        return breadthFirstSearch(start, finish, mapList)
    elif algorithm == "custom":
        return custom(start, finish)


def aStar(start, finish):
    openList = []
    closedList = []


    path = start

def depthFirstSearch(currentPos, finish, walls):
    # All directions
    r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))
    # Is finished
    if currentPos == finish:
        return [currentPos]
    if currentPos not in walls:
        walls.append(currentPos)
        for i in r:
            neighbour = (currentPos[0] + i[0], currentPos[1] + i[1])
            # Save and check if we ever got stuck during search
            path = depthFirstSearch(neighbour, finish, walls)
            if not path == []:
                return [currentPos] + path
        return []
    return []

def breadthFirstSearch(currentPos,finish,mapList):
    r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))

    graph = copy.deepcopy(mapList)

    for x in range(len(graph)):
        for y in range(len(graph[0])):
            if graph[x][y] == "X":
                graph[x][y] = False
            else:
                graph[x][y] = True

    queue = []
    # Add start pos to walls and queue
    queue.append(currentPos)
    graph[s[0]][s[1]] = False

    while queue:
        s = queue.pop(0)

        for neighbour in r:
            if graph[neighbour[0]+r[0]][neighbour[1]+r[1]] == True:
                graph[neighbour[0]+s[0]][neighbour[1]+s[1]] = False
                queue.append(neighbour)

def custom(start, finish):
    zxc