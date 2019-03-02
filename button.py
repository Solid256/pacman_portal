from game_object import GameObject


class Button(GameObject):
    def __init__(self, x, y, type, text, text_color, highlight_color, font, input_manager):
        super(Button, self).__init__(x, y)

        self.type = type
        self.text = text
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.font = font
        self.input_manager = input_manager
        self.hovered = False

        self.image = self.font.render(self.text, True, self.text_color)
        self.image_rect = self.image.get_rect()

    def check_was_hovered(self):
        button_hovered = self.image_rect.collidepoint(self.input_manager.mouse_x, self.input_manager.mouse_y)

        if self.hovered and not button_hovered:
            self.image = self.font.render(self.text, True, self.text_color)
            self.image_rect = self.image.get_rect()
            self.hovered = False
        elif not self.hovered and button_hovered:
            self.image = self.font.render(self.text, True, self.highlight_color)
            self.image_rect = self.image.get_rect()
            self.hovered = True

    def check_was_clicked(self):
        # Check if the button was clicked.
        button_clicked = self.image_rect.collidepoint(self.input_manager.mouse_x, self.input_manager.mouse_y)

        return button_clicked
