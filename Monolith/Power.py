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
class SolarPanel(PowerSupply):
    is3d=True
    img=Img.imgret2("Electricity\\SolarPanel.png")
    def get_power(self,world):
        return 200
class PowerCategory(object):
    img=Img.imgret2("PowerIcon.png")
    iscat=True
    doc="Power Suppliers and Storage"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(SolarPanel,1000)]