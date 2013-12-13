#coding=utf8
import items
import pygame
import movables

class Player(movables.Tank):
    buttons = [{'up': pygame.K_UP, 'down': pygame.K_DOWN,
                'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                'shoot': pygame.K_KP_ENTER},
               {'up': pygame.K_w, 'down': pygame.K_s,
                'left': pygame.K_a, 'right': pygame.K_d,
                'shoot': pygame.K_SPACE},
               ]
    def __init__(self, game,  x, y, number):
        super(Player, self).__init__(game, x, y)
        #items.Item.__init__(self,game,x,y)
        self.anim = pygame.Surface((256, 32))
        all_tanks = pygame.image.load("images/tanks.bmp") # Картинка объекта
        self.anim.blit(all_tanks,(0,0), (0,number*32,256,32))

        self.image.blit(self.anim, (0,0))
        self.rect = pygame.Rect(x, y, 32, 32)
        self.max_speed = 10
        self.dir = self.game.RIGHT
        self.speed = 0
        self.number = number
        self.immortality = 0

    def do(self, event):
        if event.key == self.buttons[self.number]['up']:
            self.dir = self.game.UP
            self.speed = self.max_speed
        if event.key == self.buttons[self.number]['down']:
            self.dir = self.game.DOWN
            self.speed = self.max_speed
        if event.key == self.buttons[self.number]['left']:
            self.dir = self.game.LEFT
            self.speed = self.max_speed
        if event.key == self.buttons[self.number]['right']:
            self.dir = self.game.RIGHT
            self.speed = self.max_speed

        if event.key == self.buttons[self.number]['shoot']:
            if self.cool_down < 0:
                self.game.bullets.add([movables.Bullet(self.game, self.rect.centerx, self.rect.centery, self.dir, True)])
                self.cool_down = self.max_cool_down

    def think(self):
        if self.immortality > 0:
            self.immortality -= 1
            if self.immortality == 0:
                self.imm_anim.die()

    def donot(self, event):
        if event.key == self.buttons[self.number]['up']:
            if self.dir == self.game.UP:
                self.speed = 0
        if event.key == self.buttons[self.number]['down']:
            if self.dir == self.game.DOWN:
                self.speed = 0
        if event.key == self.buttons[self.number]['left']:
            if self.dir == self.game.LEFT:
                self.speed = 0
        if event.key == self.buttons[self.number]['right']:
            if self.dir == self.game.RIGHT:
                self.speed = 0

    def die(self):
        if not self.immortality:
            self.game.player_die(self.number)

    def immortal(self):
        self.immortality = 20
        self.imm_anim = items.ImmortalAnim(self.game,0,0)
        self.imm_anim.rect = self.rect