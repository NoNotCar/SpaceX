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
Research.add_recipesearch({"ChaosCrystal":3,"Stone":10},(Items.resources["ChaosCrystal"],4),[1],10)
class Universe(object):
    AUTOSAVE_INTERVAL=3600
    t=0
    def __init__(self,js,ssz,gm):
        self.area=Area.InfiniteArea(Generators.Earth())
        self.players=[Player(None,j) for j in js]
        shuffle(self.players)
        self.gm=gm
        self.gm.setup(self.area,self.players)
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
        self.area.update(events)
    def saved(self):
        return self,Research.current_research,Research.done,Research.rprogs
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
            p.gui=None
        for x,j in enumerate(js[n+1:]):
            np=Player(None,j)
            np.spawn=self.players[min((x+n+1)%2,len(self.players)-1)].spawn
            np.respawn()
            self.players.append(np)
def re_search(r):
    return None if r is None else [re for re in Research.all_researches if re.name==r.name][0]
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
        return universe
