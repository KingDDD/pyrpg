"""
This Module contains button related code and functionality
"""
import pygame

class Button:
    """
    This class handles the button drawing and pressing

    :param x: x position to draw button
    :param y: y position to draw button
    :param image: image to draw at provided position
    :param scale: scaling factor for image
    """
    def __init__(self, x, y, image, scale):
        """
        This initializes image size and button clickability
        """
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False


    def draw(self, surface):
        """
        This method draws buttons and registers clicks
        """
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked:
                self.clicked = True
                # pygame.time.wait(400)
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
