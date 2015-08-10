'''
Created on 24 Jun 2015

@author: Thomas
'''
import Entity,Object,pygame,Img,Buyers
class RGBResource(Entity.ResourceB):
    name="RGBTILE"
    def __init__(self,x,y,rgb):
        self.x = x
        self.y = y
        self.hidden = False
        self.rgb=rgb
        self.img=Img.blank32.copy()
        pygame.draw.rect(self.img,rgb,pygame.Rect(8,8,16,16))
class RGBSpawner(Object.Object):
    hasio="output"
    updatable=True
    is3d=True
    def __init__(self,x,y,rgb):
        self.x=x
        self.y=y
        self.rgb=rgb
        self.img=Img.imgret("MachBlock.png")
        pygame.draw.rect(self.img,rgb,pygame.Rect(4,4,8,8))
        self.img=pygame.transform.scale2x(self.img)
        self.output=[]
    def update(self,world):
        if not self.output:
            self.output=[RGBResource(self.x,self.y,self.rgb)]
class RGBSetter(Object.OObject):
    hasio="both"
    is3d=True
    def __init__(self,x,y,p):
        self.x=x
        self.y=y
        self.owner=p
        self.output=[]
    def input(self,ent):
        if ent.name=="RGBTILE" and not self.output:
            nrgb=[]
            for n,col in enumerate(ent.rgb):
                nrgb.append(255 if self.rgbx[n] else col)
            nrgb=tuple(nrgb)
            self.output.append(RGBResource(self.x,self.y,nrgb))
            return True
        return False
class RGBSpect(Object.OObject):
    hasio="input"
    is3d=True
    img=Img.imgret2("RGB\\RGBSpect.png")
    def __init__(self,x,y,p,startrgb=(0,0,0)):
        self.x=x
        self.y=y
        self.owner=p
        self.rgb=startrgb
    def input(self,ent):
        if ent.name=="RGBTILE":
            self.rgb=ent.rgb
            return True
        return False
    def get_img(self,world):
        screen=Img.blank32.copy()
        Img.bcentre(Img.sfont, str(self.rgb[0]), screen, -8,(self.rgb[0],0,0))
        Img.bcentre(Img.sfont, str(self.rgb[1]), screen, 1,(0,self.rgb[1],0))
        Img.bcentre(Img.sfont, str(self.rgb[2]), screen, 10,(0,0,self.rgb[2]))
        img=self.img.copy()
        img.blit(screen,(0,0))
        return img
class RGBSred(RGBSetter):
    img=Img.imgret2("RGB\\RLoad.png")
    rgbx=(1,0,0)
    doc="Sets the red value of tiles to 255. IO: Both"
class RGBSgreen(RGBSetter):
    img=Img.imgret2("RGB\\GLoad.png")
    rgbx=(0,1,0)
    doc="Sets the green value of tiles to 255. IO: Both"
class RGBSblue(RGBSetter):
    img=Img.imgret2("RGB\\BLoad.png")
    rgbx=(0,0,1)
    doc="Sets the blue value of tiles to 255. IO: Both"
class RGBMixer(Object.OObject):
    hasio="both"
    is3d=True
    img=Img.imgret2("RGB\\Mixer.png")
    doc="Takes in two tiles and produces one tile with the average of their colours. IO: Both (2 Inputs recommended)"
    def __init__(self,x,y,p):
        self.x=x
        self.y=y
        self.owner=p
        self.output=[]
        self.reserve=None
    def input(self,ent):
        if ent.name=="RGBTILE" and not self.output:
            if self.reserve and self.reserve.rgb!=ent.rgb:
                nrgb=[]
                for n,col in enumerate(ent.rgb):
                    nrgb.append((col+self.reserve.rgb[n])//2)
                nrgb=tuple(nrgb)
                self.output.append(RGBResource(self.x,self.y,nrgb))
                self.reserve=None
            elif not self.reserve:
                self.reserve=ent
            else:
                return False
            return True
        return False
class RGBBuyer(Object.OObject):
    solid=False
    playerenter=False
    img=Img.imgret2("RGB\\RGBBUY.png")
    name="RGBBUY"
    is3d=True
    hasio="input"
    rgbvalues={}
    doc="Sells RGB Tiles. The normal seller will not work"
    def input(self,ent):
        if ent.name!="RGBTILE":
            return False
        else:
            if ent.rgb not in self.rgbvalues.keys():
                self.rgbvalues[ent.rgb]=100
            self.owner.money+=self.rgbvalues[ent.rgb]
            if self.rgbvalues[ent.rgb]>0:
                self.rgbvalues[ent.rgb]-=1
            return True
class RGBGoal(Object.Object):
    solid=False
    playerenter=False
    img=Img.imgret2("RGB\\RGBBUY.png")
    name="RGBBUY"
    is3d=True
    hasio="input"
    updatable=True
    rgbvalues={}
    def __init__(self,x,y,rgb):
        self.x=x
        self.y=y
        self.ileft=10
        self.rgb=rgb
        self.img=Img.imgret("GoldBlock.png")
        pygame.draw.rect(self.img,rgb,pygame.Rect(4,4,8,8))
        self.img=pygame.transform.scale2x(self.img)
    def input(self,ent):
        if ent.name!="RGBTILE":
            return False
        else:
            if ent.rgb == self.rgb:
                self.ileft-=1
            return True
    def update(self,world):
        if self.ileft<1:
            world.complete=True
class RGBCategory(object):
    img=Img.imgret2("RGB\\RGBTab.png")
    iscat=True
    doc="RGB stuff"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(RGBSred,500),Buyers.ObjBuyer(RGBSgreen,500),Buyers.ObjBuyer(RGBSblue,500),Buyers.ObjBuyer(RGBMixer,500),Buyers.ObjBuyer(RGBBuyer,500),Buyers.ObjBuyer(RGBSpect,1000)]
class RGBCategoryPuzz(object):
    img=Img.imgret2("RGB\\RGBTab.png")
    iscat=True
    doc="RGB stuff"
    def __init__(self):
        self.menu=[Buyers.ObjBuyer(RGBSred,500),Buyers.ObjBuyer(RGBSgreen,500),Buyers.ObjBuyer(RGBSblue,500),Buyers.ObjBuyer(RGBMixer,500),Buyers.ObjBuyer(RGBSpect,1000)]