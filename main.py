# coding=utf8
import pygame
from pygame.tests.base_test import pygame_quit
import sys
import player
import items
import movables
import random


def intersect(pos1, pos2):
    if pos1[0] >= pos2[0] + pos2[2] or pos2[0] >= pos1[0] + pos1[2]:
        return False
    if pos1[1] >= pos2[1] + pos2[3] or pos2[1] >= pos1[1] + pos1[3]:
        return False
    return True


class Game:
    WIN = 0
    PLAY = 1
    LOSE = 2
    UP    = (0, -1)
    DOWN  = (0,  1)
    LEFT  = (-1, 0)
    RIGHT = (1,  0)
    SCREEN_SIZE = (640, 480)
    def __init__(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption('War Town')
        self.background = pygame.image.load('background.bmp')
        self.screen.blit(self.background, (0, 0))


        self.all_objects = pygame.sprite.Group( )
        self.tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()
        self.my_group = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.score_font = pygame.font.Font(None, 36)
        self.win_font = pygame.font.Font(None, 100)
        self.lose_font = pygame.font.Font(None, 90)
        self.live_img = pygame.image.load("images/live.bmp")
        self.live_img.set_colorkey((0,0,0))

        self.lives = 0
        self.state = self.PLAY
        self.score = 0
        self.replay_timer = 80
        self.player_default = (0,0)
        self.tanks_count = 0

    def tank_die(self):
        self.tanks_count -= 1
        self.score += 100
        if self.tanks_count <= 0:
            self.state = self.WIN

    def base_die(self):
        self.state = self.LOSE
        self.my_group.empty()

    def player_die(self, number):
        self.lives -= 1
        if self.lives < 0:
            self.state = self.LOSE
        else:
            self.player[number].rect.x = self.player_default[number][0]
            self.player[number].rect.y = self.player_default[number][1]
            self.player[number].immortal()

    def start_screen(self):
        game_type = 1
        game_selected = False
        while not game_selected:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif i.key == pygame.K_DOWN:
                        game_type = 2
                    elif i.key == pygame.K_UP:
                        game_type = 1
                    elif i.key == pygame.K_SPACE:
                        game_selected = True

            self.screen.blit(self.background, (0, 0))
            text = self.win_font.render("COMBAT TOWN", 2, (250,30,50))
            w,h = text.get_size()
            self.screen.blit(text,(320-w//2,220-h))

            cursor = pygame.image.load("images/tanks.bmp")
            cursor.set_colorkey((0, 0, 0))
            cur_pos = (200,240)
            if game_type == 2:
                cur_pos = (200, 270)
            self.screen.blit(cursor, (cur_pos), (0,0,32,32))
            text = self.score_font.render("one player", 1, (20,10,10))
            self.screen.blit(text,(250, 240))
            text = self.score_font.render("two players", 1, (20,10,10))
            self.screen.blit(text,(250, 270))

            text = self.score_font.render("press space to select", 1, (20,10,10))
            w,h = text.get_size()
            self.screen.blit(text,(320-w//2, 350-h))

            pygame.display.flip()
            self.fps_clock.tick(30)
        self.load_level(game_type)

    def load_level(self, players=1):
        self.lives = 0
        self.state = self.PLAY
        self.score = 0
        self.replay_timer = 40
        self.all_objects.empty()
        self.my_group.empty()
        self.tanks.empty()
        self.borders.empty()
        self.bullets.empty()
        self.items.empty()
        self.player = []
        self.player_default = []

        borders = [
                items.Border(self, -25,0,25,self.SCREEN_SIZE[1]),
                items.Border(self, 0,-25,self.SCREEN_SIZE[0],25),
                items.Border(self, 0,self.SCREEN_SIZE[1],self.SCREEN_SIZE[0],25),
                items.Border(self, self.SCREEN_SIZE[0],0,25,self.SCREEN_SIZE[1])]
        self.borders.add(borders)

        #level = open("level.txt",'r')
        level = []
        tank_count = 20
        wall_len = 0
        for x in range(12):
            level.append('')
            for y in range(16):
                if wall_len >0 :
                    level[-1]+= 'w'
                    wall_len -= 1
                else:
                    if tank_count > 0:
                        if random.random() < 0.2:
                            level[-1] += 't'
                            tank_count -= 1
                        elif random.random() < 0.2:
                            wall_len = random.randint(1,5)
                            level[-1] += ' '
                    level[-1] += ' '
        base_pos = (random.randint(1, 14),random.randint(2, 10))
        if players == 1:
            level[base_pos[1]-2] = level[base_pos[1]-2][0:base_pos[0]-1]+'p  '+level[base_pos[1]-2][base_pos[0]+1:]
        else:
            level[base_pos[1]-2] = level[base_pos[1]-2][0:base_pos[0]-1]+'p p'+level[base_pos[1]-2][base_pos[0]+1:]
        level[base_pos[1]-1] = level[base_pos[1]-1][0:base_pos[0]-1]+'www'+level[base_pos[1]-1][base_pos[0]+1:]
        level[base_pos[1]] = level[base_pos[1]][0:base_pos[0]-1]+'wbw'+level[base_pos[1]][base_pos[0]+1:]
        level[base_pos[1]+1] = level[base_pos[1]+1][0:base_pos[0]-1]+'www'+level[base_pos[1]+1][base_pos[0]+1:]
        for y,line in enumerate(level):
            for x,c in enumerate(line):
                if c == 'p':
                    self.player_default.append( (x*40, y*40))
                    self.player.append(player.Player(self, x*40, y*40, len(self.player)))
                    self.my_group.add([self.player[-1]])
                    self.player[-1].immortal()
                    self.lives += 3
                elif c == 'b':
                    self.base = items.Base(self, x*40, y*40)
                    self.my_group.add([self.base])
                elif c == 'w':
                    wall = [items.Wall(self,x*40, y*40),
                            items.Wall(self,x*40+20, y*40),
                            items.Wall(self,x*40, y*40+20),
                            items.Wall(self,x*40+20, y*40+20)]
                    self.items.add(wall)
                elif c == 't':
                    self.tanks_count += 1
                    tank = movables.Tank(self, x*40, y*40)
                    self.tanks.add([tank])
        

    def draw(self, image, pos, rect = None):
        self.screen.blit(image,pos, rect)


    def run(self):
        while True:

            for i in pygame.event.get(): # Перебор в списке событий
                if i.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_ESCAPE:
                        sys.exit()
                    else:
                        if self.state == self.PLAY:
                            for pl in self.player:
                                pl.do(i)
                if i.type == pygame.KEYUP:
                    if self.replay_timer < 0 and i.key == pygame.K_SPACE :
                        self.load_level()
                    if self.state == self.PLAY:
                        for pl in self.player:
                            pl.donot(i)



            self.screen.blit(self.background, (0, 0))
            self.all_objects.update()
            self.all_objects.draw(self.screen)

            if self.state == self.PLAY:
                text = self.score_font.render(str(self.score), 1, (10, 10, 10))
                #textpos = text.get_rect()
                self.screen.blit(text,(0,0))
                for i in range(1,1+self.lives):
                    self.screen.blit(self.live_img, (self.SCREEN_SIZE[0]-i*20,0))
            elif self.state == self.WIN:
                text = self.win_font.render("YOU WIN!", 2, (250,30,50))
                w,h = text.get_size()
                self.screen.blit(text,(320-w//2,220-h))
                self.replay_timer -= 1
            elif self.state == self.LOSE:
                text = self.lose_font.render("YOU LOSE...", 2, (40,30,250))
                w,h = text.get_size()
                self.screen.blit(text,(320-w//2,220-h))
                self.replay_timer -= 1

            if self.replay_timer < 0:
                text = self.score_font.render("your score: %s"%self.score, 1, (20,10,10))
                w,h = text.get_size()
                self.screen.blit(text,(320-w//2, 240-h))
                text = self.score_font.render("press space to play again", 1, (20,10,10))
                w,h = text.get_size()
                self.screen.blit(text,(320-w//2, 280-h))

            pygame.display.flip()
            self.fps_clock.tick(30)



if __name__ == '__main__':
    game = Game()
    game.start_screen()
    game.run()