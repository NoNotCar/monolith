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
import Power
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
                   Buyers.ObjBuyer(Mech.Splitter,500),Buyers.ObjBuyer(Mech.PurpPri,500),Buyers.VBuyer(Vehicles.Lorry,1000),Buyers.ObjBuyer(Mech.VInput,50),Buyers.ObjBuyer(Object.SellPointBlock,10000)]

tabclasses=[MechCategory,Power.PowerCategory]
toolclasses=[]
class KeyPlayer(Entity.Entity):
    name="Player"
    solid=True
    estop=False
    psupply=0
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
        self.mmovewait=0
    def pupdate(self,world):
        self.psupply=0
        for psup in self.psuppliers[:]:
            if world.exists(psup):
                self.psupply+=psup.get_power(world)
            else:
                self.psuppliers.remove(psup)
        #Garbage collection
        for psto in [pst for pst in self.pstorage if not world.exists(pst)]:
            self.pstorage.remove(psto)
    def update(self,world,events):
        self.pupdate(world)
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
                    if not pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                        self.move(*(hatpos+ (2, world,True)))
                    elif self.mmovewait==0:
                        self.tsel=(self.tsel+hatpos[1])%len(self.tools)
                        if self.submenu is None:
                            self.selected=(self.selected+hatpos[0])%len(self.menu)
                        else:
                            self.submenu=(self.submenu+hatpos[0])%len(self.menu[self.selected].menu)
                        self.mmovewait=10
                    else:
                        self.mmovewait-=1
            mp=pygame.mouse.get_pos()
            mdx=mp[0]-176
            mdy=mp[1]-176
            if abs(mdx)>abs(mdy):
                self.dir=(-1,0) if mdx<0 else (1,0)
            else:
                self.dir=(0,-1) if mdy<0 else (0,1)
        else:
            self.disable=False
    def vupdate(self,world,events,v):
        self.pupdate(world)
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
    def get_img(self):
        return self.images[hdirconv[self.dir]]
    def get_power(self,amount):
        if self.psupply>=amount:
            self.psupply-=amount
            return True
        elif self.psupply+sum([ps.stored for ps in self.pstorage])>=amount:
            amount-=self.psupply
            self.psupply=0
            pstonum=0
            while amount>0:
                supply=self.pstorage[pstonum]
                if supply.stored>=amount:
                    supply.stored-=amount
                    amount=0
                else:
                    amount-=supply.stored
                    supply.stored=0
            return True
        return False
            