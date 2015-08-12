'''
Created on 13 Jun 2015
The Trees Are Growing Once More
@author: NoNotCar
'''
import Object
import Entity
import Vehicles
import Img
import Buyers
trimg=Img.imgret2("Tree.png")
   
class Woodpile(Entity.ResourceB):
    img=Img.imgret2("Wood.png")
    value=100
    name="Woodpile"
class Paper(Entity.ResourceB):
    img=Img.imgret2("Paper.png")
    value=15
    name="Paper"
class WoodpileSp(Entity.ResourceB):
    img=Img.imgret2("WoodSp.png")
    value=500
    name="WoodpileSp"
class AutoChopper(Object.OObject):
    solid=True
    is3d=True
    img=Img.imgret2("AutoChopper.png")
    hasio="output"
    updatable=True
    doc="Chops down trees in the 3x3 square around it and outputs the logs. IO: Output"
    def __init__(self,x,y,owner):
        Object.OObject.__init__(self,x,y,owner)
        self.idle=60
        self.output=[]
    def update(self,world):
        if self.idle==0:
            for x in range(self.x-1,self.x+2):
                for y in range(self.y-1,self.y+2):
                    if world.get_obj(x,y) and world.get_objname(x,y)[:4]=="Tree" and not self.output:
                        self.output.append(world.get_obj(x,y).cut(world,False))
                        break
            self.idle=60
        else:
            self.idle-=1
class AutoChopperPlus(AutoChopper):
    img=Img.imgret2("AutoChopperPlus.png")
    doc="Chops down trees in the 5x5 square around it and outputs the logs. IO: Output"
    def update(self,world):
        if self.idle==0:
            for x in range(self.x-2,self.x+3):
                for y in range(self.y-2,self.y+3):
                    if not (x in range(self.x-1,self.x+2) and y in range(self.y-1,self.y+2)) and world.get_obj(x,y) and world.get_objname(x,y)[:4]=="Tree" and not self.output:
                        self.output.append(world.get_obj(x,y).cut(world,False))
                        break
            self.idle=60
        else:
            self.idle-=1
class PaperMill(Object.OObject):
    solid=True
    is3d=True
    img=Img.imgret2("PaperMill.png")
    hasio="both"
    updatable=False
    doc="Will turn 1 log into 10 paper. Paper is worth "+"\xa3"+"15. IO: Both"
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.owner=owner
        self.output=[]
    def input(self,ent):
        if not self.output and ent.name[:8]=="Woodpile":
            for x in range(10):
                self.output.append(Paper(self.x,self.y))
            return True
        return False
        
class Tree(Object.Object):
    img=trimg
    name="Tree"
    woodpileclass=Woodpile
    doc="Plants a tree"
    mcol=(0,127,0)
    def cut(self,world,drop=True):
        world.dest_obj(self.x,self.y)
        if drop:
            newent=self.woodpileclass(self.x,self.y)
            world.ents.append(newent)
            return newent
        else:
            return self.woodpileclass(self.x,self.y)
    def is_owner(self,player):
        return False
class SpTree(Tree):
    img=Img.imgret2("TreeSp.png")
    name="TreeSp"
    doc="Plants a tree"
    woodpileclass=WoodpileSp
class ChopMaster9000(Vehicles.Vehicle):
    #A Superb creation from NoNotCo.
    img=Img.imgret2("SawTruck.png")
    doc="This will cut down trees it runs into and has storage for 9 logs"
    def movev(self, direction, world):
        if not self.moving:
            tx=self.x+direction[0]
            ty=self.y+direction[1]
            self.dir=(direction[0],direction[1])
            if world.inworld(tx,ty):
                if world.is_clear(tx,ty,True):
                    self.movesteps(direction[0],direction[1], self.vspeed, world, True)
                    if not world.get_tid(tx,ty):
                        world.set_terr(tx,ty,3)
                elif world.get_obj(tx,ty) and world.get_objname(tx,ty)[:4]=="Tree" and len(self.output)<9:
                    self.output.append(world.get_obj(tx,ty).cut(world,False))
                    self.movesteps(direction[0],direction[1], self.vspeed, world, True)
                    world.set_terr(tx,ty,3)
class ChopMaster1000(Vehicles.Vehicle):
    #A pretty good creation from NoNotCo.
    img=Img.imgret2("SawCar.png")
    vspeed=8
    doc="This will cut down trees it runs into and leaves the logs lying around."
    def exinit(self,x,y,p):
        self.hiddenent=None
    def movev(self, direction, world):
        if not self.moving:
            tx=self.x+direction[0]
            ty=self.y+direction[1]
            self.dir=(direction[0],direction[1])
            if world.inworld(tx,ty):
                if world.is_clear(tx,ty,True):
                    self.movesteps(direction[0],direction[1], self.vspeed, world, True,ignoreobs=True)
                    if self.hiddenent:
                        self.hiddenent.hidden=False
                        self.hiddenent=None
                elif world.get_obj(tx,ty) and world.get_objname(tx,ty)[:4]=="Tree":
                    if self.hiddenent:
                        self.hiddenent.hidden=False
                    self.hiddenent=world.get_obj(tx,ty).cut(world)
                    self.hiddenent.hidden=True
                    self.movesteps(direction[0],direction[1], self.vspeed, world, True,ignoreobs=True)
class FTab(object):
    img=Img.imgret2("Tree.png")
    iscat=True
    doc="Things to do with Trees"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(AutoChopper,1000),Buyers.ObjBuyer(PaperMill,2000),Buyers.VBuyer(ChopMaster9000,3000),
                   Buyers.ObjBuyer(AutoChopperPlus,5000),Buyers.VBuyer(ChopMaster1000,1000),Buyers.UnOwnObjBuyer(Tree,1000),Buyers.UnOwnObjBuyer(SpTree,5000)]