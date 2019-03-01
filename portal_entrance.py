from game_object import GameObject
import pygame


class PortalEntrance(GameObject):
    def __init__(self, x, y, portal_type, direction, image1, image2, image3):
        super(PortalEntrance, self).__init__(x, y)

        self.portal_type = portal_type
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image = self.image1
        self.direction = direction

        self.angle = 180

        if self.direction == 1:
            self.angle = 0
        elif self.direction == 2:
            self.angle = 90
        elif self.direction == 3:
            self.angle = 270

        self.image_rect = image1.get_rect()

        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        self.cur_anim = 0
        self.max_anim = 6

        self.portal_ready = False
        self.in_use = False

    def update_obj(self):

        if not self.portal_ready:
            if self.cur_anim == 2:
                self.image = self.image2
            if self.cur_anim == 4:
                self.image = self.image3

            if self.cur_anim >= self.max_anim:
                self.cur_anim = 0
                self.portal_ready = True
            else:
                self.cur_anim += 1

