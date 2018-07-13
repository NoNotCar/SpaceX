from Objects.Base import Object
from Lib.Img import UltraTiles
from random import randint
from Lib import Vector
tuts={}
class Tile(Object):
    layers = ["Tiles"]
    updates = False
    def __init__(self,name):
        super().__init__(None)
        tuts[name]=UltraTiles("Tiles/"+name)
        self.override_name=name
    def __gt__(self, other):
        return tileorder[self.name]>tileorder[other.name]
    @property
    def uts(self):
        return tuts[self.override_name]
class Liquid(Tile):
    support = False
tiles=[Liquid("Water"),Tile("Sand"),Tile("Grass"),Tile("MetalFloor"),Tile("Bridge")]
tileorder={t.name:n for n,t in enumerate(tiles)}
tdict={t.name:t for t in tiles}