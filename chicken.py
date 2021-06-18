import argparse
import sys
from utils import readFile, outputSolutionToFile
from enum import Enum
import heapq


"""
first line: (left bank)
first column = number of chickens
second column = number of wolves
third column = number of boats on the left bank

second line: (right bank)
first column = number of chickens
second column = number of wolves
third column = number of boats on the right bank

Conditions:
1. num wolves cannot be more than num chickens
2. at least one animal has to be on the boat

start_1
0, 0, 0 (left bank)
3, 3, 1 (right bank)

goal_1
3, 3, 1 (left bank)
0, 0, 0 (right bank)

BFS:


Optimal Solution:
1. Bring 2 wolves over to left bank.
2. Bring 1 wolf back to the right bank.
3. Bring 2 wolves over to left bank.
4. Bring 1 wolf back to the right bank.
5. Bring 2 chicks over to the left bank.
6. Bring 1 wolf and 1 chick back to the right bank.
7. Bring 2 chicks over to the left bank.
8. Bring 1 wolf back to the right bank.
9. Bring 2 wolves over to left bank.
10. Bring 1 wolf back to the right bank.
11. Bring 2 wolves over to left bank.

"""
Actions = ["oneChicken", "twoChickens", "oneOfEach", "oneWolf", "twoWolves"]


class Node:
    # state is a dictionary
    def __init__(self, state):
        #         start_1
        # 0, 0, 0 (left bank)
        # 3, 3, 1 (right bank)
        self.leftBank = state["leftBank"]
        self.rightBank = state["rightBank"]
        self.cameFrom = None
        self.distanceFromStart = float("inf")  # g - score
        self.distanceToEnd = float("inf")  # f - score

    def __lt__(self, other):
        return self.distanceToEnd < other.distanceToEnd


def depthFirstSearch(initState, goalState, outputFile):

    nodeExpanded = 0
    exploredNodes = {}
    # only use append or pop
    frontier = []

    initNode = Node(initState)
    goalNode = Node(goalState)
    frontier.append(initNode)

    print("\n\n======== Checking Depth First Search\n")

    while len(frontier) > 0:

        # for i in range(100):
        # print("Frontier length: ", len(frontier))
        # print("ExploredNodes length: ", len(exploredNodes))
        curNode = frontier.pop(-1)  # LIFO
        exploredNodes[str(curNode.leftBank)] = curNode.leftBank

        # check for goal
        if curNode.leftBank == goalNode.leftBank:
            print("!!! FOUND THE SOULTION !!!")
            exploredNodes[str(curNode.leftBank)] = curNode.leftBank
            goalNode.cameFrom = curNode.cameFrom
            break
        else:
            # expand this curNode
            nodeExpanded += 1
            expandNode(curNode, exploredNodes, frontier)

    path = reconstructPath(curNode, outputFile, nodeExpanded)
    print("\nNumber of nodes expanded: ", nodeExpanded)
    print("Number of nodes in path: ", len(path))
    return path


def reconstructPath(endNode, outputFile, expandedCount):
    path = []
    if endNode.cameFrom == None:
        outputSolutionToFile(outputFile, path, expandedCount)
        print("!!! NO SOLUTION !!!")
        return path
    elif endNode == nodeNoSolution:
        outputSolutionToFile(outputFile, path, expandedCount)
        print("!!! NO SOLUTION !!!")
        return path
    currentNode = endNode

    while currentNode:
        # path.append([currentNode.leftBank, currentNode.rightBank])
        path.append(
            [
                currentNode.rightBank,
                currentNode.leftBank,
            ]
        )
        currentNode = currentNode.cameFrom
        # print('Step ', i)
        # print(currentNode.leftBank)
        # print(currentNode.rightBank, '\n')
        # i += 1
    path = path[::-1]  # reverse
    # f = open("output.txt", "w")
    # for i, item in enumerate(path):
    outputSolutionToFile(outputFile, path, expandedCount)
    print("Path Length: ", len(path))
    # print(i+1, ": ", item)
    # , end =" "
    return path


# Take a node, explore all 5 branches, add valid branch to result array and return array


