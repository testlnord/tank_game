#coding=utf8
import items
import pygame
import movables

class Player(items.Item):
    def __init__(self, game,  x, y):
        items.Item.__init__(self,game,x,y)
        self.img = pygame.image.load("player.bmp") # Картинка объекта
        self.w = 20
        self.h = 20
        self.max_speed = 10
        self.speed = (0,0)
        self.dir = self.game.UP

    def do(self, event):
        if event.key == pygame.K_UP: #273 код клавиши вверх
            self.speed = (0, -self.max_speed)
            self.dir = self.game.UP
        if event.key == pygame.K_DOWN:
            self.speed = (0, self.max_speed)
            self.dir = self.game.DOWN
        if event.key == pygame.K_LEFT:
            self.speed = (-self.max_speed, 0)
            self.dir = self.game.LEFT
        if event.key == pygame.K_RIGHT:
            self.speed = (self.max_speed, 0)
            self.dir = self.game.RIGHT
        if event.key == pygame.K_SPACE:
            self.game.items.append(movables.Bullet(self.game, self.x + self.w//2 ,self.y -1 , self.dir))
    #todo shooting with holding space
    #todo cooldown for shooting
    def donot(self, event):
        if event.key == pygame.K_UP: #273 код клавиши вверх
            self.speed = ( self.speed[0], 0)
        if event.key == pygame.K_DOWN:
            self.speed = ( self.speed[0], 0)
        if event.key == pygame.K_LEFT:
            self.speed = (0, self.speed[1])
        if event.key == pygame.K_RIGHT:
            self.speed = (0, self.speed[1])

    def move(self):
        self.old_pos = self.pos

        self.x += self.speed[0]
        self.y += self.speed[1]

    def interact(self, other):
        if isinstance(other, items.Wall):
            self.x = self.old_pos[0]
            self.y = self.old_pos[1]




    def draw(self):
        self.game.draw(self.img, (self.x, self.y))
