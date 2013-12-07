import items
import pygame
import random


class Tank(items.Item):
    def __init__(self, game, x, y):
        items.Item.__init__(self,game,x,y)
        self.w = 20
        self.h = 20

        self.cool_down = 0
        self.max_cool_down = 20
        self.max_speed = 3
        self.dir = game.RIGHT
        self.speed = {
            0: (0, -self.max_speed),
            1: (0, self.max_speed),
            2: (-self.max_speed, 0),
            3: (self.max_speed, 0)
        }[self.dir]
        #todo rotate image with dir
        self.image = pygame.image.load('player.bmp') #todo tank picture
        self.image.set_colorkey((0,0,0))

    def think(self):
        self.cool_down -=1
        if self.x < 20:
            self.speed = (self.max_speed, 0)
        elif self.x > 500:
            self.speed = (-self.max_speed, 0)
        elif self.y < 20:
            self.speed = ( 0,self.max_speed)
        elif self.y > 400:
            self.speed = (0, -self.max_speed)
        else:
            if random.randint(0, 20) > 18:
                self.dir = random.randint(0, 3)
                self.speed = {
                    0: (0, -self.max_speed),
                    1: (0, self.max_speed),
                    2: (-self.max_speed, 0),
                    3: (self.max_speed, 0)
                }[self.dir]
            if random.randint(0,20) > 10:
                if self.cool_down < 1:
                    self.game.items.append(Bullet(self.game, self.x + self.w//2 ,self.y -1 , self.dir, True))
                    self.cool_down = self.max_cool_down

    def move(self):
        self.old_pos = self.pos
        self.x += self.speed[0]
        self.y += self.speed[1]

    def draw(self):
        self.game.draw(self.image, (self.x, self.y))

    def interact(self, other):
        if isinstance(other, items.Wall):
            self.speed = (-self.speed[0], - self.speed[1])
            self.x = self.old_pos[0]
            self.y = self.old_pos[1]

    def die(self):
        self.game.kill_me_please(self)

class Bullet(items.Item):
    def __init__(self, game, x, y, dir, type = False):
        items.Item.__init__(self,game,x,y)
        self.w = 8
        self.h = 8
        self.image = pygame.image.load("images/bullet.bmp")
        self.image.set_colorkey((0,0,0))
        self.max_speed = 20
        self.speed = {game.UP: (0,-self.max_speed),
                      game.DOWN: (0, self.max_speed),
                      game.LEFT: (-self.max_speed, 0),
                      game.RIGHT: (self.max_speed, 0)}[dir]
        if dir == game.DOWN:
            self.image = pygame.transform.rotate(self.image, 180)
        if dir == game.LEFT:
            self.image = pygame.transform.rotate(self.image, 90)
        if dir == game.RIGHT:
            self.image = pygame.transform.rotate(self.image, 270)
        self.type = type


    def die(self):
        self.dead = True
        self.game.items.append(items.Explosion(self.game,self.x,self.y))
        self.game.kill_me_please(self)


    def interact(self, other):
        if other.dead or (self.type and isinstance(other,Tank)):
            return
        other.die()
        self.die()

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def draw(self):
        if 1000 < self.x or self.x < -10 or 1000 < self.y or self.y < -10:
            del self.game.items[self.game.items.index(self)]
        else:
            self.game.draw(self.image, (self.x, self.y))