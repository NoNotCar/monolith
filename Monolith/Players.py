'''
Created on 22 Sep 2014

@author: NoNotCar
'''
import pygame
import os
import Entity
import Buyers,Tools
import Mech
import Object
import Forestry
import Vehicles
import Img
pygame.init()
loc = os.path.dirname(os.getcwd())+"\Assets\\"
imgconv = "u", "l", "", "r"
colinpl = (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 0), (255, 255, 255)
hdirconv={(0,-1):0,(-1,0):1,(0,1):2,(1,0):3}
ps2map=[2,1,5,6,7,0,4,9]
xboxmap=[0,1,2]
picksound=Img.sndget("Randomize2.wav")
class MechCategory(object):
    img=Img.imgret2("Gear.png")
    iscat=True
    doc="Tech stuff"
    def __init__(self):
        self.menu=[Buyers.RotObjBuyer(Mech.SlowConv,25),Buyers.RotObjBuyer(Mech.Conv,100),Buyers.RotObjBuyer(Mech.RainConv,1000),
                   Buyers.RotObjBuyer(Mech.Output,100),Buyers.RotObjBuyer(Mech.Output2,200),Buyers.ObjBuyer(Mech.Input,100),Buyers.RotObjBuyer(Mech.IOput,300),Buyers.ObjBuyer(Mech.Buffer5,500),
                   Buyers.ObjBuyer(Mech.Splitter,500),Buyers.VBuyer(Vehicles.Lorry,1000),Buyers.ObjBuyer(Mech.VInput,50),Buyers.ObjBuyer(Object.SellPointBlock,10000)]

