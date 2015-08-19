'''
Created on 24 Jun 2015

@author: NoNotCar
'''
import Img
import pygame

destsound=Img.sndget("explode.wav")
class Tool(object):
    img=Img.blank32
    def use(self,x,y,world,p):
        pass
class Axe(Tool):
    img=Img.imgret2("Axe.png")
    def use(self,x,y,world,p):
        if world.get_obj(x,y):
            return world.get_obj(x,y).cut(world)
class Wrench(Tool):
    img=Img.imgret2("Wrench.png")
    def use(self,x,y,world,p):
        kmods=pygame.key.get_mods()
        if world.get_obj(x,y):
            if kmods & pygame.KMOD_LSHIFT:
                world.get_obj(x,y).rotate()
                return True
            elif kmods & pygame.KMOD_LCTRL:
                world.get_obj(x,y).wrench(world)
                return True
            elif world.get_obj(x,y).is_owner(p):
                world.dest_obj(x,y)
                destsound.play()
                return True