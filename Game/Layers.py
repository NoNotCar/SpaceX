from Lib.Vector import VectorX as V
from Lib import Img, Vector
from . import Tiles
import pygame
class Layer(object):
    fixed=False
    def __init__(self,off,name):
        self.objs={}
        self.outobjs={}
        self.off=off
        self.name=name
    def update(self):
        if self.outobjs:
            for tpos,oo in list(self.outobjs.items()):
                if not oo.mprog:
                    del self.outobjs[tpos]
    def render(self,surf,poss,start,offset,area,player):
        ox,oy=V(0, self.off)+offset
        sx,sy=start
        rendered=set()
        if self.outobjs:
            rendered.update(self.outobjs.values())
            for v in poss:
                vx,vy=v
                if v in self.outobjs:
                    oo = self.outobjs[v]
                    oo.render(self.name, surf, ((vx - sx) * 64 + ox, (vy - sy) * 64 + oy), area, 3)
        for v in poss:
            vx,vy=v
            o=self[v]
            if o and o.is_visible(player) and o not in rendered:
                o.render(self.name, surf, ((vx-sx)*64+ox,(vy-sy)*64+oy), area, 3)
    def __getitem__(self, item):
        return self.objs.get(item,None)
    def __setitem__(self, key, value):
        self.objs[key]=value
    def reset(self):
        self.objs={}
    def del_obj(self,pos):
        del self.objs[pos]
imgcache={}
class TileLayer(Layer):
    def __init__(self,off,name):
        Layer.__init__(self,off,name)
        self.utscache={}
        self.recache=set()
        self.blocked=set()
    def regen_uts(self,pos,area):
        at = self[pos]
        if area.infinite:
            for tpos in Vector.iter_offsets(pos, Vector.vdirs + Vector.ddirs):
                area.ping(tpos)
        surround = [at] + [self[tpos] for tpos in Vector.iter_offsets(pos, Vector.vdirs + Vector.ddirs) if self[tpos]]
        torender = sorted(set(t for t in surround if Tiles.tileorder[t.name] <= Tiles.tileorder[surround[0].name]))
        comp=[(torender[0],(4,4,4,4))]
        for t in torender[1:]:
            uts = Vector.get_uts(pos, self, lambda ot: Tiles.tileorder[ot.name] >= Tiles.tileorder[t.name])
            if uts != (0, 0, 0, 0) or t == at:
                comp.append((t,uts))
        comp=tuple(comp)
        self.utscache[pos]=comp
        if pos in self.recache:
            self.recache.remove(pos)
    def get_img(self,comp):
        # FLASHBACKS
        try:
            return imgcache[comp]
        except KeyError:
            img=comp[0][0].uts[comp[0][1]].copy()
            for t,uts in comp[1:]:
                img.blit(t.uts[uts],V(0,0))
            imgcache[comp]=img
            return img
    def render(self,surf,poss,start,offset,area,player):
        ox,oy=V(0,self.off)+offset
        sx,sy=start
        for v in poss:
            vx,vy=v
            if v in self.utscache and v not in self.recache:
                surf.blit(self.get_img(self.utscache[v])[3],((vx - sx) * 64 + ox, (vy - sy) * 64 + oy))
            elif self[v]:
                self.regen_uts(v,area)
                surf.blit(self.get_img(self.utscache[v])[3], ((vx - sx) * 64 + ox, (vy - sy) * 64 + oy))
    def __setitem__(self, key, value):
        self.objs[key] = value
        self.recache.add(key)
        self.recache.update(set(Vector.iter_offsets(key,Vector.vdirs+Vector.ddirs)))