tabclasses=[MechCategory]
toolclasses=[]
class Player(Entity.Entity):
    name="Player"
    solid=True
    estop=False
    psupply=0
    def __init__(self, num,bm):
        self.j=pygame.joystick.Joystick(num)
        self.j.init()
        self.num=num
        self.x=0
        self.y=0+24*num
        self.images=[pygame.image.load(loc+"Manh%s.png" % (str(imgconv[n]))) for n in range(4)]
        for im in self.images:
            pygame.draw.rect(im, colinpl[num], pygame.Rect(5,8,6,7))
        self.images=[pygame.transform.scale2x(im) for im in self.images]
        self.dir=(0,-1)
        self.hand=None
        self.godmode=0
        if bm!="Inf":
            self.money=bm
        else:
            self.money="INFINITE"
            self.godmode=True
        self.map=ps2map
        self.selected=0
        self.tsel=0
        self.hatrest=False
        self.disable=False
        self.submenu=None
        self.menu=[Buyers.ObjBuyer(Object.Monolith,30000),Buyers.TerrBuyer(2,10),Buyers.VBuyer(Vehicles.FastCar,1000),Buyers.VBuyer(Vehicles.Boat,500),Buyers.BridgeBuyer()]
        for tab in tabclasses:
            self.menu.append(tab())
        self.tools=[Tools.Hammer()]
        for tool in toolclasses:
            self.tools.append(tool())
        self.pstorage=[]
        self.psuppliers=[]
    def get_img(self):
        return self.images[hdirconv[self.dir]]
    def update(self,world,events):
        if not self.disable:
            for e in events:
                if e.type==pygame.JOYBUTTONDOWN:
                    if self.submenu is None:
                        selbuy = self.menu[self.selected]
                    else:
                        selbuy = self.menu[self.selected].menu[self.submenu]
                    if self.j.get_button(self.map[0]):
                        self.do_tool(world)
                    elif self.j.get_button(self.map[1]):
                        self.pickup(world)
                    elif self.j.get_button(self.map[2]):
                        if not selbuy.iscat and (self.money>=selbuy.cost or self.godmode):
                            if selbuy.forward:
                                tx=self.dir[0]+self.x
                                ty=self.dir[1]+self.y
                                if world.inworld(tx,ty) and selbuy.buy(world,tx,ty,self) and not self.godmode:
                                    self.money-=selbuy.cost
                            else:
                                if selbuy.buy(world,self.x,self.y,self):
                                    self.money-=selbuy.cost
                        elif selbuy.iscat:
                            self.submenu=0
                    elif self.j.get_button(self.map[3]):
                        pass
                    elif self.j.get_button(self.map[4]):
                        pass
                    elif self.j.get_button(self.map[5]):
                        if not selbuy.iscat:
                            selbuy.rotate()
                    elif self.j.get_button(self.map[6]):
                        self.submenu=None
                    elif self.j.get_button(self.map[7]):
                        self.x,self.y=(0,24*self.num)
            if not self.moving:
                hatpos=(self.j.get_axis(0),self.j.get_axis(1))
                hatpos=[int(round(h)) for h in hatpos]
                if abs(hatpos[0])!=abs(hatpos[1]):
                    self.dir=(hatpos[0],hatpos[1])
                    self.move(*(hatpos+ [2, world,True]))
            hatpos2=(self.j.get_axis(3),-self.j.get_axis(2))
            hatpos2=[int(round(h)) for h in hatpos2]
            hatpos2=tuple(hatpos2)
            if abs(hatpos2[0])!=abs(hatpos2[1]):
                self.dir=(hatpos2[0],-hatpos2[1])
            ahat=self.j.get_hat(0)
            if ahat[0]:
                if not self.hatrest:
                    if self.submenu is None:
                        self.selected=(self.selected+ahat[0])%len(self.menu)
                    else:
                        self.submenu=(self.submenu+ahat[0])%len(self.menu[self.selected].menu)
                    self.hatrest=True
            elif ahat[1]:
                if not self.hatrest:
                    self.tsel=(self.tsel-ahat[1])%len(self.tools)
                    self.hatrest=True
            else:
                self.hatrest=False
        else:
            self.disable=False
    def vupdate(self,world,events,v):
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN:
                if self.j.get_button(self.map[1]):
                    if v.imgflip:
                        tx=v.x-1
                    else:
                        tx=v.x+1
                    if world.is_clear(tx,v.y,True):
                        self.x=tx
                        self.y=v.y
                        world.spawn_ent(self)
                        v.hasp=False
                        self.disable=True
                elif self.j.get_button(self.map[7]):
                    self.x,self.y=(0,24*self.num)
                    world.spawn_ent(self)
                    v.hasp=False
        hatpos=(self.j.get_axis(0),-self.j.get_axis(1))
        hatpos=[int(round(h)) for h in hatpos]
        hatpos=tuple(hatpos)
        if abs(hatpos[0])!=abs(hatpos[1]):
            v.movev((hatpos[0],-hatpos[1]),world)
    def do_tool(self,world):
        tx=self.x+self.dir[0]
        ty=self.y+self.dir[1]
        if world.inworld(tx,ty):
            self.tools[self.tsel].use(tx,ty,world,self)
    def pickup(self,world):
        tx=self.x+self.dir[0]
        ty=self.y+self.dir[1]
        if world.inworld(tx,ty):
            if world.get_ent(tx,ty) and world.get_ent(tx,ty).name=="Vehicle" and world.get_ent(tx,ty).p==self:
                world.ents.remove(self)
                world.get_ent(tx,ty).hasp=True
            elif not self.hand and world.get_ent(tx,ty) and world.get_ent(tx,ty).pickup:
                self.hand=world.get_ent(tx,ty)
                world.ents.remove(self.hand)
                picksound.play()
            elif self.hand and world.is_clear(tx,ty):
                world.ents.append(self.hand)
                self.hand.place(tx,ty)
                if world.get_obj(tx,ty):
                    world.get_obj(tx,ty).drop(world,self.hand)
                self.hand=None
                picksound.play()
