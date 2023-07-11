import pygame
import json
from config import TILE_SIZE, TOP_BORDER
from entities import *

def load_level(level_number):
    """
    \nQué hace:
    - Carga los datos de un nivel en base a un archivo .json. Los archivos de
    todos los niveles se encuentran en la carpeta levels
    \nParámetros:
    - level_number: el número del nivel.
    \nDevuelve:
    - Una lista con varias listas dentro, siendo estas últimas las
    filas de tiles del nivel.
    """
    
    # Se crea la variable de la ruta del archivo
    route = 'levels/{0}.json'.format(level_number)
    
    # Se abre el archivo y se guarda el dict "level data"
    with open(route, 'r') as file:
        data = json.load(file)
        data = data['level_data']
    
    return data

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class World():
    def __init__(self):
        # Se crea la lista de las tiles a rellenar
        self.tile_list = []
        
        # Se crean listas de tiles que tengan características similares
        self.tile_end = []
        self.tile_ground = []
        self.tile_decoration = []
        self.tile_player = []
        self.tile_enemy = []
        
    def process_data(self, data):
        # Por cada fila data, se revisa cada columna
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                # Si el valor es distinto a 0, se añade a la lista
                if tile > -1:
                    # Crea una imagen en base al valor de la tile y luego la escala
                    image = pygame.image.load('images/stage/{0}.png'.format(tile)).convert_alpha()
                    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    
                    # Crea el rect de la imagen y lo ubica
                    image_rect = image.get_rect()
                    image_rect.x = x * TILE_SIZE
                    image_rect.y = y * TILE_SIZE + TOP_BORDER
                    
                    # La imagen y el rect se guardan juntos y se añaden a la lista
                    values = (image, image_rect)
                    
                    if tile < 3:
                        self.tile_ground.append(values)
                    elif tile > 2 and tile < 14:
                        self.tile_decoration.append(values)
                    elif tile > 13 and tile < 16:
                        finish_tile = Exit(values[0], x * 32, y *32)
                        finish_tile_group.add(finish_tile)
                    elif tile == 16:
                        player = Entity('mewtwo', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 2, 100)
                    elif tile > 16:
                        if tile == 17:
                            enemy = Entity('novice_male', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 10)
                        if tile == 18:
                            enemy = Entity('novice_female', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 10)
                        if tile == 19:
                            enemy = Entity('ace_male', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 20)
                        if tile == 20:
                            enemy = Entity('ace_female', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 20)
                        if tile == 21:
                            enemy = Entity('veteran_male', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 30)
                        if tile == 22:
                            enemy = Entity('veteran_female', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 30)
                        if tile == 23:
                            enemy = Entity('giovanni', x * TILE_SIZE, (y + 1) * TILE_SIZE + TOP_BORDER, 2, 1, 50)
                        enemy_group.add(enemy)
                    
        return player, enemy_group, finish_tile_group
        
    def draw(self, screen, screen_scroll):
        for tile in self.tile_ground:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

        for tile in self.tile_decoration:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        
enemy_group = pygame.sprite.Group()

finish_tile_group = pygame.sprite.Group()