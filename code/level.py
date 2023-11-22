import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Foliage, Tree, Rock, Bush, Building, Fence, Interaction, PeachTree
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.peach_tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites)

        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)


    def setup(self):
        tmx_data = load_pygame('../data/test.tmx')

        # load ground level at settings in LAYERS
        for x, y, surf in tmx_data.get_layer_by_name("Ground").tiles():
            Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    groups = self.all_sprites,
                    z = LAYERS['ground']
                    )

        # Large Rocks
        for obj in tmx_data.get_layer_by_name("Rocks"):
            Rock(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites],
                 z = LAYERS['main']
                 )

        # Small decorative objects with no hitbox or draw priority
        for obj in tmx_data.get_layer_by_name("Foliage"):
            Foliage(
                pos = (obj.x, obj.y),
                surf = obj.image,
                groups = self.all_sprites,
                z = LAYERS["soil"]
                )

        # Large Bushes
        for obj in tmx_data.get_layer_by_name("Bush"):
            Bush(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites],
                 z = LAYERS['main']
                 )

        # Apple Trees
        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                 name = obj.name,
                 player_add = self.player_add
                 )

        # Peach Trees
        for obj in tmx_data.get_layer_by_name("PeachTrees"):
            PeachTree(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites, self.peach_tree_sprites],
                 name = obj.name,
                 player_add = self.player_add
                 )

        # Large Buildings with static collision
        for obj in tmx_data.get_layer_by_name("Building"):
            Building(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites],
                 z = LAYERS["main"]
                 )

        # load water level, also animated with a sprite
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water(
                 pos = (x * TILE_SIZE, y * TILE_SIZE),
                 frames = water_frames,
                 groups = [self.all_sprites, self.collision_sprites]
                 )

        # Fence
        for obj in tmx_data.get_layer_by_name("Fence"):
            Fence(
                 pos = (obj.x, obj.y),
                 surf = obj.image,
                 groups = [self.all_sprites, self.collision_sprites],
                 z = LAYERS["main"]
                 )

        # collision tiles
        # for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE),
        #              pygame.Surface((TILE_SIZE, TILE_SIZE)),
        #              self.collision_sprites,
        #              LAYERS['main'])

        # PLAYER
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites,
                    peach_tree_sprites = self.peach_tree_sprites,
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer)

            # sleep
            if obj.name == 'House':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
            # enter house
            if obj.name == 'Home Door':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)


    def player_add(self, item):
        self.player.item_inventory[item] += 1
        print(self.player.item_inventory)

    def reset(self):
        # apples on trees
        for tree in self.tree_sprites.sprites():
            #get rid of hanging apples
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()
        for tree in self.peach_tree_sprites.sprites():
            for peach in tree.peach_sprites.sprites():
                peach.kill()
            # generate new apples
            tree.create_peach()

    def change_map(self):
        self.map_data = load_pygame('../data/test_small.tmx')

    def run(self, dt):
        # black background
        self.display_surface.fill('black')
        # draw sprites in new positions for the next update() call
        self.all_sprites.custom_draw(self.player, self.collision_sprites)
        # update frame with newly drawn sprite positions
        self.all_sprites.update(dt)
        # draw tool/seed overlay
        self.overlay.display()

        # check if player wants to sleep
        if self.player.sleep:
            self.transition.play_sleep()
        if self.player.travel:
            self.transition.play_travel()

class CameraGroup(pygame.sprite.Group):
    """
    Class for drawing sprites to the screen.
    """

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def overlay_debug_boxes(self, player, sprite, collision_sprites, offset_rect):
        """
        Draw object and hitbox rectangles on the screen for debugging.

        :param player: Player object with surface and position properties
        :param sprite: Sprite object with surface and position properties
        :param collision_sprites: Collision objects with position properties
        :param offset_rect: Positional offset to account for map origin
        """

        if sprite in collision_sprites or sprite == player: # == player:
            pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
            hitbox_rect = sprite.hitbox.copy()
            hitbox_rect.center = offset_rect.center
            pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 2)
            target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
            if sprite == player:
                pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)

    def custom_draw(self, player, collision_sprites):
        """
        Draw all sprite surfaces according to their layer level and sorted
        such that sprites on the same layer with greater 'y' coordinate
        are drawn on top of sprites who are higher on screen.

        :param player: Player object with surface and position properties
        :param collision_sprites: Collision objects with position properties
        """

        # make the player the Center point of the Camera
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # draw each layer in order
        for layer in LAYERS.values():
            # sort by lowest Y value first for drawing same layer sprites
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    # if hasattr(sprite, 'offset'):
                    #     offset_rect = sprite.rect.copy().move(sprite.offset)
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # Use this to draw hitbox outlines
                    if player.debug:
                        self.overlay_debug_boxes(player, sprite, collision_sprites, offset_rect)
