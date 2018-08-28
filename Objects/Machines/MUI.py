from Lib import Vector,Img
from Game import Registry,Research
from Engine import Items
from collections import Counter
from pygame import draw,Rect
tfont= Img.fload("cool", 64)
sel=Img.imgx("GUISelect")
arrow=Img.imgx("Arrow")
error=Img.sndget("error")
class MUI(object):
    bcol=(210,)*3
    size=Vector.zero
    def __init__(self,title,elements):
        self.re_init(title,elements)
        self.cdict={}
    def re_init(self,title,elements):
        self.title = title
        self.es = elements
    def on_enter(self,j,sz):
        self.size=sz
        self.cdict[j]=Vector.zero
    def render(self,screen,srcj):
        screen.fill(self.bcol)
        Img.bcentrex(tfont,self.title,screen,48)
        y=0
        cc=self.cdict[srcj]
        for e in self.es:
            h=e.get_h(self.size.x)
            e.render(screen,y*64+128,self.size,cc-Vector.VectorX(0,y) if y<=cc.y<y+h else None)
            y+=h
    def update(self,p,events):
        j=p.j
        self.cdict[j]+=j.get_dir_pressed(events)
        cpos=self.cdict[j]
        if cpos.x<0:
            cpos+=Vector.up
        e,y=self.current_element(j)
        if e is None or not e.inside(cpos-Vector.VectorX(0,y),self.size.x):
            self.cdict[j]=Vector.VectorX(0,cpos.y+1)
        if cpos.y<0 or cpos.y>=sum(e.get_h(self.size.x) for e in self.es):
            self.cdict[j]=Vector.zero
        buttons=j.get_buttons(events)
        e, y = self.current_element(j)
        cpos = self.cdict[j]
        if buttons[0]:
            e.on_a(cpos-Vector.VectorX(0,y),self.size.x,p)
        elif buttons[3]:
            e.on_drop(cpos - Vector.VectorX(0, y),self.size.x, p.cslot)
    def current_element(self,j):
        cpos=self.cdict[j]
        y=0
        for e in self.es:
            h = e.get_h(self.size.x)
            if cpos.y<y+h:
                return e,y
            y+=h
        return None,None
    def mupdate(self,machine):
        for e in self.es:
            e.machine_update(self,machine)
    def get_power(self,needed):
        need=needed
        for e in self.es:
            needed-=e.get_power(needed)
            if not needed:
                break
        return need-needed
class Element(object):
    def get_h(self,w):
        return 1
    def render(self,screen,y,size,rcpos=None):
        pass
    def inside(self,rpos,w):
        return True
    def on_a(self,rpos,w,p):
        pass
    def on_drop(self,rpos,w,slot):
        pass
    def machine_update(self,ui,machine):
        pass
    def get_power(self,needed):
        return 0