class KeyPlayer(Player):
    def __init__(self, num,bm):
        self.num=num
        self.x=0
        self.y=0
        self.images=[pygame.image.load(loc+"Manh%s.png" % (str(imgconv[n]))) for n in range(4)]
        for im in self.images:
            pygame.draw.rect(im, colinpl[num], pygame.Rect(5,8,6,7))
        self.images=[pygame.transform.scale2x(im) for im in self.images]
        self.dir=(0,-1)
        self.hand=None
        self.godmode=0
        if bm!="Inf":
            self.money=bm
        else:
            self.money="INFINITE"
            self.godmode=True
        self.selected=0
        self.tsel=0
        self.hatrest=False
        self.disable=False
        self.submenu=None
        self.menu=[Buyers.ObjBuyer(Object.Monolith,30000),Buyers.TerrBuyer(2,10),Buyers.VBuyer(Vehicles.FastCar,1000)]
        for tab in tabclasses:
            self.menu.append(tab())
        self.tools=[Tools.Hammer(),Tools.Estop()]
        for tool in toolclasses:
            self.tools.append(tool())
        self.pstorage=[]
        self.psuppliers=[]
    def update(self,world,events):
        if not self.disable:
            for e in events:
                if e.type==pygame.MOUSEBUTTONDOWN:
                    if self.submenu is None:
                        selbuy = self.menu[self.selected]
                    else:
                        selbuy = self.menu[self.selected].menu[self.submenu]
                    if e.button==1:
                        self.do_tool(world)
                    elif e.button==2:
                        if not selbuy.iscat:
                            selbuy.rotate()
                    elif e.button==3:
                        if not selbuy.iscat and (self.money>=selbuy.cost or self.godmode):
                            if selbuy.forward:
                                tx=self.dir[0]+self.x
                                ty=self.dir[1]+self.y
                                if world.inworld(tx,ty) and selbuy.buy(world,tx,ty,self) and not self.godmode:
                                    self.money-=selbuy.cost
                            else:
                                if selbuy.buy(world,self.x,self.y,self):
                                    self.money-=selbuy.cost
                        elif selbuy.iscat:
                            self.submenu=0
                    elif e.button==4 or e.button==5:
                        sdir=-1 if e.button==4 else 1
                        if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                            self.tsel=(self.tsel+sdir)%len(self.tools)
                        else:
                            if self.submenu is None:
                                self.selected=(self.selected+sdir)%len(self.menu)
                            else:
                                self.submenu=(self.submenu+sdir)%len(self.menu[self.selected].menu)
                elif e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_LSHIFT:
                        self.pickup(world)
                    elif e.key==pygame.K_e:
                        self.submenu=None
                    elif e.key==pygame.K_r:
                        self.x,self.y=(0,24*self.num)
            if not self.moving:
                hatpos=self.get_dirkeys()
                if hatpos!=(0,0):
                    self.move(*(hatpos+ (2, world,True)))
            mp=pygame.mouse.get_pos()
            if world.scroll:
                mdx=mp[0]-176
                mdy=mp[1]-176
            else:
                mdx=mp[0]-self.x*32-self.xoff-40
                mdy=mp[1]-self.y*32-self.yoff-40
            if abs(mdx)>abs(mdy):
                self.dir=(-1,0) if mdx<0 else (1,0)
            else:
                self.dir=(0,-1) if mdy<0 else (0,1)
        else:
            self.disable=False
    def vupdate(self,world,events,v):
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_LSHIFT:
                    if v.imgflip:
                        tx=v.x-1
                    else:
                        tx=v.x+1
                    if world.is_clear(tx,v.y,True):
                        self.x=tx
                        self.y=v.y
                        world.spawn_ent(self)
                        v.hasp=False
                        self.disable=True
                elif e.key==pygame.K_r:
                    self.x,self.y=(0,24*self.num)
                    world.spawn_ent(self)
                    v.hasp=False
        hatpos=self.get_dirkeys()
        v.movev((hatpos[0],hatpos[1]),world)
    def get_dirkeys(self):
        pkeys=pygame.key.get_pressed()
        if pkeys[pygame.K_w]:
            return (0,-1)
        elif pkeys[pygame.K_a]:
            return (-1,0)
        elif pkeys[pygame.K_s]:
            return (0,1)
        elif pkeys[pygame.K_d]:
            return (1,0)
        else:
            return (0,0)
            
            