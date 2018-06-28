from ..Base import Object,Rotatable,Rotowned
from Lib import Vector,Img
from Engine import Items
class Machine(Rotowned):
    gui=None
    layers = ["Conv","Items","Objects"]
    renderlayer = "Objects"
    hardness = 30
    slayer = "Tiles"
    def __init__(self,c,r,p):
        super().__init__(c,r,p)
        self.output={v:None for v in Vector.vdirs}
    def update(self, pos, area, events):
        if self.gui:
            self.gui.mupdate(self)
        for d,i in self.output.items():
            if i:
                c=area.get("Conv",pos+d)
                c=c if c and "Conveyor" in c.name else None
                if area.move(i,pos,d,True,c.cspeed if c else None):
                    self.output[d]=None
    def add_output(self,item,add_r=0,override_d=None):
        d=override_d or Vector.vdirs[(self.r+add_r)%4]
        if not self.output[d]:
            self.output[d]=Items.ItemObject(self.coords.copy(),item)
            return True
        return False
    def mined(self):
        return Items.ObjPlaceable(self) if self.gui else Items.Placeable(self.__class__)
    def interact(self,player,ppos,pos,area):
        if self.gui:
            player.enter_gui(self.gui)
class FixedMachine(Machine):
    rotates = False
    def __init__(self,coords,p):
        super().__init__(coords,0,p)
class SlotMachine(Machine):
    outputslot=None
    output_enabled=False
    arrows=Img.imgrot("Machines/StandardIO")
    def update(self, pos, area, events):
        if self.output_enabled:
            if self.outputslot and self.outputslot.q:
                if self.add_output(self.outputslot.item):
                    self.outputslot.remove(1)
        elif area.get("Conv",pos+Vector.vdirs[self.r]):
            self.output_enabled=True
        super().update(pos,area,events)
    def render(self, layer, surf, tpos, area,scale=3):
        super().render(layer,surf,tpos,area,scale)
        if layer==self.renderlayer:
            surf.blit(self.arrows[self.r][scale],tpos)