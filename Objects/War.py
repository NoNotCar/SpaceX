#THIS MEANS WAR
from .Base import Object,Rotatable,Owned
from Lib import Img,Vector
from .Machines.Base import Machine,FixedMachine
from Game.Registry import add_recipe
from Engine.Items import Placeable,MultiSlot,Slot
from .Machines import MUI
class Explosion(Object):
    layers = ["Objects"]
    img=Img.imgx("War/Exp")
    t=20
    def update(self, pos, area, events):
        self.t-=1
        if self.t==0:
            area.dobj(self,pos)
class Mine(Owned):
    layers = ["Conv"]
    img=Img.imgx("War/Mine")
    def update(self, pos, area, events):
        o=area.get("Objects",pos)
        if o and not o.mprog:
            self.explode(area,pos,1)
    def explode(self,area,pos,tier):
        area.dobj(self, pos)
        area.create_exp(pos, 1, "Square")
        return False
    def is_visible(self,p):
        return p.team==self.p.team
class Bomb(Object):
    layers = ["Objects"]
    imgs=Img.imgstripx("War/Bomb")
    t=99
    def update(self, pos, area, events):
        self.t-=1
        if not self.t:
            self.explode(area,pos,1)
    def explode(self,area,pos,tier):
        area.dobj(self, pos)
        area.create_exp(pos, 2, "Cross")
        return False
    @property
    def img(self):
        return self.imgs[4-self.t//20]
add_recipe({"Iron":3,"Circuit":1,"Bomb":1},Placeable(Mine))
add_recipe({"Iron":2,"Coal":2},Placeable(Bomb))