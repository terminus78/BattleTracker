def correctPlacement(coordinate, size, mapSize):
    cornerList = findCorners(coordinate, size)
    refSpace = moveOntoMap(cornerList, mapSize)
    return refSpace

def findCorners(coordinate, size):
    if size == 'large':
        offset = 1
    elif size == 'huge':
        offset = 2
    else:
        offset = 3
    topLeft = coordinate
    topRight = [
        coordinate[0] + offset,
        coordinate[1],
        coordinate[2]
        ]   
    bottomLeft = [
        coordinate[0],
        coordinate[1] + offset,
        coordinate[2]
        ]
    bottomRight = [
        coordinate[0] + offset,
        coordinate[1] + offset,
        coordinate[2]
        ]
    return [topLeft, topRight, bottomLeft, bottomRight]

def moveOntoMap(cornerList, mapSize):
    refSpace = cornerList[0]
    topRight = cornerList[1]
    bottomLeft = cornerList[2]
    bottomRight = cornerList[3]
    while checkIfInMap(cornerList, mapSize) == False:
        for corner in cornerList:
            if corner[0] < 0:
                delta = 0 - corner[0]
                refSpace[0] += delta
                topRight[0] += delta
                bottomLeft[0] += delta
                bottomRight[0] += delta
                break
            elif corner[0] > mapSize[0] - 1:
                delta = corner[0] - mapSize[0] + 1
                refSpace[0] -= delta
                topRight[0] -= delta
                bottomLeft[0] -= delta
                bottomRight[0] -= delta
                break
            if corner[1] < 0:
                delta = 0 - corner[1]
                refSpace[1] += delta
                topRight[1] += delta
                bottomLeft[1] += delta
                bottomRight[1] += delta
                break
            elif corner[1] > mapSize[1] - 1:
                delta = corner[1] - mapSize[1] + 1
                refSpace[1] -= delta
                topRight[1] -= delta
                bottomLeft[1] -= delta
                bottomRight[1] -= delta
                break
        cornerList = [refSpace, topRight, bottomLeft, bottomRight]
    return refSpace

def checkIfInMap(cornerList, mapSize):
    onMap = True
    for corner in cornerList:
        if corner[0] < 0 or corner[0] > mapSize[0] - 1:
            onMap = False
            return onMap
        if corner[1] < 0 or corner[1] > mapSize[1] - 1:
            onMap = False
            return onMap
    return onMap