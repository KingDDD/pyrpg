import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Transition:
    """
    This class plays a white to black transition to darken the screen. Do
    whatever shenanigans you dont want the player to see behind this.
    """
    def __init__(self, reset, player):

        # setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.change_map = reset
        self.player = player

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play_travel(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.change_map()
        if self.color > 255:
            self.color = 255
            self.player.travel = False
            self.speed = -2

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

    def play_sleep(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
