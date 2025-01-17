import pygame, os, time, random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Laser Blaster")

BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")

# SpaceShips
YELLOW_SPACE_SHIP = pygame.image.load("Assets/pixel_ship_yellow.png")
RED_SPACE_SHIP = pygame.image.load("Assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("Assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("Assets/pixel_ship_blue_small.png")

# Lasers
YELLOW_LASER = pygame.image.load("Assets/pixel_laser_yellow.png")
RED_LASER = pygame.image.load("Assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("Assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("Assets/pixel_laser_blue.png")

# Background
BG = pygame.transform.scale(pygame.image.load("Assets/background-black.png"), (WIDTH, HEIGHT))

class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                BULLET_HIT_SOUND.play()
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(WIN, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(WIN, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
        
    def collision(self, obj):
        return collide(self, obj)
    
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    level = 0
    lives = 5
    player_vel = 5
    laser_vel = 6
    enemies = []
    wave_length = 5
    enemy_vel  = 1
    lost = False
    lost_count = 0
    font = pygame.font.SysFont("comicsans", 40)

    player = Player(WIDTH//2 - 25, 550)

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_text = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_text = font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_text, (10, 10))
        WIN.blit(level_text, (WIDTH - lives_text.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_text = font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <=0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > 3 * FPS:
                run = False
            else:
                continue
            
        if len(enemies) == 0:
            level += 1
            wave_length += 5 #increase the number of enemies
            for i in range(wave_length):
                enemy = Enemy(random.randint(50, WIDTH - 100), random.randint(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and player.x - player_vel > 0) or (keys[pygame.K_a] and player.x - player_vel > 0): #LEFT
            player.x -= player_vel
        if (keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH) or (keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH): #RIGHT
            player.x += player_vel
        if (keys[pygame.K_UP] and player.y - player_vel > 0) or (keys[pygame.K_w] and player.y - player_vel > 0): #UP
            player.y -= player_vel
        if (keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT) or (keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT): #DOWN
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()
            BULLET_FIRE_SOUND.play()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                BULLET_HIT_SOUND.play()
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            
                
            
        player.move_lasers(-laser_vel, enemies)

        
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    subtitle_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_text = title_font.render("Laser Blasters", 1, (255, 255, 255))
        subtitle_text = subtitle_font.render("Click to begin", 1, (255, 255, 255))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - title_text.get_height()/2))
        WIN.blit(subtitle_text, (WIDTH/2 - subtitle_text.get_width()/2, HEIGHT/2 + 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

if __name__ == "__main__":
    main_menu()