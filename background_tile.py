import pygame
from game_object import GameObject


class BackgroundTile(GameObject):
    def __init__(self, tile_image, white_tile_image, x, y, has_collision):
        super(BackgroundTile, self).__init__(x, y)
        self.image = tile_image
        self.tile_image = tile_image
        self.white_tile_image = white_tile_image
        self.has_collision = has_collision
        self.collision_rect = None

        if self.image is not None:
            # The original rect of the original sprite image.
            original_rect = self.image.get_rect()

            self.image_rect = pygame.Rect(x - 8, y - 8, original_rect.width, original_rect.height)

        if self.has_collision:
            self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)
