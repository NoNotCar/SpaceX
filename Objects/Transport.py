from .Base import Object,Rotatable
from Lib import Img,Vector
from .Machines.Base import Machine,FixedMachine
from Game.Registry import add_recipe
from Game.Research import add_recipesearch
from Engine.Items import Placeable,MultiSlot,Slot,chaos_slots
from .Machines import MUI
class Conveyor(Rotatable):
    override_name="Conveyor1"
    override_ss = 100
    cspeed=2
    imgs=Img.conv_imgs("Transport/Conveyor1")
    ani=0
    layers = ["Conv"]
    hardness = 10
    slayer = "Tiles"
    cm=None
    def __init__(self,c,r):
        super().__init__(c,r)
        self.tpos=c.pos+Vector.vdirs[self.r]
        self.d=Vector.vdirs[self.r]
    def update(self, pos, area, events):
        if self.cm:
            self.cm.conv_update(pos,area,self)
        self.ani=area.anitick
        item=area.get("Items",pos)
        if item and not item.mprog:
            area.move(item,pos,self.d,override_speed=self.cspeed,tpos_cache=self.tpos)
    def mined(self):
        return Placeable(self.__class__)
    @property
    def img(self):
        return self.imgs[(self.ani*self.cspeed%64)//4][self.r]
class Conveyor2(Conveyor):
    override_name = "Conveyor2"
    cspeed = 8
    imgs=Img.conv_imgs("Transport/Conveyor2")
class Input(Rotatable):
    imgs=Img.imgstripxf("Transport/Input")
    layers = ["Objects"]
    hardness = 10
    slayer = "Conv"
    def update(self, pos, area, events):
        conv=area.get("Conv",pos)
        if isinstance(conv,Conveyor):
            conv.cm=self
            area.de_update(self,pos)
    def conv_update(self,pos,area,conv):
        item = area.get("Items", pos)
        if item and not item.mprog:
            area.move(item, pos, Vector.vdirs[self.r], override_speed=conv.cspeed)
    def mined(self):
        return Placeable(self.__class__)
class Crossover(FixedMachine):
    imgs=[Img.imgx("Transport/Crossover")]
    exoff = Vector.VectorX(0,-4)
    def input(self,d,i):
        return self.add_output(i,override_d=d)
class Splitter(Machine):
    imgs=Img.imgstripxf("Transport/Splitter",16)
    phase=-1
    def input(self,d,i):
        for r in (self.phase,-self.phase):
            if self.add_output(i,r):
                self.phase=-r
                return True
class Storage(FixedMachine):
    imgs=[Img.imgx("Transport/Storage")]
    def __init__(self,c,p):
        super().__init__(c,p)
        self.inv=MultiSlot([Slot() for _ in range(7)])
        self.gui=MUI.MUI("Storage",[MUI.Inventory(self.inv)])
    def input(self,d,i):
        return self.inv.add(i)
class Buffer(Machine):
    imgs=Img.imgstripxf("Transport/Buffer")
    def __init__(self,c,r,p):
        super().__init__(c,r,p)
        self.inv=MultiSlot([Slot() for _ in range(7)])
        self.gui=MUI.MUI("Buffer",[MUI.Inventory(self.inv)])
        self.v=Vector.vdirs[self.r]
    def input(self,d,i):
        if d==self.v:
            return self.inv.add(i)
    def update(self, pos, area, events):
        if not self.output[self.v]:
            for s in self.inv.slots:
                if s.q:
                    if self.add_output(s.item):
                        s.remove(1)
                        break
        super().update(pos,area,events)
class ChaosChest(FixedMachine):
    imgs=[Img.imgx("Transport/ChaosChest")]
    def __init__(self,c,p):
        super().__init__(c,p)
        self.inv=MUI.ChaosInventory(self.p.team)
        self.gui=MUI.MUI("Chaos Chest",[self.inv])
    def input(self,d,i):
        return chaos_slots[self.p.team].add(i,1)
    def re_own(self,p):
        self.p=p
        self.inv.team=p.team
class Tunnel(Rotatable):
    imgs=Img.imgstripxf("Transport/Tunnel")
    updates = False
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    exoff = Vector.VectorX(0,-8)
    hardness = 60
    def in_warp(self,d):
        if d==Vector.vdirs[self.r]:
            for x in range(1,6):
                tc=self.coords+d*x
                o=tc.get("Objects")
                if isinstance(o,Tunnel) and o.r==(self.r+2)%4:
                    tc.pos+=d
                    return tc
    def mined(self):
        return Placeable(Tunnel)
add_recipe({"Gear":1,"Iron":2},(Placeable(Conveyor),5))
add_recipe({"Conveyor1":2,"Iron":4},Placeable(Crossover))
add_recipe({"Conveyor1":2,"Iron":3},Placeable(Splitter))
add_recipe({"Log":5},Placeable(Storage))
add_recipesearch({"Conveyor1":1,"Gear":3},Placeable(Conveyor2),[1],40)
add_recipe({"Brick":2},Placeable(Tunnel))
add_recipesearch({"Steel":2,"Storage":1},Placeable(Buffer),[1],10)
add_recipesearch({"ChaosCrystal":1,"Storage":1},Placeable(ChaosChest),[1],40)
add_recipe({"Conveyor1":1,"Iron":3},Placeable(Input))