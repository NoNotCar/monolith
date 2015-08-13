'''
Created on 11 Aug 2015
AGRICOLA!!!
@author: NoNotCar
'''
import Tools
import Img
import Object
import random
import Buyers
class Hoe(Tools.Tool):
    img=Img.imgret2("Farming\\Hoe.png")
    def use(self, x, y, world, p):
        if world.get_tid(x,y)==0 and not world.get_obj(x,y):
            world.set_terr(x,y,10)
class Crop(Object.OObject):
    imgs=[]
    doc="A good crop for growing"
    updatable=True
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.growth=0
    def get_img(self,world):
        return self.imgs[self.growth]
    def update(self,world):
        if not random.randint(0,2000) and self.growth<4:
            self.growth+=1
class Wheat(Crop):
    imgs=[Img.imgret32("Farming\\Wheat%s.png" % (n+1)) for n in range(5)]
    is3d=True
    off3d=10
class CropBuyer(Buyers.ObjBuyer):
    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty) and world.get_tid(tx,ty)==10:
            world.spawn_obj(self.objclass(tx, ty, p))
            return True
        return False
class FarmCat(object):
    img=Img.imgret2("Farming\\Hoe.png")
    iscat=True
    doc="Farming Essentials"
    def __init__(self):
        self.menu=[CropBuyer(Wheat,10)]