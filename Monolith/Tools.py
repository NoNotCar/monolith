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
            world.get_obj(x,y).cut(world)
class Wrench(Tool):
    img=Img.imgret2("Wrench.png")
    def use(self,x,y,world,p):
        kmods=pygame.key.get_mods()
        if world.get_obj(x,y):
            if kmods & pygame.KMOD_LSHIFT:
                world.get_obj(x,y).rotate()
            elif kmods & pygame.KMOD_LCTRL:
                world.get_obj(x,y).wrench(world)
            elif world.get_obj(x,y).is_owner(p):
                world.dest_obj(x,y)
                destsound.play()
class Estop(Tool):
    img1=Img.imgret2("EStop.png")
    img2=Img.imgret2("EStop2.png")
    img=img1
    def use(self,x,y,world,p):
        if not p.estop:
            p.estop=True
            self.img=self.img2
        else:
            p.estop=False
            self.img=self.img1