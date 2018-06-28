from .Base import Object,Rotatable,Owned
from Lib import Img,Vector
from Engine.Items import Placeable,resources
from Game.Research import add_recipesearch
import sys,math
class Monolith(Owned):
    imgs=Img.imgstripxf("Buildings/Monolith",16)
    t=0
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    def update(self, pos, area, events):
        self.t+=1
        if self.t==240:
            from Lib import GUI
            raise GUI.GameEnd(self.p.team)
    @property
    def img(self):
        return self.imgs[self.t%20==19]
class ChaosCrystal(Object):
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    cimg=resources["ChaosCrystal"].img
    shadow=Img.imgx("Shadow")
    tick=0
    def interact(self,player,ppos,pos,area):
        if player.inv.add(resources["ChaosCrystal"]):
            area.dobj(self,pos)
    def update(self, pos, area, events):
        self.tick+=0.1
        self.tick%=math.tau
    def render(self, layer, surf, tpos, area,scale=3):
        if layer==self.renderlayer:
            surf.blit(self.shadow[scale],tpos)
            surf.blit(self.cimg[scale],[tpos[0],tpos[1]-8+(scale+1)*math.sin(self.tick)])
add_recipesearch({"Girder":20,"Circuit":100,"ChaosCrystal":20},Placeable(Monolith),[1,2],100)