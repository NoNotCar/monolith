'''
Created on 1 Aug 2015

@author: Thomas
'''
import Img
import Entity
import Object
import Tools
import Buyers
from random import randint
def imgref2(fil):
    return Img.imgret2("Fishery\\"+fil)
class Fish(Entity.ResourceB):
    img=imgref2("Fish.png")
    value=20
    name="Fish"
class FishingRod(Tools.Tool):
    img=imgref2("Fishingrod.png")
    def use(self,x,y,w,p):
        if not randint(0,5) and w.get_terr(x,y).iswasser and not p.hand:
            p.hand=Fish(x,y)
class Fisher(Object.OObject):
    solid=True
    is3d=True
    img=imgref2("Shocker.png")
    hasio="output"
    updatable=True
    doc="Shocks fish in the water below it and output them. Must be placed in water (obviously). IO: Output"
    def __init__(self,x,y,owner):
        Object.OObject.__init__(self,x,y,owner)
        self.idle=randint(360,1000)
        self.output=[]
    def update(self,world):
        if self.idle:
            self.idle-=1
        else:
            if not self.output:
                self.output.append(Fish(self.x,self.y))
            self.idle=randint(360,1000)
class FloatBuyer(Buyers.ObjBuyer):
    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty,True):
            world.spawn_obj(self.objclass(tx, ty, 
             p))
            return True
        return False
class FisheryTab(object):
    img=imgref2("Fish.png")
    iscat=True
    doc="Fishing apparatus"
    def __init__(self):
        self.menu=[FloatBuyer(Fisher,1000)]
            