import pygame
import random
import time
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
COMMET_WIDTH, COMMET_HEIGHT = 5, 15
PLAYER_VEL = 10
COMMET_VEL = 3
FONT = pygame.font.SysFont("comicsans", 35)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# BG = pygame.transform.scale(pygame.image.load("space-bg.jpg"), (WIDTH, HEIGHT))
BG = (pygame.image.load("space-bg.jpg"))
pygame.display.set_caption("Space Invaders")


def draw(player, elapsed_time, commets):
    ''' Draws a bg image in the window
    '''
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (WIDTH-(time_text.get_width()+15), 15))
    # WIN.blit(time_text, (15, 15))
    pygame.draw.rect(WIN, (50, 255, 255), player)

    for commet in commets:
        pygame.draw.rect(WIN, (255, 255, 255), commet)
    pygame.display.update()

def main():
    run = True
    player = pygame.Rect((WIDTH-PLAYER_WIDTH)//2, (HEIGHT - PLAYER_HEIGHT), 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0


    new_commet_counter = 0 
    commet_inc_time = 2000

    commets = []
    hit = False

    while run:
        new_commet_counter += clock.tick(60)
        elapsed_time = time.time() - start_time

        if new_commet_counter > commet_inc_time:
            for _ in range(3):
                commet_x = random.randint(0, WIDTH - COMMET_WIDTH)
                commet = pygame.Rect(commet_x, -COMMET_WIDTH, COMMET_WIDTH, COMMET_HEIGHT)
                commets.append(commet)

            commet_inc_time = max(200, commet_inc_time - 200)    
            new_commet_counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH < WIDTH:
            player.x += PLAYER_VEL

        for commet in commets[:]:
            commet.y += COMMET_VEL
            if commet.y > HEIGHT:
                commets.remove(commet)
            elif commet.y + commet.height >= player.y and commet.colliderect(player):
                commets.remove(commet)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "White")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        
        draw(player, elapsed_time, commets)

    pygame.quit()

if __name__ == "__main__":
    main()