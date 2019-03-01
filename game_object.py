from pygame.sprite import Sprite


class GameObject(Sprite):
    def __init__(self, x, y):
        super(GameObject, self).__init__()

        self.position_x = float(x)
        self.position_y = float(y)
        self.image_rect = None
        self.sprites = None
        self.marked_for_deletion = False

    def update_rect(self):
        self.image_rect.centerx = int(self.position_x)
        self.image_rect.centery = int(self.position_y)
