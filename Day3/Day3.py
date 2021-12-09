import math

intersections = []

class Line:

    def __init__(self, p1, p2):
        self.x1 = p1[0]
        self.y1 = p1[1]
        self.x2 = p2[0]
        self.y2 = p2[1]

    def __len__(self):
        diffX = abs(self.x2 - self.x1)
        diffY = abs(self.y2 - self.y1)

        return (int)(math.sqrt(diffX * diffX + diffY * diffY))

    def isX(self) -> bool:
        return (self.x1 != self.x2)

    def isY(self) -> bool:
        return (self.y1 != self.y2)

    def containsPoint(self, point) -> bool:
        if (self.isX()):
            if (point[1] != self.y1):
                return False
            if ((point[0] <= self.x1 and point[0] >= self.x2) or (point[0] >= self.x1 and point[0] <= self.x2)):
                return True

        if (self.isY()):
            if (point[0] != self.x1):
                return False
            if ((point[1] <= self.y1 and point[1] >= self.y2) or (point[1] >= self.y1 and point[1] <= self.y2)):
                return True

        return False

    def distanceFromLineStartToPoint(self, point) -> int:
        if (self.isY()):
            return abs(self.y1 - point[1])
        if (self.isX()):
            return abs(self.x1 - point[0])

def getIntersectionPoint(l1, l2): 
    if (l1.isX()):
        x = (l1.x1 < l2.x1 and l1.x2 > l2.x1 or l1.x1 > l2.x1 and l1.x2 < l2.x1)
        y = (l2.y1 < l1.y1 and l2.y2 > l1.y1 or l2.y1 > l1.y1 and l2.y2 < l1.y1)
        if not(x and y):
            return None
    else:
        x = (l2.x1 < l1.x1 and l2.x2 > l1.x1 or l2.x1 > l1.x1 and l2.x2 < l1.x1)
        y = (l1.y1 < l2.y1 and l1.y2 > l2.y1 or l1.y1 > l2.y1 and l1.y2 < l2.y1)
        if not(x and y):
            return None

    x = l1.x1 if (l1.x1 == l1.x2) else l2.x1
    y = l1.y1 if (l1.y1 == l1.y2) else l2.y1

    intersections.append((x, y))
    return (x, y)
    
def calculateIntersectionPoints(line1, line2):
    points = []

    for i in range(len(line1) - 1):
        firstSegment = Line(line1[i], line1[i + 1])
        for j in range(len(line2) - 1):
            secondSegment = Line(line2[j], line2[j + 1])

            intersectionPoint = getIntersectionPoint(firstSegment, secondSegment)
            if intersectionPoint is not None:
                points.append(intersectionPoint)
    return points

def parseLine(lineAsString):
    x = 0
    y = 0
    points = [(0, 0)]

    for move in lineAsString.split(","):
        direction = move[0]
        distance = move[1:len(move)]
        if (direction == 'U'):
            y += int(distance)
        elif (direction == 'R'):
            x += int(distance)
        elif (direction == 'D'):
            y -= int(distance)
        else:
            x -= int(distance)
        points.append((x, y))

    return points

def Puzzle1(line1, line2):
    points = calculateIntersectionPoints(line1, line2)
    
    minDistance = None

    for point in points:
        distance = abs(point[0]) + abs(point[1])
        if minDistance == None or distance < minDistance:
            minDistance = distance

    return str(minDistance)

def calculateDistanceToFirstIntersectionPoint(line) -> int:
    distance = 0
    intersectionPoint = intersections[0]

    for i in range(len(line) - 1):
        lineSegment = Line(line[i], line[i + 1])

        if (lineSegment.containsPoint(intersectionPoint)):
            return distance + lineSegment.distanceFromLineStartToPoint(intersectionPoint)
        else:
            distance += len(lineSegment)
                

def Puzzle2(line1, line2):
    shortestDistance = calculateDistanceToFirstIntersectionPoint(line1)
    shortestDistance += calculateDistanceToFirstIntersectionPoint(line2)
    return str(shortestDistance)


if __name__ == "__main__":
    inputFile = open("input.txt", "r")
    line1 = parseLine(inputFile.readline())
    line2 = parseLine(inputFile.readline())
    print("Puzzle 1: " + Puzzle1(line1, line2))
    print("Puzzle 2: " + Puzzle2(line1, line2))