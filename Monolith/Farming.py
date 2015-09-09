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
import Entity

randint = random.randint


class Hoe(Tools.Tool):
    img = Img.imgret2("Farming/Hoe.png")

    def use(self, x, y, world, p):
        if world.get_tid(x, y) == 0 and not world.get_obj(x, y):
            world.set_terr(x, y, 10)
            return True


class Crop(Object.OObject):
    imgs = []
    doc = "A good crop for growing"
    updatable = True
    cropitem = None
    gm = 1
    types = ["Crop"]

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.growth = 0
        self.tngrow = randint(1800 * self.gm, 3600 * self.gm)

    def get_img(self, world):
        if self.owner:
            return self.imgs[self.growth]
        return self.cropitem.img

    def update(self, world):
        if self.tngrow == 0 and self.growth < 4:
            self.growth += 1
            self.tngrow = randint(1800 * self.gm, 3600 * self.gm)
        elif self.tngrow > 0:
            self.tngrow -= 1

    def pick(self, world):
        if self.growth == 4:
            self.growth = 0
            return self.cropitem(self.x, self.y)


class WheatItem(Entity.ResourceB):
    value = 5
    img = Img.imgret2("Farming/Wheat.png")
    name = "Wheat"
    doc = "Wheat: Not a valuable crop on its own, but can be baked into bread in an oven."


class BreadItem(Entity.ResourceB):
    value = 40
    img = Img.imgret2("Farming/Bread.png")
    name = "Bread"


class BBreadItem(Entity.ResourceB):
    value = -40
    img = Img.imgret2("Farming/BurntBread.png")
    name = "Burnt Bread"


class Wheat(Crop):
    imgs = [Img.imgret2b("Farming/Wheat%s.png" % (n + 1)) for n in range(5)]
    is3d = True
    off3d = 10
    cropitem = WheatItem


class Oven(Object.OObject):
    doc = "This can be used to turn wheat into bread. Requires 200W to start, and 50W while idle. IO: Both"
    hasio = "both"
    is3d = True
    off3d = 8
    heat = 20
    updatable = True
    imgs = [Img.imgret2("Farming/Oven%s.png" % str(n)) for n in range(1, 4)]

    def __init__(self, x, y, owner):
        Object.OObject.__init__(self, x, y, owner)
        self.inv = []
        self.output = []

    def update(self, world):
        if self.heat < 250 and self.owner.get_power(200):
            self.heat += 1
        elif self.heat > 20 and not self.owner.get_power(50):
            self.heat -= 1
        if self.heat == 250:
            for pair in self.inv[:]:
                pair[1] += 1
                if pair[1] >= 1900 and not self.output:
                    self.output = [BBreadItem(self.x, self.y)]
                    self.inv.remove(pair)
                elif pair[1] >= 1800 and not self.output:
                    self.output = [BreadItem(self.x, self.y)]
                    self.inv.remove(pair)

    def input(self, ent):
        if len(self.inv) < 4 and ent.name in ["Wheat", "Flour"]:
            self.inv.append([ent, 0])
            return True

    def get_img(self, world):
        return self.imgs[2 if self.heat == 250 else 1 if self.heat >= 100 else 0]


class CropBuyer(Buyers.ObjBuyer):
    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty) and world.get_tid(tx, ty) == 10:
            world.spawn_obj(self.objclass(tx, ty, p))
            return True
        return False


class AutoPicker(Object.OObject):
    is3d = True
    img = Img.imgret2("Farming/AutoFarm.png")
    hasio = "output"
    updatable = True
    doc = "Harvests Plants in the 5x5 square around it and outputs the crops. Uses 500W. IO: Output"

    def __init__(self, x, y, owner):
        Object.OObject.__init__(self, x, y, owner)
        self.idle = 60
        self.output = []

    def update(self, world):
        hasp = self.owner.get_power(500)
        if self.idle == 0:
            for x in range(self.x - 2, self.x + 3):
                for y in range(self.y - 2, self.y + 3):
                    if world.get_obj(x, y) and not self.output and hasp:
                        ent = world.get_obj(x, y).pick(world)
                        if ent:
                            self.output.append(ent)
                            break
            self.idle = 60
        else:
            self.idle -= 1


class FarmCat(object):
    img = Img.imgret2("Farming/Hoe.png")
    iscat = True
    doc = "Farming Essentials"

    def __init__(self):
        self.menu = [CropBuyer(Wheat, 10), Buyers.ObjBuyer(Oven, 200), Buyers.ObjBuyer(AutoPicker, 1000)]
