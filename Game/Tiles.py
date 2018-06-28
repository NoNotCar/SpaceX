from Objects.Base import Object
from Lib.Img import UltraTiles
from random import randint
from Lib import Vector
class Tile(Object):
    layers = ["Tiles"]
    updates = False
    uts=None
    def __init__(self,name):
        super().__init__(None)
        self.uts=UltraTiles("Tiles/"+name)
        self.override_name=name
    def __gt__(self, other):
        return tiles.index(self)>tiles.index(other)
class Liquid(Tile):
    support = False
tiles=[Liquid("Water"),Tile("Sand"),Tile("Grass"),Tile("MetalFloor"),Tile("Bridge")]
tdict={t.name:t for t in tiles}