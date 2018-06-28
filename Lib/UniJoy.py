'''
Created on 25 Jul 2015
@author: Thomas
'''
from pygame import joystick

from . import Vector
VX=Vector.VectorX
joystick.init()
buconv = {"XBOX": {"A": 0, "B": 1, "X": 2, "Y": 3, "L1": 4, "R1": 5, "SELECT": 6, "START": 7},
          "PS2": {"A": 2, "B": 1,"X":3,"Y":0, "L1": 6,"R1":7,"START":9},
          "CHEAP": {"A": 2, "B": 3, "L1": 4,"R1":6}}


class Unijoy:
    def __init__(self, jnum):
        self.rstick=True
        self.jnum = jnum
        self.j = joystick.Joystick(jnum)
        self.j.init()
        if self.j.get_numaxes() == 5:
            self.type = "XBOX"
        elif self.j.get_numaxes() == 4:
            self.type = "PS2"
        else:
            self.type = "CHEAP"
            self.rstick=False
        self.binarystick=self.type=="CHEAP"

    def get_b(self, b):
        if b == "L2" and self.type == "XBOX":
            return self.j.get_axis(2) > 0.5
        elif b == "R2" and self.type == "XBOX":
            return self.j.get_axis(2) < -0.5
        return self.j.get_button(buconv[self.type][b])
    def getstick(self, stick):
        s = 2 * stick - 2
        if stick == 2 and self.type == "XBOX":
            return self.j.get_axis(4), self.j.get_axis(3)
        elif stick==2 and self.type=="PS2":
            return self.j.get_axis(3),self.j.get_axis(2)
        else:
            return self.j.get_axis(s), self.j.get_axis(s + 1)

    def getdirstick(self, stick):
        sx, sy = self.getstick(stick)
        if abs(sx) > 0.5 or abs(sy) > 0.5:
            if abs(sx) > abs(sy):
                return VX(int(round(sx)), 0)
            else:
                return VX(0, int(round(sy)))
        return Vector.zero
    def getdirstickmag(self,stick):
        sx, sy = self.getstick(stick)
        if abs(sx) > 0.1 or abs(sy) > 0.1:
            if abs(sx) > abs(sy):
                return VX(int(round(sx)), 0), abs(sx)
            else:
                return VX(0, int(round(sy))), abs(sy)
        return Vector.zero, 0


# Testing
"""import pygame
pygame.init()
teststick=Unijoy(0)
while True:
    pygame.event.pump()
    if teststick.get_b("R2"):
        print "UGO JAV"
        break"""