def expandNode(currentNode, exploredNodes, frontier):
    leftChicken = currentNode.leftBank[0]
    leftWolf = currentNode.leftBank[1]
    # leftBoat = currentNode.leftBank[2]

    rightChicken = currentNode.rightBank[0]
    rightWolf = currentNode.rightBank[1]
    rightBoat = currentNode.rightBank[2]

    # if boat is on the right bank
    if rightBoat == 1:
        # one chicken
        newRightChicken = rightChicken - 1
        newLeftChicken = leftChicken + 1
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # two chickens
        newRightChicken = rightChicken - 2
        newLeftChicken = leftChicken + 2
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 chicks from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # one wolf

        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newLeftWolf = leftWolf + 1
        newRightWolf = rightWolf - 1
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 wolf from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # one wolf one chicken
        newRightChicken = rightChicken - 1
        newLeftChicken = leftChicken + 1
        newLeftWolf = leftWolf + 1
        newRightWolf = rightWolf - 1
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick 1 wolf from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # two wolves
        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newLeftWolf = leftWolf + 2
        newRightWolf = rightWolf - 2
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 wolves from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

    # moving from left to right
    else:
        # one chicken
        newRightChicken = rightChicken + 1
        newLeftChicken = leftChicken - 1
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # two chickens
        newRightChicken = rightChicken + 2
        newLeftChicken = leftChicken - 2
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 chicks from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):

            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # one wolf

        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newRightWolf = rightWolf + 1
        newLeftWolf = leftWolf - 1
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 wolf from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # one wolf one chicken
        newRightChicken = rightChicken + 1
        newLeftChicken = leftChicken - 1
        newRightWolf = rightWolf + 1
        newLeftWolf = leftWolf - 1
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick 1 wolf from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)

        # two wolves
        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newRightWolf = rightWolf + 2
        newLeftWolf = leftWolf - 2
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 wolves from left to right: ')

        if isExpansionLegal(newNode, exploredNodes):
            # print(newNode.leftBank)

            # print(newNode.rightBank)
            newNode.cameFrom = currentNode
            addToFrontier(newNode, frontier)


def addToFrontier(node, frontier):
    if node not in frontier:
        frontier.append(node)


def isExpansionLegal(node, exploredNodes):
    # print('--- checking if legal. ')
    # print('Left:', node.leftBank)
    # print('Right:', node.rightBank)
    # print('---- checking if explored. Left:', str(node.leftBank),
    #       '  - exploredNodes: ', exploredNodes)

    # if the node is in explored nodes

    # check leftbank: wolf > chicken
    if ((node.leftBank[1] > node.leftBank[0]) and node.leftBank[0] != 0) or (
        (node.rightBank[1] > node.rightBank[0]) and node.rightBank[0] != 0
    ):
        # print("new node is ILLEGAL because wolves > chicken\n")
        return False
    # cases where you move 2 chickens or 2 wolves
    if (
        node.leftBank[1] < 0
        or node.leftBank[0] < 0
        or node.rightBank[1] < 0
        or node.rightBank[0] < 0
        or node.rightBank[2] < 0
        or node.leftBank[2] < 0
    ):
        # print("new node is ILLEGAL because negative numbers\n")
        return False
    if str(node.leftBank) in exploredNodes:

        return False
    else:
        exploredNodes[str(node.leftBank)] = node.leftBank
    # print("===== new node is valid\n")
    return True


def isExpansionLegalDLS(node):
    # check leftbank: wolf > chicken
    if ((node.leftBank[1] > node.leftBank[0]) and node.leftBank[0] != 0) or (
        (node.rightBank[1] > node.rightBank[0]) and node.rightBank[0] != 0
    ):
        # print("new node is ILLEGAL because wolves > chicken\n")
        return False
    # cases where you move 2 chickens or 2 wolves
    if (
        node.leftBank[1] < 0
        or node.leftBank[0] < 0
        or node.rightBank[1] < 0
        or node.rightBank[0] < 0
        or node.rightBank[2] < 0
        or node.leftBank[2] < 0
    ):
        # print("new node is ILLEGAL because negative numbers\n")
        return False

    return True


nodeCutOff = Node({"leftBank": [-1, -1, -1], "rightBank": [-1, -1, -1]})
nodeNoSolution = Node({"leftBank": [-2, -2, -2], "rightBank": [-2, -2, -2]})


