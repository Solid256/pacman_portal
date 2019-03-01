from game_object import GameObject
import pygame


class PortalShot(GameObject):
    def __init__(self, x, y, portal_type, image1, angle):
        super(GameObject, self).__init__(x, y)

        self.portal_type = portal_type
        self.angle = angle

        self.image = image1
        self.image_rect = self.image.get_rect()

        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)
