import pygame

from . import UniJoy
from . import Vector


class Controller(object):
    icon=0
    avatar=None
    col=None
    coln=None
    active=False
    num=None
    score=0
    mouse=False
    tandem=False
    def get_buttons(self,events):
        return 0,0,0,0
    def get_dirs(self):
        return []
    def get_pressed(self):
        return 0,0
    def get_dir_pressed(self, events):
        return Vector.zero
    def get_rstick(self):
        return Vector.zero
    def get_lstick(self):
        return Vector.zero
    def switch(self):
        pass
    def get_start(self,events):
        return False
class TandemController(Controller):
    cnum=0
    tandem = True
    def __init__(self,cs):
        self.cs=cs
    def switch(self):
        self.cnum+=1
        self.cnum%=len(self.cs)
    def get_buttons(self,events):
        return self.cs[self.cnum].get_buttons(events)
    def get_dirs(self):
        return self.cs[self.cnum].get_dirs()
    def get_pressed(self):
        return self.cs[self.cnum].get_pressed()
    def get_dir_pressed(self, events):
        return self.cs[self.cnum].get_dir_pressed(events)
    def get_rstick(self):
        return self.cs[self.cnum].get_rstick()
    def get_lstick(self):
        return self.cs[self.cnum].get_lstick()
    @property
    def lastscore(self):
        return self.cs[0].lastscore
    @lastscore.setter
    def lastscore(self,value):
        for c in self.cs:
            c.lastscore=value
class Keyboard1(Controller):
    kconv = {pygame.K_w: Vector.up, pygame.K_s: Vector.down, pygame.K_a: Vector.left, pygame.K_d: Vector.right}
    kconv2 = {pygame.K_UP: Vector.up, pygame.K_DOWN: Vector.down, pygame.K_LEFT: Vector.left,pygame.K_RIGHT: Vector.right}
    def get_buttons(self,events):
        bomb=False
        act=False
        rot=False
        drop=False
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    bomb=True
                elif e.key==pygame.K_LSHIFT:
                    act=True
                elif e.key==pygame.K_r:
                    rot=True
                elif e.key==pygame.K_LCTRL:
                    drop=True
        return bomb,act,rot,drop
    def get_lr(self,events):
        lr=0
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_q:
                    lr-=1
                elif e.key==pygame.K_e:
                    lr+=1
        return lr
    def get_pressed(self):
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_SPACE],keys[pygame.K_LSHIFT])
    def get_dirs(self):
        keys = pygame.key.get_pressed()
        kpr=[]
        for k, v in self.kconv.items():
            if keys[k]:
                kpr.append(v)
        return kpr
    def get_rstick(self):
        keys = pygame.key.get_pressed()
        for k, v in self.kconv2.items():
            if keys[k]:
                return v
    def get_lstick(self):
        gd=self.get_dirs()
        if gd:
            gd=sum(gd, Vector.zero)
            return gd.unit()
        return Vector.zero
    def get_dir_pressed(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN and e.key in self.kconv.keys():
                return self.kconv[e.key]
        return Vector.zero
    def get_start(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_c:
                    return True
class UniJoyController(Controller):
    icon=1
    def __init__(self,n):
        self.uj= UniJoy.Unijoy(n)
        self.ld= Vector.zero
        self.cooldown=0
    def get_buttons(self,events):
        bomb=False
        act=False
        rot=False
        drop=False
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                if self.uj.get_b("A"):
                    bomb=True
                if self.uj.get_b("B"):
                    act=True
                if self.uj.get_b("Y"):
                    rot=True
                if self.uj.get_b("X"):
                    drop=True
        return bomb,act,rot,drop
    def get_lr(self,events):
        lr=0
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                if self.uj.get_b("L1"):
                    lr = -1
                if self.uj.get_b("R1"):
                    lr = 1
        return lr
    def get_dirs(self):
        ds=self.uj.getdirstick(1)
        if ds!= Vector.zero:
            return [ds]
        return []
    def get_lstick(self):
        return Vector.VectorX(*self.uj.getstick(1))
    def get_rstick(self):
        return self.uj.getdirstick(2)
    def get_dir_pressed(self,events):
        if self.uj.binarystick:
            ds = self.uj.getdirstick(1)
            if ds!=self.ld:
                self.ld = ds
                return ds
        else:
            ds,mg = self.uj.getdirstickmag(1)
            if self.cooldown:
                self.cooldown-=1
            else:
                if ds!= Vector.zero:
                    self.cooldown=int((1.2-mg)*20)
                return ds
        return Vector.zero
    def get_pressed(self):
        return (self.uj.get_b("A"),self.uj.get_b("B"))
    def get_start(self,events):
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                return self.uj.get_b("START")