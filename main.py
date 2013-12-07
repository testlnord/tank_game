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
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('example')
        self.background = pygame.image.load('background.bmp')
        self.screen.blit(self.background, (0, 0))

        self.items = []

        self.player = player.Player(self, 320, 220)
        self.items.append(self.player)
        #todo lifes
        self.score = 0
        self.score_font = pygame.font.Font(None, 36)

    def load_level(self): #todo load from file
        self.items.append(items.Wall(self,100, 100))
        self.items.append(movables.Tank(self, 20, 100))
        self.max_tanks = 20


    def draw(self, image, pos, rect = None):
        self.screen.blit(image,pos, rect)

    def kill_me_please(self, item):
        if isinstance(item, movables.Tank):
            self.score += 100
        if item in self.items:
            del self.items[self.items.index(item)]

    #todo loosing
    #todo winning

    def run(self):
        while True:
            for i in pygame.event.get(): # Перебор в списке событий
                if i.type == pygame.QUIT: # Обрабатываем событие шечка по крестику закрытия окна
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_ESCAPE:
                        sys.exit()
                    else:
                        self.player.do(i)
                if i.type == pygame.KEYUP:
                    self.player.donot(i)

            if self.max_tanks > 0:
                if random.randint(0,100) < 2:
                    self.max_tanks -=1
                    self.items.append(movables.Tank(self,100+10*random.randint(2,5),150+10*random.randint(2,5)))

            for item in self.items:
                item.think()
                item.move()

            for i,item in enumerate(self.items[:-1]):
                for other in self.items[i+1:]:
                    if intersect(item.pos, other.pos):
                        other.interact(item)
                        item.interact(other)

            self.screen.blit(self.background, (0, 0))
            for item in self.items:
                item.draw()
	        text = self.score_font.render(str(self.score), 1, (10, 10, 10))
	        #textpos = text.get_rect()
            self.screen.blit(text,(0,0))
            pygame.display.flip()
            self.fps_clock.tick(30)



if __name__ == '__main__':
    game = Game()
    game.load_level()
    game.run()