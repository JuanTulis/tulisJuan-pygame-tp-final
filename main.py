import pygame
from pygame.locals import *
from config import *
from entities import *
from stages import *
from projectiles import *
from items import *
from auxiliar import draw_text, draw_bg
from menus import *

pygame.init()

# Crea la ventana principal
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('holis')

clock = pygame.time.Clock()

flag_screen = 'main_menu'

flag_locked_1 = False
flag_locked_2 = True
flag_locked_3 = True

# Crea el jugador
world = World()
data = load_level(1)
player, enemy_group, finish_tile_group = world.process_data(data)

run = True
while run:
    clock.tick(FPS)
    
    flag_screen = menu_flag_changer(flag_screen, screen, world, player, finish_tile_group)
    
    flag_locked_1 = False
    flag_locked_2 = check_level_locked(flag_screen, flag_locked_2, screen)
    flag_locked_3 = check_level_locked(flag_screen, flag_locked_2, screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_w:
                player.jumping = True
            if event.key == pygame.K_SPACE:
                player.shooting = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_w:
                player.jumping = False
            if event.key == pygame.K_SPACE:
                player.shooting = False
    
    if flag_screen == 'level_1':
        play_level(flag_screen, screen, world, player, finish_tile_group)
        # Aquí puedes agregar código para actualizar y dibujar el estado del jugador y el mundo después de jugar el nivel
    
    elif flag_screen == 'exit_game':
        run = False
    
    pygame.display.update()

pygame.quit()
