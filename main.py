
# main.py - FLAPPY BIRD Clone para sa Pygame + APK (Buildozer Ready)
# Touch-friendly para sa Android. Simple, optimized, at full working!

import pygame
import sys
import random
import os

pygame.init()

# Mobile-friendly portrait screen (400x600)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy YOLL - APK Ready")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)  # Sky blue
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Game variables
clock = pygame.time.Clock()
gravity = 0.5
bird_movement = 0
game_active = False
score = 0
highscore = 0
pipes = []
pipe_height = [200, 250, 300, 350, 400, 450]  # Random pipe gaps
pipe_speed = 3
pipe_frequency = 1200  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Bird
bird_x = 50
bird_y = 300
bird_size = 25
bird_velocity = 0

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = int(height)
        self.top = 0
        self.bottom = SCREEN_HEIGHT - self.height - 150  # Gap size
        self.passed = False
        self.width = 60
        self.gap = 150

    def draw_pipe(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.top, self.width, self.height))
        # Bottom pipe  
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom, self.width, self.bottom))
        # Gap outline
        pygame.draw.rect(screen, WHITE, (self.x - 5, self.height, self.width + 10, self.gap), 3)

    def update(self):
        self.x -= pipe_speed

    def destroy(self):
        pipes.remove(self)

    def collide(self, bird_rect):
        if bird_rect.colliderect(self.x, self.height, self.width, self.gap) or \
           bird_rect.colliderect(self.x, 0, self.width, self.height) or \
           bird_rect.colliderect(self.x, SCREEN_HEIGHT - self.bottom, self.width, self.bottom):
            return True
        return False

def draw_bird():
    # Simple bird (circle + wing)
    pygame.draw.circle(screen, YELLOW, (int(bird_x), int(bird_y)), bird_size)
    pygame.draw.circle(screen, BLACK, (int(bird_x), int(bird_y)), bird_size, 2)
    # Wing
    pygame.draw.ellipse(screen, (255, 165, 0), (bird_x - 15, bird_y - 5, 20, 10))

def handle_input():
    global bird_movement, game_active
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            if not game_active:
                game_active = True
                pipes.clear()
                bird_y = 300
                bird_movement = 0
                score = 0
            else:
                bird_movement = -10  # Jump!

def update_bird():
    global bird_y, bird_movement, game_active
    if game_active:
        bird_movement += gravity
        bird_y += bird_movement
        # Ground/ceiling collision
        if bird_y > SCREEN_HEIGHT - 50 or bird_y < 0:
            game_active = False

def update_pipes():
    global last_pipe
    time_now = pygame.time.get_ticks()
    # Create new pipe
    if time_now - last_pipe > pipe_frequency:
        pipe_height_chosen = random.choice(pipe_height)
        pipes.append(Pipe(SCREEN_WIDTH, pipe_height_chosen))
        last_pipe = time_now
    
    # Update existing pipes
    for pipe in pipes[:]:
        pipe.update()
        
        # Score when passed
        if pipe.x + pipe.width < bird_x and not pipe.passed:
            pipe.passed = True
            global score
            score += 1
        
        # Remove off-screen pipes
        if pipe.x < -pipe.width:
            pipe.destroy()

def check_collisions():
    global game_active
    if game_active:
        bird_rect = pygame.Rect(bird_x - bird_size, bird_y - bird_size, bird_size * 2, bird_size * 2)
        for pipe in pipes:
            if pipe.collide(bird_rect):
                game_active = False
                global highscore
                if score > highscore:
                    highscore = score

def draw_score():
    score_text = font_medium.render(str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 50))
    screen.blit(score_text, score_rect)

def draw_menu():
    global highscore
    screen.fill(BLUE)
    
    # Title
    title_text = font_large.render("FLAPPY YOLL", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
    screen.blit(title_text, title_rect)
    
    # High Score
    hs_text = font_medium.render(f"High Score: {highscore}", True, WHITE)
    hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH//2, 250))
    screen.blit(hs_text, hs_rect)
    
    # Instructions
    inst1 = font_small.render("Tap to flap!", True, WHITE)
    inst2 = font_small.render("Avoid pipes!", True, WHITE)
    screen.blit(inst1, (SCREEN_WIDTH//2 - 80, 350))
    screen.blit(inst2, (SCREEN_WIDTH//2 - 80, 380))
    
    # Start button effect
    pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH//2, 480, 60))
    start_text = font_small.render("TAP", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH//2 - 20, 465))

# MAIN GAME LOOP
running = True
while running:
    handle_input()
    
    screen.fill(BLUE)
    
    if game_active:
        update_bird()
        update_pipes()
        check_collisions()
        draw_bird()
        draw_score()
        for pipe in pipes:
            pipe.draw_pipe()
    else:
        draw_menu()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
