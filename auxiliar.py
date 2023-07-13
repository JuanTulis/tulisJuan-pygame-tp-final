import pygame
from config import *

def create_animation_frame_list(frames, char_type, animation, scale):
    frame_list = []
    
    for i in range(frames):
        sprite = pygame.image.load(f'images/entities/{char_type}/{animation}/{i}.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))
        frame_list.append(sprite)
    
    return frame_list

def load_image(route):
    pass
    

def draw_bg(surface):
    surface.fill((0, 0, 120))

def draw_text(text, text_col, x, y, screen):
    font = pygame.font.SysFont('Arial', 20)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def damage_calculator(char_type):
    
    if char_type == 'mewtwo':
        ball = 'shadowball'
        damage = 10
    
    elif char_type == 'novice_male' or char_type == 'novice_female':
        ball = 'pokeball'
        damage = 2
    
    elif char_type == 'ace_male' or char_type == 'ace_female':
        ball = 'greatball'
        damage = 5
    
    elif char_type == 'veteran_male' or char_type == 'veteran_female':
        ball = 'ultraball'
        damage = 7
    
    elif char_type == 'giovanni':
        ball = 'masterball'
        damage = 10
    return ball, damage
    