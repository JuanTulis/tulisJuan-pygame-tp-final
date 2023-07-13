import pygame
from pygame.locals import *
from auxiliar import draw_text

class ScreenTop():
    def __init__(self, x, y, health, max_health, points):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, surface, health):
        self.health = health
        
        health_left = self.health / self.max_health
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 1280, 80))
        pygame.draw.rect(surface, (255, 0, 0), (10, 40, 300, 20))
        pygame.draw.rect(surface, (0, 255, 0), (10, 40, 300 * health_left, 20))



        draw_text("player's health", (255, 255, 255), 10, 10, surface)
