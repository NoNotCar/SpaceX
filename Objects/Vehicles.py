from Lib import Img,Vector
from Objects.Base import Object
from Game import Registry
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
            rs=j.get_rstick()
            if rs:
                self.lv = Vector.vdirs.index(rs)
            self.ldx=self.lv.x or self.ldx
    def mined(self):
        return Items.Placeable(self.__class__)
    def on_shoot(self,area,pos,power):
        self.hp-=power/self.armour
        if self.hp<=0:
            area.dobj(self,pos)
            self.player.respawn()
            self.player.vehicle=None
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
Registry.add_recipe({"Log":10},Items.Placeable(Boat))
