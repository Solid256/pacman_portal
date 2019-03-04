from game_object import GameObject
import pygame


class PortalShot(GameObject):
    def __init__(self, x, y, portal_type, image1, direction):
        """The init function for initializing the default values."""
        super(PortalShot, self).__init__(x, y)

        self.portal_type = portal_type
        # The direction the portal shot is facing.
        # 1 - left.
        # 2 - right.
        # 3 - up.
        # 4 - down.
        self.direction = direction

        self.angle = 180

        if self.direction == 1:
            self.angle = 0
        elif self.direction == 2:
            self.angle = 90
        elif self.direction == 3:
            self.angle = 270

        self.image = image1
        self.image_rect = self.image.get_rect()

        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        self.speed = 8.0

    def update_obj(self):
        if self.angle == 0:
            self.position_x += self.speed
        elif self.angle == 90:
            self.position_y -= self.speed
        elif self.angle == 180:
            self.position_x -= self.speed
        else:
            self.position_y += self.speed

        if self.position_x < 0 or self.position_x > 500:
            self.marked_for_deletion = True

        self.collision_rect.centerx = self.position_x
        self.collision_rect.centery = self.position_y
