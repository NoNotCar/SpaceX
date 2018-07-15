from collections import defaultdict
from Lib import Img
from . import Registry
from Engine import Items
all_researches=[]
research_imgs={}
def tuplise(t):
    return t if isinstance(t,tuple) else (t,1)
class Research(object):
    packs=[]
    n=0
    name="Research"
    requirements=()
    def effect(self,team):
        pass
    @property
    def img(self):
        return research_imgs[self.name]
class RecipeResearch(Research):
    def __init__(self,recipes,packs,n,img,name):
        self.recipes=recipes
        self.packs=packs
        self.n=n
        research_imgs[name]=img
        self.name=name
    def effect(self,team):
        for r in self.recipes:
            Registry.add_recipe(*r,team=team)
class SRResearch(Research):
    def __init__(self,inputs,output,packs,n,type="Crafting"):
        self.i=inputs
        self.o=tuplise(output)
        self.n=n
        self.packs=packs
        self.t=type
        self.name=self.o[0].name
        research_imgs[self.name]=self.o[0].img
    def effect(self,team):
        Registry.add_recipe(self.i,self.o,self.t,team)
def starting_researches():
    return sorted([r for r in all_researches if not r.requirements],key=lambda r:r.n)
def ret_none():
    return None
rprogs=defaultdict(int)
current_research=defaultdict(ret_none)
done=defaultdict(list)
current=defaultdict(starting_researches)
def add_research(r,requirements=()):
    r.requirements=requirements+tuple("SP%s" % n for n in r.packs if n>1)
    all_researches.append(r)
def add_recipesearch(i,o,packs,n,r=()):
    add_research(SRResearch(i,o,packs,n),r)
def on_complete(team):
    cr=current_research[team]
    cr.effect(team)
    done[team].append(cr.name)
    current_research[team]=None
    current[team]=[r for r in all_researches if r.name not in done[team] and all(req in done[team] for req in r.requirements)]
Registry.add_recipe({"Copper":1,"Gear":1},Items.resources["SP1"])
add_recipesearch({"Conveyor":1,"Circuit":1},Items.resources["SP2"],[1],50)
#add_recipesearch({"AutoCrafter":1,"AdvCircuit":1},Items.resources["SP3"],[1,2],100)