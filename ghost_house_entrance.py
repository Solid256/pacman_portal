from game_object import GameObject

import pygame


class GhostHouseEntrance(GameObject):
    def __init__(self, x, y, sprites):
        """The init function for initializing the default values."""
        super(GhostHouseEntrance, self).__init__(x, y)

        self.sprites = sprites

        self.image = sprites['debug_2.png']

        # The original rect of the original sprite image.
        original_rect = self.image.get_rect()

        self.image_rect = pygame.Rect(x - 8, y - 8, original_rect.width, original_rect.height)

        # The collision rect.
        self.collision_rect = pygame.Rect(x, y - 8, 2, 16)
