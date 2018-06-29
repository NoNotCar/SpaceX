import sys
import pygame
from Lib import Vector
V=Vector.VectorX
pygame.init()
pygame.font.init()
screen=pygame.display.Info()
screensize=V(screen.current_w,screen.current_h)
screen = pygame.display.set_mode(screensize,pygame.FULLSCREEN)
screen.convert()
clock=pygame.time.Clock()
from Lib import Img, Controllers, Colour, GUI
from random import randint,choice,shuffle
from Game import Gamemodes
tfont= Img.fload("cool", 64)
sfont= Img.fload("cool", 32)
controllers= [Controllers.Keyboard1()] + [Controllers.UniJoyController(n) for n in range(pygame.joystick.get_count())]
menu=GUI.System(screensize)
menu.add_screen(GUI.Screen((255,150,0)),Vector.zero)
for e in [GUI.Text("SPACEX",V(0,200),64),GUI.Button("PLAY",V(0,500),Vector.right)]:
    menu.last.add_element(e,"centre")
menu.add_screen(GUI.Screen((0,0,0)),Vector.right)
menu.last.add_element(GUI.Text("PLAYER SELECT",V(0,0),64,(255,255,255)),"centre")
menu.last.add_element(GUI.ColourSelect(controllers,V(0,100)),"centre")
menu.add_screen(GUI.Screen((0,0,50)),V(2,0))
for n,gm in enumerate(Gamemodes.gamemodes):
    menu.last.add_element(GUI.SButton(controllers,gm,V(0,n*64)),"centred")
tick=0
frame=False
def rscale(i):
    return i*16+16
def check_exit(event,no_exit=False):
    if (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE) or event.type==pygame.QUIT:
        if no_exit:
            return True
        sys.exit()
while True:
    events=pygame.event.get()
    for event in events:
        check_exit(event)
    menu.update(events)
    menu.render(screen)
    pygame.display.flip()
    if frame:
        tick+=1
        clock.tick()
    else:
        clock.tick(60)
    if tick==60:
        tick=0
        print(clock.get_fps())