'''
Created on 22 Sep 2014

@author: NoNotCar
'''
import Players
from Img import imgret2
import Img
from random import randint
from Terrain import terrlist
import Object
import Generators
import pygame
#util
e=enumerate
selimage=imgret2("Mouse.png")
border=imgret2("MenuWrapper.png")
picon=imgret2("PowerIcon.png")
border2=pygame.transform.rotate(border,90)
ranconv={32:(1,7),64:(1,1),128:(4,1)}
def cmenu(menu,select):
    return [menu[(select-1)%len(menu)],menu[select],menu[(select+1)%len(menu)]]
class World(object):
    def __init__(self,np,wgen,puz,pn,ps,kp,scroll,size=(32,25)):
        if puz:
            generator = Generators.puzzles[ps][pn]
        else:
            generator = Generators.gens[wgen]
        basemoney=generator.bm
        Players.tabclasses=[Players.MechCategory]
        for etab in generator.extabs:
            Players.tabclasses.append(etab)
        for extool in generator.extools:
            Players.toolclasses.append(extool)
        self.terr=[]
        self.objs=[]
        if not kp:
            if puz:
                self.ents=[Players.Player(0,"Inf")]
            else:
                self.ents=[Players.Player(0,basemoney),Players.Player(1,basemoney)][:np]
        else:
            if puz:
                self.ents=[Players.KeyPlayer(0,"Inf")]
            else:
                self.ents=[Players.KeyPlayer(0,basemoney)]
        self.players=self.ents[:]
        if puz:
            for p in self.players:
                p.menu=[b for b in p.menu if b.iscat]
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
        music=generator.generate(self)
        if music:
            Img.musply(music)
        if generator.gspoint:
            self.objs[0][0]=Object.SellPoint(0,0,self.ents[0])
            if np==2:
                self.objs[0][24]=Object.SellPoint(0,24,self.ents[1])
        self.anitick=0
        self.scroll=scroll
        if scroll:
            self.scrollp=self.ents[0]
    def update(self,events):
        """Update Everything"""
        for n in range(self.tran[0]):
            if not randint(0,self.tran[1]):
                rx=randint(0,self.size[0]-1)
                ry=randint(0,self.size[1]-1)
                terrlist[self.terr[rx][ry]].ranupdate(self,rx,ry)
        for ent in self.ents:
            ent.update(self,events)
            ent.mupdate(self,events)
        self.anitick=(self.anitick+1)%56
        for row in self.objs:
            for obj in row:
                if obj and obj.updatable:
                    obj.update(self)
    def render(self,screen):
        """Render Everything"""
        is3ds=[]
        for x,row in e(self.terr):
            for y,tile in e(row):
                screen.blit(terrlist[tile].image,(x*32+32,y*32+32))
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                obj = self.get_obj(x, y)
                if obj:
                    if not obj.is3d:
                        screen.blit(obj.get_img(self),(x*32+32,y*32+32))
                    else:
                        is3ds.append(obj)
        for ent in [en for en in self.ents if not en.hidden]:
            screen.blit(ent.get_img(),(ent.x*32+32+int(round(ent.xoff)),ent.y*32+32+int(round(ent.yoff))))
        for ent in self.players:
            if ent.submenu is None:
                smenu=cmenu(ent.menu,ent.selected)
            else:
                smenu=cmenu(ent.menu[ent.selected].menu,ent.submenu)
            stools=cmenu(ent.tools,ent.tsel)
            for n,buyer in e(smenu):
                if buyer.iscat:
                    screen.blit(buyer.img,(32*(n+1)+16,0+832*ent.num))
                else:
                    screen.blit(buyer.get_img(self),(32*(n+1)+16,0+832*ent.num))
            screen.blit(Img.sfont.render(smenu[1].doc,True,(255,255,255)),(300,0))
            screen.blit(border,(32,0+832*ent.num))
            for n,tool in e(stools):
                screen.blit(tool.img,(0,32*(n+1)+16+672*ent.num))
            screen.blit(border2,(0,32+672*ent.num))
            if ent.submenu is None:
                selitem=ent.menu[ent.selected]
            else:
                selitem=ent.menu[ent.selected].menu[ent.submenu]
            if not selitem.iscat:
                if selitem.cost%1000==0:
                    screen.blit(Img.sfont.render("\xa3"+str(selitem.cost//1000)+"k",True, (0,0,0)),(80,23+832*ent.num))
                else:
                    screen.blit(Img.sfont.render("\xa3"+str(selitem.cost),True, (0,0,0)),(80,23+832*ent.num))
            screen.blit(selimage,(0,0+832*ent.num))
            screen.blit(Img.dfont.render("\xa3"+str(ent.money),True, (255,255,255)),(160,0+832*ent.num))
            if ent.hand:
                screen.blit(ent.hand.get_img(),(0,0+832*ent.num))
        for obj3 in is3ds:
            screen.blit(obj3.get_img(self),(obj3.x*32+32,obj3.y*32+32-obj3.off3d))
    def scrollrender(self,screen):
        """Render Everything in scrolling mode"""
        is3ds=[]
        sx=self.scrollp.x
        sy=self.scrollp.y
        asx=sx*32+int(round(self.scrollp.xoff))-128
        asy=sy*32+int(round(self.scrollp.yoff))-128
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
        for ent in [en for en in self.ents if not en.hidden]:
            if abs(ent.x-sx)<7 and abs(ent.y-sy)<7:
                sscreen.blit(ent.get_img(),(ent.x*32-asx+int(round(ent.xoff)),ent.y*32-asy+int(round(ent.yoff))))
        for ent in self.players:
            if ent.submenu is None:
                smenu=cmenu(ent.menu,ent.selected)
            else:
                smenu=cmenu(ent.menu[ent.selected].menu,ent.submenu)
            stools=cmenu(ent.tools,ent.tsel)
            for n,buyer in e(smenu):
                if buyer.iscat:
                    screen.blit(buyer.img,(32*(n+1)+16,0+832*ent.num))
                else:
                    screen.blit(buyer.get_img(self),(32*(n+1)+16,0+832*ent.num))
            if len(smenu[1].doc)>60:
                for n,char in enumerate(smenu[1].doc):
                    if char==" " and n>60:
                        screen.blit(Img.sfont.render(smenu[1].doc[:n],True,(255,255,255)),(0,325))
                        screen.blit(Img.sfont.render(smenu[1].doc[n+1:],True,(255,255,255)),(0,335))
                        break
            else:
                screen.blit(Img.sfont.render(smenu[1].doc,True,(255,255,255)),(0,330))
            screen.blit(border,(32,0+832*ent.num))
            for n,tool in e(stools):
                screen.blit(tool.img,(0,32*(n+1)+16+672*ent.num))
            screen.blit(border2,(0,32+672*ent.num))
            if ent.submenu is None:
                selitem=ent.menu[ent.selected]
            else:
                selitem=ent.menu[ent.selected].menu[ent.submenu]
            if not selitem.iscat:
                if selitem.cost%1000==0:
                    screen.blit(Img.sfont.render("\xa3"+str(selitem.cost//1000)+"k",True, (0,0,0)),(80,23+832*ent.num))
                else:
                    screen.blit(Img.sfont.render("\xa3"+str(selitem.cost),True, (0,0,0)),(80,23+832*ent.num))
            screen.blit(selimage,(0,0+832*ent.num))
            screen.blit(Img.dfont.render("\xa3"+str(ent.money),True, (255,255,255)),(160,0+832*ent.num))
            if ent.hand:
                screen.blit(ent.hand.get_img(),(0,0+832*ent.num))
            screen.blit(picon,(0,352))
            screen.blit(Img.dfont.render("%g" % (ent.psupply/1000.0)+"kW",True, (255,255,255)),(32,352))
            screen.blit(Img.dfont.render("%g" % (sum([ps.stop for ps in ent.pstorage])/60000.0)+"kJ",True, (100,255,100)),(128,352))
        for obj3 in is3ds:
            sscreen.blit(obj3.get_img(self),(obj3.x*32-asx,obj3.y*32-obj3.off3d-asy))
        screen.blit(sscreen,(32,32))
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(32,32,288,288),2)
        screen.blit(self.make_map(),(320,320))
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
        pygame.draw.rect(mmap,(255,0,0),pygame.Rect(self.players[0].x*64//self.size[0]-1,self.players[0].y*64//self.size[1]-1,4,4))
        return mmap
    def exists(self,obj):
        """Has this object been destroyed?"""
        return self.get_obj(obj.x, obj.y) is obj