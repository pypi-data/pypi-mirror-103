from numpy import array, append, cross, sign, seterr, around, array_equal
from numpy.linalg import det, solve
seterr(all='raise')

def dist(p,q):
    """ Calculates the distance between the points p and q.

    Parameters
    ---------
    p : Point
        the first point
    
    q : Point
        the second point

    Returns
    ----------
    Float
        The distance between the points p and q.
    """
    return (sum((p.array()-q.array())**2))**0.5

def orient(*points):
    """ Performs the ccw test to determine the orientation of the points.

    Parameters:
    -------------
    points : Points
        An arbitrary number of Points to determine the orientation of

    Returns
    -------
    Integer
        Returns 1 if the points are ordered in ccw order. Returns -1 if the points are ordered in clockwise order.
        Returns 0 if the points are colinear.
    """
    points = [p.array() for p in points]
    d = det(array(points))
    if d > 0:
        return 1
    elif d < 0:
        return -1
    else:
        return 0

def incircle(a,b,c,d):
    """ Determines if the Point d is inside of the circle formed by the traingle a,b,c.

    Parameters
    ------------
    a : Point
        The first point of the triangle

    b : Point
        the second point on the triangle

    c : Point
        The third point on the triangle
    
    Returns
    -------------
    Integer
        Returns 0 if the point d is on the circle. Returns -1 if the point d lies outside the circle
        Returns 1 if the point d lies inside the circle.
    """

    
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
    """Finds the circumcenter of a triangle.

    Parameters
    ------------
    a : Point
        The first point of the triangle
    
    b : Point
        the second point of the triangle

    c : Point
        the third point of the triangle

    Returns
    -------------
    Point
        The circumcenter of the triangle
    """
    zero = Point(0,0)
    d = 2*((a[0]*(b[1]-c[1])) + (b[0]*(c[1]-a[1])) + (c[0]*(a[1]-b[1])))
    x = ((dist(a, zero)**2)*(b[1]-c[1]) + (dist(b, zero)**2)*(c[1]-a[1]) + (dist(c, zero)**2)*(a[1]-b[1])) / d
    y = ((dist(a, zero)**2)*(c[0]-b[0]) + (dist(b, zero)**2)*(a[0]-c[0]) + (dist(c, zero)**2)*(b[0]-a[0])) / d
    return Point(x,y)

# Slope from a to b
def slope(a,b):
    """ Gets the slope between two points.

    Parameters
    -------------
    a : Point
        The first point in the slope calculation.

    b : Point
        The second point is the slope calculation.

    Returns
    ------------
    Float
        The slope between the two points. If we have the case where we divide by zero, if b[1] > a[1], then
        we return float('inf'). Otherwise, returns float('-inf').
    """
    try:
        return (b[1]-a[1]) / (b[0]-a[0])
    except (ZeroDivisionError, RuntimeWarning, FloatingPointError) as e:
        if (b[1] > a[1]):
            return float('inf')
        else:
            return float('-inf')

class Point:
    """This class represents a point that has been lifted up to some z plane."""

    def __init__(self, *coordinates, z = 1):
        """
        Parameters
        --------------

        coordinates : Integers or Floats
            An arbitrary number of Intergers and Floats that correspond to the coordinates of the point to be created.

        z : Integer
            The z plane for the coordinate to be lifted up to. Defaults to z=1.
        """

        self._p = append(coordinates, z)

    def array(self):
        """Gets an array of the coordinates of the point.

        Returns
        ----------
        numpy.Array
            An array containing the coordinates of the point.
        """
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



