#THIS MEANS WAR
from .Base import Object,Rotatable,Owned
from Lib import Img,Vector
from .Machines.Base import Machine,FixedMachine
from Game.Registry import add_recipe
from Game.Research import add_recipesearch
from Game import FX
from Engine.Items import Placeable,MultiSlot,Slot,ammos,resources
from .Machines import MUI
import math
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
def ang_d(a1,a2):
    return min(a1-a2,a1-a2-math.tau,key=abs)
class Turret(Machine):
    img=Img.imgx("War/GunBase")
    ds=1
    turret=Img.lotsrots(Img.imgx("War/GunTurret"),ds)
    angle=0
    rspeed=0.04
    sleep=60
    hardness = 300
    targetable = True
    hp=1
    fx=FX.Gunfire
    damage=0.01
    def render(self, layer, surf, tpos, area,scale=3):
        super().render(layer,surf,tpos,area,scale)
        if layer==self.renderlayer:
            surf.blit(self.turret[int(math.degrees(self.angle%math.tau)//self.ds)][scale],(tpos[0],tpos[1]-4))
    def shoot(self,area,target):
        target.on_shoot(area, target.coords.pos, self.damage)
        return True
    def update(self, pos, area, events):
        ls=[]
        if self.hp<=1:
            self.hp+=0.001
        if self.sleep:
            self.sleep-=1
        for t in area.targets:
            length=pos.len_to(t.coords.pos)
            if t.team is not None and t.team!=self.p.team:
                if length<=4:
                    apos=t.coords.pos+t.moveoff/64
                    tar_ang=pos.angle_to(apos)%math.tau
                    d=ang_d(self.angle,tar_ang)
                    if abs(d)<=self.rspeed:
                        self.angle=tar_ang
                        if self.shoot(area,t):
                            area["FX"].add(self.fx(pos*64+Vector.VectorX(32+32*math.cos(self.angle),24-32*math.sin(self.angle)),t.coords.pos*64+t.moveoff,self.angle,pos.len_to(apos)*64-32))
                    elif d<0:
                        self.angle+=self.rspeed
                    else:
                        self.angle-=self.rspeed
                    self.angle%=math.tau
                    break
                else:
                    ls.append(length)
        else:
            self.sleep=60 if not ls else min(ls)*10
    def on_shoot(self,area,pos,power):
        self.hp-=power
        if self.hp<=0:
            self.explode(area,pos,1)
    @property
    def team(self):
        return self.p.team
class LaserTurret(Turret):
    img=Img.imgx("War/LaserBase")
    ds=1
    turret=Img.lotsrots(Img.imgx("War/LaserTurret"),ds)
    fx=FX.Laser
    def explode(self,area,pos,tier):
        return False
class GunTurret(Turret):
    fx =FX.Gunfire
    reload=0
    damage = 0.105
    def __init__(self,c,r,p):
        super().__init__(c,r,p)
        self.ammo=MUI.ConsumableSlot(ammos,(50,100,50))
        self.gui=MUI.MUI("GunTurret",[self.ammo])
    def input(self,d,i):
        if i.name in ammos:
            return self.ammo.slot.add(i,1)
    def update(self, pos, area, events):
        if self.reload:
            self.reload-=1
        super().update(pos,area,events)
    def shoot(self,area,target):
        if self.reload or not self.ammo.get(1):
            return False
        self.reload=10
        return super().shoot(area,target)
add_recipesearch({"Iron":3,"Circuit":1,"Bomb":1},Placeable(Mine),[1],30)
add_recipesearch({"Iron":4,"Gear":2},Placeable(GunTurret),[1],10)
add_recipesearch({"Coal":1,"Copper":2},resources["Ammo"],[1],5)
add_recipe({"Iron":2,"Coal":2},Placeable(Bomb))
add_recipesearch({"Steel":8,"Circuit":20},Placeable(LaserTurret),[1,2],50)