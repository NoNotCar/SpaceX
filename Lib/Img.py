__author__ = 'NoNotCar'
import pygame
import os
from random import choice, randint
import math
import colorsys
from itertools import count
from collections import defaultdict

tau = math.pi * 2
hpi = math.pi / 2

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()
from . import Colour

class ScaledImage(object):
    def __init__(self,img):
        self.imgs=img if isinstance(img,list) else (img,)+tuple(xn(img,n) for n in (2,3,4))
        self.img=self.imgs[0]
        self.h,self.w=self.img.get_height(),self.img.get_width()
    def blit(self,other,tpos,**kwargs):
        for n,i in enumerate(self.imgs):
            i.blit(other.imgs[n],(tpos[0]*(n+1),tpos[1]*(n+1)),**kwargs)
    def copy(self):
        return ScaledImage(self.img.copy())
    def __getitem__(self, item):
        return self.imgs[item]
def path(fil):
    return np(loc+fil)
def convertx(i):
    return i.convert_alpha()
    """px=pygame.PixelArray(i)
    for p in px:
        for n in p:
            if i.unmap_rgb(n)[3]!=255:
                del px
                return i.convert_alpha()
    else:
        del px
        return i.convert()"""
def img(fil):
    return convertx(pygame.image.load(np(loc + fil + ".png")))
def imgx(fil):
    i=img(fil)
    return ScaledImage(i)
def imgn(fil,n):
    return xn(img(fil),n)
def xn(img,n):
    return pygame.transform.scale(img,(int(img.get_width()*n),int(img.get_height()*n))).convert_alpha()
def ftrans(f,folder):
    return lambda x: f(folder+"/"+x)
