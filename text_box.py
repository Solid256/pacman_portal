from game_object import GameObject


class TextBox(GameObject):
    def __init__(self, x, y, text, font, color):
        super(TextBox, self).__init__(x, y)

        self.text = text
        self.font = font
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.image_rect = self.image.get_rect()
