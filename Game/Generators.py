from Lib.Vector import VectorX as V
from Objects import Overlays,Special,World,Agriculture
from NoiseGen.perlin import UltraPerlin,HarmonicPerlin
from random import randint,uniform
from Engine import Ores
class Generator(object):
    def generate(self,area):
        for p in area.bounds.iter_space():
            self.gen_pos(area,p)
    def gen_pos(self,area,pos):
        pass
class OreGen(Generator):
    def __init__(self,ore,density,richness,scale=16):
        self.noise=UltraPerlin(scale)
        self.ore=ore
        self.density=density
        self.richness=richness
    def gen_pos(self,area,pos):
        n=self.noise.get(pos)
        if n>1-self.density:
            q="INF" if not randint(0,29) else int((n-(1-self.density))/(1-self.density)*self.richness)
            area.spawn_new(self.ore,pos,q,q if q=="INF" else q*1000/self.richness+1)
oregens={Ores.IronOre:(0.35,1000),Ores.Stone:(0.3,500),Ores.Coal:(0.3,1000,20),Ores.CopperOre:(0.3,1000,28),Ores.ChaosOre:(0.2,100)}
class Building(Generator):
    def gen_pos(self,area,pos):
        area.set_tile("MetalFloor",pos)
        if (not all(pos) or not pos.within(area.bounds-V(1,1))) and (pos.x==area.bounds.x//2 or pos.y==area.bounds.y//2):
            area.spawn_new(Overlays.Arrow, pos,3 if pos.x==0 else 0 if pos.y==0 else 1 if pos.x==area.bounds.x-1 else 2)
class EntangledBuilding(Generator):
    def gen_pos(self,area,pos):
        area.set_tile("MetalFloor",pos)
        if (not all(pos) or not pos.within(area.bounds-V(1,1))) and (area.bounds.x//2 in (pos.x-1,pos.x+1) or area.bounds.y//2 in (pos.y-1,pos.y+1)):
            area.spawn_new(Overlays.OneTwo,pos,pos.x-1==area.bounds.x//2 or pos.y-1==area.bounds.y//2)
class SurfaceGen(Generator):
    ores=[]
    surface=None
    def __init__(self):
        self.oregens=[OreGen(o,*oregens[o]) for o in self.ores]
    def gen_pos(self,area,pos):
        for o in self.oregens:
            o.gen_pos(area,pos)
        area.set_tile(self.surface, pos)
class Islands(SurfaceGen):
    ores = [Ores.IronOre,Ores.Stone,Ores.Coal,Ores.CopperOre]
    def __init__(self):
        super().__init__()
        self.height=HarmonicPerlin(3,32)
    def gen_pos(self,area,pos):
        h=self.height.get(pos)-(pos.alt_len(area.bounds//2)/(area.bounds.x//2))**5
        if h<0:
            area.set_tile("Water",pos)
        elif h<0.07:
            area.set_tile("Sand",pos)
        else:
            area.set_tile("Grass",pos)
        if h>0:
            for o in self.oregens:
                o.gen_pos(area,pos)
            if not randint(0,200):
                area.spawn_new(Special.ChaosCrystal,pos)
            elif h>0.1 and randint(0,1):
                area.spawn_new(World.Tree,pos)
            elif not randint(0,50):
                area.spawn_new(Agriculture.FireFlower,pos)
class IceCap(SurfaceGen):
    ores = [Ores.ChaosOre]
    def __init__(self):
        super().__init__()
        self.height=HarmonicPerlin(3,32)
    def gen_pos(self,area,pos):
        h=self.height.get(pos)-(pos.alt_len(area.bounds//2)/(area.bounds.x//2))**5*2
        if h<-1:
            area.set_tile("Water",pos)
        else:
            area.set_tile("Ice",pos)
            for o in self.oregens:
                o.gen_pos(area,pos)