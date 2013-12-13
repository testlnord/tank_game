import items
import pygame
import random
import math

class Tank(items.Item):
    def __init__(self, game, x, y):
        items.Item.__init__(self,game,x,y)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.cool_down = 0
        self.max_cool_down = 20
        self.max_speed = 3
        self.dir = game.RIGHT
        self.speed = 0

        self.anim_time = 64
        self.anim = pygame.image.load('images/badboys.bmp')
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.blit(self.anim, (0,0))
        self.image.set_colorkey((0,0,0))


    def collide(self):
        collided = pygame.sprite.spritecollide(self, self.game.borders, False)
        collided.extend(pygame.sprite.spritecollide(self, self.game.items, False))
        collided.extend(pygame.sprite.spritecollide(self, self.game.tanks, False))
        collided.extend(pygame.sprite.spritecollide(self, self.game.my_group, False))

        for bord in collided:
            if bord == self:
                continue
            if self.dir == self.game.DOWN:
                self.rect.bottom = bord.rect.top
            elif self.dir == self.game.UP:
                self.rect.top = bord.rect.bottom
            elif self.dir == self.game.LEFT:
                self.rect.left = bord.rect.right
            elif self.dir == self.game.RIGHT:
                self.rect.right = bord.rect.left

    def think(self):
        if self.cool_down < 0:
            self.game.bullets.add([Bullet(self.game, self.rect.centerx, self.rect.centery, self.dir)])
            self.cool_down = 20
        self.speed = self.max_speed
        if random.randint(0,100)<20:
            if random.randint(0,30) < 10:
                self.dir = [self.game.UP, self.game.DOWN, self.game.LEFT, self.game.RIGHT][random.randint(0,3)]
            else:
                if abs(self.game.base.rect.centerx - self.rect.centerx) >\
                   abs(self.game.base.rect.centery - self.rect.centery):
                    if self.game.base.rect.centerx < self.rect.centerx:
                        self.dir = self.game.LEFT
                    else:
                        self.dir = self.game.RIGHT
                else:
                    if self.game.base.rect.centery < self.rect.centery:
                        self.dir = self.game.UP
                    else:
                        self.dir = self.game.DOWN


    def update(self):
        self.cool_down -=1
        if self.speed > 0:
            self.rect.centerx += self.speed * self.dir[0]
            self.rect.centery += self.speed * self.dir[1]
            self.collide()

            self.image.blit(self.anim, (0,0), ( (7-self.anim_time//8)* self.rect.w,0 , self.rect.w, self.rect.h))
            if self.dir == self.game.DOWN:
                self.image = pygame.transform.rotate(self.image, 270)
            if self.dir == self.game.LEFT:
                self.image = pygame.transform.rotate(self.image, 180)
            if self.dir == self.game.UP:
                self.image = pygame.transform.rotate(self.image, 90)
            self.anim_time += 1
            if self.anim_time > 63:
                self.anim_time = 0

        self.think()

    def die(self):
        self.game.tank_die()
        self.kill()


class Bullet(items.Item):
    def __init__(self, game, x, y, dir, friend = False):
        items.Item.__init__(self,game,x,y)
        self.rect = pygame.Rect(x-4, y-4 , 8, 8)
        self.image = pygame.image.load("images/bullet.bmp")
        self.image.set_colorkey((0,0,0))
        self.max_speed = 20
        self.speed = self.max_speed
        self.dir = dir
        if dir == game.DOWN:
            self.image = pygame.transform.rotate(self.image, 180)
        if dir == game.LEFT:
            self.image = pygame.transform.rotate(self.image, 90)
        if dir == game.RIGHT:
            self.image = pygame.transform.rotate(self.image, 270)
        self.friend = friend


    def collide(self):
        collided = (pygame.sprite.spritecollide(self, self.game.items, False))
        collided.extend(pygame.sprite.spritecollide(self, self.game.borders, False))
        if self.friend:
            collided.extend(pygame.sprite.spritecollide(self, self.game.tanks, False))
        else:
            collided.extend(pygame.sprite.spritecollide(self, self.game.my_group, False))

        for obj in collided:
            if self.dir == self.game.DOWN:
                self.rect.bottom = obj.rect.top
            elif self.dir == self.game.UP:
                self.rect.top = obj.rect.bottom
            elif self.dir == self.game.LEFT:
                self.rect.left = obj.rect.right
            elif self.dir == self.game.RIGHT:
                self.rect.right = obj.rect.left
            obj.die()
        if len(collided)> 0:
            self.die()

    def update(self):
        self.rect.centerx += self.speed * self.dir[0]
        self.rect.centery += self.speed * self.dir[1]
        self.collide()

    def die(self):
        items.Explosion(self.game, self.rect.centerx, self.rect.centery)
        self.game.bullets.remove(self)
        self.game.all_objects.remove([self])

