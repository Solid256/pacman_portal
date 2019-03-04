import pygame
from game_object import GameObject


class BackgroundTile(GameObject):
    def __init__(self, tile_image, white_tile_image, x, y, has_collision):
        """The init function for initializing the default values."""
        super(BackgroundTile, self).__init__(x, y)

        # The sprite image.
        self.image = tile_image

        # The tile image.
        self.tile_image = tile_image

        # The white version of the tile image.
        self.white_tile_image = white_tile_image

        # Checks if the background tile has collision.
        self.has_collision = has_collision

        # The collision rect for colliding with objects.
        self.collision_rect = None

        # If the there isn't an image, create the image rect for the image rendering.
        if self.image is not None:
            # The original rect of the original sprite image.
            original_rect = self.image.get_rect()

            # Create the image rect.
            self.image_rect = pygame.Rect(x - 8, y - 8, original_rect.width, original_rect.height)

        # If the background tile
        if self.has_collision:
            self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)
