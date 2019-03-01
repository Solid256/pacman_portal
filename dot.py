import pygame

from game_object import GameObject


class Dot(GameObject):
    def __init__(self, x, y, image):
        super(Dot, self).__init__(x, y)

        self.image = image
        self.image_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        self.collision_rect = pygame.Rect(x - 1, y - 1, 2, 2)
