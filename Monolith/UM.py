'''
Created on 15 Aug 2015
Universal Machines
@author: NoNotCar
'''
import Object
import Img
import Buyers
import Entity
class Incinerator(Object.OObject):
    is3d=True
    img=Img.imgret2("UM/Incinerator.png")
    doc="Burns fuel to destroy items (such as fish poo). IO: Input (2 recommended)"
    hasio="input"
    updatable=True
    fuels={"Woodpile":60,"WoodpileSp":30}
    fuel=0
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
class UMRMachine(Object.OObject):
    is3d=True
    hasio="both"
    doc="Turns stuff into other stuff. This shouldn't be in the game. IO: Both"
    recipes={}
    progress=0
    ent=None
    powerusage=0
    numproducts=1
    def __init__(self, x, y, owner):
        self.x=x
        self.y=y
        self.owner=owner
        self.output=[]
    def update(self,world):
        if self.progress and self.owner.get_power(self.powerusage):
            self.progress-=1
        elif self.progress==0 and not self.output:
            self.output=[self.ent(self.x,self.y) for _ in range(self.numproducts)]
            self.ent=None
            self.updatable=False
    def input(self,ent):
        if self.recipes.has_key(ent.name) and not self.ent:
            self.ent=self.recipes[ent.name][0]
            self.progress=self.recipes[ent.name][1]
            self.updatable=True
            return True
        return False
class WoodChips(Entity.ResourceB):
    name="Wood Chips"
    img=Img.imgret2("UM/WoodChip.png")
    value=20
class FrozenFish(Entity.ResourceB):
    name="Frozen Fish"
    img=Img.imgret2("UM/FroFish.png")
    value=40
class Grinder(UMRMachine):
    imgs=[Img.imgret2("UM/Grinder%s.png" % str(n)) for n in range(5)+range(5)[::-1]]
    doc="Grinds items into 2 powder items. Consumes 500W while operating. IO: Both"
    recipes={"Woodpile":[WoodChips,240],"WoodpileSp":[WoodChips,240]}
    powerusage=500
    numproducts=2
    def get_img(self,world):
        return self.imgs[self.progress//2%10]
class Fridge(UMRMachine):
    img=Img.imgret2("UM/Fridge.png")
    doc="Freezes items (a slow process). Can freeze up to 10 items at once. Consumes 500W when starting, and 100W to keep cool. IO: Both"
    temperature=20
    updatable=True
    recipes={"Fish":[FrozenFish,3600]}
    def __init__(self, x, y, owner):
        self.x=x
        self.y=y
        self.owner=owner
        self.inv=[]
        self.output=[]
    def update(self,world):
        if self.temperature>-20 and self.owner.get_power(500):
            if world.anitick%8==0:
                self.temperature-=1
        elif self.temperature<20 and not self.owner.get_power(100):
            self.temperature+=1
        for pair in self.inv[:]:
            if pair[1]:
                pair[1]-=1
            elif pair[1]==0 and not self.output:
                self.output=[pair[0](self.x,self.y)]
                self.inv.remove(pair)
    def input(self,ent):
        if self.recipes.has_key(ent.name) and len(self.inv)<10:
            self.inv.append(self.recipes[ent.name][:])
            return True
        return False
class UMCategory(object):
    img=Img.imgret2("UM/logo.png")
    iscat=True
    doc="Universal Machines"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(Incinerator,1000),Buyers.ObjBuyer(Grinder,500),Buyers.ObjBuyer(Fridge,200)]