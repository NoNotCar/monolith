'''
Created on 15 Aug 2015
Universal Machines
@author: NoNotCar
'''
import Object
import Img
import Buyers
class Incinerator(Object.OObject):
    is3d=True
    img=Img.imgret2("UM/Incinerator.png")
    hasio="Input"
    doc="Burns fuel to destroy items (such as fish poo). IO: Input (2 recommended)"
    hasio="input"
    updatable=True
    fuels={"Woodpile":60,"WoodpileSp":30}
    def __init__(self, x, y, owner):
        self.x=x
        self.y=y
        self.owner=owner
        self.fuel=0
    def update(self,world):
        if self.fuel:
            self.fuel-=1
    def input(self,ent):
        if self.fuels.has_key(ent.name):
            if not self.fuel:
                self.fuel=self.fuels[ent.name]*60
                return True
            return False
        elif self.fuel:
            return True
        return False
class UMCategory(object):
    img=Img.imgret2("UM/logo.png")
    iscat=True
    doc="Universal Machines"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(Incinerator,1000)]