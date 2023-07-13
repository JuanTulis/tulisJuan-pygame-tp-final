import pygame
import random
from pygame.locals import *
from config import *
from projectiles import *
from auxiliar import create_animation_frame_list
from items import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        
        # Declara el tipo de personaje
        self.char_type = char_type
        flagJugador = False
        
        # Si el personaje es Mewtwo, se lo detecta como jugador
        if char_type == 'mewtwo':
            flagJugador = True
        
        # Estados de acción del personaje
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.in_air = False
        self.shooting = False
        
        # Características del personaje
        self.alive = True
        self.speed_x = speed
        self.speed_y = 0
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        
        # Declara la derecha como la posición inicial
        self.direction = 1
        self.flip = False        
        
        # AI
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 400, 10)
        
        # Variables de animación del personaje
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Agrega las animaciones a animation_list

        self.animation_list.append(create_animation_frame_list(1, char_type, 'Idle', scale))
        self.animation_list.append(create_animation_frame_list(4, char_type, 'Walking', scale))
        self.animation_list.append(create_animation_frame_list(1, char_type, 'Death', scale))
        
        # Si es un jugador, se agrega la animación de saltar
        if flagJugador:
            self.animation_list.append(create_animation_frame_list(1, char_type, 'Jumping', scale))
        
        self.sprite_actual = self.animation_list[self.action][self.frame_index]
        
        # Crea el rectángulo de la entidad
        self.rect = self.sprite_actual.get_rect()
        self.rect.center = (x, y)
        
        self.width = self.sprite_actual.get_width()
        self.height = self.sprite_actual.get_height()
    
    def general_update(self, screen, lista):
        self.update_animation()
        self.update_cooldown()
        self.move(lista, self.moving_left, self.moving_right)
        self.check_for_action()
        
        if self.shooting == True:
            self.shoot()
        
        self.check_if_alive()
        self.draw(screen)

    def update_animation(self):
        """
        \nQué hace:
        - Toma el índice de acciones y el índice de frames de una animación para
        pasar al siguiente frame cuando se alcance una cantidad de tiempo deseada
        \nParámetros:
        - self.
        """
        # Se declara el sprite actual
        self.sprite_actual = self.animation_list[self.action][self.frame_index]
        
        # Si el tiempo transcurrido es mayor al cooldown entre frames...
        if pygame.time.get_ticks() - self.update_time > ENTITY_ANIMATION_COOLDOWN:
            # ...se actualiza el tiempo transcurrido y se pasa al siguiente frame
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        # Si se llega al último frame de la animación, vuelve a empezar
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
  
    def update_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, lista, moving_left, moving_right):
        delta_x = 0
        delta_y = 0
        screen_scroll = 0
        
        if self.alive:
            if moving_left:
                delta_x = -self.speed_x
                self.flip = True
                self.direction = -1
            
            if moving_right:
                delta_x = self.speed_x
                self.flip = False
                self.direction = 1
            
            if self.jumping == True and self.in_air == False:
                self.speed_y = -4
                self.jump = False
                self.in_air = True
        
        self.speed_y += GRAVITY
        if self.speed_y > 10:
            self.speed_y = 10
        delta_y += self.speed_y
        
        for tile in lista:
            if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height):
                delta_x = 0
                
                # ia check to turn around
                if self.char_type != 'mewtwo':
                    self.direction *= -1
                    self.move_counter = 0
                
            if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                if self.speed_y < 0:
                    self.speed_y = 0
                    delta_y = tile[1].bottom - self.rect.top
                elif self.speed_y >= 0:
                    self.speed_y = 0
                    self.in_air = False
                    delta_y = tile[1].top - self.rect.bottom
        
        self.rect.x += delta_x
        self.rect.y += delta_y
        
        
        
        if self.char_type == 'mewtwo':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
                self.rect.x -= delta_x
                screen_scroll = -delta_x
        
        return screen_scroll

    def check_for_action(self):
        if self.alive:        
            if self.in_air:
                self.update_action(3) # Saltar
        
            elif self.moving_left or self.moving_right:
                self.update_action(1) # Caminar
            
            else:
                self.update_action(0) # Estar quieto
        
        else:
            self.update_action(2) # Morir
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.alive:
            self.shoot_cooldown = COOLDOWN_PROJECTILE_PLAYER
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * self.direction) * 1,
                            self.rect.centery, self.direction, self.char_type)
            projectile_group.add(bullet)
    
    def ai(self, lista, player, screen_scroll):
        if self.alive and player.alive:
            
            if self.idling == False and random.randint(1, 800) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 128
            
            # check if the ai is near the player
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot()
            
            else:           
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(lista, ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    # update vision
                    self.vision.center = (self.rect.centerx + self.vision[2] // 2 * self.direction, self.rect.centery)
                                
                    if self.move_counter > 128:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter < 1:
                        self.idling = False
        
        self.rect.x += screen_scroll
        
    def check_if_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed_x = 0
            
            self.alive = False
            self.update_action(2)            
 
    def update_action(self, new_action:int):
        """
        \nQué hace:
        - Actualiza el estado del personaje, ya sea que esté quieto, moviéndose,
        haya muerto o esté en el aire.
        \nParámetros:
        - self.
        - new_action: el índice de la nueva acción. Puede ser 0 (estar quieto),
        1 (moverse), 2 (morir) o 3 (en el aire)
        """
        # Si la acción nueva es diferente a la vieja, se cambia la acción vieja
        if new_action != self.action:
            self.action = new_action
            
            # También vuelve a empezar la animación y actualiza el tiempo
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        """
        \nQué hace:
        - Muestra al personaje en pantalla
        \nParámetros:
        - self.
        - screen: la pantalla en la que se mostrará.
        """
        screen.blit(pygame.transform.flip(self.sprite_actual, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)