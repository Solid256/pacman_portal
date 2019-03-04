

class AStarNode:
    def __init__(self, position_x, position_y):
        """The init function for initializing the default values."""

        # Checks if the node was visited by a ghost.
        self.visited = False

        # The manhattan distances.
        self.value_g = 0
        self.value_h = 0
        self.value_f = 99999

        # The position of the object.
        self.position_x = position_x
        self.position_y = position_y

        # The four children of the node.
        self.child_left = None
        self.child_right = None
        self.child_up = None
        self.child_down = None

    def collided(self, position_x, position_y):
        """Checks if the node was collided with."""
        if self.position_x <= position_x < (self.position_x + 16) and \
                self.position_y <= position_y < (self.position_y + 16):
            return True

        return False
