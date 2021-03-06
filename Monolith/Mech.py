'''
Created on 14 Jun 2015
"All The Latest Gadgets"
@author: NoNotCar
'''
import Object
import Img
import pygame
import GUI
import Buyers
import GameRegistry
import Crafting

convimgs = []
slowconvimgs = []
rainconvimgs = []
baseimg = Img.imgret("Conv/ConvBase.png")
sbaseimg = Img.imgret("Conv/ConvBaseSlow.png")
rbaseimg = Img.imgret("Conv/ConvBaseRain.png")
plusimg = Img.imgret("Conv/ConvPlus.png")
splusimg = Img.imgret("Conv/SlowConvPlus.png")
rplusimg = Img.imgret("Conv/RainConvPlus.png")
dirconv = [[-1, 0], [0, 1], [1, 0], [0, -1]]
odirconv = [[0, -1], [-1, 0], [0, 1], [1, 0]]
idirconv = [[0, 1], [1, 0], [0, -1], [-1, 0]]
for bi, imgs, pimg in [(baseimg, convimgs, plusimg), (sbaseimg, slowconvimgs, splusimg),
                       (rbaseimg, rainconvimgs, plusimg)]:
    for ani in range(14):
        bit1 = pimg.subsurface(pygame.Rect(0, 0, ani, 10))
        bit2 = pimg.subsurface(pygame.Rect(ani, 0, 14 - ani, 10))
        newimg = bi.copy()
        newimg.blit(bit1, (15 - ani, 3))
        newimg.blit(bit2, (1, 3))
        imgs.append(pygame.transform.scale(newimg, (32, 32)))
    nconvimgs = []
    for n in range(3):
        for c in imgs:
            nconvimgs.append(pygame.transform.rotate(c, n * 90 + 90))
    for ni in nconvimgs:
        imgs.append(ni)


class Conv(Object.OObject):
    name = "Conveyor"
    solid = False
    speed = 2
    images = convimgs
    doc = "Moves items on top of it"
    stopped = False

    def __init__(self, x, y, dire, owner):
        self.dir = dire
        self.x = x
        self.y = y
        self.ent = None
        self.owner = owner

    def get_img(self, world):
        if self.stopped or (self.owner is not None and self.owner.estop):
            return self.images[self.dir * 14]
        return self.images[world.anitick % 14 + self.dir * 14]

    def update(self, world):
        if self.ent.x != self.x or self.ent.y != self.y:
            self.ent = None
            self.updatable = False
            return None
        if not self.owner.estop and not self.stopped and self.ent.move(dirconv[self.dir][0], dirconv[self.dir][1],
                                                                       self.speed, world):
            self.updatable = False

    def drop(self, world, ent):
        if world.inworld(ent.x + dirconv[self.dir][0], ent.y + dirconv[self.dir][1]):
            self.ent = ent
            self.updatable = True

    def wrench(self, world):
        self.stopped = not self.stopped


