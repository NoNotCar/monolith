__author__ = 'NoNotCar'
import Object, Img, GameRegistry, GUI, Img, pygame, sys


class CrGUI(GUI.GUI):
    def __init__(self, crafter):
        self.cr = crafter

    def run(self, screen, player):
        recrects = []
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    for rr in recrects:
                        if rr[1].collidepoint(mpos):
                            self.cr.recipe = rr[0]
                            self.cr.recipeprogress = GameRegistry.craftrecipes[rr[0]][0][:]
                elif e.type==pygame.KEYDOWN and e.key==pygame.K_LSHIFT:
                    return None
            screen.fill((200, 200, 200))
            recrects = []
            Img.fblit(screen, Img.dfont, "CRAFTING: ", (0, 0, 0), (0, 0))
            Img.fblit(screen,Img.sfont,", ".join(self.cr.recipeprogress),(0, 0, 0), (0, 32))
            if self.cr.recipeprogress == GameRegistry.craftrecipes[self.cr.recipe][0]:
                for n, r in enumerate(GameRegistry.craftrecipes):
                    recrects.append([n, screen.blit(r[2], (n * 32, 64))])
            pygame.display.flip()


class CraftingTable(Object.OObject):
    updatable = False
    is3d = True
    img = Img.imgret2("CraftTable.png")
    recipe = 0
    solid = False
    playerenter = False

    def __init__(self, x, y, owner):
        Object.OObject.__init__(self, x, y, owner)
        self.recipeprogress = GameRegistry.craftrecipes[0][0][:]
        self.gui = CrGUI(self)

    def drop(self, world, ent):
        if ent.name in self.recipeprogress:
            self.recipeprogress.remove(ent.name)
            world.dest_ent(self.x,self.y)
            if not len(self.recipeprogress):
                rec = GameRegistry.craftrecipes[self.recipe]
                world.player.inv[rec[1][0]] += rec[1][1]
                self.recipeprogress = GameRegistry.craftrecipes[self.recipe][0][:]

    def pick(self, world):
        world.run_GUI(self.gui)
        return None
