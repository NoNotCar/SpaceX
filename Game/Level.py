from Layers import Layer, EntityLayer
import Things
from Lib import Gen,Vector
import itertools
from random import sample
V=Vector.Vector2
exghosts=[Things.Lazy,Things.Clyde,Things.Crazy]
class Level(object):
    backcol=(0,0,0)
    scale=1
    cpairs=[("Enemies","Players"),("Dots","Players")]
    jscores=None
    def __init__(self,size,walls=None):
        self.size=size*2-Vector.Vector2(1,1)
        self.basesize=size
        self.objs=set()
        self.layers=[Layer(0,"Walls"),EntityLayer(0,"Dots"),EntityLayer(0,"Enemies"),EntityLayer(0,"Players")]
        self.ldict = {l.name: l for l in self.layers}
        if walls:
            self["Walls"].objs=walls
            self["Walls"].fix(Vector.zero,self.size,self)
        else:
            self.regen()
        self.rs=self.scale*16+16
    def __getitem__(self, item):
        return self.ldict[item]
    def spawn(self,nobj,pos):
        for l in nobj.layers:
            self.ldict[l][pos]=nobj
        if nobj.updates:
            self.objs.add((pos,nobj))
    def dest(self,layer,pos):
        tobj=self.ldict[layer][pos]
        self.dobj(tobj,pos)
    def dobj(self,obj,pos):
        if obj:
            for l in obj.layers:
                self.ldict[l].del_obj(pos)
        if (pos,obj) in self.objs:
            self.objs.remove((pos,obj))
    def move(self,obj,pos,d):
        if self.solid(pos+d):
            return False
        for l in obj.layers:
            if self.ldict[l][pos+d]:
                return False
        self.dobj(obj,pos)
        self.spawn(obj,pos+d)
        obj.moveoff=-d
        obj.mprog=self.rs
        return True
    def render(self,surf):
        for l in self.layers:
            l.render(surf,Vector.zero,self.size,self)
    def update(self,events):
        for p,o in set(self.objs):
            o.update(p,self,events)
            o.mupdate(p,self,events)
        for l,ol in self.cpairs:
            for p,o in ((q,x) for q,x in self[l].objs.items() if x):
                self[ol].collide(self,p,o.rect.move((p*self.rs+o.moveoff).tuple),l,o)
    def regen(self):
        self["Walls"].reset()
        for p,x in Gen.gen_good_maze(self.basesize).iteritems():
            if x:
                self.spawn(Things.Wall(),p)
        for p,o in self["Walls"].objs.iteritems():
            o.gen_img(p,self)
        self["Walls"].fix(Vector.zero,self.size,self)
    def solid(self,pos):
        return not pos.within(self.size) or self["Walls"][pos]
    def mirrored_pos(self,p):
        return {p,V(self.size.x-p.x-1,p.y),V(p.x,self.size.y-p.y-1),V(self.size.x-p.x-1,self.size.y-p.y-1)}
    def prepare(self,js):
        spos=[]
        aspos=[]
        for n in range(self.size.y//2):
            if not self.solid(V(n,n)):
                spos.extend(self.mirrored_pos(V(n,n)))
        for n,j in enumerate(js):
            self.spawn(Things.Pacman(j),spos[n])
            aspos.append(spos[n])
        gpos=[]
        for n in range(self.size.y//2):
            if not self.solid(self.size//2-V(n,n)):
                gpos.extend(self.mirrored_pos(self.size//2-V(n,n)))
        for n,g in enumerate(self.get_ghosts(max(len(js)-2,0))):
            self.spawn(g(),gpos[n])
        for p in self.size.iter_locs():
            if p not in aspos and not self.solid(p):
                self.spawn(Things.Dot(),p)
        self.jscores={j:0 for j in js}
    def iter_pon(self,name):
        for p,o in self.objs:
            if o.name==name:
                yield p,o
    def get_ghosts(self,extra):
        return [Things.Blinky,Things.Hood,Things.Pincer,Things.Hazy]+sample(exghosts,extra)
    @property
    def done(self):
        return self.jscores and all(self.jscores.itervalues())

