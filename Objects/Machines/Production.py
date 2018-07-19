from Lib import Img,Vector
from .Base import Machine
from Engine import Items
from Game import Registry
from pygame import Rect
V=Vector.VectorX
import math
class Miner(Machine):
    imgs=Img.imgstripxf("Machines/Miner",16)
    mine_prog=0
    mine_speed=0.25
    a=0
    mrects=[Rect(4,36,56,40),Rect(4,4,44,72),Rect(4,4,56,44),Rect(16,4,44,72)]
    def update(self, pos, area, events):
        super().update(pos,area,events)
        if "Ore" in area.ldict:
            ore=area.get("Ore",pos)
            if ore:
                self.a += 0.1
                self.a %= math.tau
                self.mine_prog+=self.mine_speed
                if self.mine_prog>=ore.hardness and self.add_output(Items.resources[ore.name]):
                    ore.q-=1
                    if ore.q==0:
                        area.dobj(ore,pos)
                    self.mine_prog=0
    def render(self, layer, surf, tpos, area,scale=3):
        if layer==self.renderlayer:
            Img.draw_rotor(surf,V(*tpos)+V(32,48),24,3,self.a,(80,80,80))
        super().render(layer,surf,tpos,area,scale)

Registry.add_recipe({"Iron":4,"Gear":2},Items.Placeable(Miner))


