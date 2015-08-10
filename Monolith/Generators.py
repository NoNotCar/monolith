'''
Created on 21 Jun 2015
And the computer said .generate(world) and it was
@author: Thomas
'''
import math
import Forestry
import Hunting
import RGB
import Object
import Fishery
import Entity
import Tools
from random import randint,shuffle
e=enumerate
ruleround=((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
class Generator:
    music=None
    bm=0
    extabs=[]
    etools=[]
    def generate(self,world):
        for x in range(len(world.terr)):
            for y in range(len(world.terr[0])):
                self.generatec(world,x,y)
        self.egen(world)
        return self.music
    def egen(self,world):
        pass
    def generatec(self,world,x,y):
        pass
class Original(Generator):
    music="NNC_SPLASH.ogg"
    extabs=[Forestry.FTab]
    extools=[Tools.Axe]
    def __init__(self):
        self.lake=randint(10,22),randint(7,18)
    def egen(self,world):
        for n in range(randint(3,5)):
            tx = randint(1, 30)
            ty = randint(1, 23)
            if world.get_tid(tx,ty)==1:
                world.spawn_obj(Hunting.RabbitHole(tx,ty))
    def generatec(self,world,x,y):
        generatelake(x,y,5,self.lake,3,5,world)
        dmiddle=math.sqrt(abs(x-16)**2+abs(y-12)**2)
        if dmiddle<randint(3,12) and not world.get_tid(x,y):
            if randint(0,50):
                world.spawn_obj(Forestry.Tree(x,y))
            else:
                world.spawn_obj(Forestry.SpTree(x,y))
class HeightMap(Generator):
    music="NNC_SPLASH.ogg"
    extabs=[Forestry.FTab,Fishery.FisheryTab]
    bm=1000
    etools=[Fishery.FishingRod,Tools.Axe]
    def generate(self,world):
        poss=[]
        heightmap=[[None]*len(world.terr[0]) for n in range(len(world.terr))]
        for x in range(len(world.terr)):
            for y in range(len(world.terr[0])):
                poss.append((x,y))
        shuffle(poss)
        heightmap[0][0]=5
        for pos in poss:
            x,y=pos
            roundp=[]
            if heightmap[x][y] is None:
                for dx,dy in ruleround:
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
        return self.music
class EcoDesert(Generator):
    music="desert.ogg"
    extabs=[Forestry.FTab]
    extools=[Tools.Axe]
    def generatec(self,world,x,y):
        dmiddle=math.sqrt(abs(x-16)**2+abs(y-12)**2)
        if dmiddle<randint(2,4):
            if randint(0,50):
                world.spawn_obj(Forestry.Tree(x,y))
            else:
                world.spawn_obj(Forestry.SpTree(x,y))
        elif dmiddle>randint(6,8):
            world.set_terr(x,y,4)
class RGBFactory(Generator):
    music="Tetris.ogg"
    extabs=[RGB.RGBCategory]
    bm=5000
    def generatec(self,world,x,y):
        world.set_terr(x,y,6)
    def egen(self,world):
        for n in range(randint(4,6)):
            tx = randint(1, 30)
            ty = randint(1, 23)
            world.spawn_obj(RGB.RGBSpawner(tx,ty,(0,0,0)))
        for n in range(randint(4,6)):
            tx = randint(1, 30)
            ty = randint(1, 23)
            world.spawn_obj(RGB.RGBSpawner(tx,ty,(255,255,255)))
class RGBPuzzle(Generator):
    music="Tetris.ogg"
    extabs=[RGB.RGBCategoryPuzz]
    bm=1000000
    def __init__(self,rgb):
        self.rgb=rgb
    def generatec(self,world,x,y):
        world.set_terr(x,y,6)
    def egen(self,world):
        world.spawn_obj(RGB.RGBSpawner(0,24,(0,0,0)))
        world.spawn_obj(RGB.RGBGoal(15,24,self.rgb))
        world.spawn_obj(RGB.RGBSpect(16,24,None,self.rgb))
class Test(Generator):
    music="Tetris.ogg"
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
gens=[Original(),EcoDesert(),RGBFactory(),HeightMap(),Test()]
puzzles=[[RGBPuzzle((0,0,0)),RGBPuzzle((0,255,0)),RGBPuzzle((255,255,255)),RGBPuzzle((127,127,0))],
         [RGBPuzzle((63,0,63)),RGBPuzzle((0,191,63)),RGBPuzzle((127,63,191)),RGBPuzzle((31,127,0))]]