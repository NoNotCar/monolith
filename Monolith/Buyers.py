'''
Created on 14 Jun 2015
FOUND A BUYER!!!
@author: NoNotCar
'''
import Terrain
import Img
import pygame


class Buyer(object):
    forward = True
    iscat = False
    doc = "ABBA JAV"
    ismoney = True

    def buy(self, world, tx, ty, p):
        return True

    def get_img(self, world):
        return Terrain.Img.blank32

    def rotate(self):
        pass


class TerrBuyer(Buyer):
    forward = False
    doc = "Replaces the tile you are standing on"

    def __init__(self, tid, cost):
        self.tid = tid
        self.cost = cost

    def buy(self, world, tx, ty, p):
        if world.get_tid(tx, ty) not in [self.tid, 8]:
            world.set_terr(tx, ty, self.tid)
            return True
        return False

    def get_img(self, world):
        return Terrain.terrlist[self.tid].image


class BridgeBuyer(Buyer):
    forward = True
    doc = "Builds a bridge tile in the water"
    img = Img.imgret2("BridgeB.png")

    def __init__(self):
        self.tid = 8
        self.cost = 500

    def buy(self, world, tx, ty, p):
        if world.get_tid(tx, ty) == 5:
            world.set_terr(tx, ty, self.tid)
            return True
        return False

    def get_img(self, world):
        return self.img


class RotObjBuyer(Buyer):
    forward = True

    def __init__(self, objclass, cost):
        self.objclass = objclass
        self.cost = cost
        self.renobj = objclass(0, 0, 0, None)
        self.dir = 0
        if hasattr(objclass, "doc"):
            self.doc = objclass.doc

    def get_img(self, world):
        nsurf = Img.blank32.copy()
        nsurf.blit(self.renobj.get_img(world), (0, 0))
        return nsurf

    def rotate(self):
        self.dir = (self.dir + 1) % 4
        self.renobj.dir = self.dir

    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty):
            world.spawn_obj(self.objclass(tx, ty, self.dir, p))
            return True
        return False


class ObjBuyer(Buyer):
    forward = True

    def __init__(self, objclass, cost):
        self.objclass = objclass
        self.cost = cost
        self.renobj = objclass(0, 0, None)
        if hasattr(objclass, "doc"):
            self.doc = objclass.doc

    def get_img(self, world):
        nsurf = Img.blank32.copy()
        nsurf.blit(self.renobj.get_img(world), (0, 0))
        return nsurf

    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty):
            world.spawn_obj(self.objclass(tx, ty, p))
            return True
        return False


class CrObjBuyer(ObjBuyer):
    forward = True
    ismoney = False

    def __init__(self, objclass):
        self.objclass = objclass
        self.name = objclass.name
        self.renobj = objclass(0, 0, None)
        if hasattr(objclass, "doc"):
            self.doc = objclass.doc


class CRotObjBuyer(RotObjBuyer):
    forward = True
    ismoney = False

    def __init__(self, objclass):
        self.objclass = objclass
        self.name = objclass.name
        self.dir = 0
        self.renobj = objclass(0, 0, 0, None)
        if hasattr(objclass, "doc"):
            self.doc = objclass.doc


class UnOwnObjBuyer(ObjBuyer):
    forward = True

    def __init__(self, objclass, cost):
        self.objclass = objclass
        self.cost = cost
        self.renobj = objclass(0, 0)
        if hasattr(objclass, "doc"):
            self.doc = objclass.doc

    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty):
            world.spawn_obj(self.objclass(tx, ty))
            return True
        return False


class VBuyer(Buyer):
    forward = True

    def __init__(self, vclass, cost):
        self.vclass = vclass
        self.cost = cost
        self.img = self.vclass.img
        if hasattr(vclass, "doc"):
            self.doc = vclass.doc

    def get_img(self, world):
        return self.img

    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty, self.vclass.boat):
            world.spawn_ent(self.vclass(tx, ty, p))
            return True
        return False
