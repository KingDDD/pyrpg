import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Mushroom, Tree, Invisible
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()

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

        # load house level
        for x, y, surf in tmx_data.get_layer_by_name("house").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE),
                     surf,
                     self.all_sprites,
                     LAYERS['house top']
                     )

        # load rocks level
        for x, y, surf in tmx_data.get_layer_by_name("rocks").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE),
                     surf,
                     self.all_sprites,
                     LAYERS['ground']
                     )

        # # load trees level
        # for x, y, surf in tmx_data.get_layer_by_name("trees").tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE),
        #              surf,
        #              self.all_sprites,
        #              LAYERS['trees']
        #              )


        # load water level, also animated with a sprite
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name("water").tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE),
                     water_frames,
                     self.all_sprites,
                     )

        # load what will be interactable decoration
        for obj in tmx_data.get_layer_by_name("Decoration"):
            Mushroom((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # load interactable tree sprites. mechanics not implemented yet
        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                 name = obj.name,
                 player_add = self.player_add)

        # collision tiles
        # for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE),
        #              pygame.Surface((TILE_SIZE, TILE_SIZE)),
        #              self.collision_sprites,
        #              LAYERS['main'])

        for x, y, surf in tmx_data.get_layer_by_name("Collision").tiles():
            Invisible((x * TILE_SIZE, y * TILE_SIZE),
                      pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)

        # PLAYER
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                                     pos = (obj.x, obj.y),
                                     group = self.all_sprites,
                                     collision_sprites = self.collision_sprites,
                                     tree_sprites = self.tree_sprites)


    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player, self.collision_sprites)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, collision_sprites):
        # make the player the Center point of the Camera
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # draw each layer in order
        for layer in LAYERS.values():
            # sort by lowest Y value first for drawing correctly
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # analyze positions
                    if sprite in collision_sprites or sprite == player: # == player:
                        pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
                        hitbox_rect = sprite.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 2)
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        if sprite == player:
                            pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)
