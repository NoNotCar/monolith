'''
Created on 13 Jun 2015
And The Earth Rose To Cleanse Him
@author: NoNotCar
'''
import Img
from random import randint,choice
import Forestry
class Terrain(object):
    image=Img.blank32
    walkspeed=10
    iswasser=False
    mcol=(200,200,200)
    def ranupdate(self,world,x,y):
        pass
ruleround=((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
class Grass(Terrain):
    image=Img.imgret2("Grass2.png")
    mcol=(0,255,0)
    def ranupdate(self,world,x,y):
        if world.is_empty(x,y):
            trees=[]
            for coords in ruleround:
                if world.get_obj(x+coords[0],y+coords[1]) and "Tree" == world.get_objname(x+coords[0],y+coords[1])[:4]:
                    trees.append(world.get_objname(x+coords[0],y+coords[1]))
            if 6>len(trees)>randint(0,5):
                Treetype=choice(trees)
                world.objs[x][y]={x.name:x for x in [Forestry.Tree,Forestry.SpTree]}[Treetype](x,y)
class Road(Terrain):
    image=Img.imgret2("Road.png")
    walkspeed=5
class Gravel(Terrain):
    image=Img.imgret2("Gravel.png")
    walkspeed=20
class Sand(Terrain):
    mcol=(255,255,0)
    image=Img.imgret2("Sand.png")
    walkspeed=20
class Sand2(Sand):
    mcol=(200,200,0)
    image=Img.imgret2("Sand2.png")
class Dirt(Terrain):
    image=Img.imgret2("Dirt.png")
    walkspeed=20
    def ranupdate(self,world,x,y):
        world.set_terr(x,y,0)
class Wasser(Terrain):
    mcol=(0,0,255)
    image=Img.imgret2("Wasser.png")
    walkspeed=20
    iswasser=True
class Metal(Terrain):
    image=Img.imgret2("Metal.png")
    walkspeed=8
class Bridge(Terrain):
    image=Img.imgret2("Bridge.png")
    walkspeed=8
class GrassIF(Terrain):
    image=Img.imgret2("GrassIF.png")
    walkspeed=8
class Field(Terrain):
    image=Img.imgret2("Farming\\Farmland.png")
    mcol=(66,26,0)
                
terrlist=[Grass(),Road(),Gravel(),Dirt(),Sand(),Wasser(),Metal(),Sand2(),Bridge(),GrassIF(),Field()]