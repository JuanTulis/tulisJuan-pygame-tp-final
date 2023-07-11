import pygame
from config import *

coin = pygame.image.load('images/items/coin.png')
amulet = pygame.image.load('images/items/amulet.png')


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = pygame.image.load('images/items/coin.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, entity, screen_scroll):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, entity):
            if self.item_type == 'coin':
                entity.health -= 20
            elif self.item_type == 'amulet':
                pass
            self.kill()
            


item_box_group = pygame.sprite.Group()

item_box = ItemBox(250, 250, 'coin')
item_box_group.add(item_box)