import pygame

from game_object import GameObject


class Dot(GameObject):
    def __init__(self, x, y, image):
        """The init function for initializing the default values."""
        super(Dot, self).__init__(x, y)

        # The image of the dot.
        self.image = image

        # The image rect of the dot.
        self.image_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        # The collision rect of the dot.
        self.collision_rect = pygame.Rect(x - 1, y - 1, 2, 2)
