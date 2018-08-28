from Lib.Vector import VectorX as V
from Lib import Vector
import pygame
class Object(object):
    img=None
    layers=[]
    mspeed=4
    mprog=0
    updates=True
    lmo=Vector.zero
    vp=None
    renderlayer=None
    area=None
    exoff=Vector.zero
    override_name=None
    override_ss=None
    aspeed=0
    rotates=False
    hardness=0
    support=True
    slayer=None
    inverse_support=False
    owned=False
    exists=True
    targetable=False
    team=None
    def __init__(self,coords):
        self.coords=coords
    def render(self, layer, surf, tpos, area,scale=3):
        if not self.renderlayer or self.renderlayer==layer:
            surf.blit(self.img[scale],V(*tpos)+self.moveoff+self.exoff if self.mprog or self.exoff else tpos)
    def mupdate(self):
        if self.mprog:
            self.mprog-=self.aspeed
            if self.mprog<=0:
                self.mprog=0
    def update(self, pos, area, events):
        pass
    def interact(self,player,ppos,pos,area):
        pass
    def wrench(self,player,ppos,pos,area):
        pass
    def out_warp(self,iarea,pos,d):
        return False
    def in_warp(self,d):
        return False
    def input(self,d,i):
        return False
    def mined(self):
        return None
    def on_mine(self,area,pos,reverse=False):
        if reverse:
            area.spawn(self,pos)
        else:
            area.dobj(self,pos)
    def explode(self,area,pos,tier):
        if self.hardness and tier:
            area.dobj(self,pos)
            return True
    def on_spawn(self,area,pos):
        self.exists=True
    def on_dest(self,area,pos):
        self.exists=False
    def re_own(self,p):
        pass
    def gui_trigger(self,*args):
        pass
    def is_visible(self,p):
        return True
    def on_shoot(self,area,pos,power):
        pass
    @property
    def name(self):
        return self.override_name or self.__class__.__name__
    @classmethod
    def get_name(cls):
        return cls.override_name or cls.__name__
    @property
    def moveoff(self):
        return self.lmo*int(self.mprog)
class Rotatable(Object):
    rotates = True
    imgs=[]
    def __init__(self,coords,r):
        self.r=r
        super().__init__(coords)
    @property
    def img(self):
        return self.imgs[self.r]
class Owned(Object):
    owned = True
    def __init__(self,coords,p):
        self.p=p
        super().__init__(coords)
    def re_own(self,p):
        self.p=p
class Rotowned(Rotatable):
    owned = True
    def __init__(self,c,r,p):
        self.p=p
        super().__init__(c,r)
