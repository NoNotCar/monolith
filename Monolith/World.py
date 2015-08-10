'''
Created on 22 Sep 2014

@author: Thomas
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
border2=pygame.transform.rotate(border,90)
def cmenu(menu,select):
    return [menu[(select-1)%len(menu)],menu[select],menu[(select+1)%len(menu)]]
class World(object):
    def __init__(self,np,wgen,puz,pn,ps,kp,scroll):
        if puz:
            generator = Generators.puzzles[ps][pn]
        else:
            generator = Generators.gens[wgen]
        basemoney=generator.bm
        Players.tabclasses=[Players.MechCategory]
        for etab in generator.extabs:
            Players.tabclasses.append(etab)
        for etool in generator.etools:
            Players.toolclasses.append(etool)
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
        for x in xrange(32):
            xr=[]
            oxr=[]
            for y in xrange(25):
                xr.append(0)
                oxr.append(None)
            self.terr.append(xr)
            self.objs.append(oxr)
        music=generator.generate(self)
        if music:
            Img.musply(music)
        self.objs[0][0]=Object.SellPoint(0,0,self.ents[0])
        if np==2:
            self.objs[0][24]=Object.SellPoint(0,24,self.ents[1])
        self.anitick=0
        self.scroll=scroll
        if scroll:
            self.scrollp=self.ents[0]
    def update(self,events):
        """Update Everything"""
        if not randint(0,8):
            rx=randint(0,31)
            ry=randint(0,24)
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
        for x,row in e(self.objs):
            for y,obj in e(row):
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
            screen.blit(obj3.get_img(self),(obj3.x*32+32,obj3.y*32+26))
    def scrollrender(self,screen):
        """Render Everything"""
        is3ds=[]
        sx=self.scrollp.x
        sy=self.scrollp.y
        asx=sx*32+int(round(self.scrollp.xoff))-128
        asy=sy*32+int(round(self.scrollp.yoff))-128
        sscreen=pygame.Surface((288,288))
        sscreen.fill((100,100,100))
        for x,row in e(self.terr):
            for y,tile in e(row):
                if abs(x-sx)<6 and abs(y-sy)<6:
                    sscreen.blit(terrlist[tile].image,(x*32-asx,y*32-asy))
        for x,row in e(self.objs):
            for y,obj in e(row):
                if obj and abs(x-sx)<6 and abs(y-sy)<6:
                    if not obj.is3d:
                        sscreen.blit(obj.get_img(self),(x*32-asx,y*32-asy))
                    else:
                        is3ds.append(obj)
        for ent in [en for en in self.ents if not en.hidden]:
            if abs(ent.x-sx)<6 and abs(ent.y-sy)<6:
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
        for obj3 in is3ds:
            sscreen.blit(obj3.get_img(self),(obj3.x*32-asx,obj3.y*32-6-asy))
        screen.blit(sscreen,(32,32))
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(32,32,288,288),2)
    def get_obj(self,x,y):
        """Get object from coordinates. If the coordinates are not in the world, returns None"""
        if self.inworld(x,y):
            return self.objs[x][y]
        return None
    def get_ent(self,x,y):
        for ent in self.ents:
            if (ent.x,ent.y)==(x,y):
                return ent
        return None
    def dest_ent(self,x,y):
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
        return 0<=x<=31 and 0<=y<=24
    def dest_obj(self,x,y):
        self.objs[x][y]=None
    def spawn_obj(self,obj):
        self.objs[obj.x][obj.y]=obj
    def move_ent(self,ent,tx,ty):
        ent.place(tx,ty)
        if self.get_obj(tx, ty):
            self.get_obj(tx, ty).drop(self,ent)
    def spawn_ent(self,ent):
        self.ents.append(ent)
    def is_empty(self,x,y):
        return self.get_obj(x, y)==None and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def is_placeable(self,x,y,boat=False):
        if boat and not self.get_terr(x,y).iswasser:
            return False
        elif not boat and self.get_terr(x,y).iswasser:
            return False
        return self.get_obj(x, y)==None and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def is_clear(self,x,y,player=False,boat=False):
        if not self.inworld(x, y):
            return False
        if player and not boat and self.get_terr(x,y).iswasser:
            return False
        if boat and not self.get_terr(x,y).iswasser:
            return False
        return not (self.get_obj(x, y) and (self.get_obj(x, y).solid or (player and not self.get_obj(x,y).playerenter))) and not (self.get_ent(x,y) and self.get_ent(x,y).solid)
    def get_terr(self,x,y):
        return terrlist[self.get_tid(x, y)]
    def get_tid(self,x,y):
        return self.terr[x][y]
    def set_terr(self,x,y,tid):
        self.terr[x][y]=tid