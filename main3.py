import pygame
from random import randint
from pygame import mixer

# Ініціалізація pygame
pygame.init()
mixer.init()

# Основні параметри гри
win_width = 700
win_height = 500
FPS = 60

# Створення вікна
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Speed")

# Змінні для гри
crashed = 0
score = 0
# Завантаження фону
background = pygame.transform.scale(pygame.image.load("back.png"), (win_width, win_height))

# Змінна для руху фону
bg_y = 0
bg_speed = 5  # Швидкість руху фону

# Шрифти
font = pygame.font.Font(None, 36)

# Клас GameSprite
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас CarPlayer
class CarPlayer(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

# Клас Enemy
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(100, win_width - 100)
            self.rect.y = -self.rect.height

# Створення об'єктів
CarPlayers = CarPlayer("CarPlayer.png", 300, win_height - 120, 80, 100, 10)
CarEnemies = pygame.sprite.Group()

for i in range(3):
    enemy = Enemy("CarEnemy.png", randint(100, 600), -40, 100, 100, randint(2, 4))
    CarEnemies.add(enemy)

# Основний ігровий цикл
finish = False
run = True
clock = pygame.time.Clock()

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    if not finish:
        # Рух фону
        bg_y += bg_speed
        if bg_y >= win_height:
            bg_y = 0  # Перезапускаємо фон

        # Малюємо рухомий фон
        window.blit(background, (0, bg_y - win_height))
        window.blit(background, (0, bg_y))

        # Оновлення та малювання спрайтів
        CarPlayers.update()
        CarPlayers.reset()
        CarEnemies.update()
        CarEnemies.draw(window)

        # Перевірка зіткнень
        if pygame.sprite.spritecollide(CarPlayers, CarEnemies, False):
            crashed += 1

        # Відображення тексту
        text_lose = font.render(f"Пропущено: {crashed}", True, (255, 0, 0))
        text_win = font.render(f"Очки: {score}", True, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        window.blit(text_win, (10, 40))

        # Перевірка програшу
        if crashed >= 5:
            finish = True
            lose_text = font.render("Ви програли!", True, (255, 0, 0))
            window.blit(lose_text, (win_width // 2 - 100, win_height // 2))

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()
