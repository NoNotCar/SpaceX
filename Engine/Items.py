from Lib import Img,Vector,Colour
import os
from pygame import draw,Rect,error
from Objects.Base import Object
from collections import Counter,defaultdict
iimgs={}
def get_item_image(name):
    try:
        return iimgs[name]
    except KeyError:
        try:
            nimg=Img.imgx("Resources/"+name)
        except error:
            nimg=Img.imgx("Placeables/"+name)
        iimgs[name]=nimg
        return nimg
def get_item(name):
    if name in resources:
        return resources[name]
    return placeables[name]
class Item(object):
    stack_size=25
    name="Item"
    img=None
    prog=0
    prog_max=0
    singular=False
    continuous=False
    def stacks(self,other):
        return self.name==other.name
    def can_stack(self,other):
        return self.stacks(other) and other.stacks(self)
    def match(self,string):
        return self.name==string
    def use(self,area,tpos,tr,p):
        pass
    def copy(self):
        return self.__class__()
    def new(self):
        return self.copy() if self.singular else self
class Resource(Item):
    def __init__(self,name):
        self.name=name
    @property
    def img(self):
        return get_item_image(self.name)
class Placeable(Item):
    def __init__(self,pc):
        self.name=pc.get_name()
        self.pc=pc
        if self.name not in placeables:
            placeables[self.name]=self
    def use(self,area,tpos,tr,p):
        for l in self.pc.layers:
            if not area.clear(l,tpos):
                return False
        if not area.supported(self.pc,tpos):
            return False
        if self.pc.rotates and self.pc.owned:
            area.spawn_new(self.pc,tpos,tr,p)
        elif self.pc.rotates:
            area.spawn_new(self.pc,tpos,tr)
        elif self.pc.owned:
            area.spawn_new(self.pc, tpos, p)
        else:
            area.spawn_new(self.pc,tpos)
        return True
    @property
    def img(self):
        return get_item_image(self.name)
    @property
    def stack_size(self):
        return self.pc.override_ss or 10
class ObjPlaceable(Item):
    def __init__(self,o):
        self.name=o.get_name()
        self.o=o
    def use(self,area,tpos,tr,p):
        for l in self.o.layers:
            if area.get(l,tpos):
                return False
        if not area.supported(self.o,tpos):
            return False
        if self.o.rotates:
            self.o.r=tr
        if self.o.owned:
            self.o.re_own(p)
        area.spawn(self.o,tpos)
        return True
    def stacks(self,other):
        return False
    @property
    def img(self):
        return get_item_image(self.name)
resources={n:Resource(n) for n in [f[:-4] for f in os.listdir(Img.np(Img.loc+"/Resources"))]}
placeables={}
fuels={"Coal":400,"Log":200}
ammos={"Ammo":10}
class ItemObject(Object):
    layers = ["Items"]
    pickup=Img.sndget("pickup")
    slayer = "Conv"
    def __init__(self,coords,item):
        super().__init__(coords)
        self.item=item
    def interact(self,player,ppos,pos,area):
        if player.inv.add(self.item):
            area.dobj(self,pos)
            self.pickup.play()
    @property
    def img(self):
        return self.item.img
class BigStack(Object):
    #BIG SHAQ
    #In awe at the size of this lad. ABSOLUTE UNIT
    layers = ["Conv","Items"]
    renderlayer = "Items"
    pickup = Img.sndget("pickup")
    def __init__(self,coords,item,q):
        super().__init__(coords)
        self.item=item
        self.q=q
    def interact(self,player,ppos,pos,area):
        self.q-=player.inv.add(self.item,self.q)
        if self.q==0:
            area.dobj(self,pos)
        self.pickup.play()
    def render(self, layer, surf, tpos, area,scale=3):
        super().render(layer,surf,tpos,area,scale)
        if layer==self.renderlayer:
            Img.draw_num(surf,self.q,tpos,scale+1,True)
    @property
    def img(self):
        return self.item.img
class Slot(object):
    item=None
    q=0
    f=False
    backcol=(150,)*3
    oss=None
    def add(self,item,q=1):
        if self.item is None:
            self.item=item
            self.q=q
            return q
        elif self.item.can_stack(item):
            if self.q+q<=self.stack_size:
                self.q+=q
                return q
            else:
                taken=self.stack_size-self.q
                self.q=self.stack_size
                return taken
        return 0
    def can_add(self,item,q=1):
        if self.item is None:
            return True
        if self.item.can_stack(item):
            return q<=self.stack_size-self.q
        return False
    def transfer(self,other):
        if self.q:
            trans=other.add(self.item,self.q)
            self.remove(trans)
            return trans
    def remove(self,q=1):
        if q>self.q:
            taken=self.q
            self.q=0
        else:
            taken=q
            self.q-=q
        if not (self.q or self.f):
            self.item=None
        return taken
    def render(self,surf,pos,scale):
        draw.rect(surf,self.backcol,Rect(pos,(scale*16+16,)*2))
        draw.rect(surf,Colour.darker(self.backcol,0.9),Rect(pos,(scale*16+15,)*2),2)
        if self.item:
            surf.blit(self.item.img[scale],pos)
            Img.draw_num(surf,self.q,pos,scale+1)
    @property
    def stack_size(self):
        return self.oss or self.item.stack_size
    def __bool__(self):
        return bool(self.q)
class FilterSlot(Slot):
    f=True
    backcol = (150,150,200)
    trans=Img.trans_rect((16,16),backcol+(128,))
    def __init__(self,item,oss=None):
        self.item=item
    def render(self,surf,pos,scale):
        draw.rect(surf,self.backcol,Rect(pos,(scale*16+16,)*2))
        draw.rect(surf,Colour.darker(self.backcol,0.9),Rect(pos,(scale*16+15,)*2),2)
        surf.blit(self.item.img[scale],pos)
        Img.draw_num(surf,self.q,pos,scale+1)
        if not self.q:
            surf.blit(self.trans[scale],pos)
class ChaosSlot(FilterSlot):
    backcol = (200, 100, 200)
    trans = Img.trans_rect((16, 16), backcol + (128,))
class ChaosPlaceHolder(Slot):
    backcol = ChaosSlot.backcol
class MultiSlot(object):
    def __init__(self,slots):
        self.slots=slots
    def add(self,item,q=1):
        oq=q
        for s in sorted(self.slots,key=lambda slot:bool(slot.item and slot.item.can_stack(item)),reverse=True):
            q-=s.add(item,q)
            if q==0:
                return oq
        return oq-q
    def remove(self,name,q=1):
        removed=Counter()
        for s in self.slots:
            if s and s.item.match(name):
                removed[s.item]+=min(s.q,q)
                q-=s.remove(q)
                if not q:
                    return removed
    def render(self,surf,pos,scale):
        for n,s in enumerate(self.slots):
            s.render(surf,pos+Vector.VectorX(n*(scale*16+16),0),scale)
    def get_counter(self):
        return sum((Counter({s.item.name:s.q}) if s.item else Counter() for s in self.slots),Counter())
class ChaosSlots(MultiSlot):
    def __init__(self):
        super().__init__([ChaosPlaceHolder()])
        self.sdict={}
    def add(self,item,q=1):
        if item.name in self.sdict:
            return self.sdict[item.name].add(item,q)
        nslot=ChaosSlot(item)
        nslot.q=q
        self.slots.insert(len(self.slots)-1,nslot)
        self.sdict[item.name]=nslot
        return q
chaos_slots=defaultdict(ChaosSlots)