class SlowConv(Conv):
    name = "SlowConveyor"
    solid = False
    speed = 0.5
    images = slowconvimgs
    doc = "Moves items on top of it slowly"

    def get_img(self, world):
        if self.stopped or (self.owner is not None and self.owner.estop):
            return self.images[self.dir * 14]
        return self.images[world.anitick // 4 % 14 + self.dir * 14]


class RainConv(Conv):
    name = "FastConveyor"
    solid = False
    speed = 4
    images = rainconvimgs
    doc = "Moves items on top of it at great speed!"

    def get_img(self, world):
        if self.stopped or (self.owner is not None and self.owner.estop):
            return self.images[self.dir * 14]
        return self.images[(world.anitick * 2) % 14 + self.dir * 14]


class Output(Object.OObject):
    name = "Output"
    solid = True
    imgb = Img.imgret("OutputBottom.png")
    imgbo = Img.imgret("OutputBottomOpen.png")
    imgt = Img.imgret("OutputTop.png")
    is3d = True
    updatable = True
    doc = "When next to a machine, outputs items in the machine's output buffer onto conveyor belts"

    def __init__(self, x, y, dire, owner):
        self.dir = dire
        self.x = x
        self.y = y
        self.machines = []
        self.owner = owner
        self.make_imgs()

    def get_img(self, world):
        return self.imgs[self.dir]

    def update(self, world):
        self.machines = []
        for direction in dirconv:
            obj = world.get_obj(self.x + direction[0], self.y + direction[1])
            if obj and obj.hasio in ["output", "both", "2both", "2output"]:
                self.machines.append(obj)
        for mach in self.machines:
            if mach.output:
                ent = mach.output[0]
                tx = self.x + odirconv[self.dir][0]
                ty = self.y + odirconv[self.dir][1]
                if world.is_clear(tx, ty) and world.get_objname(tx, ty) in ["Conveyor", "SlowConveyor", "FastConveyor"]:
                    world.spawn_ent(ent)
                    ent.place(self.x, self.y)
                    ent.move(odirconv[self.dir][0], odirconv[self.dir][1], 2, world)
                    mach.output.pop(0)
                break

    def make_imgs(self):
        self.imgs = []
        for d in range(4):
            i = pygame.Surface((16, 19))
            i.blit(pygame.transform.rotate(self.imgt, 90 * d), (0, 0))
            i.blit(self.imgbo if d == 2 else self.imgb, (0, 16))
            self.imgs.append(pygame.transform.scale2x(i))


class Output2(Output):
    name = "Output2"
    imgb = Img.imgret("Output2Bottom.png")
    imgbo = Img.imgret("Output2BottomOpen.png")
    imgt = Img.imgret("Output2Top.png")
    doc = "A secondary output, used in some machines"

    def update(self, world):
        self.machines = []
        for direction in dirconv:
            obj = world.get_obj(self.x + direction[0], self.y + direction[1])
            if obj and obj.hasio in ["2both", "2output"]:
                self.machines.append(obj)
        for mach in self.machines:
            if mach.output2:
                ent = mach.output2[0]
                tx = self.x + odirconv[self.dir][0]
                ty = self.y + odirconv[self.dir][1]
                if world.is_clear(tx, ty) and world.get_objname(tx, ty) in ["Conveyor", "SlowConveyor", "FastConveyor"]:
                    world.spawn_ent(ent)
                    ent.place(self.x, self.y)
                    ent.move(odirconv[self.dir][0], odirconv[self.dir][1], 2, world)
                    mach.output2.pop(0)
                break


class Input(Object.OObject):
    name = "Input"
    solid = False
    playerenter = False
    img = Img.imgret2("Input.png")
    is3d = True
    updatable = True
    doc = "Inputs everything dumped onto it into an adjacent machine"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.machines = []
        self.buffer = None
        self.owner = owner

    def update(self, world):
        self.machines = []
        for direction in dirconv:
            obj = world.get_obj(self.x + direction[0], self.y + direction[1])
            if obj and obj.hasio in ["input", "both", "2both"]:
                self.machines.append(obj)
        if self.buffer and self.machines:
            for mach in self.machines:
                if mach.input(self.buffer):
                    self.solid = False
                    self.buffer = None
                    break

    def drop(self, world, ent):
        self.buffer = ent
        world.ents.remove(ent)
        self.solid = True


class IOput(Input):
    name = "IOput"
    img = Img.imgret2("Input.png")
    is3d = True
    updatable = True
    doc = "Acts like an input and an output"
    imgb = Img.imgret("InputBottom.png")
    imgt = Img.imgret("IOput.png")

    def __init__(self, x, y, dire, owner):
        self.x = x
        self.y = y
        self.imachines = []
        self.omachines = []
        self.buffer = None
        self.owner = owner
        self.dir = dire
        self.make_imgs()

    def get_img(self, world):
        return self.imgs[self.dir]

    def update(self, world):
        self.imachines = []
        self.omachines = []
        for direction in dirconv:
            obj = world.get_obj(self.x + direction[0], self.y + direction[1])
            if obj and obj.hasio in ["input", "both", "2both"]:
                self.imachines.append(obj)
            if obj and obj.hasio in ["output", "both", "2both", "2output"]:
                self.omachines.append(obj)
        if self.buffer and self.imachines:
            for mach in self.imachines:
                if mach.input(self.buffer):
                    self.solid = False
                    self.buffer = None
                    break
        for mach in self.omachines:
            if mach.output:
                ent = mach.output[0]
                tx = self.x + odirconv[self.dir][0]
                ty = self.y + odirconv[self.dir][1]
                if world.is_clear(tx, ty) and world.get_objname(tx, ty) in ["Conveyor", "SlowConveyor", "FastConveyor"]:
                    world.spawn_ent(ent)
                    ent.place(self.x, self.y)
                    ent.move(odirconv[self.dir][0], odirconv[self.dir][1], 2, world)
                    mach.output.pop(0)
                break

    def drop(self, world, ent):
        self.buffer = ent
        world.ents.remove(ent)
        self.solid = True

    def make_imgs(self):
        self.imgs = []
        for d in range(4):
            i = pygame.Surface((16, 19))
            i.blit(pygame.transform.rotate(self.imgt, 90 * d), (0, 0))
            i.blit(self.imgb, (0, 16))
            self.imgs.append(pygame.transform.scale2x(i))


# For basic machines. DO NOT USE BY ITSELF
class BasicMachine(Object.OObject):
    solid = True
    is3d = True
    img = Img.imgret2("MachBlock.png")
    hasio = "both"
    updatable = False
    recipes = [["Input", None, 1]]
    doc = "This should not be in the game"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []

    def input(self, ent):
        for r in self.recipes:
            if not self.output and ent.name == r[0]:
                for _ in range(r[2]):
                    self.output.append(r[1](self.x, self.y))
                return True
        return False


class VInput(Object.OObject):
    is3d = True
    img = Img.imgret2("VIn.png")
    imgf = pygame.transform.flip(img, True, False)
    hasio = "output"
    updatable = True
    doc = "Drive a vehicle (or robot) in front of this to output its contents. IO: Output"

    def __init__(self, x, y, dire, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []
        self.dir = dire

    def get_img(self, world):
        return self.imgf if self.dir % 2 else self.img

    def update(self, world):
        if not self.output:
            for ent in world.ents:
                if ent.name == "Vehicle" or "Robotic" in ent.types:
                    if ent.x == self.x + (-1 if self.dir % 2 else 1) and ent.y == self.y and ent.output:
                        self.output.append(ent.output.pop())
                        break


class VLoader(Object.OObject):
    is3d = True
    img = Img.imgret2("VLoad.png")
    imgf = pygame.transform.flip(img, True, False)
    hasio = "input"
    updatable = True
    doc = "Drive a vehicle (or robot) in front of this to load items (if possible). IO: Input"

    def __init__(self, x, y, dire, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.lv = None
        self.dir = dire

    def get_img(self, world):
        return self.imgf if self.dir % 2 else self.img

    def update(self, world):
        if not self.lv:
            for ent in world.ents:
                if ent.name == "Vehicle" or "Robotic" in ent.types:
                    if ent.x == self.x + (-1 if self.dir % 2 else 1) and ent.y == self.y:
                        self.lv = ent
        else:
            if self.lv.x != self.x + 1 or self.lv.y != self.y:
                self.lv = None

    def input(self, ent):
        return self.lv and self.lv.load(ent)


class Buffer5(Object.OObject):
    solid = True
    is3d = True
    img = Img.imgret2("5Buffer.png")
    name = "5Buffer"
    hasio = "both"
    updatable = False
    buffer = 5
    doc = "Will store up to 5 items in an internal buffer. IO: Both"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []

    def input(self, ent):
        if len(self.output) < self.buffer:
            self.output.append(ent)
            return True
        return False


class Splitter(Object.OObject):
    solid = True
    is3d = True
    img = Img.imgret2("Splitter.png")
    name = "Splitter"
    hasio = "2both"
    updatable = False
    doc = "Splits items between its two outputs. IO: Both (2 outputs)"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []
        self.output2 = []
        self.buffer = None

    def input(self, ent):
        if self.buffer and not (self.output or self.output2):
            self.output.append(self.buffer)
            self.output2.append(ent)
            self.buffer = None
            return True
        elif not self.buffer:
            self.buffer = ent
            return True
        return False


class PurpPri(Object.OObject):
    is3d = True
    img = Img.imgret2("PPBlock.png")
    name = "PurplePrioritizer"
    hasio = "2both"
    updatable = False
    doc = "Will send items to its purple output if possible, otherwise the blue output. IO: Both (2 outputs)"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []
        self.output2 = []

    def input(self, ent):
        if not self.output2:
            self.output2.append(ent)
            return True
        elif not self.output:
            self.output.append(ent)
            return True
        return False


class Filter(Object.OObject):
    is3d = True
    img = Img.imgret2("Filter.png")
    name = "Filter"
    hasio = "2both"
    updatable = False
    doc = "Sorts items. CTRL+Wrench (with item in hand) to configure. IO: Both (2 outputs)"

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.output = []
        self.output2 = []
        self.gui = GUI.ListGui("BLUE OUTPUT:", (65, 155, 224))

    def input(self, ent):
        if ent.name in self.gui.contents:
            if not self.output:
                self.output = [ent]
                return True
            return False
        else:
            if not self.output2:
                self.output2 = [ent]
                return True
            return False

    def wrench(self, world):
        world.run_GUI(self.gui)


class MultiBlock(Object.Object):
    def __init__(self, x, y, exblock):
        self.x = x
        self.y = y
        self.eo = exblock
        self.hasio = self.eo.hasio
        self.updatable = True
        if self.hasio in ["output", "both", "2both", "2output"]:
            self.output = self.eo.output
        if self.hasio in ["2both", "2output"]:
            self.output2 = self.eo.output2

    def input(self, ent):
        return self.eo.input(ent)

    def update(self, world):
        if not world.exists(self.eo):
            world.dest_obj(self.x, self.y)


class DownTunnel(Object.OObject):
    is3d = True
    off3d = 16
    hasio = "input"
    imgs = [Img.imgret2("Tunnel/TunDown" + s + ".png") for s in ["L", "D", "R", "U"]]
    maxlength = 5
    doc = "Will send items to an upward tunnel no more than 5 tiles away. IO: Input"

    def __init__(self, x, y, dire, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.dir = dire
        self.buffer = None

    def get_img(self, world):
        return self.imgs[self.dir]

    def input(self, ent):
        if not self.buffer:
            self.buffer = ent
            self.updatable = True
            return True
        return False

    def update(self, world):
        if self.buffer:
            tx, ty = self.x, self.y
            for stretch in range(self.maxlength):
                tx += dirconv[self.dir][0]
                ty += dirconv[self.dir][1]
                if world.get_objname(tx, ty) == "UpTunnel":
                    if world.get_obj(tx, ty).addent(self, self.buffer, stretch):
                        self.buffer = None
                        self.updatable = False
                    break


class DownTunnelL(DownTunnel):
    imgs = [Img.imgret2("Tunnel/TunDownL" + s + ".png") for s in ["L", "D", "R", "U"]]
    doc = "Long distance tunnel: Will send items to an upward tunnel no more than 15 tiles away. IO: Input"
    maxlength = 15


class UpTunnel(Object.OObject):
    is3d = True
    off3d = 16
    hasio = "output"
    imgs = [Img.imgret2("Tunnel/TunUp" + s + ".png") for s in ["L", "D", "R", "U"]]
    speed = 16
    updatable = True
    name = "UpTunnel"
    doc = "Accepts items from downward tunnels and outputs them. IO: Output"

    def __init__(self, x, y, dire, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.dir = dire
        self.tunnel = []
        self.output = []
        self.wait = self.speed

    def get_img(self, world):
        return self.imgs[self.dir]

    def update(self, world):
        if self.wait:
            self.wait -= 1
        else:
            self.wait = self.speed
            for pair in self.tunnel[:]:
                if not pair[0] and not self.output:
                    self.output = [pair[1]]
                    self.tunnel.remove(pair)
                elif pair[0]:
                    if not len([x for x in self.tunnel if x[0] == pair[0] - 1]):
                        pair[0] -= 1

    def addent(self, tun, ent, stretch):
        if self.dir != tun.dir or len([x for x in self.tunnel if x[0] == stretch]):
            return False
        self.tunnel.append([stretch, ent])
        return True


class RobMechCategory(object):
    img = Img.imgret2("Gear.png")
    iscat = True
    doc = "Tech stuff"

    def __init__(self):
        self.menu = [Buyers.RotObjBuyer(DownTunnel, 200), Buyers.RotObjBuyer(DownTunnelL, 1000),
                     Buyers.RotObjBuyer(UpTunnel, 500),
                     Buyers.RotObjBuyer(Output, 100), Buyers.RotObjBuyer(Output2, 200), Buyers.ObjBuyer(Input, 100),
                     Buyers.RotObjBuyer(IOput, 300), Buyers.ObjBuyer(Buffer5, 500),
                     Buyers.ObjBuyer(Splitter, 500), Buyers.ObjBuyer(PurpPri, 500), Buyers.ObjBuyer(Filter, 500),
                     Buyers.RotObjBuyer(VInput, 50), Buyers.RotObjBuyer(VLoader, 50),
                     Buyers.ObjBuyer(Object.SellPointBlock, 10000),Buyers.ObjBuyer(Crafting.CraftingTable,50)]


GameRegistry.add_recipe(["Woodpile", "Wheat", "Wheat"], ["SlowConveyor", 4], SlowConv.images[0])
