from .Player import Player
from . import Area
from Lib.Vector import VectorX as V
from . import Generators,Boxes,Registry,Gamemodes
from Engine import Items
from Objects import Transport,Special
from Objects.Machines import Production,Basic
from random import shuffle
Registry.add_recipe({"Iron":2},Items.resources["Gear"])
Registry.add_process_recipe("Smelting",("Iron",5),(Items.resources["Steel"],1),200)
Registry.add_recipe({"Steel":5},Items.resources["Girder"])
Registry.add_recipe({"Iron":1,"Wire":2},Items.resources["Circuit"])
Registry.add_recipe({"Copper":1},(Items.resources["Wire"],3))
Registry.add_recipe({"ChaosCrystal":3,"Stone":10},(Items.resources["ChaosCrystal"],4))
class Universe(object):
    gm=Gamemodes.Standard()
    def __init__(self,js,ssz):
        self.area=Area.InfiniteArea(Generators.Earth())
        self.players=[Player(None,j) for j in js]
        shuffle(self.players)
        self.gm.setup(self.area,self.players)
        for p in self.players:
            p.ssz=ssz
            self.gm.starting_inv(p.inv)
    def update(self,events):
        self.area.update(events)