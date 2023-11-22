import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, peach_tree_sprites, interaction, soil_layer):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # hitbox debug flag
        self.debug = False

        # place player above ground but below other objects
        self.z = LAYERS['main']

        # movement attr
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.1, -self.rect.height * 0.5)

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
            }

        # tools
        self.tools = ['axe', 'hoe']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'peach': 0,
            'corn': 0,
            'tomato': 0
        }

        # interaction
        self.tree_sprites = tree_sprites
        self.peach_tree_sprites = peach_tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.travel = False
        self.soil_layer = soil_layer

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
            for tree in self.peach_tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        if self.selected_tool == 'water':
            pass

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                            'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                            'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index=0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # hold tab for hitbox debug
            if keys[pygame.K_TAB]:
                self.debug = True
            if not keys[pygame.K_TAB] and self.debug:
                self.debug = False

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                # stop player movement while tool use
                self.direction = pygame.math.Vector2()
                self.frame_index=0

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                # bound for end out of tools index
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                # stop player movement while seed use
                self.direction = pygame.math.Vector2()
                self.frame_index=0

            # change seed part
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                # bound for end out of tools index
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]

            if keys[pygame.K_RETURN]:
                #takes sprite, group, and do kill arguments
                # if self collide with interact kill?
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        pass
                    if collided_interaction_sprite[0].name == 'Home Door':
                        self.status = 'up_idle'
                        self.travel = True
                    else:
                        self.status = 'up_idle'
                        self.sleep = True

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tools
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:# moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:# moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # normalize vector speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        # round to avoid truncating to the integer floor
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)
