from . import Vector,Img
import pygame
import pickle
from pygame import Rect
from collections import defaultdict
import textwrap
from Engine import Items
V=Vector.VectorX
coldict={(255,50,50):"red",(50,255,50):"green",(100,100,255):"blue",(255,255,0):"yellow",(255,0,255):"magenta",(50,255,255):"cyan",(255,128,50):"orange",(255,128,255):"pink"}
teams=["Left","Right"]
class GameEnd(Exception):
    def __init__(self,team):
        self.team=team
class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
def smoothaib(s,e,x):
    if x<0 or x>1:
        return s if x<0 else e
    smooth=6*x**5-15*x**4+10*x**3
    return s*(1-smooth)+e*smooth
class System(object):
    TRANSITION_SPEED=0.015
    t=0
    campos=Vector.zero
    moving=False
    spos=Vector.zero
    lpos=Vector.zero
    last=None
    def __init__(self,ss):
        self.ss=ss
        self.screens={}
        self.dj=Img.DJ()
        self.u=None
    def add_screen(self,ns,pos):
        self.screens[pos]=ns
        ns.parent=self
        self.last=ns
    def render(self,screen):
        if not self.moving:
            screen.fill(self.cs.col)
            self.cs.render(screen, Vector.zero)
        else:
            screen.fill(smoothaib(V(*self.ls.col),V(*self.cs.col),self.t))
            self.cs.render(screen, self.spos * self.ss - self.campos)
            self.ls.render(screen, self.lpos * self.ss - self.campos)
    def update(self,events):
        self.dj.update()
        if self.moving:
            self.t+=self.TRANSITION_SPEED
            if self.t>=1:
                self.moving=False
            self.campos=smoothaib(self.lpos*self.ss,self.spos*self.ss,self.t)
        else:
            if self.u:
                try:
                    self.u.update(events)
                except GameEnd as ge:
                    self.add_screen(Screen((0,0,0)),self.spos+Vector.right)
                    self.last.add_element(Text("%s team wins!" % teams[ge.team],Vector.zero,96,(255,255,255)),"centred")
                    self.switch(Vector.right)
                    self.u=None
            self.cs.update(events)
            for e in events:
                if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                    mpos=pygame.mouse.get_pos()
                    for e in reversed(self.cs.elements):
                        if e.c_rect(self.ss).collidepoint(mpos):
                            e.on_click(self, V(*mpos)-V(*e.rect.topleft))
                            return
            if pygame.mouse.get_pressed()[0]:
                mpos = pygame.mouse.get_pos()
                for e in reversed(self.cs.elements):
                    if e.c_rect(self.ss).collidepoint(mpos):
                        e.on_hold(self, V(*mpos) - V(*e.rect.topleft))
                        break
    def switch(self,dpos):
        #NINTENDO
        self.t=0
        self.lpos=self.spos
        self.spos+=dpos
        self.moving=True
    def get_element(self,cls):
        for e in self.cs.elements:
            if isinstance(e,cls):
                return e
        raise ValueError("NO ELEMENT OF THAT TYPE EXISTS")
    def __getitem__(self, item):
        return self.screens[item]
    @property
    def cs(self):
        return self.screens[self.spos]
    @property
    def ls(self):
        return self.screens[self.lpos]
