import math
from random import randint
class VectorX(tuple):
    def __new__(cls,*n):
        return super(VectorX,cls).__new__(cls,n)
    def __add__(self, other):
        return VectorX(*(x + y for x, y in zip(self, other)))
    def __sub__(self, other):
        return VectorX(*(x - y for x, y in zip(self, other)))
    def __mul__(self, other):
        if isinstance(other, VectorX):
            return VectorX(*(x * y for x, y in zip(self, other)))
        else:
            return VectorX(*(x * other for x in self))
    def __truediv__(self, other):
        return self*(1/other)
    def __floordiv__(self, other):
        return VectorX(*(x // other for x in self))
    def __repr__(self):
        return "VX"+tuple.__repr__(self)
    def __neg__(self):
        return self*-1
    def __bool__(self):
        return any(self)
    def __abs__(self):
        return VectorX(*(abs(x) for x in self))
    def unit(self):
        try:
            return self/self.rlen
        except ZeroDivisionError:
            return VectorX(*[0] * len(self))
    def iter_space(self,layer=0):
        for x in range(self[layer]):
            if layer<len(self)-1:
                for v in self.iter_space(layer+1):
                    yield VectorX(x, *v)
            else:
                yield VectorX(x)
    def iter_space_2d(self,start):
        if start is None:
            start=zero
        for y in range(start.y,start.y+self.y):
            for x in range(start.x,start.x+self.x):
                yield VectorX(x,y)
    def iter_space_2d_tuple(self,start=None):
        if start is None:
            start=zero
        for y in range(start.y,start.y+self.y):
            for x in range(start.x,start.x+self.x):
                yield x,y
    def within(self, other):
        return all(0<=self[n]<other[n] for n in range(len(self)))
    @property
    def rlen(self):
        return sum(x**2 for x in self)**0.5
    @property
    def smil(self):
        return max(abs(x) for x in self)
    @property
    def int(self):
        return VectorX(*(int(x) for x in self))
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @property
    def z(self):
        return self[2]
    @property
    def hoz(self):
        return VectorX(self[0], 0)
    @property
    def vert(self):
        return VectorX(0, self[1])
class Coordinate(object):
    def __init__(self,area,pos):
        self.area=area
        self.pos=pos
    def __add__(self, other):
        return Coordinate(self.area,self.pos+other)
    def __sub__(self, other):
        return Coordinate(self.area,self.pos-other)
    def copy(self):
        return Coordinate(self.area,self.pos)
    def match(self,other):
        self.area=other.area
        self.pos=other.pos
    def __iter__(self):
        yield self.area
        yield self.pos
up=VectorX(0,-1)
left=VectorX(-1,0)
right=VectorX(1,0)
down=VectorX(0,1)
zero=VectorX(0,0)
vdirs = up, right, down, left
ddirs=VectorX(-1,-1),VectorX(1,-1),VectorX(-1,1),VectorX(1,1)
def iter_offsets(root, offs=vdirs):
    for d in offs:
        yield root+d
def get_uts(pos,dic,eq):
    uts=[]
    for dd in ddirs:
        u=0
        if eq(dic[pos+dd.hoz]):
            u+=1
        if eq(dic[pos+dd.vert]):
            u+=2
        if u==3 and eq(dic[pos+dd]):
            u=4
        uts.append(u)
    return tuple(uts)