def iterativeDeepeningDepthFirstSearch(initState, goalState, outputFile):
    initNode = Node(initState)
    goalNode = Node(goalState)
    depth = 0
    nodeExpanded = 0
    while True:
        exploredNodes = {}
        result, count = depthLimitedSearch(initNode, goalNode, depth, exploredNodes, nodeExpanded)
        nodeExpanded += count
        if result == nodeNoSolution:
            # print("XXXX No solution AT ALL. FAILURE")
            return reconstructPath(Node(initState), outputFile, nodeExpanded)
        elif result == nodeCutOff:
            # print("Can't find solution at this depth. Increment depth")
            depth += 1

        else:
            # print("goalNode parent: ", result.cameFrom)
            # print("Node Expanded: ", nodeExpanded)
            path = reconstructPath(result, outputFile, nodeExpanded)
            print("\nNumber of nodes expanded: ", nodeExpanded)
            print("Number of nodes in path: ", len(path))
            return path


def depthLimitedSearch(initNode, goalNode, limit, exploredNodes, nodeExpanded):
    return recursiveDLS(initNode, goalNode, limit, exploredNodes, nodeExpanded)


def recursiveDLS(node, goalNode, limit, exploredNodes, nodeExpanded):
    # nodeExpanded = 0
    if node.leftBank == goalNode.leftBank:
        print("!!! FOUND THE SOLUTION !!!")
        return node, nodeExpanded
    elif limit == 0:
        # return -1 if there's no solution within this depth limit
        # print("No solution for this depth limit: ", depth)
        return nodeCutOff, nodeExpanded
    else:
        cutoffOccurred = False
        for action in Actions:
            nodeExpanded += 1

            child = depthLimitExpandNode(node, action)
            if not isExpansionLegalDLS(child) or str(child.leftBank) in exploredNodes:
                continue
            child.cameFrom = node
            exploredNodes[str(child.leftBank)] = child.leftBank

            result, _ = recursiveDLS(child, goalNode, limit - 1, exploredNodes, nodeExpanded)
            if result == nodeCutOff:
                cutoffOccurred = True
            elif result != nodeNoSolution:
                # print("No solution at all failure -2")
                return result, nodeExpanded

        if cutoffOccurred:
            # print("Returning cutoff -1")
            return nodeCutOff, nodeExpanded
        else:
            # print("THIS PROBLEM HAS NO SULUTION, returning -2")
            # return -2 if failure, meaning no solution for all depths
            return nodeNoSolution, nodeExpanded


def breadthFirstSearch(initState, goalState, outputFile):
    print("\n\n======== Checking Breadth First Search\n")
    nodeExpanded = 0
    exploredNodes = {}
    # only use append or pop
    frontier = []
    initNode = Node(initState)
    goalNode = Node(goalState)
    frontier.append(initNode)

    while len(frontier) > 0:
        # print(exploredNodes)
        # for i in range(50):
        # print("Frontier length: ", len(frontier))
        # print("ExploredNodes length: ", len(exploredNodes))
        curNode = frontier.pop(0)  # FIFO
        exploredNodes[str(curNode.leftBank)] = curNode.leftBank
        # check for goal
        if curNode.leftBank == goalNode.leftBank:
            print("!!! FOUND THE SOULTION !!!")
            exploredNodes[str(curNode.leftBank)] = curNode.leftBank
            goalNode.cameFrom = curNode.cameFrom
            break
        else:
            # expand this curNode
            nodeExpanded += 1
            expandNode(curNode, exploredNodes, frontier)

    path = reconstructPath(curNode, outputFile, nodeExpanded)
    # print("Explored List: ", exploredNodes)
    # for i in frontier:
    #     print("Frontier: ", i.leftBank)
    print("\nNumber of nodes expanded: ", len(exploredNodes))
    print("Number of nodes in path: ", len(path))
    return path


def aStarSearch(initState, goalState, outputFile):
    nodeExpanded = 0
    initNode = Node(initState)
    goalNode = Node(goalState)
    initNode.distanceFromStart = 0
    initNode.distanceToEnd = heuristic(initNode, goalNode) + initNode.distanceFromStart

    # Heap operations: insert(), remove(), containsNode()
    frontier = []
    heapq.heappush(frontier, initNode)
    # frontier = MinHeap([initNode])

    exploredNodes = {}

    # expand all children
    # while not frontier.isEmpty():
    while True:
        try:
            curNode = heapq.heappop(frontier)
            # print("tuple: ", curNode[0])
        except IndexError:
            break

        exploredNodes[str(curNode.leftBank)] = curNode.leftBank
        # check for goal
        if curNode.leftBank == goalNode.leftBank:
            print("!!! FOUND THE SOLUTION !!!")
            exploredNodes[str(curNode.leftBank)] = curNode.leftBank
            goalNode.cameFrom = curNode.cameFrom
            break
        else:
            # expand this curNode
            nodeExpanded += 1
            aStarExpand(curNode, exploredNodes, frontier, goalNode)
    path = reconstructPath(curNode, outputFile, nodeExpanded)

    print("\nNumber of nodes expanded: ", nodeExpanded)
    print("Number of nodes in path: ", len(path))
    return path


