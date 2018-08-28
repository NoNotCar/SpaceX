from Lib import Img,Vector
from .Base import Machine,OutputMachine
from . import MUI
from Engine import Items
from Game import Registry,Research
from pygame import Rect
from .. import Agriculture
from random import randint,choice
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
                    if not ore.inf:
                        ore.q-=1
                        if ore.q==0:
                            area.dobj(ore,pos)
                    self.mine_prog=0
    def render(self, layer, surf, tpos, area,scale=3):
        if layer==self.renderlayer:
            Img.draw_rotor(surf,V(*tpos)+V(32,48),24,3,self.a,(80,80,80))
        super().render(layer,surf,tpos,area,scale)
class Farmer(OutputMachine):
    imgs=Img.imgstripxf("Machines/Farmer")
    crops=None
    crop=None
    def __init__(self,c,r,p):
        self.gui=MUI.MUI("Select Crop",[MUI.SelList([c.get_name() for c in Agriculture.crops])])
        super().__init__(c,r,p)
    def init_crops(self,area,pos):
        self.crops={}
        for tpos in V(5,5).iter_space_2d(pos-V(2,2)):
            pcrop=True
            for l in self.crop.layers:
                if not area.clear(l,tpos):
                    pcrop=False
                tcrop=area.get(l,tpos)
                if isinstance(tcrop,self.crop) and not tcrop.bound:
                    tcrop.bound=self
                    area.ups.remove((tpos,tcrop))
                    self.crops[tpos]=tcrop
                    break
            if area.get("Tiles",tpos).name!=self.crop.tile:
                pcrop=False
            if tpos not in self.crops:
                self.crops[tpos]=area.spawn_new(self.crop,tpos,self) if pcrop else None
    def gui_trigger(self,*args):
        self.crop=Agriculture.crops[args[0]]
    def update(self, pos, area, events):
        if self.crops:
            if not randint(0,self.crop.gspeed//25):
                tpos,ch=choice(list(self.crops.items()))
                if ch:
                    if not ch.exists:
                        self.crops[tpos]=None
                    elif ch.growth < ch.max_g:
                        ch.growth += 1
                    elif self.add_output(ch.mined()):
                        ch.growth=ch.harvest_state
        elif self.crop:
            self.init_crops(area,pos)
        super().update(pos,area,events)
    def on_dest(self,area,pos):
        if self.crops:
            for tpos,crop in self.crops.items():
                if crop:
                    crop.bound=None
                    area.ups.add((tpos,crop))
Registry.add_recipe({"Iron":4,"Gear":2},Items.Placeable(Miner))
Research.add_recipesearch({"Copper":8,"Gear":4},Items.Placeable(Farmer),[1],20)


