from .Layers import Layer,TileLayer
from Lib import Vector,Img
from Engine import Items
from . import Tiles
from random import shuffle
from Objects import War
V=Vector.VectorX
exp=Img.sndget("bomb")
class Area(object):
    backcol=(0,0,0)
    infinite=False
    explored=()
    building=None
    anitick=0
    ebuffer=0
    emax=10
    def __init__(self,bounds,generator,building):
        self.bounds=bounds
        self.layers=[TileLayer(16,"Tiles"),Layer(16,"Overlay"),Layer(16,"Conv"),Layer(16,"Items"),Layer(0,"Objects")]
        self.ldict = {l.name: l for l in self.layers}
        self.ups=set()
        self.mups=set()
        self.gen=generator
        self.building=building
        generator.generate(self)
    def spawn(self,nobj,pos):
        for l in nobj.layers:
            self.ldict[l][pos]=nobj
        if nobj.updates:
            self.ups.add((pos,nobj))
        if nobj.coords:
            nobj.coords.area=self
            nobj.coords.pos=pos
        else:
            nobj.coords=Vector.Coordinate(self,pos)
        nobj.on_spawn(self,pos)
    def spawn_new(self,oc,pos,*args):
        self.spawn(oc(Vector.Coordinate(self,pos),*args),pos)
    def spawn_item(self,item,pos):
        self.spawn_new(Items.ItemObject,pos,item)
    def set_tile(self,tile,pos):
        self.ldict["Tiles"][pos]=Tiles.tdict[tile]
    def dest(self,layer,pos):
        tobj=self.ldict[layer][pos]
        self.dobj(tobj,pos)
    def dobj(self,obj,pos):
        if obj:
            for l in obj.layers:
                self.ldict[l].del_obj(pos)
            obj.on_dest(self,pos)
        if (pos,obj) in self.ups:
            self.ups.remove((pos,obj))
    def super_dest(self,pos):
        for l in self.layers:
            if l!="Tiles":
                self.dest(l.name,pos)
    def move(self,obj,pos,d,warped=False,override_speed=None,tpos_cache=None):
        tpos = tpos_cache or pos + d
        if not self.infinite and not tpos.within(self.bounds):
            if self.building:
                warp=self.building.out_warp(self,pos,d)
                if warp:
                    return self.warp(warp, obj, pos, d,warped,override_speed)
            return False
        blocked=False
        for l in obj.layers:
            o=self.get(l, tpos)
            if o:
                blocked=True
                warp=o.in_warp(d)
                if warp:
                    return self.warp(warp,obj,pos,d,warped,override_speed)
                elif isinstance(obj,Items.ItemObject) and o.input(d,obj.item):
                    if not warped:
                        self.dobj(obj, pos)
                    for l in obj.layers:
                        self.ldict[l].outobjs[tpos] = obj
                    obj.lmo = -d
                    obj.mprog = 64
                    obj.aspeed = override_speed or obj.mspeed
                    self.mups.add(obj)
                    return True
        if blocked or not self.supported(obj, tpos):
            return False
        if not warped:
            self.dobj(obj,pos)
        self.spawn(obj, tpos)
        if warped:
            for l in obj.layers:
                self.ldict[l].outobjs[tpos] = obj
        obj.lmo=-d
        obj.mprog=64
        obj.aspeed=override_speed or obj.mspeed
        return True
    def warp(self,warp,obj,pos,d,warped,ospeed):
        if warp.area.move(obj, warp.pos - d, d, True,ospeed):
            if not warped:
                self.dobj(obj, pos)
            for l in obj.layers:
                self.ldict[l].outobjs[pos + d] = obj
            return True
        return False
    def render(self,surf,player,pos):
        sr=surf.get_rect()
        start, size = pos - V(sr.w // 128 + 1, sr.h // 128 + 2), V(sr.w // 64 + 2, sr.h // 64 + 3)
        poss=list(size.iter_space_2d(start))
        for l in self.layers:
            l.render(surf,poss,start,-player.moveoff-V(64,128),self,player)
    def update(self,events):
        for p,o in set(self.ups):
            o.update(p,self,events)
        for p,o in self.ups:
            o.mupdate()
        for o in set(self.mups):
            o.mupdate()
            if not o.mprog:
                self.mups.remove(o)
        for l in self.layers:
            l.update()
        self.anitick+=1
        self.anitick%=64
    def de_update(self,obj,pos):
        self.ups.remove((pos,obj))
        obj.updates=False
    def supported(self,obj,tpos):
        if obj.slayer:
            s=self.get(obj.slayer,tpos)
            if bool(s and s.support)==obj.inverse_support:
                return False
        return True
    def get(self,layer,pos):
        return self.ldict[layer][pos]
    def clear(self,layer,pos):
        return (self.infinite or pos.within(self.bounds)) and not self.get(layer,pos)
    def warped(self,pos,d):
        return False
    def has_player(self):
        for p,o in self.ups:
            if o.area:
                if o.area.has_player():
                    return True
            if o.name=="Player":
                return True
    def respawn(self,p):
        locs=list(self.bounds.iter_space_2d(Vector.zero))
        shuffle(locs)
        for tpos in locs:
            if self.clear("Objects",tpos):
                self.spawn(p,tpos)
                return
        raise RuntimeError("COULD NOT SPAWN PLAYER ANYWHERE")
    def create_exp(self, fpos, r, exps,exptier=1, expeffect=None):
        if exps == "Cross":
            self.explode(fpos,exptier,expeffect)
            for dpos in Vector.vdirs:
                pos = fpos + dpos
                for n in range(r):
                    if not self.explode(pos, expeffect):
                        break
                    pos += dpos
        elif exps == "Square":
            for pos in [fpos + v - V(r, r) for v in (V(r, r) * 2 + V(1, 1)).iter_space()]:
                self.explode(pos, expeffect)
        elif exps == "Circle":
            for pos in [fpos + v - V(r, r) for v in (V(r, r) * 2 + V(1, 1)).iter_space()]:
                if (fpos - pos).rlen < r + 0.5:
                    self.explode(pos, expeffect)
        exp.play()
    def explode(self, pos,exptier, expeffect=None):
        rt=False
        for l in self.layers:
            o=self.get(l.name,pos)
            if (not o or o.explode(self,pos,exptier)) and l.name=="Objects":
                rt=True
        if rt:
            self.add_exp(pos,expeffect)
        return rt
    def add_exp(self, pos, expeffect):
        se = True
        # if expeffect == "Nuclear" and not randint(0, 2):
        #     self.change_t(pos, "RadGoop")
        # elif expeffect == "Incendiary" and randint(0, 3):
        #     self.spawn(Enemies.Fire(pos))
        #     se = False
        if se:
            self.spawn_new(War.Explosion,pos)
    def get_power(self,needed):
        prov=min(needed,self.ebuffer)
        self.ebuffer-=prov
        return prov
    def generate(self,gfunc):
        if self.infinite:
            return 0
        self.ebuffer+=gfunc(self.emax-self.ebuffer)
class InfiniteArea(Area):
    infinite = True
    def __init__(self,generator):
        self.layers=[TileLayer(16,"Tiles"),Layer(16,"Ore"),Layer(16,"Conv"),Layer(16,"Items"),Layer(0,"Objects")]
        self.ldict = {l.name: l for l in self.layers}
        self.ups=set()
        self.mups=set()
        self.gen=generator
        self.explored=set()
    def render(self,surf,player,pos):
        sr=surf.get_rect()
        start, size = pos - V(sr.w // 128 + 1, sr.h // 128 + 2), V(sr.w // 64 + 2, sr.h // 64 + 3)
        poss=list(size.iter_space_2d(start))
        for v in poss:
            self.ping(v)
        for l in self.layers:
            l.render(surf,poss,start,-player.moveoff-V(64,128),self,player)
    def ping(self,pos):
        if pos not in self.explored:
            self.gen.gen_pos(self,pos)
            self.explored.add(pos)
    def get(self,layer,pos):
        self.ping(pos)
        return self.ldict[layer][pos]