from game_object import GameObject


class Button(GameObject):
    def __init__(self, x, y, button_type, text, text_color, highlight_color, font, input_manager):
        """The init function for initializing the default values."""
        super(Button, self).__init__(x, y)

        # Checks if the mouse is hovering over the button.
        self.hovered = False

        # The type of button being pressed.
        # 0 - Play button.
        # 1 - High score button.
        # 2 - Back button.
        self.button_type = button_type

        # The text for the button.
        self.text = text

        # The color of the text.
        self.text_color = text_color

        # The highlight color of the text.
        self.highlight_color = highlight_color

        # The font of the text.
        self.font = font

        # The input manager for checking if the button was pressed.
        self.input_manager = input_manager

        # The image for the text box.
        self.image = self.font.render(self.text, True, self.text_color)

        # The image rect for the text box.
        self.image_rect = self.image.get_rect()

    def check_was_hovered(self):
        """Checks if the mouse is hovering over the button."""

        # Checks if the mouse is hovering over the button using a point collision.
        button_hovered = self.image_rect.collidepoint(self.input_manager.mouse_x, self.input_manager.mouse_y)

        # Choose which text color to use.
        if self.hovered and not button_hovered:
            self.image = self.font.render(self.text, True, self.text_color)
            self.image_rect = self.image.get_rect()
            self.hovered = False
        elif not self.hovered and button_hovered:
            self.image = self.font.render(self.text, True, self.highlight_color)
            self.image_rect = self.image.get_rect()
            self.hovered = True

    def check_was_clicked(self):
        """Checks if the mouse is clicking the button."""
        # Check if the button was clicked.
        button_clicked = self.image_rect.collidepoint(self.input_manager.mouse_x, self.input_manager.mouse_y)

        return button_clicked
