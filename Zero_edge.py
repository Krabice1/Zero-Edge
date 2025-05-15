import pygame
import random
import math

pygame.init()

window_width = 1080
window_height = 1080

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Zero Edge")

clock = pygame.time.Clock()

# Globální rychlost střel
rychlost_strel = 4
interval = 5000
posledni_zmena = pygame.time.get_ticks()

# Třída pro hráče
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 25
        prumer = self.radius * 2
        self.image = pygame.Surface((prumer, prumer), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 0), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(window_width // 2, window_height // 2))

    def get_center(self):
        return self.rect.center


# Třída pro jednotlivé střely
class Projectile:
    def __init__(self, speed):
        self.radius = 20
        self.x, self.y, self.vx, self.vy = self.spawn(speed)

    def spawn(self, speed):
        souradnice = random.choice(["x", "y"])
        strana = random.choice(["max", "min"])
        if souradnice == "x" and strana == "min":
            x = 0
            y = random.randint(0, window_height)
        elif souradnice == "y" and strana == "min":
            y = 0
            x = random.randint(0, window_width)
        elif souradnice == "x" and strana == "max":
            x = window_width
            y = random.randint(0, window_height)
        else:
            y = window_height
            x = random.randint(0, window_width)

        angle = math.atan2((window_height // 2) - y, (window_width // 2) - x)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        return x, y, vx, vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 200), (int(self.x), int(self.y)), self.radius)

    def collides_with_player(self, player):
        px, py = player.get_center()
        dx = self.x - px
        dy = self.y - py
        distance = math.hypot(dx, dy)
        return distance < (self.radius + player.radius)


# Inicializace hráče a střel
player = Player()
player_group = pygame.sprite.GroupSingle(player)
projectiles = []

# Hlavní herní smyčka
running = True
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Zrychlení střel v čase
    curent_time = pygame.time.get_ticks()
    if curent_time - posledni_zmena > interval:
        rychlost_strel += 0.4  
        posledni_zmena = curent_time

    # Spawn nových střel
    spawn_timer += 1
    if spawn_timer >= 60 - (round(rychlost_strel) * 3):
        projectiles.append(Projectile(rychlost_strel))
        spawn_timer = 0

    for proj in projectiles[:]:
        proj.update()
        if proj.collides_with_player(player):
            projectiles.remove(proj)

    # Vykreslení
    screen.fill((30, 30, 30))
    player_group.draw(screen)
    for proj in projectiles:
        proj.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# problémy: Střely mohou zasáhnout hráče ve stejnou dobu. 
# řešení: Střely se budou spawnovat po kruhu.

# ToDo: štít, body, zvuk, grafika, animace