'''
Created on 31 Aug 2015

@author: NoNotCar
'''
import Object
from Buyers import ObjBuyer, RotObjBuyer, Buyer, VBuyer
import Img
from GUI import HelpGUI
import Tools
import Mech
import Forestry
import pygame
from Generators import Original


class Help(Buyer):
    doc = "Right click for help!"
    forward = False
    img = Img.imgret2("Tutorial/Help.png")

    def __init__(self, num):
        self.cost = 0
        self.gui = HelpGUI(Img.imgret("Tutorial/" + str(num) + ".png"))

    def buy(self, world, tx, ty, p):
        world.run_GUI(self.gui)
        return True

    def get_img(self, world):
        return self.img


class FilterSellPoint(Object.SellPoint):
    img = Img.imgret2("Bridge.png")

    def __init__(self, x, y, owner, fent):
        self.x = x
        self.y = y
        self.owner = owner
        self.ent = fent
        simg = pygame.transform.scale(self.ent.img, (16, 16))
        self.img.blit(simg, (4, 8))
        self.img.blit(Img.imgret("Tutorial\Psign.png"), (16, 8))

    def drop(self, world, ent):
        if ent.name == self.ent.name:
            world.ents.remove(ent)
            self.owner.sell(ent)


class Tutorial(object):
    musics = None
    bm = 0
    extabs = []
    extools = []
    gspoint = True
    pmenu = []

    def __init__(self, generator):
        self.generator = generator

    def generate(self, world):
        world.player.menu = self.pmenu
        return self.generator.generate(world)

    def egen(self, world):
        pass

    def generatec(self, world, x, y):
        pass


class TT1(Tutorial):
    def __init__(self, generator, pmenu, extools):
        self.generator = generator
        self.pmenu = pmenu
        self.extools = extools


class TT1F(TT1):
    gspoint = False

    def __init__(self, generator, pmenu, extools, fent):
        self.generator = generator
        self.pmenu = pmenu
        self.extools = extools
        self.fent = fent

    def generate(self, world):
        world.player.menu = self.pmenu
        world.spawn_obj(FilterSellPoint(0, 0, world.player, self.fent))
        return self.generator.generate(world)


ttpaper = TT1F(Original(), [Help(4), ObjBuyer(Forestry.PaperMill, 500), ObjBuyer(Forestry.AutoChopperNP, 500),
                            RotObjBuyer(Mech.Output, 25), ObjBuyer(Mech.Input, 25), RotObjBuyer(Mech.Conv, 25),
                            ObjBuyer(Object.Monolith, 10000)], [Tools.Axe], Forestry.Paper)
ttpaper.bm = 1000
tutorials = [TT1(Original(), [Help(1), ObjBuyer(Object.Monolith, 1000)], [Tools.Axe]),
             TT1(Original(), [Help(2), RotObjBuyer(Mech.SlowConv, 25), ObjBuyer(Object.Monolith, 2000)], [Tools.Axe]),
             TT1(Original(), [Help(3), ObjBuyer(Forestry.AutoChopperNP, 500), RotObjBuyer(Mech.Output, 25),
                              RotObjBuyer(Mech.Conv, 25), ObjBuyer(Object.Monolith, 10000)], [Tools.Axe]),
             ttpaper,
             TT1(Original(),
                 [Help(5), RotObjBuyer(Mech.Output, 25), RotObjBuyer(Mech.Conv, 25), ObjBuyer(Object.Monolith, 10000),
                  RotObjBuyer(Mech.VInput, 50), VBuyer(Forestry.ChopMaster9000, 1000)], [Tools.Axe]),
             TT1(Original(),
                 [Help(6), RotObjBuyer(Mech.Conv, 25), ObjBuyer(Object.Monolith, 20000), RotObjBuyer(Mech.VInput, 50),
                  VBuyer(Forestry.ChopMaster9000, 1000), ObjBuyer(Forestry.AutoChopperNP, 500),
                  ObjBuyer(Forestry.PaperMill, 500), ObjBuyer(Mech.Input, 25), RotObjBuyer(Mech.Output, 25)],
                 [Tools.Axe])]