def aStarExpand(currentNode, exploredNodes, frontier, goalNode):
    leftChicken = currentNode.leftBank[0]
    leftWolf = currentNode.leftBank[1]
    # leftBoat = currentNode.leftBank[2]

    rightChicken = currentNode.rightBank[0]
    rightWolf = currentNode.rightBank[1]
    rightBoat = currentNode.rightBank[2]

    # if boat is on the right bank
    if rightBoat == 1:
        # one chicken
        newRightChicken = rightChicken - 1
        newLeftChicken = leftChicken + 1
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # two chickens
        newRightChicken = rightChicken - 2
        newLeftChicken = leftChicken + 2
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 chicks from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # one wolf

        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newLeftWolf = leftWolf + 1
        newRightWolf = rightWolf - 1
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 wolf from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # one wolf one chicken
        newRightChicken = rightChicken - 1
        newLeftChicken = leftChicken + 1
        newLeftWolf = leftWolf + 1
        newRightWolf = rightWolf - 1
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick 1 wolf from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # two wolves
        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newLeftWolf = leftWolf + 2
        newRightWolf = rightWolf - 2
        newLeftBoat = 1
        newRightBoat = 0
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 wolves from right to left: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

    # moving from left to right
    else:
        # one chicken
        newRightChicken = rightChicken + 1
        newLeftChicken = leftChicken - 1
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # two chickens
        newRightChicken = rightChicken + 2
        newLeftChicken = leftChicken - 2
        newLeftWolf = leftWolf
        newRightWolf = rightWolf
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 chicks from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):

            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # one wolf

        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newRightWolf = rightWolf + 1
        newLeftWolf = leftWolf - 1
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 wolf from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # one wolf one chicken
        newRightChicken = rightChicken + 1
        newLeftChicken = leftChicken - 1
        newRightWolf = rightWolf + 1
        newLeftWolf = leftWolf - 1
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 1 chick 1 wolf from left to right: ')
        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)

        # two wolves
        newRightChicken = rightChicken
        newLeftChicken = leftChicken
        newRightWolf = rightWolf + 2
        newLeftWolf = leftWolf - 2
        newLeftBoat = 0
        newRightBoat = 1
        newNode = Node(
            {
                "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                "rightBank": [newRightChicken, newRightWolf, newRightBoat],
            }
        )
        # print('move 2 wolves from left to right: ')

        if isExpansionLegal(newNode, exploredNodes):
            newNode.cameFrom = currentNode
            newNode.distanceFromStart = currentNode.distanceFromStart + 1
            newNode.distanceToEnd = newNode.distanceFromStart + heuristic(newNode, goalNode)
            heapq.heappush(frontier, newNode)


def heuristic(currentNode, goalNode):
    cost = 0
    cost += abs(currentNode.leftBank[0] - goalNode.leftBank[0])
    cost += abs(currentNode.leftBank[1] - goalNode.leftBank[1])
    # cost += abs(currentNode.leftBank[2] - goalNode.leftBank[2])

    cost += abs(currentNode.rightBank[0] - goalNode.rightBank[0])
    cost += abs(currentNode.rightBank[1] - goalNode.rightBank[1])
    # cost += abs(currentNode.rightBank[2] - goalNode.rightBank[2])

    return cost


def QuanHeuristic(node):
    return node.rightBank[0] + node.rightBank[1]


