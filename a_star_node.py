

class AStarNode:
    def __init__(self, position_x, position_y):
        self.value_g = 0
        self.value_h = 0
        self.value_f = 99999
        self.position_x = position_x
        self.position_y = position_y
        self.visited = False
        self.child_left = None
        self.child_right = None
        self.child_up = None
        self.child_down = None

    def collided(self, position_x, position_y):
        if self.position_x <= position_x < (self.position_x + 16) and \
                self.position_y <= position_y < (self.position_y + 16):
            return True

        return False
