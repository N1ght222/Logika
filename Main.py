import pygame
from random import randint
import time
import sys
from pygame import *

pygame.init()
clock = pygame.time.Clock()
#start_time = clock()
#time_live = time.time(start_time)

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
turn_sound = mixer.Sound('shiny.mp3')

img_player = "CarPlayer.png"
img_back = "back.png"
img_enemy = "CarEnemy.png"
img_tree = "tree.png"
img_house = "house.png"

font.init()
font2 = font.Font(None, 36)
crashed = 0
score = 0
#player_speed = 1000

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Speed")
background = transform.scale(image.load("back.png"), (win_width, win_height))
clock = time.Clock()
'''
def anim_Background():
    background = pygame.image.load("back.png") 
    background_rect = background.get_rect()
    scroll_speed = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                background_rect.y -= scroll_speed  
            if background_rect.y <= -background.get_height():
                background_rect.y = win_height  
                window.blit(background, background_rect)
                pygame.display.flip()
                pygame.time.Clock().tick(60)
        pygame.quit()
        sys.exit()
        scroll_image()
'''
FPS = 240

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (200, 180))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))  # Задаємо зображення
        self.image.fill((255, 0, 0))  # Червоний колір
        self.rect = self.image.get_rect(topleft=(x, y))  # Визначаємо прямокутник (rect)

# Створюємо екземпляри
CarPlayer = Car(100, 200, 50, 30)
CarEnemy = Car(300, 200, 50, 30)


class CarPlayer(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.y > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.y < win_width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global time
        if self.rect.y > win_height:
            self.rect.x = randint(100, 300)
            self.rect.y = 0
        #if sprite.spritecollide(CarPlayer, CarEnemy, False):
       

    
class Tree(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -self.rect.height
tree = Tree(img_tree, 550, 10, 60,60,5)

class House(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -self.rect.height
house = House(img_house, 1, 10, 60,60,5)


CarPlayers = CarPlayer(img_player,5,win_height-100,80,100,10) 
CarEnemies = sprite.Group()
#CarPlayers = sprite.Group()

for i in range(1, 2):
    CarEnemy = Enemy(img_enemy, randint(100, 300), -40, 80, 50, (randint(1, 2)))
    CarEnemy.add(CarEnemies)
    CarEnemies.update()
    CarEnemies.draw(window)


finish = False
run = True

while run:
    if not finish:
        window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                turn_sound.play()
            if e.key == K_RIGHT:
                turn_sound.play()
           # anim_Background()
    if sprite.spritecollide(CarPlayer, CarEnemy,False):
        crashed += 1
    if crashed == 5:
        finish = True
        window.blit(text_lose, (200, 200))
    if not finish:
        window.blit(background, (0, 0))
        text_lose = font2.render("Пропущено: " + str(crashed), 20, (255, 0, 0)) 
        window.blit(text_lose, (0, 20))
        text_win = font2.render("Ви Виграли " + str(score), 1, (255, 255, 255)) 
        CarPlayers.update()
        CarPlayers.reset()
        CarEnemies.update()
        tree.update()
        tree.reset()
        house.update()
        house.reset()
        CarEnemies.draw(window)
        display.update()
    time.delay(0)
    clock.tick(FPS)



    