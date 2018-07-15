from pygame import math
from pygame import draw
from math import degrees
def polars(ps,origin=math.Vector2(0,0),angd=0):
    for r,phi in ps:
        v=math.Vector2()
        v.from_polar((r,degrees(phi+angd)))
        yield v+origin
def tuplise(vlist):
    return [(v.x,v.y) for v in vlist]
def ppolygon(screen,ps,centre,angle,col,outline=None,thicc=1):
    points=tuplise(polars(ps,centre,angle))
    draw.polygon(screen,col,points)
    if outline:
        draw.polygon(screen,outline,points,thicc)
