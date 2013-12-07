#coding=utf8
import pygame

#todo перевести все на sprites
class Item:
    def __init__(self,game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.dead = False
        self.image = pygame.image.load('player.bmp')

    @property
    def pos(self):
        return self.x, self.y, self.w, self.h

    @pos.setter
    def pos(self, other):
        self.x = other[0]
        self.y = other[1]
        self.w = other[2]
        self.h = other[3]

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

#todo wall desctruction
class Wall(Item):
    def __init__(self, game, x, y):
        Item.__init__(self,game,x,y)
        self.w = 20
        self.h = 20
        self.image = pygame.image.load('images/items/brick.bmp')

    def interact(self, other):
        pass


    def draw(self):
        self.game.draw(self.image, (self.x, self.y))

#todo ice
#todo concrete
#todo trees
#todo Base to protect
#todo water

class Explosion(Item):
    def __init__(self, game, x, y):
        Item.__init__(self,game,x,y)
        self.w = 20  #todo bigger explosions
        self.h = 20
        self.image = pygame.image.load('images/explosion.bmp')
        self.image.set_colorkey((0,0,0))
        self.time = 16

    def die(self):
        self.game.kill_me_please(self)

    def think(self):
        self.time -= 1
        if self.time == 0:
            self.die()

    def draw(self):
        p_y = (16-self.time)//4
        p_x = (16-self.time)%4
        self.game.draw(self.image, (self.x, self.y), (p_x*20,p_y*20,20,20))

