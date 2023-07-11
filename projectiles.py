import pygame
from config import *
from auxiliar import damage_calculator

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, char_type):
        pygame.sprite.Sprite.__init__(self)
        
        ball, damage = damage_calculator(char_type)
                
        self.speed = 1
        self.image = pygame.image.load('images/projectiles/{0}.png'.format(ball)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.damage = damage
    
    def update(self, entity, lista):
        self.rect.x += (self.direction * self.speed)
    
        for tile in lista:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        if pygame.sprite.spritecollide(entity, projectile_group, False):
            if entity.alive:
                entity.health -= self.damage
                print(entity.health)
                self.kill()

projectile_group = pygame.sprite.Group()
