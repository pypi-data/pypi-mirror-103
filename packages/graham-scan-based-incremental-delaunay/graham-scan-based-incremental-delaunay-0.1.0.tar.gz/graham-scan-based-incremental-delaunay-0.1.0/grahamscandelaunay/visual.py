from point import *
from random import randrange
import pyglet
from pyglet import shapes
from pyglet.window import key,mouse
from grahamscandelaunay import *
from copy import deepcopy
W,H = 1280, 720
window =pyglet.window.Window(W,H)

def pt_1(p):
    shapes.Circle(p[0],p[1],5,segments=12,color=(192,192,192)).draw()
def pt_2(p):
    shapes.Circle(p[0],p[1],5,segments=12,color=(0,0,0)).draw()
def pt_3(p):
    shapes.Circle(p[0],p[1],5,segments=12,color=(255,0,0)).draw()
def line_1(a,b):
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(128,128,128)).draw()
def line_2(a,b):
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(0,0,255)).draw()
def line_3(a,b):
    shapes.Line(a[0],a[1],b[0],b[1],width=3,color=(0,192,0)).draw()
def randpt():
    margin = 100
    return  Point(randrange(margin,W-margin),randrange(margin,H-margin))

V = []
ready = False
done = False
state = None
stepofthealgorithm = None
@window.event
def on_mouse_press(x,y,button,modifiers):
    if not ready and button == mouse.LEFT:
        V.append(Point(x,y))

@window.event
def on_key_press(symbol,modifiers):
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
        if len(V) < 3:
            return
        g = GrahamScanDelaunay(V)
        stepofthealgorithm = g.run()
        state = next(stepofthealgorithm)
        ready = True
    elif ready and symbol == key.SPACE: # next
        try:
            state = next(stepofthealgorithm)
            save_state(state)
            print("NEXT")
        except StopIteration:
            done = True
            state = load_state()
            save_state(state)
            print("STOP")
            pass

@window.event
def on_draw():
    shapes.Rectangle(0,0,W,H,(255,255,255)).draw()
    if done:
        shapes.Rectangle(0,0,W,H,(0,255,0)).draw()
    pts = []
    for v in V:
        pt_1(v)
    if ready:
        for halfedge in state[1]: # draw edges
            pts.append(halfedge.point)
            line_1(halfedge.point,halfedge.link.point)
        if len(state[2]) > 0: # highlight current edge
            for h in state[2]: #color queued edges
                line_3(h.point, h.link.point)
            line_2(state[2][0].point,state[2][0].link.point)
        for p in pts: # draw points
            pt_2(p)
        if state[0] is not None: # highlight current pt
            pt_3(state[0])
    
savestate = None
def save_state(state):
    global savestate
    savestate = deepcopy(state)
def load_state():
    return savestate
pyglet.app.run()
