import pygame
import sys
import random

pygame.init()


WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))


WHITE = (255, 255, 255)
PURPLE = (255,192,203)
RED = (255, 0, 0)


background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume (0.6)
pygame.mixer.music.play(0) 


bird_img = pygame.image.load("bird.png")
bird_rect = bird_img.get_rect()
bird_x = WIDTH // 3
bird_y = HEIGHT // 2
bird_dy = 0

pipe_img = pygame.image.load("pipe.png")
pipe_x = WIDTH
pipe_y = 0
pipe_gap = 155
pipe_speed = 9
pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()

gravity = 1


score = 0
font = pygame.font.Font(None, 36)

def draw():
    win.blit(background_img, (0, 0))
    win.blit(bird_img, (bird_x, bird_y))
    win.blit(pipe_img, (pipe_x, pipe_y))
    win.blit(pipe_img, (pipe_x, pipe_y + pipe_height + pipe_gap))
    score_text = font.render("Score: " + str(score), True, PURPLE)
    win.blit(score_text, (10, 10))
    pygame.display.update()

paused = False
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_dy = -8
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()  # Ïàóçà ìóçûêè
                else:
                    pygame.mixer.music.unpause()  # Ïðîäîëæåíèå ìóçûêè

    if not paused:
        bird_dy += gravity
        bird_y += bird_dy

        pipe_x -= pipe_speed
        if pipe_x <= -pipe_width:
            pipe_x = WIDTH
            pipe_y = random.randint(-pipe_height // 2, 0)
            score += 1

        if bird_y <= 0 or bird_y >= HEIGHT - bird_rect.height:
            paused = True

        bird_rect.topleft = (bird_x, bird_y)
        pipe_rect1 = pygame.Rect(pipe_x, pipe_y, pipe_width, pipe_height)
        pipe_rect2 = pygame.Rect(pipe_x, pipe_y + pipe_height + pipe_gap, pipe_width, pipe_height)
        if bird_rect.colliderect(pipe_rect1) or bird_rect.colliderect(pipe_rect2):
            score_text = font.render("ez win", True, RED)
            win.blit(score_text, (130, 20))
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(2)  
            pygame.quit()
            sys.exit()

        if paused:
            pygame.mixer.music.stop()  

        draw()

    clock.tick(30)
