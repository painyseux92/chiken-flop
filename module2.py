import pygame
import time
import random

# Initialisation de pygame
pygame.init()

# Créer l'écran de jeu
width, height = 350, 622
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chicken Flop")

# Framerate
clock = pygame.time.Clock()

# Chargement des images
back_img = pygame.image.load("fond.jpg")
floor_img = pygame.image.load("route.png")
floor_x = 0
pipe_img = pygame.image.load("tuyaux.png")
bird_up = pygame.image.load("bird_up.png")  # Remplacez par l'image réelle de votre oiseau
bird_down = pygame.image.load("bird_down.png")  # Remplacez par l'image réelle de votre oiseau
bird_mid = pygame.image.load("bird_mid.png")  # Remplacez par l'image réelle de votre oiseau
birds = [bird_up, bird_mid, bird_down]
pipe_height = [400, 350, 533, 490]  # Hauteurs possibles des tuyaux

# Variables liées au jeu
bird_index = 0
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(67, height // 2))
bird_movement = 0
gravity = 0.17
pipes = []
score = 0
game_over = False
score_time = True

# Fonction pour dessiner le sol
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))

# Fonction pour créer les tuyaux
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))  # Tuyau du haut
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))  # Tuyau du bas
    return top_pipe, bottom_pipe

# Fonction pour animer les tuyaux
def pipe_animation():
    global game_over
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True

# Fonction principale du jeu
def game_loop():
    global bird_movement, bird_rect, pipes, game_over, score, score_time

    running = True
    while running:
        clock.tick(120)  # Limiter à 120 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = 0
                    bird_movement = -5  # Le mouvement de l'oiseau lorsque l'espace est pressé

                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    pipes = []
                    bird_movement = 0
                    bird_rect = bird_img.get_rect(center=(67, height // 2))
                    score_time = True
                    score = 0

        # Afficher l'arrière-plan
        screen.blit(back_img, (0, 0))

        # Logique de mouvement de l'oiseau
        if not game_over:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)
            if bird_rect.top < 0 or bird_rect.bottom >= 550:
                game_over = True
            screen.blit(rotated_bird, bird_rect)

            # Déplacer et afficher les tuyaux
            pipe_animation()

        # Dessiner les tuyaux et le sol
        if not game_over:
            score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 50))
            pipes.extend(create_pipes())

        draw_floor()

        # Mettre à jour l'écran
        pygame.display.update()

    pygame.quit()

# Lancer le jeu
game_loop()
