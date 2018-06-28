from collections import defaultdict
from Lib import Img
from . import Registry
class Research(object):
    img=None
    packs=[]
    n=0
    def effect(self):
        pass
class RecipeResearch(Research):
    def __init__(self,recipes,packs,n):
        self.recipes=recipes
        self.packs=packs
        self.n=n
    def effect(self):
        for r in self.recipes:
            Registry.add_recipe(*r)
rprogs=defaultdict(int)