import Map
import FogOfWar
import Agents

# Slightly modified heuristic function to fit the goal of the AI.
def heuristic(neighbour, finish, g, r):
    multiplier = 1
    if r[0] == 0 or r[1] == 0:
        neighbour.append(g+1) # g
    else:
        neighbour.append(g+1.4)

    # If ground is slow to walk on, prioritize it less.
    if Map.map[neighbour[0]][neighbour[1]] in ("G", "t"):
        multiplier = 2
    else:
        multiplier = 1

    if not FogOfWar.fogOfWar[neighbour[0]][neighbour[1]]:
        multiplier *= 0.7

    dx = abs(neighbour[0] - finish[0])
    dy = abs(neighbour[1] - finish[1])

    neighbour.append(dx + dy) # h
    neighbour.append(multiplier * (dx + dy) + (1.4 - 2 * multiplier) * min(dx, dy)) # f

    return neighbour

# Checks if current neighbour is better than what is currently in the open list and then adds it.
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

# A* pathfinding algorithm, look it up if you need more info...
def aStar(startPos, finishPos, r, agent):
    nonExplorer = False
    mapList = Map.map
    i = 0
    openList = []
    closedList = []
    nodes = []
    start = [startPos[0], startPos[1], -1, 0, 0, 0]
    finish = [finishPos[0], finishPos[1], 0, 0, 0, 0]
    unwalkables = ("B", "V")
    openList.append(start)

    if agent.getRole() != "explorer":
        # Also exclude fogOfWar
        nonExplorer = True

    while len(openList) > 0:
        #Sort list
        openList.sort(key=lambda x: x[5])

        #Pop lowest cost
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
            # Checks if agent can walk here or not
            if nonExplorer and not FogOfWar.fogOfWar[next[0] + currentPos[0]][next[1] + currentPos[1]]:
                continue

            if mapList[next[0] + currentPos[0]][next[1] + currentPos[1]] in unwalkables:
                continue

            elif next == (1, 1):
                if mapList[currentPos[0]][currentPos[1] + 1] in unwalkables or mapList[currentPos[0] + 1][currentPos[1]] in unwalkables:
                    continue
            elif next == (-1, 1):
                if mapList[currentPos[0]][currentPos[1] + 1] in unwalkables or mapList[currentPos[0] + -1][currentPos[1]] in unwalkables:
                    continue
            elif next == (1, -1):
                if mapList[currentPos[0]][currentPos[1] + -1] in unwalkables or mapList[currentPos[0] + 1][currentPos[1]] in unwalkables:
                    continue
            elif next == (-1, -1):
                if mapList[currentPos[0]][currentPos[1] + -1] in unwalkables or mapList[currentPos[0] + -1][currentPos[1]] in unwalkables:
                    continue

            neighbour = [next[0] + currentPos[0], next[1] + currentPos[1], i]
            heuristic(neighbour, finish, currentPos[3], r)

            for x in closedList:
                if neighbour[0] == x[0] and neighbour[1] == x[1]:
                    continue

            addToOpen(openList, closedList, neighbour)
        i += 1

# Runs a* and returns path
def findPath(agent, finish):
    start = agent.getPos()
    path = aStar(start, finish, Map.r, agent)
    return (path)