from Lib import Img,Vector
from Objects.Base import Object
from .Machines import MUI
from Game import Registry,Research
from Engine import Items
class Vehicle(Object):
    layers=["Objects"]
    ldx=1
    lv=Vector.right
    slayer = "Tiles"
    player=None
    imgs=[]
    literally_just_entered=False
    hardness = 30
    hp=1
    armour=1
    targetable = True
    def interact(self,player,ppos,pos,area):
        if not self.player:
            self.player=player
            area.dobj(player,ppos)
            player.vehicle=self
            self.literally_just_entered=True
            self.team=player.team
    def update(self, pos, area, events):
        if self.literally_just_entered:
            self.literally_just_entered=False
            return
        if self.player:
            j=self.player.j
            if not self.mprog:
                buttons = j.get_buttons(events)
                if buttons[1]:
                    if area.move(self.player, pos, self.lv, True,64):
                        self.player.vehicle=None
                        self.player=None
                        self.team=None
                        return
                for v in j.get_dirs():
                    self.lv = v
                    if area.move(self,pos,v):
                        break
                else:
                    rs=j.get_rstick()
                    if rs:
                        self.lv = rs
            self.ldx=self.lv.x or self.ldx
    def mined(self):
        return Items.Placeable(self.__class__)
    def on_shoot(self,area,pos,power):
        self.hp-=power/self.armour
        if self.hp<=0:
            area.dobj(self,pos)
            self.player.respawn()
            self.player.vehicle=None
    def explode(self,area,pos,tier):
        if super().explode(area,pos,tier):
            self.player.respawn()
            self.player.vehicle = None
    @property
    def img(self):
        return self.imgs[self.ldx==-1]
class Boat(Vehicle):
    base=Img.imgstripx("Vehicles/Boat")
    occupied=Img.ColourImageManager(Img.hflip(base[1]))
    unocc=Img.hflip(base[0])
    inverse_support = True
    @property
    def imgs(self):
        return self.occupied[self.player.col] if self.player else self.unocc
class Plane(Vehicle):
    unocc=Img.imgstripx("Vehicles/Plane")
    occupied=Img.ColourImageManager(Img.imgstripx("Vehicles/PlaneOcc"))
    inverse_support = True
    state="Taxi"
    TAKEOFF_SPEED=8
    TAXI_SPEED=2
    ACCELERATION=0.05
    DECELERATION=0.1
    POWER=20/60
    mspeed = 2
    def __init__(self,c):
        super().__init__(c)
        self.fuel=MUI.FuelSlot()
        self.gui=MUI.MUI("SeaPlane",[self.fuel])
    @property
    def imgs(self):
        return self.occupied[self.player.col] if self.player else self.unocc
    @property
    def img(self):
        return self.imgs[Vector.vdirs.index(self.lv)]
    def wrench(self,player,ppos,pos,area):
        player.enter_gui(self.gui)
    def update(self, pos, area, events):
        if self.literally_just_entered:
            self.literally_just_entered=False
            return
        if self.state=="Takeoff":
            if not self.fuel.get(self.POWER*2):
                self.state="Landing"
            elif self.mspeed<self.TAKEOFF_SPEED:
                self.mspeed+=self.ACCELERATION
                self.aspeed=self.mspeed
                if not self.mprog:
                    if not area.move(self,pos,self.lv):
                        area.create_exp(pos,1,"Cross",1)
            elif not self.mprog:
                if area.move(self,pos,self.lv,re_layer=["Air"]):
                    self.state="Air"
                    self.slayer=None
                else:
                    area.create_exp(pos, 1, "Cross", 1)
        elif self.state=="Air":
            j = self.player.j
            buttons = j.get_buttons(events)
            if buttons[0] or not self.fuel.get(self.POWER):
                self.state = "Landing"
                self.slayer="Tiles"
            if not self.mprog:
                for v in j.get_dirs():
                    if v!=-self.lv:
                        self.lv = v
                        break
                if not area.move(self, pos, self.lv):
                    area.create_exp(pos, 1, "Cross", 1)
            self.ldx = self.lv.x or self.ldx
        elif self.state=="Landing":
            if self.mspeed>self.TAXI_SPEED:
                self.mspeed-=self.DECELERATION
                self.aspeed=self.mspeed
                if not self.mprog:
                    if not area.move(self,pos,self.lv,re_layer=["Objects"] if "Air" in self.layers else None):
                        area.create_exp(pos,1,"Cross",1)
            else:
                self.state="Taxi"
        elif self.player:
            j=self.player.j
            if not self.mprog:
                buttons = j.get_buttons(events)
                if buttons[1]:
                    if area.move(self.player, pos, self.lv, True,64):
                        self.player.vehicle=None
                        self.player=None
                        self.team=None
                        return
                elif buttons[0]:
                    self.state="Takeoff"
                for v in j.get_dirs():
                    self.lv = v
                    if area.move(self,pos,v):
                        break
                else:
                    rs=j.get_rstick()
                    if rs:
                        self.lv = rs
Registry.add_recipe({"Log":10},Items.Placeable(Boat))
Research.add_recipesearch({"Steel":5,"Furnace":1},Items.Placeable(Plane),[1],30)
