'''
Created on 12 Aug 2015
POWER TO TEH PEOPLES
@author: NoNotCar
'''
import Object
import Img
import Buyers
class PowerSupply(Object.OObject):
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        if self.owner:
            self.owner.psuppliers.append(self)
    def get_power(self,world):
        return 0
class PowerStorer(Object.OObject):
    maxS=0
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.stored=0
        if self.owner:
            self.owner.pstorage.append(self)
    def give_power(self,world,amount):
        if self.stored+amount<self.maxS:
            self.stored+=amount
            return amount
        else:
            asto=self.maxS-self.stored
            self.stored=self.maxS
            return asto
class Battery(PowerStorer):
    doc="Stores electrical power. This model can store 60kJ"
    img=Img.imgret2("Electricity\\Battery.png")
    maxS=3600000
class SolarPanel(PowerSupply):
    doc="Generates power from the sun. Produces 200W"
    is3d=True
    img=Img.imgret2("Electricity\\SolarPanel.png")
    def get_power(self,world):
        return 200
class Generator1(PowerSupply):
    doc="Generates power from burning fuel. Produces 1kW. IO: Input"
    img=Img.imgret2("Electricity\\GeneratorMk1.png")
    imgon=Img.imgret2("Electricity\\GeneratorMk1on.png")
    hasio="input"
    fuels={"Woodpile":60,"WoodpileSp":30}
    def __init__(self, x, y, owner):
        PowerSupply.__init__(self, x, y, owner)
        self.fuel=0
    def get_power(self,world):
        if self.fuel:
            self.fuel-=1
            return 1000
        return 0
    def input(self,ent):
        if self.fuels.has_key(ent.name):
            self.fuel=self.fuels[ent.name]*60
            return True
        return False
    def get_img(self,world):
        if self.fuel:
            return self.imgon
        return self.img
class PowerCategory(object):
    img=Img.imgret2("PowerIcon.png")
    iscat=True
    doc="Power Suppliers and Storage"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(SolarPanel,1000),Buyers.ObjBuyer(Generator1,200),Buyers.ObjBuyer(Battery,1000)]