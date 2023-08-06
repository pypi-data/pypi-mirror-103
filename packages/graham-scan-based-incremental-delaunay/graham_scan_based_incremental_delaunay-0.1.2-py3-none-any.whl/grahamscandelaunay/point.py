from numpy import array, append, cross, sign, seterr, around, array_equal
from numpy.linalg import det, solve
seterr(all='raise')

def dist(p,q):
    return (sum((p.array()-q.array())**2))**0.5

def orient(*points):
    points = [p.array() for p in points]
    d = det(array(points))
    if d > 0:
        return 1
    elif d < 0:
        return -1
    else:
        return 0

def incircle(a,b,c,d):
    zero = Point(0,0)
    _a = [a[0], a[1], dist(a, zero)**2, 1]
    _b = [b[0], b[1], dist(b, zero)**2, 1]
    _c = [c[0], c[1], dist(c, zero)**2, 1]
    _d = [d[0], d[1], dist(d, zero)**2, 1]
    A = array([_a, _b, _c, _d])
    d = around(det(A),decimals=6)
    if d == 0:
      return 0
    return sign(d)*orient(a,b,c)

def circumcenter(a,b,c):
    zero = Point(0,0)
    d = 2*((a[0]*(b[1]-c[1])) + (b[0]*(c[1]-a[1])) + (c[0]*(a[1]-b[1])))
    x = ((dist(a, zero)**2)*(b[1]-c[1]) + (dist(b, zero)**2)*(c[1]-a[1]) + (dist(c, zero)**2)*(a[1]-b[1])) / d
    y = ((dist(a, zero)**2)*(c[0]-b[0]) + (dist(b, zero)**2)*(a[0]-c[0]) + (dist(c, zero)**2)*(b[0]-a[0])) / d
    return Point(x,y)

# Slope from a to b
def slope(a,b):
    try:
        return (b[1]-a[1]) / (b[0]-a[0])
    except (ZeroDivisionError, RuntimeWarning, FloatingPointError) as e:
        if (b[1] > a[1]):
            return float('inf')
        else:
            return float('-inf')

class Point:
    def __init__(self, *coordinates, z = 1):
        self._p = append(coordinates, z)

    def array(self):
        return self._p

    def __eq__(self, other):
        return array_equal(self._p, other._p)

    def __lt__(self, other):
        if (self._p[0] != other._p[0]):
            return self._p[0] < other._p[0]
        else:
            return self._p[1] < other._p[1]

    def __str__(self):
        return str(self._p[:2])

    def __getitem__(self, index):
        return self._p[index]



