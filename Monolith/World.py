'''
Created on 22 Sep 2014

@author: NoNotCar
'''
import Players
from Img import imgret2
import Img
from random import randint,choice
from Terrain import terrlist
import Object
import Generators
import Tutorial
import pygame
#util
e=enumerate
selimage=imgret2("Mouse.png")
border=imgret2("MenuWrapper.png")
picon=Img.imgret("PowerIcon.png")
border2=pygame.transform.rotate(border,90)
ranconv={32:(1,7),64:(1,1),128:(4,1)}
def cmenu(menu,select):
    return [menu[(select+n)%len(menu)] for n in range(-3,4)]
class World(object):
    def __init__(self,np,wgen,puz,pn,ps,kp,godmode,size=(32,32)):
        self.guitorun=None
        self.puz=puz
        if puz==2:
            generator=Tutorial.tutorials[pn]
        elif puz:
            size=(32,32)
            generator = Generators.puzzles[ps][pn]
        else:
            generator = Generators.gens[wgen]
        basemoney=generator.bm
        Players.tabclasses=Players.btabclasses+generator.extabs
        Players.toolclasses=generator.extools
        self.terr=[]
        self.objs=[]
        self.ents=[Players.KeyPlayer(0,"Inf" if godmode else basemoney)]
        self.player=self.ents[0]
        if puz:
            self.player.menu=[b for b in self.player.menu if b.iscat]
        self.complete=False
        self.size=size
        self.sv=(size[0]//32)**2
        self.tran=ranconv[size[0]]
        for x in xrange(size[0]):
            xr=[]
            oxr=[]
            for y in xrange(size[1]):
                xr.append(0)
                oxr.append(None)
            self.terr.append(xr)
            self.objs.append(oxr)
        self.music=generator.generate(self)
        if generator.gspoint:
            self.objs[0][0]=Object.SellPoint(0,0,self.ents[0])
            if np==2:
                self.objs[0][24]=Object.SellPoint(0,24,self.ents[1])
        self.anitick=0
        self.map=self.make_map()
    def update(self,events):
        """Update Everything"""
        if not pygame.mixer.music.get_busy():
            Img.musply(choice(self.music),1)
        for n in range(self.tran[0]):
            if not randint(0,self.tran[1]):
                rx=randint(0,self.size[0]-1)
                ry=randint(0,self.size[1]-1)
                terrlist[self.terr[rx][ry]].ranupdate(self,rx,ry)
        for ent in self.ents:
            ent.update(self,events)
            ent.mupdate(self,events)
        self.anitick+=1
        if self.anitick==56:
            self.anitick=0
            self.map=self.make_map()
        for row in self.objs:
            for obj in row:
                if obj and obj.updatable:
                    obj.update(self)
        if self.player.psupply>0:
            for pst in self.player.pstorage:
                self.player.psupply-=pst.give_power(self,self.player.psupply)
                if self.player.psupply==0:
                    break
    def scrollrender(self,screen):
        """Render Everything in scrolling mode"""
        if self.guitorun:
            self.guitorun.run(screen,self.player)
            self.guitorun=None
        is3ds=[]
        ply = self.player
        sx=ply.x
        sy=ply.y
        asx=sx*32+int(round(ply.xoff))-128
        asy=sy*32+int(round(ply.yoff))-128
        sscreen=pygame.Surface((288,288))
        sscreen.fill((100,100,100))
        for x,row in e(self.terr):
            for y,tile in e(row):
                if abs(x-sx)<7 and abs(y-sy)<7:
                    sscreen.blit(terrlist[tile].image,(x*32-asx,y*32-asy))
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                obj = self.get_obj(x, y)
                if obj and abs(x-sx)<7 and abs(y-sy)<7:
                    if not obj.is3d:
                        sscreen.blit(obj.get_img(self),(x*32-asx,y*32-asy))
                    else:
                        is3ds.append(obj)
        #Entity Rendering
        for ent in [en for en in self.ents if not en.hidden]:
            if abs(ent.x-sx)<7 and abs(ent.y-sy)<7:
                sscreen.blit(ent.get_img(),(ent.x*32-asx+int(round(ent.xoff)),ent.y*32-asy+int(round(ent.yoff))))
        #Player Rendering
        if ply.submenu is None:
            smenu=cmenu(ply.menu,ply.selected)
        else:
            smenu=cmenu(ply.menu[ply.selected].menu,ply.submenu)
        stools=cmenu(ply.tools,ply.tsel)
        for n,buyer in e(smenu):
            if buyer.iscat:
                screen.blit(buyer.img,(32*(n+1)+16,0))
            else:
                screen.blit(buyer.get_img(self),(32*(n+1)+16,0))
        if len(smenu[3].doc)>55:
            for n,char in enumerate(smenu[3].doc):
                if char==" " and n>55:
                    screen.blit(Img.sfont.render(smenu[3].doc[:n],True,(255,255,255)),(0,325))
                    screen.blit(Img.sfont.render(smenu[3].doc[n+1:],True,(255,255,255)),(0,335))
                    break
            else:
                screen.blit(Img.sfont.render(smenu[3].doc,True,(255,255,255)),(0,330))
        else:
            screen.blit(Img.sfont.render(smenu[3].doc,True,(255,255,255)),(0,330))
        screen.blit(border,(32,0))
        for n,tool in e(stools):
            screen.blit(tool.img,(0,32*(n+1)+16))
        screen.blit(border2,(0,32))
        if ply.submenu is None:
            selitem=ply.menu[ply.selected]
        else:
            selitem=ply.menu[ply.selected].menu[ply.submenu]
        if not selitem.iscat:
            if selitem.cost%1000==0:
                screen.blit(Img.sfont.render("\xa3"+str(selitem.cost//1000)+"k",True, (0,0,0)),(144,23))
            else:
                screen.blit(Img.sfont.render("\xa3"+str(selitem.cost),True, (0,0,0)),(144,23))
        screen.blit(selimage,(0,0+832*ply.num))
        screen.blit(Img.dfont.render("\xa3"+str(ply.money),True, (255,255,255)),(288,0))
        if ply.hand:
            screen.blit(ply.hand.get_img(),(0,0))
        screen.blit(picon,(0,368))
        screen.blit(Img.pfont2.render("%g" % (ply.rpsupply/1000.0)+"kW",True, (100,255,100) if ply.rpsupply>0 else (255,0,0) if ply.rpsupply<0 else (255,255,255)),(16,368))
        screen.blit(Img.pfont2.render("%g" % (round(sum([ps.stored for ps in ply.pstorage])/60000.0,1))+"/"+
                                     "%g" % (round(sum([ps.maxS for ps in ply.pstorage])/60000.0,1))+"kJ",True, (100,255,100)),(128,368))
        for obj3 in is3ds:
            sscreen.blit(obj3.get_img(self),(obj3.x*32-asx,obj3.y*32-obj3.off3d-asy))
        screen.blit(sscreen,(32,32))
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(32,32,288,288),2)
        screen.blit(self.map,(320,320))
    def get_obj(self,x,y):
        """Get object from coordinates. If the coordinates are not in the world, returns None"""
        if self.inworld(x,y):
            return self.objs[x][y]
        return None
    def get_ent(self,x,y):
        """Get an entity from coordinates. If there are no entities at the location, returns None"""
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                return ent
        return None
    def dest_ent(self,x,y):
        """Destroy all entities at the coordinates"""
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                self.ents.remove(ent)
    def get_objname(self,x,y):
        """Get object name from coordinates. If the coordinates are not in the world, returns None"""
        getob=self.get_obj(x, y)
        if getob:
            return getob.name
        return None
    def inworld(self,x,y):
        """Is the coordinate in the world?"""
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def ranpos(self):
        """return a random coordinate"""
        return randint(0,self.size[0]-1),randint(0,self.size[1]-1)
    def dest_obj(self,x,y):
        """Destroy the object at the coordinates"""
        self.objs[x][y]=None
    def spawn_obj(self,obj):
        """Create an object at its x,y position"""
        self.objs[obj.x][obj.y]=obj
    def move_ent(self,ent,tx,ty):
        """Legacy non-smooth movement function"""
        ent.place(tx,ty)
        if self.get_obj(tx, ty):
            self.get_obj(tx, ty).drop(self,ent)
    def spawn_ent(self,ent):
        """Does what it says on the tin"""
        self.ents.append(ent)
    def is_empty(self,x,y):
        """If there are no objects or solid entities at the location"""
        return self.get_obj(x, y)==None and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def is_placeable(self,x,y,boat=False):
        """If there are no objects, solid entities or water at the location. If boat is True, there must be water at the location. Used for buying things"""
        if not self.inworld(x,y):
            return False
        if boat and not self.get_terr(x,y).iswasser:
            return False
        elif not boat and self.get_terr(x,y).iswasser:
            return False
        return self.get_obj(x, y)==None and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def is_clear(self,x,y,player=False,boat=False):
        """If an entity can enter this location"""
        if not self.inworld(x, y):
            return False
        if player and not boat and self.get_terr(x,y).iswasser:
            return False
        if boat and not self.get_terr(x,y).iswasser:
            return False
        return not (self.get_obj(x, y) and (self.get_obj(x, y).solid or (player and not self.get_obj(x,y).playerenter))) and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def get_solidobj(self,x,y,player=False):
        """If there is a solid object here"""
        if not self.inworld(x, y):
            return True
        return  self.get_obj(x, y) and (self.get_obj(x, y).solid or (player and not self.get_obj(x,y).playerenter))
    def get_terr(self,x,y):
        """Get the terrain object of the location"""
        return terrlist[self.get_tid(x, y)]
    def get_tid(self,x,y):
        """Get the terrain id at the location"""
        return self.terr[x][y]
    def set_terr(self,x,y,tid):
        """Set the terrain id at the location"""
        self.terr[x][y]=tid
    def make_map(self):
        """Create Minimap image"""
        mmap=pygame.Surface((64,64))
        for x in range(32):
            for y in range(32):
                pygame.draw.rect(mmap,self.get_terr(x*self.size[0]//32, y*self.size[1]//32).mcol,pygame.Rect(x*2,y*2,2,2))
                if self.get_obj(x*self.size[0]//32, y*self.size[1]//32):
                    omcol=self.get_obj(x*self.size[0]//32, y*self.size[1]//32).mcol
                    if omcol:
                        pygame.draw.rect(mmap,omcol,pygame.Rect(x*2,y*2,2,2))
        pygame.draw.rect(mmap,(255,0,0),pygame.Rect(self.player.x*64//self.size[0]-1,self.player.y*64//self.size[1]-1,4,4))
        return mmap
    def exists(self,obj):
        """Has this object been destroyed?"""
        return self.get_obj(obj.x, obj.y) is obj
    def run_GUI(self,gui):
        """Run a GUI"""
        self.guitorun=gui