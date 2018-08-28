from Engine import Items,Tools
from Objects import Vehicles,Special,War,Transport
from Objects.Machines import Basic,Production
from Game import Boxes
from Lib import Vector
V=Vector.VectorX
def starting_area(area,pos,ps,team):
    for tpos in V(5, 5).iter_space_2d(pos+V(-2, -2)):
        area.ping(tpos)
        area.super_dest(tpos)
        area.set_tile("Bridge", tpos)
    area.spawn_new(Boxes.SpawnBox, pos,team)
    sb=area.get("Objects",pos)
    for n,pp in enumerate(Vector.iter_offsets(pos,Vector.ddirs+Vector.vdirs)):
        if n<len(ps):
            area.spawn(ps[n],pp)
            ps[n].spawn=sb.area
    if ps and team is not None:
        for v in Vector.ddirs+Vector.vdirs:
            area.spawn_new(War.LaserTurret,pos+v*2,0,ps[0])

class Gamemode(object):
    def setup(self,planet,ps):
        pass
    def starting_inv(self,inv):
        inv.add(Items.Placeable(Basic.Furnace))
        inv.add(Items.Placeable(Production.Miner))
        inv.add(Items.Placeable(Vehicles.Boat))
        inv.add(Items.Placeable(Boxes.StdBox))
        inv.add(Items.Placeable(Basic.Generator))
        inv.add(Items.Placeable(Basic.Electrolyser))
    @property
    def name(self):
        return self.__class__.__name__
class Standard(Gamemode):
    def setup(self,planet,ps):
        for n in range(2):
            area=planet[V(n,0)]
            offset=area.bounds//2 if area.bounds else Vector.zero
            starting_area(area,offset,ps[n::2],n)
        for n,p in enumerate(ps):
            p.team=n%2
class Coop(Gamemode):
    def setup(self,planet,ps):
        area=planet[Vector.zero]
        offset=area.bounds // 2 if area.bounds else Vector.zero
        starting_area(area,offset,ps,None)
gamemodes=[Standard(),Coop()]