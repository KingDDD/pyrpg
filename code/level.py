import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('../data/level1.tmx')

        # load ground level at settings in LAYERS
        for x, y, surf in tmx_data.get_layer_by_name("base_ground_layer").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE),
                     surf,
                     self.all_sprites,
                     LAYERS['ground']
                     )

        for x, y, surf in tmx_data.get_layer_by_name("house").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE),
                     surf,
                     self.all_sprites,
                     LAYERS['house top']
                     )
                     
        self.player = Player((640, 360), self.all_sprites)
        # Generic(
        #     pos = (0,0),
        #     surf = pygame.image.load('../data/level1.png').convert_alpha(),
        #     groups = self.all_sprites,
        #     z = LAYERS['ground']
        #     )

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # make the player the Center point of the Camera
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        # draw each layer in order
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
