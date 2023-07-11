import pygame
from pygame.locals import *
from config import *
from projectiles import *

def create_animation_frame_list(frames, char_type, animation, scale):
    frame_list = []
    
    for i in range(frames):
        sprite = pygame.image.load(f'images/entities/{char_type}/{animation}/{i}.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))
        frame_list.append(sprite)
    return frame_list

class Entity(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        
        # Declara el tipo de personaje
        self.char_type = char_type
        
        # Estados del personaje
        self.moving_right = False
        self.moving_left = False
        self.shooting = False
        self.alive = True
                
        # Variable de velocidad 
        self.speed_x = speed
        self.shoot_cooldown = 0
        
        # Declara la derecha como la posición inicial
        self.direction = 1
        self.flip = False        
        
        # Se crean todas las variables
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        self.animation_list.append(create_animation_frame_list(4, char_type, 'Walking', scale))
        self.animation_list.append(create_animation_frame_list(1, char_type, 'Idle', scale))
        self.animation_list.append(create_animation_frame_list(1, char_type, 'Death', scale))
        
        self.sprite_actual = self.animation_list[self.action][self.frame_index]
        
        # Crea el rectángulo de la entidad
        self.rect = self.sprite_actual.get_rect()
        self.rect.center = (x, y)
    
    def update_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self):
        
        delta_x = 0
        delta_y = 0
        
        if self.moving_left:
            delta_x = -self.speed_x
            self.flip = True
            self.direction = -1
        
        if self.moving_right:
            delta_x = self.speed_x
            self.flip = False
            self.direction = 1
        
        if self.jumping == True and self.in_air == False:
            self.speed_y = -10
            self.jump = False
            self.in_air = True
        
        self.speed_y += GRAVITY
        if self.speed_y > 10:
            self.speed_y = 10
        delta_y += self.speed_y
        
        
        if self.rect.bottom + delta_y > 300:
            delta_y = 300 - self.rect.bottom
            self.in_air = False
        
        
        
        self.rect.x += delta_x
        self.rect.y += delta_y
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * self.direction) * 0.6, self.rect.centery, self.direction)
            projectile_group.add(bullet)
    
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
            
    def update_action(self, new_action:int):
        """
        \nQué hace:
        - Actualiza el estado del personaje, ya sea que esté saltando, caminando,
        o esté quieto.
        \nParámetros:
        - self.
        - new_action: el índice de la nueva acción. Puede ser 0 (estar quieto),
        1 (moverse), 2 (saltar) o 3 (morir)
        """
        
        # Si la acción nueva es diferente a la vieja, se cambia la acción vieja
        if new_action != self.action:
            self.action = new_action
            
            # También vuelve a empezar la animación y actualiza el tiempo
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.sprite_actual, self.flip, False), self.rect)