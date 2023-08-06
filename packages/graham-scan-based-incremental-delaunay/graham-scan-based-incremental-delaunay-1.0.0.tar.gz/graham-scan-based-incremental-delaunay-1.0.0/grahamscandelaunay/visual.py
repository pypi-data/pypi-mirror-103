from . import point
from random import randrange
import pyglet
from pyglet import shapes
from pyglet.window import key,mouse
import grahamscandelaunay
from copy import deepcopy
W,H = 1280, 720
window =pyglet.window.Window(W,H)

def pt_1(p):
    """Draws a light grey colored point.
    
    Parameters
    -----------
    p : Point
        the point to draw.
    """
    shapes.Circle(p[0],p[1],5,segments=12,color=(192,192,192)).draw()
def pt_2(p):
    """Draws a black colored point.

    Parameters
    -----------
    p : Point
        the point to draw.
    """
    shapes.Circle(p[0],p[1],5,segments=12,color=(0,0,0)).draw()
def pt_3(p):
    """Draws a red colored point.

    Parameters
    -----------
    p : Point
        the point to draw.
    """
    shapes.Circle(p[0],p[1],5,segments=12,color=(255,0,0)).draw()
def pt_4(p):
    """Draws a rust colored point.

    Parameters
    -----------
    p : Point
        the point to draw.
    """
    shapes.Circle(p[0],p[1],5,segments=12,color=(128,0,0)).draw()
def line_1(a,b):
    """Draws a dark gray line.

    Parameters
    ------------
    a : Point
        The first point of the line
    
    b : Point
        The second point of the line
    """
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(128,128,128)).draw()
def line_2(a,b):
    """Draws a blue line.

    Parameters
    ------------
    a : Point
        The first point of the line
    
    b : Point
        The second point of the line
    """
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(0,0,255)).draw()
def line_3(a,b):
    """Draws a green line.

    Parameters
    ------------
    a : Point
        The first point of the line
    
    b : Point
        The second point of the line
    """
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(0,192,0)).draw()
def cir_1(p,r):
    """Draws a yellow circle centered at p with radius r.

    Parameters
    ------------
    p : Point
        The first point of the line
    
    r : Float
        The radius of the circle
    """
    shapes.Circle(p[0],p[1],r,color=(255,255,0)).draw()
    shapes.Circle(p[0],p[1],r-2,color=(255,255,255)).draw()
    shapes.Circle(p[0],p[1],5,segments=12,color=(255,255,0)).draw()
def randpt():
    """creates a random point within a certain margin of the width and height.
    
    Returns
    ------------
    Point
        The random Point created.
    """
    margin = 100
    return  point.Point(randrange(margin,W-margin),randrange(margin,H-margin))
def fliptext(num):
    """ Creates the visual text that shows the number of flipped edges.
    
    Parameters
    -----------
    num : Integer
        The number of flips to show on the screen.
    """
    pyglet.text.Label('Flipped edges: ' + str(num),
            font_name='Arial',
            font_size=24, color=(0,0,0,255),
            x=50, y=50,
            anchor_x='left', anchor_y='bottom').draw()
def donetext():
    """Creates the visual text that shows when the algorithm has completed."""
    pyglet.text.Label('DONE',
            font_name='Arial',
            font_size=24, color=(0,0,0,255),
            x=50, y=100,
            anchor_x='left', anchor_y='bottom').draw()

V = []
ready = False
done = False
state = None
stepofthealgorithm = None
@window.event
def on_mouse_press(x,y,button,modifiers):
    """On the click of the mouse, creates a new point at the location of the mouse pointer."""

    if not ready and button == mouse.LEFT:
        V.append(point.Point(x,y))

@window.event
def on_key_press(symbol,modifiers):
    """An event that triggers when a certain key is pressed."""

    global ready
    global state
    global stepofthealgorithm
    global V
    global done
    if ready and symbol == key.R: # reset
        ready = False
        done = False
        state = None
        stepofthealgorithm = None
    elif symbol == key.C: # clear all
        ready = False
        done = False
        state = None
        stepofthealgorithm = None
        V = []
    elif not ready and symbol == key.G: #generate randpt
        V.append(randpt())
    elif not ready and symbol == key.S: # start
        if len(V) < 4:
            return
        g = grahamscandelaunay.GrahamScanDelaunay(V)
        stepofthealgorithm = g.run()
        state = next(stepofthealgorithm)
        ready = True
    elif ready and symbol == key.SPACE: # next
        try:
            state = next(stepofthealgorithm)
            save_state(state)
        except StopIteration:
            done = True
            state = load_state()
            save_state(state)
            pass

@window.event
def on_draw():
    """ An event that triggers an draws to the window."""

    shapes.Rectangle(0,0,W,H,(255,255,255)).draw()
    if done:
        shapes.Rectangle(0,0,W,H,(224,255,224)).draw()
        donetext()
    pts = []
    if ready:
        if state[4] is not None:
            cir_1(state[4], point.dist(state[4], state[2][0].point))
    for v in V:
        pt_1(v)
    if ready:
        for halfedge in state[1]: # draw edges
            pts.append(halfedge.point)
            line_1(halfedge.point,halfedge.link.point)
        if len(state[2]) > 0: # highlight current edge
            for h in state[2]: #color queued edges
                line_3(h.point, h.link.point)
            if state[5]: 
                line_2(state[2][0].point,state[2][0].link.point)
        
        for p in pts: # draw points
            pt_2(p)
        if len(state[2]) > 0 and state[4] is not None: # highlight incircle test points
            h = state[2][0]
            pt_3(h.point)
            pt_3(h.link.point)
            pt_3(h.prev.point)
            pt_4(h.twin.prev.point)
        if state[0] is not None: # highlight current pt
            pt_3(state[0])
        fliptext(state[6])
    
savestate = None
def save_state(state):
    """ saves the state of the algorithm.
    
    Parameters
    -----------
    state : List
        The state of the algorithm containing the current point, the stack, queue, edge list, etc.
    """
    global savestate
    savestate = deepcopy(state)
def load_state():
    """ loads the state of the algorithm.

    Returns
    -----------
    List
        The state of the algorithm containing the current point, the stack, queue, edge list, etc.
    """
    return savestate
pyglet.app.run()
