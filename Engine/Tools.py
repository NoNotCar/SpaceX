from .Items import Item
from Lib import Img
import pygame
from Game import Registry
error=Img.sndget("error")
bsnd=Img.sndget("break")
class Pickaxe(Item):
    img=Img.imgx("Tools/Pickaxe")
    last_used=0
    MAX_CONTINUOUS=200
    last_mined=None
    stack_size = 1
    singular = True
    continuous = True
    def use(self,area,tpos,tr,p):
        for l in reversed(area.layers):
            o=l[tpos]
            if o and o.hardness:
                if o is self.last_mined and pygame.time.get_ticks()-self.last_used<self.MAX_CONTINUOUS:
                    self.prog+=1
                    if self.prog==o.hardness:
                        item=o.mined()
                        o.on_mine(area,tpos)
                        if p.inv.add(item,1):
                            bsnd.play()
                        elif area.clear("Items",tpos):
                            area.spawn_item(item,tpos)
                            bsnd.play()
                        else:
                            o.on_mine(area, tpos,True)
                            error.play()
                        self.prog=0
                        self.prog_max=0
                        self.last_mined=None
                else:
                    self.prog=0
                    self.prog_max=o.hardness
                    self.last_mined=o
                break
        self.last_used=pygame.time.get_ticks()
class Bridger(Item):
    img=Img.imgx("Tools/BridgeBuilder")
    def use(self,area,tpos,tr,p):
        t=area.get("Tiles",tpos)
        if t and not t.support:
            area.set_tile("Bridge",tpos)
            return True
Registry.add_recipe({"Iron":3,"Brick":5},Bridger())


