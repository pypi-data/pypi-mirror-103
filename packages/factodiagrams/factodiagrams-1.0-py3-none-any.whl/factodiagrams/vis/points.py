import math


# Point class
class Point:
    """Definition of a geometric point (x, y).
    """
    def __init__(self, x, y):
        self.x = x  # Point x position
        self.y = y  # Point y position


# Generate and distribute points
def generatePoints(factors):
    """Returns the position of each point according to the number to decompose.

    :param factors: list containing the prime factorization of a number.
    :return: list of coordinates for each point
    :rtype: list of Point object
    """
    # initialize variables
    parentPoints = []
    points = []
    a = 0
    x = 0
    y = 0
    da = 0

    point = 0
    n = 1
    d = 1

    if factors == [1]:
        return [Point(0, 0)]
    # Instantiate points for each prime factors
    while (len(factors)):
        d = d * n * 0.85  # scale depth
        n = factors.pop()  # build points from outwards

        # Compute offset
        if(n == 4):
            da = - math.pi / 4

        elif(n == 2):
            da = - math.pi / 2
        else:
            da = math.pi / 2

        if (len(points) == 0):  # check for first set of points
            for i in range(n):
                a = i * 2 * math.pi / n + da
                x = math.cos(a)
                y = math.sin(a)
                point = Point(x, y)
                points.append(point)
        else:  # iteratively build points by keeping track of parentPoints
            if(n == 2):  # rotation of groups of 2 to align with their parent points
                # for prime numbers times 2 (double circle) - aligned with absolute center (0,0)
                if (len(parentPoints) == 0):
                    # create shallow copy of points
                    parentPoints = list(points)
                    points = []  # reset points
                    for parentPoint in parentPoints:
                        for i in range(n):
                            x = parentPoint.x + (1-2*i)*parentPoint.x / d
                            y = parentPoint.y + (1-2*i)*parentPoint.y / d
                            point = Point(x, y)
                            points.append(point)
                else:  # for every other group of 2 - aligned with their 'grandparent points'
                    # create shallow copy of points without deleting previous parent points ('grandparent points')
                    parentPoints2 = list(points)
                    points = []  # reset points
                    j = 0
                    for parentPoint2 in parentPoints2:
                        coef = len(parentPoints2)/len(parentPoints)
                        for i in range(n):
                            x = parentPoints[int(
                                j//coef)].x + (parentPoint2.x - parentPoints[int(j//coef)].x) * (1.5-i*0.8)
                            y = parentPoints[int(
                                j//coef)].y + (parentPoint2.y - parentPoints[int(j//coef)].y) * (1.5-i*0.8)
                            point = Point(x, y)
                            points.append(point)
                        j += 1
            else:
                parentPoints = list(points)  # create shallow copy of points
                points = []  # reset points
                for parentPoint in parentPoints:  # build new points using parentPoints
                    for i in range(n):
                        a = i * 2 * math.pi / n + da
                        x = parentPoint.x + math.cos(a) / d
                        y = parentPoint.y + math.sin(a) / d
                        point = Point(x, y)
                        points.append(point)
    return points
