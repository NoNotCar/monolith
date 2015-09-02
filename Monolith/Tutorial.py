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
class Help(Buyer):
    doc="Right click for help!"
    forward=False
    img=Img.imgret2("Tutorial/Help.png")
    def __init__(self,img):
        self.cost=0
        self.gui=HelpGUI(img)
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
class TestTutorial1(Tutorial):
    pmenu=[Help(Img.imgret("Tutorial/1.png")),ObjBuyer(Object.Monolith,0)]
    extools=[Tools.Axe]
class TestTutorial2(Tutorial):
    pmenu=[Help(Img.imgret("Tutorial/2.png")),RotObjBuyer(Mech.SlowConv,25),ObjBuyer(Object.Monolith,0)]
    extools=[Tools.Axe]