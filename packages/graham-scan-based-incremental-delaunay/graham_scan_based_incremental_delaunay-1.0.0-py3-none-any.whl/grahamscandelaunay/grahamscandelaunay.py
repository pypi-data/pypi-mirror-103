from . import point
from collections import deque
import numpy
numpy.seterr(all='raise')

class HalfEdge:
    """This class represents a HalfEdge in a HalfEdge data structure."""

    def __init__(self, point, link = None, prev = None, twin = None):
        """
        Parameters
        -----------
        point : Point
            The start point for the half edge

        link : HalfEdge
            The next HalfEdge that this HalfEdge points to
        
        prev : HalfEdge
            the previous HalfEdge that links to this HalfEdge
        
        twin : HalfEdge
            The twin HalfEdge of this HalfEdge
        """
        self.point = point
        self.link = link
        self.prev = prev
        self.twin = twin

class GrahamScanDelaunay:
    """This class represents an instance of the Graham Scan Based Incremenatal Delaunay algorithm."""
    def __init__(self, V):
        """
        The __init__ method will sort the points to be in ccw order. It will also create the stack, queue,
        and a list of edges used in the incremental algorithm.

        Parameters
        -----------
        V : List
            The List of Point objects for the incremental delaunay algorithm to run on.

        Attributes
        --------------
        V : List
            The list of Point objects for the incremental delaunay algorithm to run on.

        stack : Deque
            The stack maintains the edges on the convex hull.

        q : Deque
            q is a queue that maintains the edges that need to be checked to see if they are delaunay.

        edges : Deque
            This is a list of all the edges that are in the triangulation.

        flips : Integer
            Maintains a count of the number of edges that have been fliped to be locally delaunay
        """
        # Assume General Position: No 3 points in V are collinear
        # and no 4 points in V are cocircular

        # Sort the points
        self.V = self._sort_points(V)
        
        # Initializing Data Structures
        self.stack = deque() # Convex Hull Half Edge Stack
        self.q = deque() # Delaunay Half Edge Queue
        self.edges = deque() # List of All Edges
        self.flips = 0

    # Yields the current iteration, the sorted list of points, and the edges in the triangulation
    def run(self):
        """ This method is used to run the graham scan based incremental delaunay algorithm.

        It yeilds the state of the algorithm at each iteration to the visualization.
        This method starts out by first creating a base triangle of the first 3 points from the list of points
        sorted in CCW order. 

        It then incrementally adds another point to the triangularization. It does this by running the graham
        scan algorithm to get the next edge of the convex hull, then adds the edge from the initial point to the 
        current point, and then checks to see if the edge added is locally delaunay. If it is delaunay, we proceed
        to the next point. If it is not delaunay, we flip the edge.
        """

        n=len(self.V)

        # Construct base triangle
        base = [self.V[0], self.V[1], self.V[2]]

        # Convert triangle into half-edges
        outside = [HalfEdge(p) for p in base]
        inside = [HalfEdge(p) for p in base]
        for i in range(3):
            outside[i - 1].twin = inside[i]
            inside[i].twin = outside[i - 1]

            outside[i - 1].link = outside[i]
            outside[i].prev = outside[i - 1]

            inside[i].link = inside[i - 1]
            inside[i - 1].prev = inside[i]
            self.stack.append(outside[i])
            self.edges.append(outside[i])

        # Return base triangle for visualization
        yield self._get_vis_data()

        # Incrementally add to the triangulation
        for i in range(3, n):
            yield from self._incrementhull(self.V[i])
            yield self._get_vis_data(self.V[i], True) # Data to visualize after convex hull
            # Check if the new edges need to be flipped
            while len(self.q) > 0:
                self._isdelaunay(self.q.popleft())
                yield self._get_vis_data(self.V[i], True) # Data to visualize after delaunay check

    # Returns a list of halfedges for visualization purposes
    def _getedges(self):
        return iter(self.edges)

    # Returns the current edge being checked for visualization purposes
    # If the queue is empty, return None
    def _currentedge(self):
        return self.q[0] if len(self.q) > 0 else None

    # Given the index of the current point, returns a list for visualization purposes
    def _get_vis_data(self, currentpt = None, delaunay_step = False):
        cc = None
        if delaunay_step and len(self.q) > 0 and not self._isOutside(self.q[0]) :
            cc = self._getCircumcenter(self.q[0])
        return [currentpt, self._getedges(), self.q, self.stack, cc, delaunay_step, self.flips]

    # returns the circumcenter of the triangle the halfedge is in
    def _getCircumcenter(self, h):
        return point.circumcenter(h.point, h.prev.point, h.link.point)

    # returns whether the edge is on the convex hull
    def _isOutside(self, h):
        return h in self.stack or h.twin in self.stack


    # Connects an edge from a.point to b.point
    # Assumes a and b are the outside halfedges
    # During the convex hull process
    def _addedge(self, a, b):
        c = HalfEdge(a.point, b, a.prev)
        d = HalfEdge(b.point, a, b.prev, c)
        c.twin = d
        a.prev.link = c
        b.prev.link = d
        a.prev = d
        b.prev = c
        # Push new edge into the Delaunay Edge Queue
        self.q.append(c)
        self.edges.append(c)
        return c

    # Connects an edge from a.point to p
    # a is the outside halfedge and p is a point
    # Only used for the convex hull
    def _addleaf(self, a, p):
        h = HalfEdge(p, a)
        t = HalfEdge(a.point, h, a.prev, h)
        h.prev = t
        h.twin = t
        a.prev.link = t
        a.prev = h
        # Push new edge into the Delaunay Edge Queue
        self.q.append(h)
        self.edges.append(t)
        return h
    
    # Use the convex hull algorithm to add edges to the triangulation
    def _incrementhull(self, p):
        # Connect the top point of the stack to the new point
        self._addleaf(self.stack[-1], p)
        yield self._get_vis_data(p)
        h = self.q[-1] # Halfedge from p
        # Run graham scan to see if backtracking is needed
        while (point.orient(self.stack[-2].point, self.stack[-1].point, p) != 1):
            self.q.append(self.stack.pop())
            self._addedge(self.stack[-1], h)
            yield self._get_vis_data(p)
        # Connect the new point to the first point
        self._addedge(h, self.stack[0])
        yield self._get_vis_data(p)
        # Add the convex hull outside halfedge to the stack
        # self.q.append(h.link)
        h2 = self.stack.pop()
        if h2 not in self.q and h.twin not in self.q:
            self.q.append(h2)
        self.stack.append(h.prev.twin.prev)
        self.stack.append(h.prev.twin)
        
    
    # check if edge is locally delaunay; returns false if the edge is flipped
    def _isdelaunay(self, h):
        # Outside edge, do not flip
        if self._isOutside(h):
            return
        # if not locally delaunay, flip the edge
        if point.incircle(h.point, h.prev.point, h.link.point, h.twin.prev.point) > 0:
            self._flipedge(h)
            self.flips += 1
            return False
        return True

    # Flip the current edge
    def _flipedge(self, h):
        # Link the quad toegether
        h.prev.link = h.twin.link
        h.twin.prev.link = h.link
        h.link.prev = h.twin.prev
        h.twin.link.prev = h.prev
        # Flip the edge
        h.link = h.prev
        h.twin.link = h.twin.prev
        h.prev = h.twin.link.prev
        h.twin.prev = h.link.prev
        # Link the quad back to the edge
        h.link.prev = h
        h.twin.link.prev = h.twin
        h.prev.link = h
        h.twin.prev.link = h.twin
        h.point = h.twin.link.point
        h.twin.point = h.link.point
        # Push the neighboring edges into the Delaunay Queue
        self.q.append(h.link)
        self.q.append(h.prev)
        self.q.append(h.twin.link)
        self.q.append(h.twin.prev)
        return
    
    # Sort the points such that the first point of the list
    # is the bottomleftmost, and the remaining points
    # are sorted in ascending order of their slope
    # with respect to the first point
    def _sort_points(self, V):
        leftmost = min(V, key = lambda p: p)
        _V = sorted(V, key = lambda p: point.slope(leftmost, p))
        return _V
