'''
Created on 13 Jun 2015
The Grubs Squirmed and Writhed
@author: Thomas
'''
import Img
from random import choice
class Entity(object):
    #Anything that can move
    solid=False
    pickup=True
    value=0
    name="Entity"
    hidden=False
    xoff=0
    yoff=0
    speed=0
    droppable=False
    moving=False
    pathfollowing=False
    path=None
    def get_img(self):
        return Img.blank32
    def update(self,world,events):
        pass
    def mupdate(self,world,events):
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed and self.moving:
            self.xoff=0
            self.yoff=0
            self.moving=False
            if world.get_obj(self.x,self.y) and self.droppable:
                world.get_obj(self.x,self.y).drop(world,self)
            if self.droppable:
                self.pickup=True
            if self.pathfollowing:
                if len(self.path.path)>1:
                    dx,dy=self.path.next()
                    if not self.move(dx, dy, self.speed, world, True, False):
                        self.pathfollowing=False
                        self.path=None
                else:
                    self.pathfollowing=False
                    self.path=None
        else:
            if self.xoff>0:
                self.xoff-=self.speed
            elif self.xoff<0:
                self.xoff+=self.speed
            if self.yoff>0:
                self.yoff-=self.speed
            elif self.yoff<0:
                self.yoff+=self.speed
    def pathfind(self,end,world):
        if end==(self.x,self.y):
            return True
        else:
            paths=[Path([(self.x,self.y)])]
            while not len([p for p in paths if p.path[-1]==end]):
                if len(paths)==0:
                    return False
                bpaths=[]
                bscore=None
                for path in paths:
                    if bscore is None:
                        bscore=path.get_score(end)
                        bpaths.append(path)
                    elif bscore>path.get_score(end):
                        bscore=path.get_score(end)
                        bpaths=[path]
                    elif bscore==path.get_score(end):
                        bpaths.append(path)
                if len(bpaths)!=1:
                    blen = max([len(b.path) for b in bpaths])
                    bpath=choice([bp for bp in bpaths if len(bp.path)==blen])
                else:
                    bpath=bpaths[0]
                bpath.extend(paths,world)
            self.pathfollowing=True
            self.path=[p for p in paths if p.path[-1]==end][0]
            dx,dy=self.path.next()
            self.move(dx, dy, self.speed, world, True, False)
    def move(self,dx,dy,s,world,player=False,boat=False,ignoreobs=False):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty,player,boat) or (world.inworld(tx,ty) and ignoreobs):
            self.x=tx
            self.y=ty
            if self.droppable:
                self.pickup=False
            self.moving=True
            self.speed=s
            self.xoff= -dx*32
            self.yoff= -dy*32
            return True
    def movesteps(self,dx,dy,steps,world,player=False,boat=False,ignoreobs=False):
        if abs(dx)>abs(dy):
            return self.move(dx, dy, abs((dx*32.0)/steps), world, player,boat,ignoreobs)
        else:
            return self.move(dx, dy, abs((dy*32.0)/steps), world, player,boat,ignoreobs)
    def place(self,x,y):
        self.x=x
        self.y=y
class ResourceB(Entity):
    solid=True
    droppable=True
    pickup=True
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.hidden=False
    def get_img(self):
        return self.img
class Path(object):
    def __init__(self,path):
        self.path=path
    def get_score(self,end):
        return len(self.path)+abs(self.path[-1][0]-end[0])+abs(self.path[-1][1]-end[1])
    def extend(self,paths,world):
        for dire in [(0,1),(1,0),(0,-1),(-1,0)]:
            tx,ty=self.path[-1][0]+dire[0], self.path[-1][1]+dire[1]
            gpaths=[]
            for path in paths:
                gpaths.extend(path.path)
            if world.is_clear(tx,ty,True) and (tx,ty) not in gpaths:
                paths.append(Path(self.path+[(tx,ty)]))
        paths.remove(self)
    def next(self):
        dx,dy=self.path[1][0]-self.path[0][0],self.path[1][1]-self.path[0][1]
        self.path.pop(0)
        return dx,dy
class PathTester(ResourceB):
    speed=2
    img=Img.imgret2("Axe.png")
    def __init__(self,x,y,world):
        self.x=x
        self.y=y
        self.pathfind((20,20), world)