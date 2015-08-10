#Import non-image modules here
import pygame
import sys
import os

#init video
pygame.init()
screen=pygame.display.set_mode((640,640))

#image modules
import World
import Generators
import Img

numplayers=1
wgen=3
pset=0
puzzles=0
pnum=0
c=pygame.time.Clock()
Img.musply("Planets\\1. Mars.ogg")
nland=Img.imgret("NiceLand.png")
rgb=[200,255,255]
tick=0
cont=True
kp=True
scroll=True
#titlescreen
srect=pygame.Rect(0,0,0,0)
while cont:
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
                sys.exit()
        elif ev.type==pygame.MOUSEBUTTONDOWN:
            mpos=pygame.mouse.get_pos()
            if srect.collidepoint(mpos):
                cont=False
    screen.fill(rgb)
    screen.blit(nland,(0,0))
    Img.bcentre(Img.bfont, "MONOLITH", screen,-200)
    srect=Img.bcentre(Img.sbfont, "START GAME", screen,275,(100,255,100))
    pygame.display.flip()
    c.tick(60)
    if rgb[1]!=0 and tick==0:
        rgb[1]-=1
        rgb[2]-=1
        tick=10
    elif tick!=0:
        tick-=1
if not scroll:
    screen=pygame.display.set_mode((1088,864))
else:
    screen=pygame.display.set_mode((352,352))
#main loop
while True:
    w=World.World(numplayers,wgen,puzzles,pnum,pset,kp,scroll)
    while not w.complete:
        e=pygame.event.get()
        for ev in e:
            if ev.type==pygame.QUIT:
                sys.exit()
        screen.fill((100,100,100))
        w.update(e)
        if scroll:
            w.scrollrender(screen)
        else:
            w.render(screen)
        pygame.display.flip()
        c.tick(60)
    pygame.mixer.music.stop()
    pygame.time.wait(1000)
    if pnum<len(Generators.puzzles[pset])-1:
        pnum+=1
    else:
        sys.exit()