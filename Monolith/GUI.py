'''
Created on 14 Aug 2015
Seeing is possibly believing
@author: NoNotCar
'''
import Img
import pygame
import sys
clock=pygame.time.Clock()
class GUI(object):
    def run(self,screen,player):
        pass
class WinGUI(GUI):
    def run(self,screen,player):
        screen.fill((255,255,255))
        Img.bcentre(Img.bfont,"WIN",screen)
        pygame.display.flip()
        pygame.time.wait(1000)
        sys.exit()
class PauseGUI(GUI):
    def run(self,screen,player):
        """The pause GUI should use minimal system resources"""
        pygame.mixer.music.pause()
        screen.fill((255,255,255))
        Img.bcentre(Img.bfont,"Paused",screen)
        pygame.display.flip()
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    sys.exit()
                if e.type==pygame.KEYDOWN and e.key==pygame.K_p:
                    pygame.mixer.music.unpause()
                    return None
            pygame.time.wait(200)
class ListGui(GUI):
    addimg=Img.imgret2("AddItem.png")
    def __init__(self,menutext,colour=(0,0,0)):
        self.mtxt=menutext
        self.mtxtc=colour
        self.contents=set()
        self.contentsimgs=[]
    def run(self,screen,player):
        arect=pygame.Rect(-1,-1,0,0)
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    sys.exit()
                if e.type==pygame.MOUSEBUTTONDOWN:
                    mpos=pygame.mouse.get_pos()
                    if arect.collidepoint(mpos):
                        self.contents.add(player.hand.name)
                        self.contentsimgs.append(player.hand.img)
                    elif pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        return None
            screen.fill((100,100,100))
            screen.blit(Img.pfont.render(self.mtxt,True,self.mtxtc),(0,0))
            nx=0
            for img in self.contentsimgs:
                screen.blit(img,(nx,32))
                nx+=32
            if player.hand and player.hand.name not in self.contents:
                arect=screen.blit(self.addimg,(nx,32))
            pygame.display.flip()