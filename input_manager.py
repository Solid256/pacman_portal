import pygame


class InputManager:
    def __init__(self, game_system):
        """The init function for initializing the default values."""
        self.pressed_up = False
        self.pressed_down = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_q = False
        self.pressed_z = False
        self.pressed_x = False
        self.mouse_button_pressed = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.game_system = game_system

    def check_events(self):
        """Respond to keypress and keyrelease events."""
        self.mouse_button_pressed = False
        for event in pygame.event.get():

            # The quit, keydown and keyup events.
            if event.type == pygame.QUIT:
                self.game_system.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.pressed_right = True
                elif event.key == pygame.K_LEFT:
                    self.pressed_left = True
                elif event.key == pygame.K_UP:
                    self.pressed_up = True
                elif event.key == pygame.K_DOWN:
                    self.pressed_down = True
                elif event.key == pygame.K_q:
                    self.pressed_q = True
                elif event.key == pygame.K_z:
                    self.pressed_z = True
                elif event.key == pygame.K_x:
                    self.pressed_x = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.pressed_right = False
                elif event.key == pygame.K_LEFT:
                    self.pressed_left = False
                elif event.key == pygame.K_UP:
                    self.pressed_up = False
                elif event.key == pygame.K_DOWN:
                    self.pressed_down = False
                elif event.key == pygame.K_q:
                    self.pressed_q = False
                elif event.key == pygame.K_z:
                    self.pressed_z = False
                elif event.key == pygame.K_x:
                    self.pressed_x = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_pressed = True

        # Get the mouse location.
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
