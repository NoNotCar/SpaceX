from Objects import Base
from random import randint
from math import log
from Lib import Img
from Engine import Items
from Game import Registry
class Ore(Base.Object):
    layers = ["Ore"]
    imgs=[]
    updates = False
    hardness = 120
    def __init__(self,coords,q):
        super().__init__(coords)
        self.q=q+1
        self.r=randint(0,3)
        self.i=max(0,min(int(log(self.q,7)-1),len(self.imgs)-1))
    @property
    def img(self):
        return self.imgs[self.i][self.r]
    def mined(self):
        return Items.resources[self.name]
    def on_mine(self,area,pos,reverse=False):
        self.q+=1 if reverse else -1
        if self.q<=0:
            area.dobj(self,pos)
    def explode(self,area,pos,tier):
        return False
class IronOre(Ore):
    imgs=Img.imgstriprot("Ores/IronOre")
class Stone(Ore):
    imgs=Img.imgstriprot("Ores/Stone")
class Coal(Ore):
    imgs=Img.imgstriprot("Ores/Coal")
class CopperOre(Ore):
    imgs=Img.imgstriprot("Ores/CopperOre")
Registry.add_process_recipe("Smelting",("IronOre",1),(Items.resources["Iron"],1),50)
Registry.add_process_recipe("Smelting",("CopperOre",1),(Items.resources["Copper"],1),50)
Registry.add_process_recipe("Smelting",("Stone",2),(Items.resources["Brick"],1),100)
