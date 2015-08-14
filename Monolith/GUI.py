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