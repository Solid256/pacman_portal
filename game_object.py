from pygame.sprite import Sprite


class GameObject(Sprite):
    def __init__(self, x, y):
        """The init function for initializing the default values."""
        super(GameObject, self).__init__()

        # Checks if the object is marked for deletion, so it gets deleted at the end of every game loop.
        self.marked_for_deletion = False

        # The position x of the game object.
        self.position_x = float(x)

        # The position y of the game object.
        self.position_y = float(y)

        # The angle of the game object for rotating.
        self.angle = 0

        # The image rect of the sprite image.
        self.image_rect = None

        # The sprites of the game object.
        self.sprites = None

    def update_rect(self):
        """Updates the image rect for rendering purposes."""

        # Update the image rect's center x.
        self.image_rect.centerx = int(self.position_x)

        # Update the image rect's center y.
        self.image_rect.centery = int(self.position_y)
