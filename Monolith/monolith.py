#Import non-image modules here
import pygame
import sys

#init video
pygame.init()
screen=pygame.display.set_mode((640,640))

#image modules
import World
import Generators
import Img
import GUI
import Tutorial

pygame.display.set_icon(Img.imgret2("Monolith.png"))
pygame.display.set_caption("monolith")
numplayers=1
wgen=0
pset=0
puzzles=0
pnum=0
c=pygame.time.Clock()
Img.musply("Planets/1. Mars.ogg")
nland=Img.imgret("NiceLand.png")
rgb=[200,255,255]
tick=0
cont=True
kp=True
#titlescreen
srect=pygame.Rect(0,0,0,0)
prect=pygame.Rect(0,0,0,0)
grects=[]
wsizemod=0
wsrects=[]
psrects=[]
godmode=False
tutorial=False
tutb=pygame.Rect(0,0,0,0)
while cont:
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
                sys.exit()
        elif ev.type==pygame.MOUSEBUTTONDOWN:
            mpos=pygame.mouse.get_pos()
            if srect.collidepoint(mpos):
                cont=False
            if prect.collidepoint(mpos):
                puzzles=not puzzles
            if tutb.collidepoint(mpos):
                tutorial=True
                puzzles=True
                cont=False
            for gr,n in grects:
                if gr.collidepoint(mpos):
                    wgen=n
            for ws,n in wsrects:
                if ws.collidepoint(mpos):
                    wsizemod=n
            for ps,n in psrects:
                if ps.collidepoint(mpos):
                    pset=n
        elif ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_g and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                godmode=True
    screen.fill(rgb)
    screen.blit(nland,(0,0))
    Img.bcentre(Img.bfont, "MONOLITH", screen,-200)
    tutb=Img.fblit(screen, Img.dfont, "TUTORIAL", (255,0,0), (0,0))
    grects=[]
    wsrects=[]
    if not puzzles:
        screen.blit(Img.dfont.render("GENERATOR:",True,(100,100,100)),(0,480))
        screen.blit(Img.dfont.render("SIZE:",True,(100,100,100)),(490,480))
        for n in range(len(Generators.gens)):
            grects.append((pygame.draw.rect(screen,(200,200,200) if n==wgen else (100,100,100),pygame.Rect(2+n*50,512,48,48)),n))
        for n in range(3):
            wsrects.append((pygame.draw.rect(screen,(200,200,200) if n==wsizemod else (100,100,100),pygame.Rect(490+n*50,512,48,48)),n))
    if puzzles:
        screen.blit(Img.dfont.render("PUZZLE SET:",True,(100,100,100)),(0,480))
        for n in range(len(Generators.puzzles)):
            psrects.append((pygame.draw.rect(screen,(200,200,200) if n==pset else (100,100,100),pygame.Rect(2+n*50,512,48,48)),n))
    srect=Img.fblit(screen,Img.sbfont, "START GAME", (100,255,100),(0,600))
    prect=Img.fblit(screen,Img.sbfont, "PUZZLES", (100,100,255) if puzzles else (50,50,127),(420,600))
    pygame.display.flip()
    c.tick(60)
    if rgb[1]!=0 and tick==0:
        rgb[1]-=1
        rgb[2]-=1
        tick=10
    elif tick!=0:
        tick-=1
#resize screen
screen=pygame.display.set_mode((384,384))
#stop music
pygame.mixer.music.stop()
screenshotting=False
#main loop
while True:
    if tutorial:
        w=World.World(1,0,2,pnum,0,kp,0,(32,32))
    else:
        w=World.World(1,wgen,puzzles,pnum,pset,kp,godmode,(32*2**wsizemod,32*2**wsizemod))
    while not w.complete:
        e=pygame.event.get()
        for ev in e:
            if ev.type==pygame.QUIT:
                sys.exit()
            elif ev.type==pygame.KEYDOWN and ev.key==pygame.K_p:
                w.run_GUI(GUI.PauseGUI())
            elif ev.type==pygame.KEYDOWN and ev.key==pygame.K_s and pygame.key.get_mods() & pygame.KMOD_LALT:
                screenshotting=True
        screen.fill((100,100,100))
        w.update(e)
        w.scrollrender(screen)
        pygame.display.flip()
        if screenshotting:
            pygame.image.save(screen,Img.np(Img.loc+"Screenshots/screen.png"))
            screenshotting=False
        c.tick(60)
    pygame.mixer.music.stop()
    pygame.time.wait(1000)
    if tutorial and pnum<len(Tutorial.tutorials)-1:
        pnum+=1
    elif not tutorial and pnum<len(Generators.puzzles[pset])-1:
        pnum+=1
    else:
        sys.exit()