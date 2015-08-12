'''
Created on 24 Jun 2015

@author: NoNotCar
'''
import Img

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
class Hammer(Tool):
    img=Img.imgret2("Hammer.png")
    def use(self,x,y,world,p):
        if world.get_obj(x,y) and world.get_obj(x,y).is_owner(p):
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