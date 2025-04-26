import pygame
import random
import os
import sys

# Ініціалізація pygame
pygame.init()

# Константи гри
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
PLAYER_SPEED = 3

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

def load_and_scale_images():
    """Завантажує та автоматично масштабує всі зображення гри"""
    images = {}
    image_dir = "images"
    
    # Розміри для різних типів зображень
    target_sizes = {
        "background": (SCREEN_WIDTH, SCREEN_HEIGHT),
        "player": (TILE_SIZE, TILE_SIZE),
        "grass": (TILE_SIZE, TILE_SIZE),
        "water": (TILE_SIZE, TILE_SIZE),
        "wall": (TILE_SIZE, TILE_SIZE),
        "radiation": (TILE_SIZE, TILE_SIZE),
        "tree": (int(TILE_SIZE*1.5), int(TILE_SIZE*2)),
        "npc": (TILE_SIZE, TILE_SIZE),
        "medkit": (int(TILE_SIZE*0.75), int(TILE_SIZE*0.75)),
        "artifact": (TILE_SIZE, TILE_SIZE),
        "weapon": (TILE_SIZE, TILE_SIZE)
    }
    
    # Кольори для заглушок
    default_colors = {
        "background": (50, 50, 100),
        "player": (0, 0, 255),
        "grass": (0, 128, 0),
        "water": (0, 0, 200),
        "wall": (139, 69, 19),
        "radiation": (0, 255, 0),
        "tree": (0, 100, 0),
        "npc": (255, 0, 0),
        "medkit": (255, 255, 255),
        "artifact": (255, 215, 0),
        "weapon": (192, 192, 192)
    }
    
    # Створюємо папку, якщо її немає
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        print(f"Створено папку {image_dir}. Додайте туди зображення!")
    
    # Завантажуємо або створюємо кожне зображення
    for img_name, size in target_sizes.items():
        filename = f"{image_dir}/{img_name}.png"
        try:
            # Спроба завантажити зображення
            img = pygame.image.load(filename)
            # Масштабуємо до потрібного розміру
            if img.get_size() != size:
                img = pygame.transform.scale(img, size)
            images[img_name] = img
        except:
            # Створюємо заглушку, якщо зображення не знайдено
            surf = pygame.Surface(size)
            color = default_colors.get(img_name, (255, 0, 255))  # рожевий для невідомих
            surf.fill(color)
            images[img_name] = surf
            print(f"Створено заглушку для {img_name}")
    
    return images

# Замінюємо старий блок завантаження зображень на новий
try:
    game_images = load_and_scale_images()
    
    # Основні текстури
    water_img = game_images["water"]
    wall_img = game_images["wall"]
    radiation_img = game_images["radiation"]
    
    # Гравця
    player_img = game_images["player"]
    
    # Предмети
    artifact_img = game_images["artifact"]
    medkit_img = game_images["medkit"]
    
    # Дерева
    tree_img = game_images["tree"]
    
    # NPC
    npc_img = game_images["npc"]
    
    # Фон
    background_img = game_images["background"]
    
except Exception as e:
    print(f"Помилка завантаження зображень: {e}")
    sys.exit()

# Створення екрану
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Stalker з картинками")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont('Arial', 16)

# Функція для завантаження зображень
def load_image(name, scale=1.0):
    try:
        image = pygame.image.load(name)
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except pygame.error as e:
        print(f"Не вдалося завантажити зображення {name}: {e}")
        # Створення заглушки
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill(RED if "player" in name else GREEN if "grass" in name else BLUE if "water" in name else YELLOW)
        return surf

# Завантаження зображень
try:
    # Основні текстури
    water_img = load_image("water.png")
    wall_img = load_image("wall.png")
    radiation_img = load_image("radiation.png")
    
    # Гравця
    player_img = load_image("player.png", 0.8)
    
    # Предмети
    artifact_img = load_image("artifact.png")
    medkit_img = load_image("medkit.png")
    
    # Дерева
    tree_img = load_image("tree.png", 1.5)
    
    # NPC
    npc_img = load_image("npc.png")
    
    # Фон
    background_img = load_image("background.png")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
