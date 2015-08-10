'''
Created on 22 Jun 2015
NOT VERY NICE
@author: Thomas
'''
import Entity
import Object
import Img
from random import randint,choice
dirconv=[[-1,0],[0,1],[1,0],[0,-1]]
class Rabbit(Entity.ResourceB):
    img=Img.imgret2("WoodBunny.png")
    value=200
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hidden = False
        self.countdown=16
    def update(self,world,events):
        if self.pickup:
            if self.countdown==0:
                dire=choice(dirconv)
                tx=self.x+dire[0]
                ty=self.y+dire[1]
                if world.is_clear(tx,ty,True):
                    world.move_ent(self,tx,ty)
                self.countdown=randint(8,16)
            else:
                self.countdown-=1
class RabbitHole(Object.Object):
    updatable=True
    img=Img.imgret2("RabbitHole.png")
    def update(self,world):
        if not randint(0,1000) and not world.get_ent(self.x,self.y):
            world.spawn_ent(Rabbit(self.x,self.y))