import pygame
from pygame.locals import *
from pygame import mixer
from config import *
from entities import *
from stages import *
from projectiles import *
from items import *
from auxiliar import draw_text, draw_bg
from menus import *

pygame.init()
mixer.init()

# Crea la ventana principal
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('holis')

clock = pygame.time.Clock()

flag_screen = 'main_menu'
flag_cargado = False
flag_level_complete = False
world = World()

jump_fx = pygame.mixer.Sound('audio/jump.mp3')
jump_fx.set_volume(0.1)
shoot_fx = pygame.mixer.Sound('audio/shoot.mp3')
shoot_fx.set_volume(0.1)
game_over_fx = pygame.mixer.Sound('audio/game_over.mp3')
game_over_fx.set_volume(0.5)

run = True
while run:
    clock.tick(FPS)
    
    if flag_screen != 'level_1' and flag_screen != 'level_2' and flag_screen != 'level_3':
        flag_screen = menu_flag_changer(flag_screen, screen)
    
    if (flag_screen == 'main_menu' or flag_screen == 'level_select_menu') and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('audio/menus.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(1, 0, 0)
    
    elif flag_screen == 'level_1' or flag_screen == 'level_2' or flag_screen == 'level_3':
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('audio/playing.mp3')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(1, 0, 0)
    
    if flag_screen == 'level_1':
        if flag_cargado == False:
            data = load_level(1)
            player, enemy_group = world.process_data(data)
            flag_cargado = True
            pygame.mixer.music.stop()
        if player.health < 1:
            player, enemy_group = reset_level(player, enemy_group, world, 1)
            game_over_fx.play()
        flag_screen = play_level(flag_screen, screen, world, player)
    
    if flag_screen == 'level_2':
        if flag_cargado == False:
            data = load_level(2)
            player, enemy_group = world.process_data(data)
            flag_cargado = True
            pygame.mixer.music.stop()
        if player.health < 1:
            player, enemy_group = reset_level(player, enemy_group, world, 2)
            game_over_fx.play()
        play_level(flag_screen, screen, world, player)
    
    if flag_screen == 'level_3':
        if flag_cargado == False:
            data = load_level(3)
            player, enemy_group = world.process_data(data)
            flag_cargado = True
            pygame.mixer.music.stop()
        if player.health < 1:
            player, enemy_group = reset_level(player, enemy_group, world, 3)
            game_over_fx.play()
        play_level(flag_screen, screen, world, player)
    
    elif flag_screen == 'exit_game':
        run = False    
    
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
                if player.in_air == False:
                    jump_fx.play()
            if event.key == pygame.K_SPACE:
                player.shooting = True
                if player.shoot_cooldown == 0:    
                    shoot_fx.play()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_w:
                player.jumping = False
            if event.key == pygame.K_SPACE:
                player.shooting = False
    
    print('main.py {0}'.format(flag_screen))
    
    pygame.display.update()

pygame.quit()
