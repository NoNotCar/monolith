'''
Created on 17 Aug 2015
MECHANICAL TAKEOVER
@author: NoNotCar
'''
import Entity
import Object
import Img
import pygame
import Buyers
dirconv=[[-1,0],[0,1],[1,0],[0,-1]]
diadirconv=[[-1,-1],[-1,1],[1,1],[1,-1]]
class Robot(Entity.Entity):
    name="Robot"
    types=["Robotic"]
    img=Img.imgret2("Robotics/Robot.png")
    maxload=10
    doc="A basic robot. Can hold up to 10 items."
    stopped=False
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.owner=owner
        self.direction=(0,0)
        self.output=[]
    def update(self, world, events):
        if not self.moving:
            if world.get_objname(self.x,self.y)=="Director":
                world.get_obj(self.x,self.y).direct(world,self)
            if self.direction!=(0,0) and not self.stopped:
                self.move(self.direction[0], self.direction[1], 2, world, True)
    def load(self,ent):
        if len(self.output)<self.maxload:
            self.output.append(ent)
            return True
        return False
class FarmBot(Robot):
    name="Farmbot"
    img=Img.imgret2("Robotics/FarmerBot.png")
    doc="This robot will harvest crops nest to it. Can hold up to 10 items"
    def update(self, world, events):
        if not self.moving:
            for dx,dy in dirconv:
                gobj=world.get_obj(self.x+dx,self.y+dy)
                if gobj:
                    pent=gobj.pick(world)
                    if pent:
                        self.output.append(pent)
            if world.get_objname(self.x,self.y)=="Director":
                world.get_obj(self.x,self.y).direct(world,self)
            if self.direction!=(0,0) and not self.stopped:
                self.move(self.direction[0], self.direction[1], 2, world, True)
class Director(Object.OObject):
    img=Img.imgret2("Robotics/Director.png")
    name="Director"
    solid=False
    doc="Makes the robot go in the arrow's direction"
    imgs=[pygame.transform.rotate(img,n*90) for n in range(4)]
    def __init__(self,x,y,dire,owner):
        Object.OObject.__init__(self, x, y, owner)
        self.dir=dire
    def get_img(self, world):
        return self.imgs[self.dir]
    def direct(self,world,bot):
        bot.direction=dirconv[self.dir]
class DiaDirector(Director):
    img=Img.imgret2("Robotics/DiaDirector.png")
    imgs=[pygame.transform.rotate(img,n*90) for n in range(4)]
    def direct(self,world,bot):
        bot.direction=diadirconv[self.dir]
class UnloadDir(Object.OObject):
    img=Img.imgret2("Robotics/Unload.png")
    name="Director"
    doc="Stops the robot until it is empty."
    solid=False
    def direct(self,world,bot):
        bot.stopped=len(bot.output)
class LoadDir(Object.OObject):
    img=Img.imgret2("Robotics/Load.png")
    name="Director"
    doc="Stops the robot until it is full."
    solid=False
    def direct(self,world,bot):
        bot.stopped=len(bot.output)!=bot.maxload
class RobOutput(Object.OObject):
    name="RobotOutput"
    img=Img.imgret2("Robotics/RobotOutput.png")
    is3d=True
    updatable=True
    doc="When next to a machine, outputs items in the machine's output buffer into adjacent robots."
    wait=0
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.machines=[]
        self.owner=owner
    def update(self,world):
        if not self.wait:
            self.machines=[]
            for direction in dirconv:
                obj=world.get_obj(self.x+direction[0],self.y+direction[1])
                if obj and obj.hasio in ["output","both","2both","2output"]:
                    self.machines.append(obj)
            for mach in self.machines:
                if mach.output:
                    ent=mach.output[0]
                    for bot in world.ents:
                        if "Robotic" in bot.types and not bot.moving and abs(bot.x-self.x)+abs(bot.y-self.y)==1 and bot.load(ent):
                            mach.output.pop(0)
                            self.wait=16
        else:
            self.wait-=1
class RobInput(Object.OObject):
    name="Robot Input"
    img=Img.imgret2("Robotics/RobotInput.png")
    is3d=True
    updatable=True
    doc="Inputs everything loaded from an adjacent robot into an adjacent machine"
    wait=0
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.machines=[]
        self.owner=owner
    def update(self,world):
        if not self.wait:
            self.machines=[]
            for direction in dirconv:
                obj=world.get_obj(self.x+direction[0],self.y+direction[1])
                if obj and obj.hasio in ["input","both","2both"]:
                    self.machines.append(obj)
            for mach in self.machines:
                for bot in world.ents:
                    if "Robotic" in bot.types and not bot.moving and len(bot.output) and abs(bot.x-self.x)+abs(bot.y-self.y)==1:
                        if mach.input(bot.output[0]):
                            bot.output.pop(0)
                            self.wait=16
        else:
            self.wait-=1
class RobotBuyer(Buyers.VBuyer):
    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty) or world.get_objname(tx,ty)=="Director":
            world.spawn_ent(self.vclass(tx, ty, 
             p))
            return True
        return False
class RobotCategory(object):
    img=Img.imgret2("Robotics/Robot.png")
    iscat=True
    doc="Robots!"
    def __init__(self):
        self.menu=[RobotBuyer(Robot,300),RobotBuyer(FarmBot,1000),
                   Buyers.RotObjBuyer(Director,100),Buyers.RotObjBuyer(DiaDirector,300),Buyers.ObjBuyer(UnloadDir,100),Buyers.ObjBuyer(LoadDir,100),Buyers.ObjBuyer(RobOutput,100),Buyers.ObjBuyer(RobInput,100)]