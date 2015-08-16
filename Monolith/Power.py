'''
Created on 12 Aug 2015
POWER TO TEH PEOPLES
@author: NoNotCar
'''
import Object
import Img
import Buyers
import Mech
import pygame
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
class PushPlate(Mech.Conv):
    doc="Uses electromagnetic force to move items much faster than a conveyor belt could. Requires 200W"
    speed=8
    hasp=False
    imgoff=Img.imgret2("Electricity/PushPlateOff.png")
    imgon=Img.imgret2("Electricity/PushPlate.png")
    imgsoff=[pygame.transform.rotate(imgoff,n*90) for n in range(4)]
    imgson=[pygame.transform.rotate(imgon,n*90) for n in range(4)]
    updatable=True
    def get_img(self,world):
        if self.owner is not None and not any([self.hasp,self.owner.estop,self.stopped]):
            return self.imgsoff[self.dir]
        else:
            return self.imgson[self.dir]
    def update(self,world):
        if not self.owner.estop or self.stopped:
            self.hasp=self.owner.get_power(200)
            if self.hasp and self.ent and self.ent.move(Mech.dirconv[self.dir][0],Mech.dirconv[self.dir][1],self.speed,world):
                self.ent=None
    def drop(self,world,ent):
        if world.inworld(ent.x+Mech.dirconv[self.dir][0],ent.y+Mech.dirconv[self.dir][1]):
            self.ent=ent
class Battery(PowerStorer):
    doc="Stores electrical power. This model can store 60kJ"
    img=Img.imgret2("Electricity/Battery.png")
    maxS=3600000
    is3d=True
class SolarPanel(PowerSupply):
    doc="Generates power from the sun. Produces 200W"
    is3d=True
    img=Img.imgret2("Electricity/SolarPanel.png")
    def get_power(self,world):
        return 200
class Generator1(PowerSupply):
    doc="Generates power from burning fuel. Produces 1kW. IO: Input"
    img=Img.imgret2("Electricity/GeneratorMk1.png")
    imgon=Img.imgret2("Electricity/GeneratorMk1on.png")
    hasio="input"
    fuels={"Woodpile":60,"WoodpileSp":30,"Wood Chips":60}
    def __init__(self, x, y, owner):
        PowerSupply.__init__(self, x, y, owner)
        self.fuel=0
    def get_power(self,world):
        if self.fuel:
            self.fuel-=1
            return 1000
        return 0
    def input(self,ent):
        if self.fuels.has_key(ent.name) and not self.fuel:
            self.fuel=self.fuels[ent.name]*60
            return True
        return False
    def get_img(self,world):
        if self.fuel:
            return self.imgon
        return self.img
class PowerOutput(Mech.Output):
    name="PowerOutput"
    imgb=Img.imgret("OutputBottom.png")
    imgbo=Img.imgret("OutputBottomOpen.png")
    imgton=Img.imgret("Electricity/OutputTopOn.png")
    imgtoff=Img.imgret("Electricity/OutputTopOff.png")
    doc="Uses electromagnetic force to move items much faster than a standard output could. Requires 500W"
    hasp=False
    def get_img(self,world):
        return self.imgs[self.dir+self.hasp*4]
    def update(self,world):
        self.machines=[]
        self.hasp=self.owner.get_power(500)
        if self.hasp:
            for direction in Mech.dirconv:
                obj=world.get_obj(self.x+direction[0],self.y+direction[1])
                if obj and obj.hasio in ["output","both","2both","2output"]:
                    self.machines.append(obj)
            for mach in self.machines:
                if mach.output:
                    ent=mach.output[0]
                    tx = self.x + Mech.odirconv[self.dir][0]
                    ty = self.y + Mech.odirconv[self.dir][1]
                    if world.is_clear(tx,ty) and world.get_objname(tx,ty) in ["Conveyor","SlowConveyor","FastConveyor"]:
                        world.spawn_ent(ent)
                        ent.place(self.x,self.y)
                        ent.move(Mech.odirconv[self.dir][0],Mech.odirconv[self.dir][1],8,world)
                        mach.output.pop(0)
                    break
    def make_imgs(self):
        self.imgs=[]
        for d in range(8):
            img=pygame.Surface((16,19))
            img.blit(pygame.transform.rotate(self.imgton if d>3 else self.imgtoff,90*(d%4)),(0,0))
            img.blit(self.imgbo if d%4==2 else self.imgb,(0,16))
            self.imgs.append(pygame.transform.scale2x(img))
class PowerCategory(object):
    img=Img.imgret2("PowerIcon.png")
    iscat=True
    doc="Power Suppliers and Storage"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(SolarPanel,1000),Buyers.ObjBuyer(Generator1,200),Buyers.ObjBuyer(Battery,500),Buyers.RotObjBuyer(PushPlate,200),Buyers.RotObjBuyer(PowerOutput,500)]