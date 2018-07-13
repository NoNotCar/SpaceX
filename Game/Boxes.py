from Objects.Base import Object
from .Area import Area
from Lib.Vector import VectorX as V
from Lib.Vector import Coordinate
from Lib import Img
from . import Generators,Registry
from Engine import Items
class Box(Object):
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    internalsize=V(7,7)
    gen=Generators.Building()
    exoff = V(0,-8)
    def __init__(self,coords):
        super().__init__(coords)
        self.area=Area(self.internalsize,self.gen,self)
    def update(self, pos, area, events):
        self.area.generate(area.get_power)
        self.area.update(events)
    def out_warp(self,iarea,pos,d):
        if iarea.get("Overlay",pos):
            return self.coords+d
    def in_warp(self,d):
        hb=self.area.bounds//2
        return Coordinate(self.area,hb-d*hb)
    def mined(self):
        return Items.ObjPlaceable(self)
    @property
    def hardness(self):
        return 120 if not self.area.has_player() else 0
class StdBox(Box):
    img=Img.imgx("Buildings/StdBox")
class SpawnBox(Box):
    img=Img.imgx("Buildings/SpawnBox")
    def in_warp(self,d):
        return False
    @property
    def hardness(self):
        return 0
class EntangledDummy(object):
    def __init__(self,e1):
        self.es=[e1]
    def out_warp(self,iarea,pos,d):
        o=iarea.get("Overlay",pos)
        if o and len(self.es)>o.i and self.es[o.i].exists:
            return self.es[o.i].coords+d
class EntangledBox1(Box):
    img=Img.imgstripxf("Buildings/EntangledBox")[0]
    gen=Generators.EntangledBuilding()
    def __init__(self,c):
        Object.__init__(self,c)
        self.dummy=EntangledDummy(self)
        self.area=Area(self.internalsize,self.gen,self.dummy)
    def in_warp(self,d):
        hb=self.area.bounds//2
        return Coordinate(self.area,hb-d*hb-V(bool(d.y),bool(d.x)))
class EntangledBox2(Box):
    img=Img.imgstripxf("Buildings/EntangledBox")[1]
    def __init__(self,c,a,d):
        Object.__init__(self,c)
        self.area=a
        self.dummy=d
        self.dummy.es.append(self)
    def update(self, pos, area, events):
        if not self.dummy.es[0].exists:
            super().update(pos,area,events)
        else:
            self.area.generate(area.get_power)
    def in_warp(self,d):
        hb=self.area.bounds//2
        return Coordinate(self.area,hb-d*hb+V(bool(d.y),bool(d.x)))
Registry.add_recipe({"Steel":4,"Wire":10,"ChaosCrystal":1},Items.Placeable(StdBox))