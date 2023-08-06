from point import *
from collections import deque
import numpy
numpy.seterr(all='raise')

class HalfEdge:
    def __init__(self, point, link = None, prev = None, twin = None):
        self.point = point
        self.link = link
        self.prev = prev
        self.twin = twin

class GrahamScanDelaunay:
    def __init__(self, V):
        # Assume General Position: No 3 points in V are collinear
        # and no 4 points in V are cocircular

        # Sort the points
        self.V = self._sort_points(V)
        
        # Initializing Data Structures
        self.stack = deque() # Convex Hull Half Edge Stack
        self.q = deque() # Delaunay Half Edge Queue
        self.edges = deque() # List of All Edges

    # Yields the current iteration, the sorted list of points, and the edges in the triangulation
    def run(self):
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
            self._incrementhull(self.V[i])
            yield self._get_vis_data(i) # Data to visualize after convex hull
            # Check if the new edges need to be flipped
            while len(self.q) > 0:
                print("Printing self.q")
                for h in self.q:
                    print(h.point)
                print("checking isdelaunay()")
                self._isdelaunay(self.q.popleft())
                yield self._get_vis_data(i) # Data to visualize after delaunay check

    # Returns a list of halfedges for visualization purposes
    def _getedges(self):
        return iter(self.edges)

    # Returns the current edge being checked for visualization purposes
    # If the queue is empty, return None
    def _currentedge(self):
        return self.q[0] if len(self.q) > 0 else None

    # Given the index of the current point, returns a list for visualization purposes
    def _get_vis_data(self, i = 0):
        currentpt = None
        if i >= 3:
            currentpt = self.V[i]
        return [currentpt, self._getedges(), self.q, self.stack]


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
        h = self.q[-1] # Halfedge from p
        # Run graham scan to see if backtracking is needed
        while (orient(self.stack[-2].point, self.stack[-1].point, p) != 1):
            self.stack.pop()
            self._addedge(self.stack[-1], h)
        # Connect the new point to the first point
        self._addedge(h, self.stack[0])
        # Add the convex hull outside halfedge to the stack
        self.q.append(h.link)
        h2 = self.stack.pop()
        if h2 not in self.q and h.twin not in self.q:
            self.q.append(h2)
        self.stack.append(h.prev.twin.prev)
        self.stack.append(h.prev.twin)
        return
        
    
    # check if edge is locally delaunay
    def _isdelaunay(self, h):
        # Outside edge, do not flip
        if h in self.stack or h.twin in self.stack:
            print(h.point, ' is an outside edge, no need to do incircle test')
            return
        # if not locally delaunay, flip the edge
        print("Checking incircle(", h.point, h.prev.point, h.link.point, h.twin.prev.point, ")")
        print("Incircle returns: ", incircle(h.point, h.prev.point, h.link.point, h.twin.prev.point))
        if incircle(h.point, h.prev.point, h.link.point, h.twin.prev.point) > 0:
            print("Flipping Edge")
            self._flipedge(h)
        return

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
        n = len(V)
        # Sort by x-coordinates to get the first point
        _V = sorted(V)
        
        # Map each point to the slope relative to the bottomleftmost point
        pairs = [(_V[0], float('-inf'))]
        for i in range(1,n):
            pairs.append((_V[i], slope(_V[0], _V[i])))

        pairs = pairs[0:1] + sorted(pairs[1:], key=lambda p: p[1]) # Sort by slope

        # Return the list of points
        output = []
        for p in pairs:
            output.append(p[0])
        return output