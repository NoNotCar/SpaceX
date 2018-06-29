from Engine import Items,Tools
from Objects import Vehicles,Special,War,Transport
from Objects.Machines import Basic,Production
from Game import Boxes
from Lib import Vector
V=Vector.VectorX
def starting_area(area,pos,ps):
    for tpos in V(3, 3).iter_space_2d(pos+V(-1, -1)):
        area.ping(tpos)
        area.super_dest(tpos)
        area.set_tile("Bridge", tpos)
    area.spawn_new(Boxes.SpawnBox, pos)
    sb=area.get("Objects",pos)
    for n,pp in enumerate(Vector.iter_offsets(pos,Vector.ddirs)):
        if n<len(ps):
            area.spawn(ps[n],pp)
            ps[n].spawn=sb.area

class Gamemode(object):
    def setup(self,area,ps):
        pass
    def starting_inv(self,inv):
        inv.add(Tools.Pickaxe())
        inv.add(Items.Placeable(Basic.Furnace))
        inv.add(Items.Placeable(Production.Miner))
        inv.add(Items.Placeable(Vehicles.Boat))
    @property
    def name(self):
        return self.__class__.__name__
class Standard(Gamemode):
    def setup(self,area,ps):
        starting_area(area,V(-30,0),ps[::2])
        starting_area(area,V(30,0),ps[1::2])
        for n,p in enumerate(ps):
            p.team=n%2
class Coop(Gamemode):
    def setup(self,area,ps):
        starting_area(area,V(0,0),ps)
gamemodes=[Standard(),Coop()]