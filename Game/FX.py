from math import pi,tau
from Lib import Img,Draw
from pygame.math import Vector2
from random import randint
right=pi/2
class FX(object):
    def render(self,screen,offset):
        pass
    def update(self,layer):
        pass
class Laser(FX):
    t=1
    hit=Img.imgrot("War/LaserImpact")
    colour=(255,0,0)
    def __init__(self,src,dest,angle,l):
        self.angle=-angle
        self.src=src
        self.dest=dest
        self.tri=[(4,-right),(4,right),(l,0)]
        self.i=randint(0,3)
    def render(self,screen,offset):
        Draw.ppolygon(screen,self.tri,Vector2(*offset+self.src),self.angle,(self.colour))
        screen.blit(self.hit[self.i][3],offset+self.dest)
    def update(self,layer):
        if self.t:
            self.t=0
        else:
            layer.remove(self)
class Gunfire(Laser):
    hit=Img.imgrot("War/GunImpact")
    colour = (255,255,0)
    def __init__(self,src,dest,angle,l):
        self.angle=-angle
        self.src=src
        self.dest=dest
        self.tri=[(2,-right),(2,right),(l,0)]
        self.i=randint(0,3)
