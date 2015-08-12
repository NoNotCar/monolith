'''
Created on 13 Jun 2015
The Base Of All Things
@author: Thomas
'''
import Img
import sys

sellsound=Img.sndget("Pickup_Coin.wav")
class Object(object):
    #Immovable things like trees and pipes
    img=Img.blank32
    name="Object"
    solid=True
    updatable=False
    playerenter=True
    is3d=False
    hasio=False
    ispipe=False
    mcol=None
    off3d=6
    def __init__(self,x,y):
        self.x=x
        self.y=y
    #override for animation
    def get_img(self,world):
        return self.img
    def cut(self,world):
        pass
    def drop(self,world,ent):
        pass
    def is_owner(self,player):
        return False
class OObject(Object):
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.owner=owner
    def is_owner(self,player):
        return player is self.owner
class SellPoint(Object):
    solid=False
    playerenter=False
    img=Img.imgret2("SellPoint.png")
    name="SellPoint"
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.owner=owner
    def drop(self,world,ent):
        world.ents.remove(ent)
        self.owner.money+=ent.value
        sellsound.play()
    def is_owner(self,player):
        return False
class Mountain(Object):
    img=Img.imgret2("Mountain.png")
class SellPointBlock(OObject):
    solid=False
    playerenter=False
    img=Img.imgret2("BuyBlock.png")
    name="SellPointBlock"
    is3d=True
    hasio="input"
    doc="Placeable selling point with io. IO: Input"
    def input(self,ent):
        self.owner.money+=ent.value
        sellsound.play()
        return True
class Monolith(OObject):
    updatable=True
    img=Img.imgret2("Monolith.png")
    doc="Build this to win the game!"
    def __init__(self,x,y,owner):
        self.x=x
        self.y=y
        self.countdown=60
        self.owner=owner
    def update(self,world):
        self.countdown-=1
        if self.countdown==0:
            print "PLAYER %s WIN" % str(self.owner.num)
            sys.exit()