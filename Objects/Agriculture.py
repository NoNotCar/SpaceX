from .Base import Object
from Lib import Img,Vector
from random import randint
from Engine import Tools
V=Vector.VectorX
class Crop(Object):
    imgs=[]
    harvest_state=0
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    gspeed=2400
    hardness = 30
    item=None
    tile="Grass"
    def __init__(self,c,b=None):
        super().__init__(c)
        self.bound=b
        self.growth=0 if self.bound else self.max_g
    def update(self, pos, area, events):
        if self.growth<self.max_g and not randint(0,self.gspeed):
            self.growth+=1
    def interact(self,player,ppos,pos,area):
        if self.growth==self.max_g and player.inv.add(self.mined()):
            self.growth=self.harvest_state
    def mined(self):
        return self.item if self.growth==self.max_g else None
    @property
    def updates(self):
        return not self.bound
    @property
    def max_g(self):
        return len(self.imgs)-1
    @property
    def img(self):
        return self.imgs[self.growth]
class FireFlower(Crop):
    imgs = Img.imgstripxf("Plants/FireFlower")
    item=Tools.FireFlower()

