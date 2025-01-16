import pygame

WIDTH, HEIGHT = 1000, 700

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 60
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

pygame.display.set_caption("Galaxy Fighters")

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT 
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20: # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT 
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 20: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

def draw(yellow, red, yellow_bullets, red_bullets):
    WIN.fill(("cyan")) # diplay bg color
    pygame.draw.rect(WIN, ("black"), BORDER)  # seperating the two halves
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 3, yellow.y + yellow.height//2 - 2.5, 10, 5)
                    yellow_bullets.append(bullet)
                    


                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + 3, red.y + red.height//2 - 2.5, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw(yellow, red, yellow_bullets, red_bullets) 
        

    pygame.quit()

if __name__ == "__main__":
    main()