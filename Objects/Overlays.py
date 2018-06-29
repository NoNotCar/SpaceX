from Objects.Base import Object
from Lib import Img
class Overlay(Object):
    layers = ["Overlay"]
    updates = False
    imgs=[]
    def __init__(self,coords,i):
        super().__init__(coords)
        self.i=i
    @property
    def img(self):
        return self.imgs[self.i]
class Arrow(Overlay):
    imgs=Img.imgrot(Img.imgx("Overlays/Arrow"))
class OneTwo(Overlay):
    imgs=Img.imgstripx("Overlays/OneTwo")