class HandCrafting(Element):
    make=Img.sndget("make")
    def __init__(self,p):
        self.rs=Registry.get_recipes(p.team,"Crafting")
    def get_h(self,w):
        return len(self.rs) // w + 1
    def render(self,screen,y,size,rcpos=None):
        for x,(i,(p,q)) in enumerate(self.rs):
            Img.draw_with_num(screen,p.img,q,(x%size.x*64,y+x//size.x*64),4)
        if rcpos is not None:
            screen.blit(sel[3],rcpos*64+Vector.VectorX(0,y))
            selr=self.rs[rcpos.x + rcpos.y * size.x]
            i,(p,q)=selr
            l=len(i)
            offset=(size.x-l-2)*32
            for x,(item,n) in enumerate(i.items()):
                Img.draw_with_num(screen,Items.get_item_image(item),n,(offset+x*64,(size.y-1)*64),4)
            screen.blit(arrow[3],(offset+l*64,(size.y-1)*64))
            Img.draw_with_num(screen, p.img, q, (offset + (l+1) * 64, (size.y - 1) * 64), 4)
    def inside(self,rpos,w):
        return rpos.x<w and rpos.x+rpos.y*w<len(self.rs)
    def on_a(self,rpos,w,p):
        i,(prd,q) = self.rs[rpos.x + rpos.y * w]
        psc=p.inv.get_counter()
        ic=Counter(i)
        if ic&psc==ic:
            taken=Counter()
            for item,n in i.items():
                taken+=p.inv.remove(item,n)
            added=p.inv.add(prd.new(),q)
            if added!=q:
                p.inv.remove(prd.name,added)
                for item, n in taken.items():
                    p.inv.add(item,n)
            else:
                self.make.play()
                return
        error.play()
class RSelect(Element):
    sel_r=None
    def __init__(self,rs):
        self.rs=rs
    def get_h(self,w):
        return len(self.rs) // w + 1
    def render(self,screen,y,size,rcpos=None):
        for x,(i,(p,q)) in enumerate(self.rs):
            Img.draw_with_num(screen,p.img,q,(x%size.x*64,y+x//size.x*64),4)
        if rcpos is not None:
            screen.blit(sel[3],rcpos*64+Vector.VectorX(0,y))
            selr=self.rs[rcpos.x + rcpos.y * size.x]
            i,(p,q)=selr
            l=len(i)
            offset=(size.x-l-2)*32
            for x,(item,n) in enumerate(i.items()):
                Img.draw_with_num(screen,Items.get_item_image(item),n,(offset+x*64,(size.y-1)*64),4)
            screen.blit(arrow[3],(offset+l*64,(size.y-1)*64))
            Img.draw_with_num(screen, p.img, q, (offset + (l+1) * 64, (size.y - 1) * 64), 4)
    def inside(self,rpos,w):
        return rpos.x<w and rpos.x+rpos.y*w<len(self.rs)
    def on_a(self,rpos,w,p):
        self.sel_r = self.rs[rpos.x + rpos.y * w]
    def machine_update(self,ui,machine):
        if self.sel_r:
            machine.gui_trigger(*self.sel_r)
            self.sel_r=None
class TSelect(Element):
    def __init__(self,team):
        self.team=team
    def get_h(self,w):
        return len(Research.current[self.team]) // w + 1
    def render(self,screen,y,size,rcpos=None):
        if Research.current[self.team]:
            for x,r in enumerate(Research.current[self.team]):
                if r is Research.current_research[self.team]:
                    draw.rect(screen,(100,100,100),Rect(x%size.x*64,y+x//size.x*64,64,64))
                screen.blit(r.img[3],(x%size.x*64,y+x//size.x*64))
            if rcpos is not None:
                screen.blit(sel[3],rcpos*64+Vector.VectorX(0,y))
                selr=Research.current[self.team][rcpos.x + rcpos.y * size.x]
                l=len(selr.packs)
                offset=(size.x-l)*32
                for x,p in enumerate(selr.packs):
                    Img.draw_with_num(screen,Items.get_item_image("SP%s"%p),selr.n,(offset+x*64,(size.y-1)*64),4)
        else:
            Img.bcentrex(tfont,"NO RESEARCH AVAILABLE",screen,y-16)
    def inside(self,rpos,w):
        return rpos.x<w and rpos.x+rpos.y*w<len(Research.current[self.team])
    def on_a(self,rpos,w,p):
        if Research.current[self.team]:
            lr=Research.current_research[self.team]
            Research.current_research[self.team] = Research.current[self.team][rpos.x + rpos.y * w]
            if lr!=Research.current_research[self.team]:
                Research.rprogs[self.team]=0
class ConsumableSlot(Element):
    colour=(240,200,100)
    left=0
    max_t=0
    def __init__(self,ctype,colour=None,max_output=None):
        self.slot=Items.Slot()
        if colour:
            self.colour=colour
        self.slot.backcol=self.colour
        self.ctype=ctype
        self.max_output=None if max_output is None else max_output/60
    def render(self,screen,y,size,rcpos=None):
        self.slot.render(screen,(0,y),3)
        if rcpos is not None:
            screen.blit(sel[3], (0,y))
        if self.left:
            draw.rect(screen,self.colour,Rect(64,y+16,(size.x*64-64)*self.left/self.max_t,32))
    def on_a(self,rpos,w,p):
        if self.slot.item:
            self.slot.remove(p.inv.add(self.slot.item,self.slot.q))
    def on_drop(self,rpos,w,slot):
        if slot.item and slot.item.name in self.ctype:
            slot.transfer(self.slot)
    def get(self,needed):
        needed=self.max_output if self.max_output and self.max_output<needed else needed
        need=needed
        while needed:
            if self.left:
                trans=min(self.left,needed)
                self.left-=trans
                needed-=trans
            elif self.slot and self.slot.item.name in self.ctype:
                self.left+=self.ctype[self.slot.item.name]
                self.max_t=self.left
                self.slot.remove(1)
            else:
                break
        return need-needed
class FuelSlot(ConsumableSlot):
    def __init__(self,max_output=None):
        super().__init__(Items.fuels,max_output=max_output)
    def get_power(self,needed):
        return self.get(needed)
class ElectroSlot(Element):
    colour = (255, 216, 0)
    nullcolour=(100,100,100)
    electro=Img.imgx("Electro")
    last_power=0
    last_need=0
    def __init__(self,mach):
        self.mach=mach
    def render(self, screen, y, size, rcpos=None):
        screen.blit(self.electro[3],(0,y))
        if rcpos is not None:
            screen.blit(sel[3], (0, y))
        draw.rect(screen, self.nullcolour, Rect(64, y + 16, (size.x * 64 - 64), 32))
        area=self.mach.coords.area
        if not area.infinite and area.ebuffer:
            draw.rect(screen, self.colour, Rect(64, y + 16, (size.x * 64 - 64) * area.ebuffer / area.emax, 32))
    def get_power(self, needed):
        self.last_need=needed
        self.last_power=self.mach.coords.area.get_power(needed)
        return self.last_power
class Processor(Element):
    progress=0
    cr=None
    pcol=(255,0,0)
    def __init__(self,recipe,power):
        self.input=Items.Slot()
        self.output=Items.Slot()
        self.recipe=recipe
        self.power=power/60
    def inside(self,rpos,w):
        return rpos.x<2
    def render(self,screen,y,size,rcpos=None):
        for n,s in enumerate((self.input,self.output)):
            s.render(screen,(size.x*64-64 if n else 0,y),3)
            if rcpos is not None and n==rcpos.x:
                screen.blit(sel[3], (size.x*64-64 if n else 0,y))
        draw.rect(screen,self.input.backcol,Rect(64,y+16,size.x*64-128,32))
        if self.progress:
            draw.rect(screen, self.pcol, Rect(64, y + 16, (size.x * 64 - 128)*self.progress/self.cr[2], 32))
    def on_a(self,rpos,w,p):
        (self.input,self.output)[rpos.x].transfer(p.inv)
    def on_drop(self,rpos,w,slot):
        slot.transfer((self.input,self.output)[rpos.x])
    def machine_update(self,ui,machine):
        if self.cr:
            if self.progress==self.cr[2]:
                if self.output.can_add(*self.cr[1]):
                    self.output.add(self.cr[1][0].new(),self.cr[1][1])
                    self.cr=None
                    self.progress=0
            else:
                self.progress+=ui.get_power(min(self.power,self.cr[2]-self.progress))
        elif self.input.q:
            for r in Registry.processing_recipes[self.recipe]:
                if r[0][0]==self.input.item.name and r[0][1]<=self.input.q:
                    gp = ui.get_power(self.power)
                    if gp:
                        self.input.remove(r[0][1])
                        self.cr=r
                        self.progress+=gp
                        break
class Crafter(Element):
    progress=0
    pcol=(255,0,0)
    def __init__(self,recipe,energy,power):
        self.inputs=Items.MultiSlot([Items.FilterSlot(Items.get_item(k),v) for k,v in recipe[0].items()])
        self.output=Items.FilterSlot(recipe[1][0])
        self.recipe=recipe
        self.energy=energy
        self.power=power/60
        self.tar_inputs=Counter(self.recipe[0])
    def inside(self,rpos,w):
        return rpos.x<len(self.inputs.slots)+1
    def render(self,screen,y,size,rcpos=None):
        for n,s in enumerate(self.inputs.slots):
            s.render(screen,(n*64,y),3)
            if rcpos is not None and n==rcpos.x:
                screen.blit(sel[3], (n*64,y))
        self.output.render(screen,(size.x*64-64,y),3)
        islots = len(self.inputs.slots)
        if rcpos and rcpos.x==islots:
            screen.blit(sel[3], (size.x*64-64,y))
        draw.rect(screen, self.inputs.slots[0].backcol, Rect(64 * islots, y + 16, (size.x-islots-1)*64, 32))
        if self.progress:
            draw.rect(screen, self.pcol, Rect(64 * islots, y + 16, (size.x-islots-1)*64*self.progress/self.energy, 32))
    def on_a(self,rpos,w,p):
        (self.inputs.slots+[self.output])[rpos.x].transfer(p.inv)
    def on_drop(self,rpos,w,slot):
        slot.transfer((self.inputs.slots+[self.output])[rpos.x])
    def machine_update(self,ui,machine):
        if self.progress:
            if self.progress==self.energy:
                if self.output.can_add(*self.recipe[1]):
                    self.output.add(self.recipe[1][0].new(),self.recipe[1][1])
                    self.progress=0
            else:
                self.progress+=ui.get_power(min(self.power,self.energy-self.progress))
        else:
            if self.tar_inputs&self.inputs.get_counter()==self.tar_inputs:
                gp=ui.get_power(self.power)
                if gp:
                    for i,n in self.recipe[0].items():
                        self.inputs.remove(i,n)
                        self.progress += gp
                        break
class Lab(Element):
    progress=0
    pcol=(200,200,255)
    backcol=(0,0,0)
    overlay=Img.imgx("SCIENCE")
    done=Img.sndget("research")
    def __init__(self,energy,power,team):
        self.inputs=Items.MultiSlot([Items.FilterSlot(Items.resources["SP%s" % n]) for n in range(1,7)])
        self.energy=energy
        self.power=power/60
        self.team=team
    def inside(self,rpos,w):
        return rpos.x<len(self.inputs.slots) and not rpos.y
    def get_h(self,w):
        return 2
    def render(self,screen,y,size,rcpos=None):
        for n,s in enumerate(self.inputs.slots):
            s.render(screen,(n*64,y),3)
            if rcpos is not None and n==rcpos.x:
                screen.blit(sel[3], (n*64,y))
        if Research.current_research[self.team]:
            Img.draw_with_num(screen,Research.current_research[self.team].img,Research.rprogs[self.team],((n+1)*64,y),4)
        draw.rect(screen, self.backcol, Rect(0, y + 64, len(self.inputs.slots)*64, 32))
        if self.progress:
            draw.rect(screen, self.pcol, Rect(0, y + 64, len(self.inputs.slots)*64*self.progress/self.energy, 32))
        screen.blit(self.overlay[3],(0,y+64))
    def on_a(self,rpos,w,p):
        self.inputs.slots[rpos.x].transfer(p.inv)
    def on_drop(self,rpos,w,slot):
        slot.transfer(self.inputs.slots[rpos.x])
    def machine_update(self,ui,machine):
        cr=Research.current_research[self.team]
        if cr:
            if self.progress:
                if self.progress==self.energy:
                    Research.rprogs[self.team]+=1
                    if Research.rprogs[self.team]==cr.n:
                        Research.on_complete(self.team)
                        self.done.play()
                    self.progress=0
                else:
                    self.progress+=ui.get_power(min(self.power,self.energy-self.progress))
            else:
                if all(self.inputs.slots[n-1] for n in cr.packs):
                    gp=ui.get_power(self.power)
                    if gp:
                        for n in cr.packs:
                            self.inputs.slots[n-1].remove(1)
                            self.progress += gp
                            break
class Button(Element):
    selcol=(255,0,0)
    triggered=False
    def __init__(self,text):
        self.text=text
    def inside(self,rpos,w):
        return rpos.x==0
    def render(self,screen,y,size,rcpos=None):
        Img.bcentrex(tfont,self.text,screen,y-16,col=(0,0,0) if rcpos is None else self.selcol)
    def on_a(self,rpos,w,p):
        self.triggered=True
    def machine_update(self,ui,machine):
        if self.triggered:
            machine.gui_trigger(self.text)
            self.triggered=False
class SelList(Element):
    selcol=(255,0,0)
    selected=None
    def __init__(self,l):
        self.sels=l
    def inside(self,rpos,w):
        return rpos.x==0 and rpos.y<len(self.sels)
    def get_h(self,w):
        return len(self.sels)
    def render(self,screen,y,size,rcpos=None):
        for n,s in enumerate(self.sels):
            Img.bcentrex(tfont,s,screen,n*64+y-16,col=(0,0,0) if rcpos is None or rcpos.y!=n else self.selcol)
    def on_a(self,rpos,w,p):
        self.selected=rpos.y
    def machine_update(self,ui,machine):
        if self.selected is not None:
            machine.gui_trigger(self.selected)
            self.selected=None
class Inventory(Element):
    def __init__(self,mslot):
        self.inv=mslot
    def get_h(self,w):
        return len(self.inv.slots) // w + 1
    def inside(self,rpos,w):
        return rpos.x+rpos.y*w<len(self.inv.slots)
    def render(self,screen,y,size,rcpos=None):
        for n,s in enumerate(self.inv.slots):
            s.render(screen,(n%size.x*64,n//size.x*64+y),3)
            if rcpos is not None:
                screen.blit(sel[3],Vector.VectorX(0,y)+rcpos*64)
    def on_a(self,rpos,w,p):
        self.inv.slots[rpos.x+rpos.y*w].transfer(p.inv)
    def on_drop(self,rpos,w,slot):
        slot.transfer(self.inv.slots[rpos.x+rpos.y*w])
class ChaosInventory(Inventory):
    def __init__(self,team):
        self.team=team
    def on_drop(self,rpos,w,slot):
        slot.transfer(self.inv)
    @property
    def inv(self):
        return Items.chaos_slots[self.team]

    










