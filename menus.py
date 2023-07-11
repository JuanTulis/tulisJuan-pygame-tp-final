import pygame
from pygame.locals import *
from config import *
from entities import *
from stages import *
from projectiles import *
from items import *
import button

main_menu_level_select_button = button.Button(835, 45, 'main_menu', 'level_select', 1)
main_menu_options_button = button.Button(835, 270, 'main_menu', 'options', 1)
main_menu_exit_button = button.Button(835, 495, 'main_menu', 'exit', 1)

level_select_menu_level_one_button = button.Button(20, 46, 'level_select', 'level_one', 1)
level_select_menu_level_two_button = button.Button(440, 46, 'level_select', 'level_two', 1)
level_select_menu_level_three_button = button.Button(860, 46, 'level_select', 'level_three', 1)
level_select_menu_come_back_button = button.Button(440, 494, 'level_select', 'come_back', 1)

level_select_menu_locked = button.Button(860, 160, 'level_select', 'level_locked', 1)

options_menu_music_button = button.Button(100, 36, 'options', 'music', 1)
options_menu_sound_button = button.Button(100, 252, 'options', 'sound', 1)
options_menu_save_button = button.Button(100, 468, 'options', 'save', 1)

def menu_flag_changer(flag, surface, world, player, finish_group):
    if flag == 'main_menu':
        new_flag = menu_main(flag, surface)
    elif flag == 'level_select':
        new_flag = menu_level_select(flag, surface)
    elif flag == 'options':
        new_flag = menu_options(flag, surface)
    elif flag == 'level_1':
        new_flag = play_level(flag, surface, world, player, finish_group)
    elif flag == 'level_locked':
        new_flag = menu_locked(flag, surface)
    else:
        new_flag = flag
    
    return new_flag

def play_level(flag, surface, world, player, finish_group):
    
    surface.fill((103, 189, 255))
    screen_scroll = player.move(world.tile_ground, player.moving_left, player.moving_right)
    
    world.draw(surface, screen_scroll)
    
    # draw_text(f'chavales {player.health}', (0, 0, 0), 600, 600, surface)
    
    
    player.update_animation()
    player.update_cooldown()
    player.check_for_action()
    if player.shooting == True:
        player.shoot()
    player.check_if_alive()
    player.draw(surface)
    
    for enemy in enemy_group:
        enemy.ai(world.tile_ground, player, screen_scroll)
        enemy.update_animation()
        enemy.update_cooldown()
        enemy.check_for_action()
        if enemy.shooting == True:
            enemy.shoot()
        enemy.check_if_alive()
        enemy.draw(surface)
        
        projectile_group.update(player, world.tile_ground)
        projectile_group.update(enemy, world.tile_ground)
        projectile_group.draw(surface)
        
    for item in item_box_group:
        item.update(player, screen_scroll)
        item_box_group.draw(surface)
    
    if pygame.sprite.spritecollide(player, finish_tile_group, False):
        level_complete = True
    
    return flag

def check_level_locked(flag, flag_second, surface):
    if flag_second == True:
        menu_locked(flag, surface)
    return flag

def menu_main(flag, surface):
    background = pygame.image.load('images/menus/main_menu/background.png').convert_alpha()
    surface.blit(background, (0, 0))
    if main_menu_level_select_button.draw(surface):
        flag = 'level_select'
        menu_level_select(flag, surface)
    if main_menu_options_button.draw(surface):
        flag = 'options'
    if main_menu_exit_button.draw(surface):
        flag = 'exit_game'
    return flag

def menu_level_select(flag, surface):
    background = pygame.image.load('images/menus/level_select/background.png').convert_alpha()
    surface.blit(background, (0, 0))
    if level_select_menu_level_one_button.draw(surface):
        flag = 'level_1'
    if level_select_menu_level_two_button.draw(surface):
        flag = check_level_locked(flag, 'flag_locked_2', surface)
    if level_select_menu_level_three_button.draw(surface):
        flag = 'level_3'    
    if level_select_menu_come_back_button.draw(surface):
        flag = 'main_menu'
    return flag

def menu_locked(flag, surface):
    background = pygame.image.load('images/menus/level_select/background.png').convert_alpha()
    surface.blit(background, (0, 0))
    if level_select_menu_locked.draw(surface):
        flag = 'level_select'
    return flag

def menu_options(flag, surface):
    background = pygame.image.load('images/menus/options/background.png').convert_alpha()
    surface.blit(background, (0, 0))
    flag_music = True
    print(flag_music)
    
    if options_menu_music_button.draw(surface):
        flag_music == False
    if options_menu_sound_button.draw(surface):
        pass
    if options_menu_save_button.draw(surface):
        flag = 'main_menu'
    return flag