################################################################
# Quan's Expand
def depthLimitExpandNode(currentNode, action):

    leftChicken = currentNode.leftBank[0]
    leftWolf = currentNode.leftBank[1]
    # leftBoat = currentNode.leftBank[2]

    rightChicken = currentNode.rightBank[0]
    rightWolf = currentNode.rightBank[1]
    rightBoat = currentNode.rightBank[2]

    # if boat is on the right bank
    if rightBoat == 1:
        # one chicken
        if action == "oneChicken":
            newRightChicken = rightChicken - 1
            newLeftChicken = leftChicken + 1
            newLeftWolf = leftWolf
            newRightWolf = rightWolf
            newLeftBoat = 1
            newRightBoat = 0
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 chick from right to left: ')
            # if isExpansionLegalDLS(newNode):
            #     newNode.cameFrom = currentNode
            #     return newNode

        # two chickens
        elif action == "twoChickens":
            newRightChicken = rightChicken - 2
            newLeftChicken = leftChicken + 2
            newLeftWolf = leftWolf
            newRightWolf = rightWolf
            newLeftBoat = 1
            newRightBoat = 0
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 2 chicks from right to left: ')

        # one wolf one chicken
        elif action == "oneOfEach":
            newRightChicken = rightChicken - 1
            newLeftChicken = leftChicken + 1
            newLeftWolf = leftWolf + 1
            newRightWolf = rightWolf - 1
            newLeftBoat = 1
            newRightBoat = 0
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 chick 1 wolf from right to left: ')

        # one wolf
        elif action == "oneWolf":
            newRightChicken = rightChicken
            newLeftChicken = leftChicken
            newLeftWolf = leftWolf + 1
            newRightWolf = rightWolf - 1
            newLeftBoat = 1
            newRightBoat = 0
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 wolf from right to left: ')

        elif action == "twoWolves":
            # two wolves
            newRightChicken = rightChicken
            newLeftChicken = leftChicken
            newLeftWolf = leftWolf + 2
            newRightWolf = rightWolf - 2
            newLeftBoat = 1
            newRightBoat = 0
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 2 wolves from right to left: ')

    # moving from left to right
    else:
        # one chicken
        if action == "oneChicken":

            newRightChicken = rightChicken + 1
            newLeftChicken = leftChicken - 1
            newLeftWolf = leftWolf
            newRightWolf = rightWolf
            newLeftBoat = 0
            newRightBoat = 1
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 chick from left to right: ')

        # two chickens
        elif action == "twoChickens":

            newRightChicken = rightChicken + 2
            newLeftChicken = leftChicken - 2
            newLeftWolf = leftWolf
            newRightWolf = rightWolf
            newLeftBoat = 0
            newRightBoat = 1
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 2 chicks from left to right: ')

        # one wolf one chicken
        elif action == "oneOfEach":

            newRightChicken = rightChicken + 1
            newLeftChicken = leftChicken - 1
            newRightWolf = rightWolf + 1
            newLeftWolf = leftWolf - 1
            newLeftBoat = 0
            newRightBoat = 1
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 chick 1 wolf from left to right: ')

        # one wolf
        elif action == "oneWolf":

            newRightChicken = rightChicken
            newLeftChicken = leftChicken
            newRightWolf = rightWolf + 1
            newLeftWolf = leftWolf - 1
            newLeftBoat = 0
            newRightBoat = 1
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 1 wolf from left to right: ')

        # two wolves
        elif action == "twoWolves":

            newRightChicken = rightChicken
            newLeftChicken = leftChicken
            newRightWolf = rightWolf + 2
            newLeftWolf = leftWolf - 2
            newLeftBoat = 0
            newRightBoat = 1
            newNode = Node(
                {
                    "leftBank": [newLeftChicken, newLeftWolf, newLeftBoat],
                    "rightBank": [newRightChicken, newRightWolf, newRightBoat],
                }
            )
            # print('move 2 wolves from left to right: ')

    return newNode


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("to run, call chicken.py < initial state file > < goal state file > < mode > < output file >")
        quit()

    initial_state_file = sys.argv[1]
    goal_state_file = sys.argv[2]
    mode = sys.argv[3]
    output_file = sys.argv[4]
    # initial_state_file = "start1.txt"
    # goal_state_file = "goal1.txt"
    # mode = "astar"
    # output_file = "output.txt"

    # parse files
    initState = readFile(initial_state_file)
    goalState = readFile(goal_state_file)

    # getMode(mode, initState, goalState)
    print("\n------ mode: ", mode)
    if mode == "bfs":
        # QuanBreadthFirstSearch(initState, goalState)
        breadthFirstSearch(initState, goalState, output_file)
    elif mode == "dfs":
        depthFirstSearch(initState, goalState, output_file)
    elif mode == "iddfs":
        iterativeDeepeningDepthFirstSearch(initState, goalState, output_file)
    elif mode == "astar":
        aStarSearch(initState, goalState, output_file)
