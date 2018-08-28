from Objects import Base
from random import randint
from math import log
from Lib import Img
from Engine import Items
from Game import Registry
infsparks = Img.imgx("Ores/InfiniteSparkles")
def ore_strip(fil):
    imgs=Img.imgstriprot(fil)
    inf=imgs[-1][0].copy()
    inf.blit(infsparks,(0,0))
    imgs.append(Img.imgrot(inf))
    return imgs
class Ore(Base.Object):
    layers = ["Ore"]
    imgs=[]
    updates = False
    hardness = 120
    def __init__(self,coords,q,aq):
        super().__init__(coords)
        self.inf=q=="INF"
        self.q=q if self.inf else q+1
        self.r=randint(0,3)
        self.i=len(self.imgs)-1 if self.inf else max(0,min(int(log(aq,7)-1),len(self.imgs)-2))
    @property
    def img(self):
        return self.imgs[self.i][self.r]
    def mined(self):
        return Items.resources[self.name]
    def on_mine(self,area,pos,reverse=False):
        if self.inf:
            return
        self.q+=1 if reverse else -1
        if self.q<=0:
            area.dobj(self,pos)
    def explode(self,area,pos,tier):
        return False
class IronOre(Ore):
    imgs=ore_strip("Ores/IronOre")
class Stone(Ore):
    imgs=ore_strip("Ores/Stone")
class Coal(Ore):
    imgs=ore_strip("Ores/Coal")
class CopperOre(Ore):
    imgs=ore_strip("Ores/CopperOre")
class ChaosOre(Ore):
    imgs=ore_strip("Ores/ChaosOre")
    def mined(self):
        return Items.resources["ChaosCrystal"]
Registry.add_process_recipe("Smelting",("IronOre",1),(Items.resources["Iron"],1),50)
Registry.add_process_recipe("Electrolyser",("IronOre",1),(Items.resources["Iron"],2),150)
Registry.add_process_recipe("Smelting",("CopperOre",1),(Items.resources["Copper"],1),50)
Registry.add_process_recipe("Electrolyser",("CopperOre",1),(Items.resources["Copper"],2),150)
Registry.add_process_recipe("Smelting",("Stone",2),(Items.resources["Brick"],1),100)
