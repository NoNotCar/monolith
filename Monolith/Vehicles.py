'''
Created on 17 Jun 2015
Don't be late!
@author: Thomas
'''
import Entity
import Img
import pygame
class Vehicle(Entity.Entity):
    vspeed=16
    img=Img.blank32
    name="Vehicle"
    pickup=False
    solid=True
    boat=False
    def __init__(self,x,y,p):
        self.p=p
        self.x=x
        self.y=y
        self.dir=(1,0)
        self.imgflip=False
        self.fimg=pygame.transform.flip(self.img,True,False)
        self.exinit(x, y, p)
        self.output=[]
        self.hasp=False
    def exinit(self,x,y,p):
        pass
    def get_img(self):
        if self.dir==(-1,0):
            self.imgflip=True
        elif self.dir==(1,0):
            self.imgflip=False
        return [self.img,self.fimg][self.imgflip]
    def movev(self,direction,world):
        if not self.moving:
            self.dir=(direction[0],direction[1])
            self.movesteps(direction[0], direction[1], self.vspeed, world, True,self.boat)
    def update(self,world,events):
        if self.hasp:
            self.p.x,self.p.xoff,self.p.y,self.p.yoff=self.x,self.xoff,self.y,self.yoff
            self.p.vupdate(world,events,self)
class FastCar(Vehicle):
    vspeed=4
    img=Img.imgret2("FastCar.png")
    doc="This is a very fast car!"
class Boat(Vehicle):
    img=Img.imgret2("Boat.png")
    boat=True
    doc="For getting across the water"
class Lorry(Vehicle):
    #A Superb creation from NoNotCo.
    img=Img.imgret2("Truck.png")
    doc="This lorry can pick up stuff it drives over. It goes slower with more items in it"
    def update(self,world,events):
        self.vspeed=5+len(self.output)
        if self.hasp:
            self.p.vupdate(world,events,self)
    def movev(self, direction, world):
        if not self.moving:
            tx=self.x+direction[0]
            ty=self.y+direction[1]
            self.dir=(direction[0],direction[1])
            if world.inworld(tx,ty):
                if world.is_clear(tx,ty,True):
                    self.movesteps(direction[0], direction[1], len(self.output)+8, world, True)
                elif world.get_ent(tx,ty) and world.get_ent(tx,ty).pickup:
                    self.output.append(world.get_ent(tx,ty))
                    world.dest_ent(tx,ty)
                    self.movesteps(direction[0], direction[1], len(self.output)+8, world, True)