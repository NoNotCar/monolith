'''
Created on 14 Aug 2015
Seeing is possibly believing
@author: NoNotCar
'''
import Img
import pygame
import sys
class GUI(object):
    def run(self,screen):
        pass
class WinGUI(GUI):
    def run(self,screen):
        screen.fill((255,255,255))
        Img.bcentre(Img.bfont,"WIN",screen)
        pygame.display.flip()
        pygame.time.wait(1000)
        sys.exit()
class PauseGUI(GUI):
    def run(self,screen):
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