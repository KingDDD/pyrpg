import pygame
from settings import *
from random import randint, choice
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.75, -self.rect.height * 0.75)

class Interaction(Generic):
    #invisible
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

class Rock(Generic):
    def __init__(self, pos, surf, groups, z = LAYERS['soil']):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.3, -self.rect.height * 0.7)

class Water(Generic):
    def __init__(self, pos, frames, groups):
        #animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(
            pos = pos,
            surf = self.frames[self.frame_index],
            groups = groups,
            z = LAYERS['water anim']
            )
        self.hitbox = self.rect.copy() \
        .inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)

    def animate(self, dt):
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Foliage(Generic):
    # Sprite class with no hitbox
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)

class Bush(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)

        # offset bush hitbox for correct depth placement per draw
        self.offset = pygame.math.Vector2(0,20)
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.5,-self.rect.height * 0.9) \
            .move(self.offset)

class Building(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)
        self.offset = pygame.math.Vector2(0,20)
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.45, -self.rect.height * 0.8) \
            .move(self.offset)

class Fence(Generic):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(pos, surf, groups, z)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.4, -self.rect.height * 0.7)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(
        self, pos, surf, groups, name,
        player_add, z = LAYERS["main"]
        ):
        super().__init__(pos, surf, groups, z)
        self.offset = pygame.math.Vector2()
        self.hitbox = self.rect.copy() \
            .inflate(-self.rect.width * 0.6, -self.rect.height * 0.45)

        # tree attributes
        self.health = 5
        self.alive = True
        if name is not None:
            stump = 'ash' if name == 'Apple' else 'birch'
        else:
            stump = 'birch'
        stump_path = f"../graphics/stumps/{stump}.png"
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer  = Timer(200)

        # apples
        self.apple_surf = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        # damaging tree
        self.health -= 1
        # remove apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos = random_apple.rect.topleft,
                surf = random_apple.image,
                groups = self.groups()[0],
                z = LAYERS['fruit'])

            self.player_add('apple')
            random_apple.kill()

    def check_tree_death(self):
        if self.health <= 0:
            Particle(
                pos = self.rect.topleft,
                surf = self.image,
                groups = self.groups()[0],
                z = LAYERS['fruit'],
                duration = 300)

            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.offset = pygame.math.Vector2(0,20)
            self.hitbox = self.rect.copy() \
                .inflate(-self.rect.width * 0.6, -self.rect.height * 0.9) \
                .move(self.offset)

            self.alive = False
            self.player_add('wood')

    def update(self, dt):
        if self.alive:
            self.check_tree_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                        pos = (x, y),
                        surf = self.apple_surf,
                        groups = [self.apple_sprites, self.groups()[0]],
                        z = LAYERS["fruit"])