except Exception as e:
    print(f"Помилка завантаження зображень: {e}")
    sys.exit()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = PLAYER_SPEED
        self.inventory = []
        self.health = 100
        self.radiation = 0
        self.money = 100
        self.quests = []
        self.direction = "down"
        self.animation_frame = 0
        self.animation_speed = 0.2
        
    def move(self, dx, dy, world):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        if 0 <= new_x < len(world[0]) * TILE_SIZE - self.width and 0 <= new_y < len(world) * TILE_SIZE - self.height:
            tile_x = int(new_x // TILE_SIZE)
            tile_y = int(new_y // TILE_SIZE)
            
            if world[tile_y][tile_x] != 1:  # 1 - стіна
                self.x = new_x
                self.y = new_y
        
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"
            
        if dx != 0 or dy != 0:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= 4:
                self.animation_frame = 0
    
    def draw(self, screen, camera_x, camera_y):
        # Малюємо гравця з картинкою
        screen.blit(player_img, (self.x - camera_x, self.y - camera_y))
        
        # Індикатор напрямку (можна прибрати, якщо картинка вже анімована)
        if self.direction == "up":
            pygame.draw.polygon(screen, RED, [
                (self.x - camera_x + self.width//2, self.y - camera_y),
                (self.x - camera_x, self.y - camera_y + self.height//2),
                (self.x - camera_x + self.width, self.y - camera_y + self.height//2)
            ])
    
    def add_to_inventory(self, item):
        self.inventory.append(item)
    
    def add_quest(self, quest):
        self.quests.append(quest)
        
    def draw_stats(self, screen):
        # Здоров'я
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 200 * (self.health / 100), 20))
        health_text = font.render(f"Здоров'я: {self.health}/100", True, WHITE)
        screen.blit(health_text, (15, 10))
        
        # Радіація
        pygame.draw.rect(screen, GRAY, (10, 40, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 40, 200 * (self.radiation / 100), 20))
        rad_text = font.render(f"Радіація: {self.radiation}/100", True, WHITE)
        screen.blit(rad_text, (15, 40))
        
        # Гроші
        money_text = font.render(f"Гроші: ${self.money}", True, WHITE)
        screen.blit(money_text, (15, 70))

class Item:
    def __init__(self, name, item_type, value, x, y):
        self.name = name
        self.type = item_type  # "weapon", "armor", "consumable", "quest"
        self.value = value
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.collected = False
        
    def draw(self, screen, camera_x, camera_y):
        if not self.collected:
            # Вибір зображення за типом предмета
            if self.type == "consumable":
                img = medkit_img
            elif self.type == "quest":
                img = artifact_img
            else:
                img = artifact_img  # За замовчуванням
                
            screen.blit(img, (self.x - camera_x, self.y - camera_y))
            
            # Підпис предмета
            name_text = font.render(self.name, True, WHITE)
            screen.blit(name_text, (self.x - camera_x, self.y - camera_y - 15))

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE * 1.5
        self.height = TILE_SIZE * 1.5
        
    def draw(self, screen, camera_x, camera_y):
        screen.blit(tree_img, (self.x - camera_x - self.width//4, self.y - camera_y - self.height//2))

class NPC:
    def __init__(self, name, x, y, dialogue, quest=None):
        self.name = name
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.dialogue = dialogue
        self.quest = quest
        self.dialogue_active = False
        self.current_dialogue = 0
        
    def draw(self, screen, camera_x, camera_y):
        screen.blit(npc_img, (self.x - camera_x, self.y - camera_y))
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (self.x - camera_x, self.y - camera_y - 15))
        
        if self.dialogue_active:
            self.draw_dialogue(screen)
    
    def draw_dialogue(self, screen):
        dialogue_box = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
        pygame.draw.rect(screen, GRAY, dialogue_box)
        pygame.draw.rect(screen, WHITE, dialogue_box, 2)
        
        dialogue_lines = []
        words = self.dialogue[self.current_dialogue].split()
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < SCREEN_WIDTH - 120:
                current_line = test_line
            else:
                dialogue_lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            dialogue_lines.append(current_line)
        
        for i, line in enumerate(dialogue_lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (70, SCREEN_HEIGHT - 130 + i * 20))
        
        continue_text = font.render("Натисніть ПРОБІЛ для продовження...", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 50))

class Quest:
    def __init__(self, title, description, objective, reward):
        self.title = title
        self.description = description
        self.objective = objective
        self.reward = reward
        self.completed = False
        self.progress = 0
    
    def update_progress(self, player):
        if self.objective["type"] == "collect":
            count = sum(1 for item in player.inventory if item.name == self.objective["target"])
            self.progress = count
            if count >= self.objective["amount"]:
                self.completed = True
                return True
        return False
    
    def draw(self, screen, x, y):
        status = "Виконано" if self.completed else f"У прогресі ({self.progress}/{self.objective['amount']})"
        color = GREEN if self.completed else WHITE
        
        title_text = font.render(f"{self.title}: {status}", True, color)
        screen.blit(title_text, (x, y))
        
        desc_text = font.render(self.description, True, WHITE)
        screen.blit(desc_text, (x, y + 20))
        
        obj_text = font.render(f"Ціль: {self.objective['type']} {self.objective['amount']} {self.objective['target']}", True, WHITE)
        screen.blit(obj_text, (x, y + 40))
        
        reward_text = font.render(f"Нагорода: ${self.reward}", True, WHITE)
        screen.blit(reward_text, (x, y + 60))

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.generate_map()
        self.items = []
        self.npcs = []
        self.trees = []
        self.generate_environment()
        
    def generate_map(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    self.map[y][x] = 1  # Стіни по краях
                else:
                    if random.random() < 0.1:
                        self.map[y][x] = 1  # Випадкові стіни
                    elif random.random() < 0.05:
                        self.map[y][x] = 2  # Вода
                    elif random.random() < 0.03:
                        self.map[y][x] = 3  # Радіація
                    else:
                        self.map[y][x] = 0  # Трава
    
    def generate_environment(self):
        # Додаємо предмети
        item_types = ["weapon", "armor", "consumable", "quest"]
        for _ in range(20):
            x, y = self.find_empty_spot()
            item_type = random.choice(item_types)
            name = f"{item_type.capitalize()} {random.randint(1, 100)}"
            value = random.randint(10, 100)
            self.items.append(Item(name, item_type, value, x * TILE_SIZE, y * TILE_SIZE))
        
        # Додаємо NPC
        dialogues = [
            ["Привіт, сталкере.", "Будь обережним у цій зоні.", "У мене є робота для тебе, якщо цікаво."],
            ["Рівень радіації сьогодні високий.", "Не ходи до червоних зон без захисту."],
            ["Я чув чутки про артефакти на півночі.", "Вони коштують багато грошей, якщо знайдеш."]
        ]
        
        quests = [
            Quest("Знайти артефакти", "Збери 3 артефакти у зоні", 
                 {"type": "collect", "target": "Artifact", "amount": 3}, 500),
            Quest("Знищити мутантів", "Знищ 5 мутантів у зоні",
                 {"type": "kill", "target": "Mutant", "amount": 5}, 800)
        ]
        
        for i in range(3):
            x, y = self.find_empty_spot()
            dialogue = random.choice(dialogues)
            quest = quests[i % len(quests)] if i < len(quests) else None
            self.npcs.append(NPC(f"NPC {i+1}", x * TILE_SIZE, y * TILE_SIZE, dialogue, quest))
        
        # Додаємо дерева
        for _ in range(30):
            x, y = self.find_empty_spot()
            self.trees.append(Tree(x * TILE_SIZE, y * TILE_SIZE))
    
    def find_empty_spot(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.map[y][x] == 0:
                return x, y
    
    def draw(self, screen, camera_x, camera_y):
        # Малюємо фон
        screen.blit(background_img, (0, 0))
        
        # Малюємо тайли карти
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE)
                
                if self.map[y][x] == 1:  # Стіна
                    screen.blit(wall_img, rect)
                elif self.map[y][x] == 2:  # Вода
                    screen.blit(water_img, rect)
                elif self.map[y][x] == 3:  # Радіація
                    screen.blit(radiation_img, rect)
                
                # Сітка (можна прибрати)
                pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Малюємо дерева
        for tree in self.trees:
            tree.draw(screen, camera_x, camera_y)

def draw_inventory(screen, player):
    inventory_box = pygame.Rect(SCREEN_WIDTH - 250, 50, 200, SCREEN_HEIGHT - 100)
    pygame.draw.rect(screen, GRAY, inventory_box)
    pygame.draw.rect(screen, WHITE, inventory_box, 2)
    
    title_text = font.render("Інвентар", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH - 240, 60))
    
    if not player.inventory:
        empty_text = font.render("Порожньо", True, WHITE)
        screen.blit(empty_text, (SCREEN_WIDTH - 240, 90))
    else:
        for i, item in enumerate(player.inventory):
            item_text = font.render(f"{item.name} ({item.type})", True, WHITE)
            screen.blit(item_text, (SCREEN_WIDTH - 240, 90 + i * 25))

def draw_quests(screen, player):
    quests_box = pygame.Rect(50, 50, 300, SCREEN_HEIGHT - 100)
    pygame.draw.rect(screen, GRAY, quests_box)
    pygame.draw.rect(screen, WHITE, quests_box, 2)
    
    title_text = font.render("Квести", True, WHITE)
    screen.blit(title_text, (60, 60))
    
    if not player.quests:
        empty_text = font.render("Немає активних квестів", True, WHITE)
        screen.blit(empty_text, (60, 90))
    else:
        for i, quest in enumerate(player.quests):
            quest.draw(screen, 60, 90 + i * 100)

def main():
    # Створення світу
    world = World(50, 50)
    
    # Створення гравця
    player = Player(world.width * TILE_SIZE // 2, world.height * TILE_SIZE // 2)
    
    # Камера
    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2
    
    # Стани гри
    show_inventory = False
    show_quests = False
    game_active = True
    
    # Головний цикл гри
    running = True
    while running:
        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i:
                    show_inventory = not show_inventory
                    show_quests = False
                elif event.key == pygame.K_q:
                    show_quests = not show_quests
                    show_inventory = False
                elif event.key == pygame.K_SPACE:
                    for npc in world.npcs:
                        if (abs(player.x - npc.x) < TILE_SIZE * 2 and 
                            abs(player.y - npc.y) < TILE_SIZE * 2):
                            npc.dialogue_active = True
                            if npc.quest and npc.quest not in player.quests:
                                player.add_quest(npc.quest)
                            break
        
        if game_active and not show_inventory and not show_quests:
            # Рух гравця
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
            
            player.move(dx, dy, world.map)
            
            # Оновлення камери
            camera_x = player.x - SCREEN_WIDTH // 2
            camera_y = player.y - SCREEN_HEIGHT // 2
            camera_x = max(0, min(camera_x, world.width * TILE_SIZE - SCREEN_WIDTH))
            camera_y = max(0, min(camera_y, world.height * TILE_SIZE - SCREEN_HEIGHT))
            
            # Збір предметів
            for item in world.items:
                if (not item.collected and 
                    abs(player.x - item.x) < TILE_SIZE and 
                    abs(player.y - item.y) < TILE_SIZE):
                    player.add_to_inventory(item)
                    item.collected = True
            
            # Радіація
            tile_x = int(player.x // TILE_SIZE)
            tile_y = int(player.y // TILE_SIZE)
            if world.map[tile_y][tile_x] == 3:
                player.radiation = min(100, player.radiation + 0.1)
                if player.radiation >= 100:
                    player.health -= 0.5
            else:
                player.radiation = max(0, player.radiation - 0.05)
            
            # Оновлення квестів
            for quest in player.quests:
                if not quest.completed:
                    quest.update_progress(player)
                    if quest.completed:
                        player.money += quest.reward
        
        # Відображення
        screen.fill(BLACK)
        
        # Малюємо світ
        world.draw(screen, camera_x, camera_y)
        
        # Малюємо предмети
        for item in world.items:
            if not item.collected:
                item.draw(screen, camera_x, camera_y)
        
        # Малюємо NPC
        for npc in world.npcs:
            npc.draw(screen, camera_x, camera_y)
            if npc.dialogue_active:
                npc.draw_dialogue(screen)
                if keys[pygame.K_SPACE]:
                    npc.current_dialogue += 1
                    if npc.current_dialogue >= len(npc.dialogue):
                        npc.dialogue_active = False
                        npc.current_dialogue = 0
        
        # Малюємо гравця
        player.draw(screen, camera_x, camera_y)
        
        # Малюємо UI
        player.draw_stats(screen)
        
        # Інвентар
        if show_inventory:
            draw_inventory(screen, player)
        
        # Квести
        if show_quests:
            draw_quests(screen, player)
        
        # Оновлення екрану
        pygame.display.flip()
        
        # Обмеження FPS
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()