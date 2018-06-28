from Objects.Base import Object
from Lib import Img,GUI,Vector
from Engine import Items,Tools
from Objects.Machines import MUI,Basic,Production
base=Img.tilemapx("Players/Man")
pimgs={col:[Img.colcopy(i,(128,128,128),col) for i in base] for col in GUI.coldict.keys()}
class Player(Object):
    layers=["Objects"]
    d=2
    ss=0
    tr=0
    gui=None
    ssz=Vector.zero
    slayer = "Tiles"
    vehicle=None
    team=None
    spawn=None
    def __init__(self,coords,j):
        super().__init__(coords)
        self.col=j.col
        self.j=j
        self.inv=Items.MultiSlot([Items.Slot() for _ in range(7)])
        self.craftingui=MUI.MUI("CRAFTING",[MUI.HandCrafting()])
    def update(self, pos, area, events):
        self.ss+=self.j.get_lr(events)
        self.ss%=7
        if self.gui:
            self.gui.update(self,events)
            if self.j.get_buttons(events)[1] or self.j.get_start(events):
                self.gui=None
            return
        elif self.j.get_start(events):
            self.enter_gui(self.craftingui)
            return
        buttons = self.j.get_buttons(events)
        pressed=self.j.get_pressed()
        if buttons[2]:
            self.tr+=1
            self.tr%=4
        if not self.mprog:
            for v in self.j.get_dirs():
                self.d = Vector.vdirs.index(v)
                if area.move(self,pos,v):
                    break
        rs=self.j.get_rstick()
        if rs:
            self.d = Vector.vdirs.index(rs)
        if not self.mprog:
            tpos = pos + Vector.vdirs[self.d]
            cslot=self.inv.slots[self.ss]
            if cslot.q and (buttons[0] or (cslot.item.continuous and pressed[0])):
                if cslot.item.use(area,pos+Vector.vdirs[self.d],self.tr,self):
                    cslot.remove(1)
            if buttons[1]:
                for l in ["Objects","Items"]:
                    obj=area.get(l,tpos)
                    if obj:
                        obj.interact(self,pos,tpos,area)
                        break
            if buttons[3]:
                if cslot.q and area.clear("Items",tpos):
                    if area.clear("Conv",tpos):
                        area.spawn_new(Items.BigStack,tpos,cslot.item,cslot.q)
                        cslot.remove(cslot.q)
                    else:
                        area.spawn_item(cslot.item,tpos)
                        cslot.remove(1)
    def explode(self,area,pos,tier):
        self.inv = Items.MultiSlot([Items.Slot() for _ in range(7)])
        self.inv.add(Tools.Pickaxe())
        self.spawn.respawn(self)
        area.dobj(self,pos)
        return True
    def enter_gui(self,gui):
        self.gui=gui
        gui.on_enter(self.j,self.ssz)
    @property
    def img(self):
        return pimgs[self.col][self.d]
    @property
    def mspeed(self):
        return 4
    @property
    def cslot(self):
        return self.inv.slots[self.ss]