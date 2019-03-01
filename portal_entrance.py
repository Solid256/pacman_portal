from game_object import GameObject


class PortalEntrance(GameObject):
    def __init__(self, x, y, portal_type, image1, image2, image3):
        super(PortalEntrance, self).__init__(x, y)

        self.portal_type = portal_type
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3

        self.image_rect = image1.get_rect()

        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)
 