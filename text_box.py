from game_object import GameObject


class TextBox(GameObject):
    def __init__(self, x, y, align_bottom_left, text, font, color):
        super(TextBox, self).__init__(x, y)

        self.align_bottom_left = align_bottom_left
        self.__text = text
        self.font = font
        self.color = color
        self.original_x = x
        self.original_y = y
        self.image = None
        self.image_rect = None

        self.set_text(text)

    def set_text(self, text):
        self.__text = text

        self.image = self.font.render(self.__text, True, self.color)
        self.image_rect = self.image.get_rect()

        if self.align_bottom_left:
            self.image_rect.centerx = self.original_x
            self.image_rect.centery = self.original_y
            self.position_x = self.image_rect.right
            self.position_y = self.image_rect.bottom
            self.image_rect.centerx = self.position_x
            self.image_rect.centery = self.position_y

    def get_text(self):
        return self.__text