class Screen(object):
    parent=None
    def __init__(self,bcol):
        self.col=bcol
        self.elements=[]
    def add_element(self,e,align=""):
        if align=="centred":
            e.rect.move_ip((self.parent.ss.x - e.rect.w) // 2, (self.parent.ss.y - e.rect.h) // 2)
        elif "centre" in align:
            e.rect.move_ip((self.parent.ss.x-e.rect.w)//2,0)
        if "bottom" in align:
            e.rect.move_ip(0,self.parent.ss.y - e.rect.h)
        if "right" in align:
            e.rect.move_ip(self.parent.ss.x-e.rect.w,0)
        self.elements.append(e)
    def render(self,screen,off):
        for e in self.elements:
            e.render(screen, off)
    def update(self,events):
        for e in self.elements:
            e.update(events,self.parent)
    def get_element(self,cls):
        for e in self.elements:
            if isinstance(e,cls):
                return e
        raise ValueError("NO ELEMENT OF THAT TYPE EXISTS")
class Element(object):
    rect=Rect(0,0,0,0)
    img=None
    def render(self,screen,off):
        screen.blit(self.img,(self.rect.left+off.x,self.rect.top+off.y))
    def on_click(self, system, rpos):
        pass
    def on_hold(self, system, rpos):
        pass
    def c_rect(self,ss):
        return self.rect
    def update(self,events,system):
        pass
class Text(Element):
    fdict=keydefaultdict(lambda sz: Img.fload("cool",sz))
    H_ADJUST=-24
    def __init__(self,text,pos,sz,col=(0,0,0)):
        self.text=text
        self.img= self.fdict[sz].render(text, True, col)
        self.rect = self.img.get_rect().move(*(pos-V(0,self.H_ADJUST)/2))
class ActiveText(Element):
    fdict=keydefaultdict(lambda sz: Img.fload("cool",sz))
    H_ADJUST=0
    def __init__(self,obj,field,func,rect,sz,col=(0,0,0)):
        self.font=self.fdict[sz]
        self.rect = rect
        self.obj=obj
        self.field=field
        self.col=col
        self.f=func
    def render(self,screen,off):
        Img.bcentrerect(self.font,self.f(getattr(self.obj,self.field)),screen,self.rect.move(*off),self.col,self.H_ADJUST)
class Button(Element):
    font = Img.fload("cool", 32)
    def __init__(self,text,pos,dpos=Vector.zero):
        self.text=text
        self.img=Img.button(text,self.font)
        self.rect=self.img.get_rect().move(*pos)
        self.dp=dpos
    def on_click(self, system, rpos):
        if self.dp:
            system.switch(self.dp)
class ColourSelect(Element):
    base=Img.imgx("Colour")
    tick=Img.imgx("Tick")
    cross=Img.imgx("Cross")
    inactive=base.copy()
    inactive.blit(cross,(0,0))
    def __init__(self,jlist,pos):
        clist=list(coldict.keys())
        self.colimgs=[Img.colcopy(self.base,(128,128,128),c) for c in clist]
        self.jdict={j:None for j in jlist}
        self.jlist=jlist
        self.rect=pygame.Rect(pos,(128,64*len(jlist)))
        self.colsels=[0]*len(jlist)
        self.clist=clist
    def render(self,screen,off):
        for y,c in enumerate(self.colsels):
            if self.jlist[y].active:
                screen.blit(self.colimgs[c][3],(self.rect.left+off.x,self.rect.top+y*64+off.y))
                tcpos=(self.rect.left+64+off.x,self.rect.top+y*64+off.y)
                if self.jdict[self.jlist[y]] is not None:
                    screen.blit(self.tick[3],tcpos)
                elif c in self.jdict.values():
                    screen.blit(self.cross[3], tcpos)
            else:
                screen.blit(self.inactive[3], (self.rect.left + off.x, self.rect.top + y * 64 + off.y))
    def update(self,events,system):
        for n,j in enumerate(self.jlist):
            if j.col is None:
                dx=j.get_dir_pressed(events).x
                if j.get_buttons(events)[0]:
                    if not j.active:
                        j.active=True
                    elif self.colsels[n] not in self.jdict.values():
                        self.jdict[j]=self.colsels[n]
                        j.col=self.clist[self.colsels[n]]
                        if len([0 for v in self.jdict.values() if v is not None])==1:
                            system.cs.add_element(Button("CONTINUE",V(0,self.rect.bottom+64),Vector.right),"centre")
                elif dx:
                    self.colsels[n]+=dx
                    self.colsels[n]%=len(self.clist)
class Surface(Element):
    def __init__(self,pos,size):
        self.rect=pygame.Rect(pos,size)
        self.img=pygame.Surface(self.rect.size)
    def redraw(self):
        pass
    def render(self,screen,off):
        self.redraw()
        Element.render(self,screen,off)
class Viewport(Surface):
    rwidge=Img.imgstripx("RotWidget")
    def __init__(self,pos,size,p):
        self.player=p
        self.size=size
        Surface.__init__(self,pos,size*64+V(0,16))
    def redraw(self):
        rt=self.player.vehicle or self.player
        area,pos =tuple(rt.coords)
        if self.player.gui:
            self.player.gui.render(self.img,self.player.j)
        else:
            self.img.fill(area.backcol)
            area.render(self.img,rt,pos)
        self.player.inv.render(self.img,Vector.zero,3)
        ssx=self.player.ss*64
        pygame.draw.polygon(self.img,self.player.j.col,((ssx,64),(ssx+64,64),(ssx+32,56)))
        selitem=self.player.inv.slots[self.player.ss].item
        # if self.size.x>7:
        #     pygame.draw.polygon(self.img,self.player.inv.slots[0].backcol,(V(448,0),V(512,0),V(448,63)))
        self.img.blit(self.rwidge[self.player.tr][3],(0,self.size.y*64-16))
        if selitem and selitem.prog and self.player.j.get_pressed()[0]:
            pygame.draw.rect(self.img,self.player.col,Rect(0,self.size.y*64-16,self.size.x*64*selitem.prog/selitem.prog_max,16))
        pygame.draw.rect(self.img,self.player.col,self.img.get_rect(),1)
class TextEntry(Element):
    active=False
    fdict = keydefaultdict(lambda sz: Img.fload("SFont", sz))
    H_ADJUST = 20
    def __init__(self,h,sz,default,suffix=".lvl"):
        self.text=default
        self.suffix=suffix
        self.sz=sz
        self.h=h
        self.img = self.fdict[sz].render(default+suffix, True, (0,0,0))
        self.rect = self.img.get_rect().move(*(V(0, self.H_ADJUST+h)))
    def rerender(self,ss):
        self.img = self.fdict[self.sz].render(self.text + self.suffix, True, (255,0,0) if self.active else (0, 0, 0))
        self.rect = self.img.get_rect().move(*V((ss.x-self.img.get_width())//2, self.H_ADJUST + self.h))
    def on_click(self, system, rpos):
        self.active=not self.active
        self.rerender(system.ss)
    def update(self,events,system):
        if self.active:
            oldt=self.text
            for e in events:
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_BACKSPACE:
                        if self.text:
                            self.text=self.text[:-1]
                    else:
                        self.text+=e.unicode
            if self.text!=oldt:
                self.rerender(system.ss)
    @property
    def ctext(self):
        return self.text+self.suffix
class SButton(Button):
    def __init__(self,cs,text,pos):
        Button.__init__(self,text,pos)
        self.cs=cs
    def on_click(self, system, rpos):
        from Game import Universe
        system.add_screen(Screen((10,10,10)),system.spos+Vector.right)
        acs=[c for c in self.cs if c.col]
        ss=(V(7,8) if len(acs)>4 else V(10,8) if len(acs)>2 else V(13,13))
        ass=ss*64+V(0,16)
        system.u=Universe.Universe(acs,ss)
        offs=self.gen_offs(len(acs))
        for n,c in enumerate(acs):
            system.last.add_element(Viewport(ass*offs[n],ss,system.u.players[n]),"centred")
        system.switch(Vector.right)
    def gen_offs(self,n):
        if n>2:
            return sum(([V(x/2,-0.5),V(x/2,0.5)] for x in range(-((n+1)//2)+1,(n+1)//2,2)),[])
        return [V(-0.5,0),V(0.5,0)] if n>1 else [Vector.zero]




