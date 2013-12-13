#coding=utf8
import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Item, self).__init__()
        #pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.rect = pygame.Rect(x, y, 10, 10)
        self.dead = False
        self.image = pygame.image.load('player.bmp')
        self.game.all_objects.add([self])

    @property
    def pos(self):
        return self.rect

    @pos.setter
    def pos(self, other):
        self.rect = other

    def update(self):
        pass

    def die(self):
        pass

    def interact(self, other):
        pass

    def draw(self):
        pass

    def think(self):
        pass

    def move(self):
        pass


class Wall(Item):
    def __init__(self, game, x, y):
        Item.__init__(self,game,x,y)
        self.rect = pygame.Rect(x,y, 20, 20)
        self.image = pygame.image.load('images/items/brick.bmp')
        self.state = 1

    def interact(self, other):
        pass

    def die(self):
        if self.state == 1:
            self.state = 0
            self.image = pygame.image.load('images/items/badbrick.bmp')
        elif self.state == 0:
            self.kill()

class Border(Item):
    def __init__(self, game, x,y,w,h):
        super(Border,self).__init__(game,x,y)
        self.rect = pygame.Rect(x, y , w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color("#333333"))


    def draw(self):
        self.game.draw(self.image, (self.x, self.y))

#todo ice
#todo concrete
#todo trees
#todo water

class Explosion(Item):
    def __init__(self, game, x, y):
        Item.__init__(self,game,x,y)
        self.rect = pygame.Rect(x,y,40,40)
        self.rect.centerx = x
        self.rect.centery = y

        self.anim = pygame.image.load('images/explosion.bmp')
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.image.set_colorkey((0, 0, 0))
        self.time = 32

    def update(self):
        p_y = (16-self.time//2)//4
        p_x = (16-self.time//2)%4
        self.image.fill((0, 0, 0))

        self.image.blit(self.anim,(0,0), (p_x*self.rect.width, p_y*self.rect.height, self.rect.width, self.rect.width))

        if self.time > 0:
            self.time -= 1
        else:
            self.die()

    def die(self):
        self.game.all_objects.remove([self])


    def draw(self):
        p_y = (16-self.time)//4
        p_x = (16-self.time)%4
        self.game.draw(self.image, (self.x, self.y), (p_x*20,p_y*20,20,20))


class Base(Item):

    def __init__(self, game, x, y):
        super(Base, self).__init__(game, x, y)
        self.rect = pygame.Rect(x,y, 24, 32)
        self.anim = pygame.image.load('images/items/base.bmp')
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.blit(self.anim, (0,0))
        self.image.set_colorkey((0, 0, 0))
        self.time = 0
        self.anim_dir = 1
        self.alive = True

    def update(self):
        if self.alive:
            self.image.blit(self.anim, (0, 0), (self.rect.w*(self.time//4), 0,self.rect.w, self.rect.h))
            self.time += self.anim_dir
            if self.time == 19 :
                self.anim_dir = -1
            if self.time == 0:
                self.anim_dir = 1

    def die(self):
        if self.alive:
            self.game.base_die()
            self.alive = False
            self.image.blit(self.anim, (0, 0), (self.rect.w*5, 0,self.rect.w, self.rect.h))


#effects
class ImmortalAnim(Item):
    def __init__(self, game, x, y):
        super(ImmortalAnim, self).__init__(game, x, y)
        self.anim = pygame.image.load('images/imm.bmp')
        self.image = pygame.Surface((32,32))
        self.image.set_colorkey((0,0,0))
        self.anim_time = 7

    def update(self):
        self.anim_time -= 1
        if self.anim_time < 0:
            self.anim_time = 7
        self.image.blit(self.anim, (0,0), (self.anim_time//2*32, 0, 32, 32))

    def die(self):
        self.kill()