def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstripx(fil):
    i = img(fil)
    imgs = []
    h=i.get_height()
    for n in range(i.get_width() // h):
        imgs.append(ScaledImage(i.subsurface(pygame.Rect(n * h, 0, h, h))))
    return imgs
def imgstripxf(fil,w=16):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(ScaledImage(img.subsurface(pygame.Rect(n * w, 0, w, h))))
    return imgs
def tilemapx(fil):
    if isinstance(fil,str):
        i = img(fil)
    else:
        i=fil
    imgs = []
    sz=16
    h=i.get_height()
    w=i.get_width()
    for y in range(h // sz):
        for x in range(w // sz):
            imgs.append(ScaledImage(i.subsurface(pygame.Rect(x * sz, y*sz, sz, sz))))
    return imgs
def tilesplit(tile):
    img=tile[0]
    sss=[]
    for y in range(2):
        for x in range(2):
            sss.append(ScaledImage(img.subsurface(pygame.Rect(x*8,y*8,8,8))))
    return sss
def imgstrip(fil):
    i = img(fil)
    imgs = []
    h=i.get_height()
    for n in range(i.get_width() // h):
        imgs.append(i.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstrip4f(fil,w):
    i = img(fil)
    imgs = []
    h=i.get_height()
    for n in range(i.get_width() // w):
        imgs.append(pygame.transform.scale(i.subsurface(pygame.Rect(n * w, 0, w, h)), (w*4, h*4)).convert_alpha())
    return imgs
def imgstripxfs(fil,ws):
    i = img(fil)
    imgs = []
    h = i.get_height()
    cw=0
    for w in ws:
        imgs.append(ScaledImage(i.subsurface(pygame.Rect(cw, 0, w, h))))
        cw+=w
    return imgs
def imgrot(i,r=4):
    if isinstance(i,str):
        i=imgx(i)
    imgs=[i]
    for n in range(r-1):
        imgs.append(ScaledImage(pygame.transform.rotate(i[0],-90*n-90)))
    return imgs
def imgstriprot(fil,r=4):
    return [imgrot(i,r) for i in imgstripx(fil)]
def irot(i,n):
    return ScaledImage(pygame.transform.rotate(i.img,-90*n))
def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col, )
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col, )
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.top = y
    return surface.blit(render, textrect)
def bcentrerect(font, text, surface, rect, col=(0, 0, 0),yoff=0):
    render = font.render(str(text), True, col, )
    textrect = render.get_rect()
    textrect.centerx = rect.centerx
    textrect.centery = rect.centery+yoff
    return surface.blit(render, textrect)
def cxblit(source, dest, y, xoff=0):
    srect=source.get_rect()
    drect=dest.get_rect()
    srect.centerx=drect.centerx+xoff
    srect.top=y
    return dest.blit(source,srect)
def bcentrepos(font,text,surface,cpos,col=(0,0,0)):
    render = font.render(str(text), True, col, )
    textrect = render.get_rect()
    textrect.center=cpos
    return surface.blit(render, textrect)
def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sounds/"+fil+".wav"))

def hflip(img):
    return [img,ScaledImage(pygame.transform.flip(img.img,1,0))]
def vflip(img):
    return [img,ScaledImage(pygame.transform.flip(img.img,0,1))]
def ixn(img,n):
    return pygame.transform.scale(img,(img.get_width()*n,img.get_height()*n))
def x4(img):
    return xn(img,4)
def colswap(img,sc,ec):
    if isinstance(img,pygame.Surface):
        px=pygame.PixelArray(img)
        px.replace(sc,ec)
    else:
        for i in img.imgs:
            px = pygame.PixelArray(i)
            px.replace(sc, ec)
    return img
def colcopy(i,sc,ec):
    if isinstance(i,list):
        return [colcopy(img,sc,ec) for img in i]
    i=i.imgs[0].copy()
    colswap(i,sc,ec)
    return ScaledImage(i)
def multicolcopy(img,*args):
    img=colcopy(img,*args[0])
    for s,e in args[1:]:
        colswap(img,s,e)
    return img
def supercolcopy(img,col):
    if isinstance(img,list):
        return [supercolcopy(i,col) for i in img]
    return multicolcopy(img,((255,255,255),col),((192,192,192),Colour.darker(col,0.75)),((191,191,191),Colour.darker(col,0.75)),((128,128,128),Colour.darker(col)),((64,64,64),Colour.darker(col,0.25)))
def new_bot(fil, col):
    imgs=imgstripx(fil)
    for i in imgs:
        colswap(i,(128,128,128),col)
    return imgs
def conv_imgs(fil):
    src=img(fil)
    conv=src.subsurface(pygame.Rect(2,0,12,16))
    imgs=[]
    for n in range(16):
        new=src.copy()
        new.blit(conv,(2,-n))
        new.blit(conv,(2,16-n))
        imgs.append(ScaledImage(new))
    return [imgrot(i) for i in imgs]
def musplay(song,loops=-1):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(np(loc+"Music/"+song+".ogg"))
    pygame.mixer.music.play(loops)
def polplus(pos,ang,l):
    return tuple(map(sum, zip(pos, (l*math.cos(ang),l*math.sin(ang)))))
def draw_rotor(screen,center,radius,arms,angle,col,w=4):
    for n in range(arms):
        #magic
        pygame.draw.polygon(screen,col,(polplus(center,angle-hpi,w),polplus(center,angle+hpi,w),polplus(polplus(center,angle+hpi,w),angle,radius),polplus(polplus(center,angle-hpi,w),angle,radius)))
        angle+=tau/arms
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    rots=[]
    for i in image.imgs:
        orig_rect = i.get_rect()
        rot_image = pygame.transform.rotate(i, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rots.append(rot_image.subsurface(rot_rect).copy())
    return ScaledImage(rots)
def lotsrots(img,degscale,sym=1):
    return [rot_center(img,ang) for ang in range(0,360//sym,degscale)]
imss=[]
class ImageManager(object):
    def __init__(self):
        self.imgs={}
        imss.append(self)
    def register(self):
        used=self.imgs.keys()
        new= next((n for n in count() if n not in used))
        self[new]
        return new
    def gen_img(self):
        return None
    def __getitem__(self, item):
        try:
            return self.imgs[item]
        except KeyError:
            ni=self.gen_img()
            self.imgs[item]=ni
            return ni
    def reload(self):
        self.imgs={}
class RandomImageManager(ImageManager):
    def __init__(self,imgs,cf,sc=(128,128,128)):
        self.i=imgs
        self.cf=cf
        self.sc=sc
        ImageManager.__init__(self)
    def gen_img(self):
        return colcopy(choice(self.i),self.sc,self.cf())
class KeyedImageManager(object):
    def __init__(self):
        self.imgs={}
    def gen_img(self,args):
        return None
    def __getitem__(self, args):
        try:
            return self.imgs[args]
        except KeyError:
            ni=self.gen_img(args)
            self.imgs[args]=ni
            return ni
class SuperImageManager(KeyedImageManager):
    def __init__(self,base):
        self.base=base
        KeyedImageManager.__init__(self)
    def gen_img(self,args):
        return supercolcopy(self.base,args)
class ColourImageManager(KeyedImageManager):
    def __init__(self,base,sc=(128,128,128)):
        self.base=base
        self.sc=sc
        KeyedImageManager.__init__(self)
    def gen_img(self,args):
        return colcopy(self.base,self.sc,args)
class ColourGenerator(object):
    def __init__(self,min_sat,cd=None):
        self.ms=min_sat
        self.cd=cd
        self.gen_cols=set()
    def __call__(self, *args, **kwargs):
        while True:
            nc=tuple(randint(0,255) for _ in range(3))
            if max(nc)-min(nc)>=self.ms:
                if self.cd is None:
                    return nc
                for c in self.gen_cols:
                    cd=sum(abs(c[n]-nc[n]) for n in range(3))
                    if cd<=self.cd:
                        break
                else:
                    self.cd+=1
                    self.gen_cols.add(nc)
                    return nc
                self.cd-=1
class UltraTiles(object):
    blank=imgx("Blank")
    def __init__(self,fil,*ccs):
        tiles=imgstripx(fil)
        for n,cc in enumerate(ccs):
            if n:
                [colswap(t, cc[0], cc[1]) for t in tiles]
            else:
                [colswap(t, (128,)*3, cc) for t in tiles]
        self.tiles=[tilesplit(t) for t in tiles]
        self.cache={}
    def __getitem__(self, item):
        try:
            return self.cache[item]
        except KeyError:
            tile=self.blank.copy()
            for n,t in enumerate(item):
                tile.blit(self.tiles[t][n],(n%2*8,n//2*8))
            self.cache[item]=tile
            return tile
def fload(fil,sz=16):
    return pygame.font.Font(np(loc+fil+".ttf"),sz)
buttimg=imgx("MenuButton")[3]
def button(text,font):
    img=buttimg.copy()
    bcentre(font,text,img,-4)
    return img
# prog=imgx("Progress")
# def draw_progress(world,pos,p,col=(0,255,0)):
#     world.blit(prog,pos,oy=-4)
#     pygame.draw.rect(world.screen,col,pygame.Rect(world.screen_space(pos,ox=1,oy=-3),(world.cam_scale*p*14//16,world.cam_scale//8)))
numerals=imgstripxfs("Numbers",[5,3]+[5]*8)
def draw_num(surf,n,pos,rscale,draw_one=False):
    if n<1+(not draw_one):
        return
    n=str(n)
    x=15*rscale
    for d in reversed(n):
        x-=2*rscale if int(d)==1 else 4*rscale
        surf.blit(numerals[int(d)][rscale-1], (pos[0]+x, pos[1]+9*rscale))
def draw_with_num(surf,scimg,n,pos,rscale):
    surf.blit(scimg[rscale-1],pos)
    draw_num(surf,n,pos,rscale)
def music_mix(dir):
    return [dir+"/"+m[:-4] for m in os.listdir(np(loc+"Music/"+dir)) if m[-4:]==".ogg"]
def trans_rect(sz,col):
    surf=pygame.Surface(sz,pygame.SRCALPHA,32)
    surf.fill(col)
    return ScaledImage(surf)
class DJ(object):
    state="BLEEEEEEEEEEEEEEEEEEERGH"
    def __init__(self,state="Title"):
        self.switch(state)
    def switch(self,d):
        if self.state!=d:
            self.state=d
            self.songs=music_mix(d)
            pygame.mixer.music.stop()
    def update(self):
        if not pygame.mixer.music.get_busy():
            musplay(choice(self.songs),1)