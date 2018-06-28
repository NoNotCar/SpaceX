from .Base import Object
from Lib import Img,Vector
from Engine import Items
class Tree(Object):
    hardness=60
    img=Img.imgx("World/Tree")
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    exoff = Vector.VectorX(0,-16)
    updates = False
    def mined(self):
        return Items.resources["Log"]