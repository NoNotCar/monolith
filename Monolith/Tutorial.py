'''
Created on 31 Aug 2015

@author: NoNotCar
'''
import Object
from Buyers import ObjBuyer,RotObjBuyer,Buyer
import Img
from GUI import HelpGUI
import Tools
import Mech
import Forestry
class Help(Buyer):
    doc="Right click for help!"
    forward=False
    img=Img.imgret2("Tutorial/Help.png")
    def __init__(self,num):
        self.cost=0
        self.gui=HelpGUI(Img.imgret("Tutorial/"+str(num)+".png"))
    def buy(self, world, tx, ty, p):
        world.run_GUI(self.gui)
        return True
    def get_img(self, world):
        return self.img
class Tutorial(object):
    musics=None
    bm=0
    extabs=[]
    extools=[]
    gspoint=True
    pmenu=[]
    def __init__(self,generator):
        self.generator=generator
    def generate(self,world):
        world.player.menu=self.pmenu
        return self.generator.generate(world)
    def egen(self,world):
        pass
    def generatec(self,world,x,y):
        pass
class TT1(Tutorial):
    def __init__(self,generator,pmenu,extools):
        self.generator=generator
        self.pmenu=pmenu
        self.extools=extools
    def generate(self,world):
        world.player.menu=self.pmenu
        return self.generator.generate(world)
    def egen(self,world):
        pass
    def generatec(self,world,x,y):
        pass
tutorials=[[[Help(1),ObjBuyer(Object.Monolith,1000)],[Tools.Axe]],
           [[Help(2),RotObjBuyer(Mech.SlowConv,25),ObjBuyer(Object.Monolith,2000)],[Tools.Axe]],
           [[Help(3),ObjBuyer(Forestry.AutoChopper,500),RotObjBuyer(Mech.Output,25),RotObjBuyer(Mech.SlowConv,25),ObjBuyer(Object.Monolith,10000)],[Tools.Axe]]]