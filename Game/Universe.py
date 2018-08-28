from .Player import Player
from . import Area
from Lib import Img,Vector
from . import Generators,Boxes,Registry,Gamemodes,Research
from Engine import Items
from Objects import Transport,Special
from Objects.Machines import Production,Basic
from random import shuffle
import pickle,pygame
Registry.add_recipe({"Iron":2},Items.resources["Gear"])
Registry.add_process_recipe("Smelting",("Iron",5),(Items.resources["Steel"],1),200)
Registry.add_recipe({"Steel":5},Items.resources["Girder"])
Registry.add_recipe({"Iron":1,"Wire":2},Items.resources["Circuit"])
Registry.add_recipe({"Copper":1},(Items.resources["Wire"],3))
#Research.add_recipesearch({"ChaosCrystal":3,"Stone":10},(Items.resources["ChaosCrystal"],4),[1],10)
AREA_SIZE=100
class PSector(object):
    def __init__(self,p,pos):
        self.planet=p
        self.pos=pos
    def out_warp(self,area,pos,d):
        return self.planet.out_warp(pos,d,self.pos)
class Planet(object):
    def __init__(self,bands):
        self.surface={}
        self.bands=bands
        self.bound=len(bands)
    def update(self,events):
        for a in list(self.surface.values()):
            a.update(events)
    def out_warp(self,pos,d,spos):
        tpos=spos+d
        if abs(tpos.y)<self.bound:
            blength=self.bound-abs(tpos.y)-1
            tpos=Vector.VectorX(min(max(tpos.x,-blength),blength) if d.y else (tpos.x+blength)%(blength*2+1)-blength,tpos.y)
            return Vector.Coordinate(self[tpos],(pos+d)%AREA_SIZE)
    def __getitem__(self, item):
        if item not in self.surface:
            self.surface[item]=Area.LargeArea(Vector.VectorX(AREA_SIZE,AREA_SIZE),self.bands[abs(item.y)](),PSector(self,item))
        return self.surface[item]
class Universe(object):
    AUTOSAVE_INTERVAL=3600
    t=0
    def __init__(self,js,ssz,gm):
        self.planet=Planet([Generators.Islands, Generators.IceCap])
        self.players=[Player(None,j) for j in js]
        self.gm=gm
        self.gm.setup(self.planet,self.players)
        for p in self.players:
            p.ssz=ssz
            self.gm.starting_inv(p.inv)
    def update(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN and e.key==pygame.K_F1:
                self.save()
        self.t+=1
        if self.t==self.AUTOSAVE_INTERVAL:
            self.t=0
            self.save()
        self.planet.update(events)
    def saved(self):
        return self,Research.current_research,Research.done,Research.rprogs,Items.chaos_slots
    def save(self):
        with open(Img.np(Img.loc+"autosave.sav"),"wb") as f:
            pickle.dump(self.saved(),f)
    def reload(self,js,ssz):
        for n,p in enumerate(self.players):
            p.ssz=ssz
            try:
                p.j=js[n]
                p.col=js[n].col
            except IndexError:
                p.coords.area.dobj(p,p.coords.pos)
                self.players.remove(p)
            p.gui=None
        for x,j in enumerate(js[n+1:]):
            np=Player(None,j)
            np.spawn=self.players[min((x+n+1)%2,len(self.players)-1)].spawn
            np.respawn()
            np.team=(x+n+1)%2
            self.players.append(np)
def re_search(r):
    return None if r is None else [re for re in Research.all_researches if re.name==(r if isinstance(r,str) else r.name)][0]
def load(file):
    Vector.special_mode=True
    with open(Img.np(Img.loc + "%s.sav" % file),"rb") as f:
        comp=pickle.load(f)
        Vector.special_mode=False
        universe = comp[0]
        for k, v in comp[2].items():
            for r in v:
                Research.current_research[k] = re_search(r)
                Research.on_complete(k)
        for k,v in comp[1].items():
            Research.current_research[k] = re_search(v)
        Research.rprogs = comp[3]
        Items.chaos_slots=comp[4]
        return universe
