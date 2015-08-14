'''
Created on 21 Jun 2015
And the computer said .generate(world) and it was
@author: NoNotCar
'''
import math
import Forestry
import Hunting
import RGB
import Object
import Fishery
import Farming
import Entity
import Tools
from random import randint,shuffle
e=enumerate
stdmix=["loop3.mp3","46b.ogg","Chopin.ogg"]
class Generator:
    musics=None
    bm=0
    extabs=[]
    extools=[]
    gspoint=True
    def generate(self,world):
        for x in range(len(world.terr)):
            for y in range(len(world.terr[0])):
                self.generatec(world,x,y)
        self.egen(world)
        return self.musics
    def egen(self,world):
        pass
    def generatec(self,world,x,y):
        pass
class Original(Generator):
    musics=stdmix
    extabs=[Forestry.FTab,Farming.FarmCat]
    extools=[Tools.Axe,Farming.Hoe]
    def generate(self,world):
        self.lake=randint(10,world.size[0]-10),randint(10,world.size[1]-10)
        for x in range(len(world.terr)):
            for y in range(len(world.terr[0])):
                self.generatec(world,x,y)
        self.egen(world)
        return self.musics
    def generatec(self,world,x,y):
        generatelake(x,y,5,self.lake,3,5,world)
        dmiddle=math.sqrt(abs(x-world.size[0]//2)**2+abs(y-world.size[1]//2)**2)
        if dmiddle<randint(3*world.size[0]//32,12*world.size[0]//32) and not world.get_tid(x,y):
            if randint(0,50):
                world.spawn_obj(Forestry.Tree(x,y))
            else:
                world.spawn_obj(Forestry.SpTree(x,y))
class HeightMap(Generator):
    musics=stdmix
    extabs=[Forestry.FTab,Fishery.FisheryTab,Farming.FarmCat]
    bm=1000
    extools=[Fishery.FishingRod,Tools.Axe,Farming.Hoe]
    def __init__(self,smoothness):
        self.smooth=smoothness
    def generate(self,world):
        poss=[]
        heightmap=[[None]*len(world.terr[0]) for n in range(len(world.terr))]
        for x in range(len(world.terr)):
            for y in range(len(world.terr[0])):
                poss.append((x,y))
        shuffle(poss)
        heightmap[0][0]=5
        rround=[]
        for x in range(-self.smooth,self.smooth+1):
            for y in range(-self.smooth,self.smooth+1):
                if (x,y) != (0,0):
                    rround.append((x,y))
        for pos in poss:
            x,y=pos
            roundp=[]
            if heightmap[x][y] is None:
                for dx,dy in rround:
                    tx=dx+x
                    ty=dy+y
                    if world.inworld(tx,ty) and heightmap[tx][ty] is not None:
                        roundp.append(heightmap[tx][ty])
                if roundp:
                    heightmap[x][y]=sum(roundp)//len(roundp)+randint(-1,1)
                else:
                    heightmap[x][y]=randint(-5,8)
        for x,row in e(heightmap):
            for y,value in e(row):
                world.terr[x][y]=5 if value<=0 else 7 if value==1 else 0 if value<6 else 9
                if 1<value<5:
                    if randint(0,50):
                        world.spawn_obj(Forestry.Tree(x,y))
                    else:
                        world.spawn_obj(Forestry.SpTree(x,y))
                elif value>7:
                    world.spawn_obj(Object.Mountain(x,y))
                    world.terr[x][y]=0
        return self.musics
class EcoDesert(Generator):
    musics=["desert.ogg"]
    extabs=[Forestry.FTab]
    extools=[Tools.Axe]
    def generatec(self,world,x,y):
        dmiddle=math.sqrt(abs(x-world.size[0]//2)**2+abs(y-world.size[1]//2)**2)
        if dmiddle<randint(2,4):
            if randint(0,50):
                world.spawn_obj(Forestry.Tree(x,y))
            else:
                world.spawn_obj(Forestry.SpTree(x,y))
        elif dmiddle>randint(6,8):
            world.set_terr(x,y,4)
class RGBFactory(Generator):
    musics=["loop3.mp3"]
    extabs=[RGB.RGBCategory]
    bm=5000
    gspoint=False
    def generatec(self,world,x,y):
        world.set_terr(x,y,6)
    def egen(self,world):
        for n in range(randint(4*world.sv,6*world.sv)):
            tx,ty=world.ranpos()
            world.spawn_obj(RGB.RGBSpawner(tx,ty,(0,0,0)))
        for n in range(randint(4*world.sv,6*world.sv)):
            tx,ty=world.ranpos()
            world.spawn_obj(RGB.RGBSpawner(tx,ty,(255,255,255)))
class RGBPuzzle(Generator):
    musics=["loop3.mp3"]
    extabs=[RGB.RGBCategoryPuzz]
    bm=1000000
    gspoint=False
    def __init__(self,rgb):
        self.rgb=rgb
    def generatec(self,world,x,y):
        world.set_terr(x,y,6)
    def egen(self,world):
        world.spawn_obj(RGB.RGBSpawner(0,24,(0,0,0)))
        world.spawn_obj(RGB.RGBGoal(15,24,self.rgb))
        world.spawn_obj(RGB.RGBSpect(16,24,None,self.rgb))
class Test(Generator):
    musics=["loop3.mp3"]
    def egen(self,world):
        world.spawn_ent(Entity.PathTester(5,5,world))
        world.dest_obj(5,5)
        world.dest_obj(20,20)
        world.set_terr(5,5,1)
        world.set_terr(20,20,1)
    def generatec(self,world,x,y):
        if not randint(0,2):
            world.spawn_obj(Object.Mountain(x,y))
def generatelake(x,y,tid,centre,fullsize,partsize,world):
    dmiddle=math.sqrt(abs(x-32+centre[0])**2+abs(y-25+centre[1])**2)
    if dmiddle<randint(fullsize,partsize):
        world.set_terr(x,y,tid)
gens=[Original(),EcoDesert(),RGBFactory(),HeightMap(1),HeightMap(3)]
puzzles=[[RGBPuzzle((0,0,0)),RGBPuzzle((0,255,0)),RGBPuzzle((255,255,255)),RGBPuzzle((127,127,0))],
         [RGBPuzzle((63,0,63)),RGBPuzzle((0,191,63)),RGBPuzzle((127,63,191)),RGBPuzzle((31,127,0))]]