import pygame
import xml.etree.ElementTree as ETree
import struct
from input_manager import InputManager

from background_tile import BackgroundTile
from pacman import Player
from dot import Dot
from pellet import Pellet
from ghost import Ghost
from a_star_node import AStarNode
from ghost_house_entrance import GhostHouseEntrance
from fruit import Fruit
from text_box import TextBox
from portal_shot import PortalShot
from portal_entrance import PortalEntrance
from game_object import GameObject
from button import Button
from sound_manager import SoundManager


class GameSystem:
    def __init__(self):
        """The init function for initializing the default values."""

        # Checks if the game is runnning.
        self.is_running = True

        # Checks if the player got an extra life.
        self.got_extra_life = False

        # The columns in the a star array.
        self.a_star_array_rows = 29

        # The rows in the a star array.
        self.a_star_array_columns = 35

        # The current game mode.
        # 0 - Title Screen.
        # 1 - Gameplay.
        # 2 - Scoreboard.
        self.game_mode = 0

        # The title anim mode.
        # 0 - pacman chased by ghosts.
        # 1 - pacman eats ghosts.
        # 2 - blinky intro.
        # 3 - blinky stop.
        # 4 - pinky intro.
        # 5 - pinky stop.
        # 6 - inky intro.
        # 7 - inky stop.
        # 8 - clyde intro.
        # 9 - clyde stop.
        # 10 - blinky leave.
        # 11 - pinky leave.
        # 12 - inky leave.
        # 13 - clyde leave.
        self.title_anim_mode = 0

        # The number of lives to start with.
        self.lives = 3

        # The ghost max time scatter.
        self.ghost_max_time_scatter = 400

        # The ghost current time scatter.
        self.ghost_cur_time_scatter = self.ghost_max_time_scatter

        # The current level that Pac-Man is on.
        self.cur_level = 0

        # The number of dots Pacman has eaten.
        self.dots_eaten = 0

        # The current score from the current playthrough.
        self.current_score = 0

        # The score needed to get an extra life. It is 10,000, just like in the original Pacman.
        self.extra_life_score = 10000

        # The current anim for the title part 1.
        self.cur_anim_title_1 = 0

        # The max anim for the title part 1.
        self.max_anim_title_1 = 172

        # The current anim for the title pacman and ghost animations.
        self.cur_anim_title_pacman = 0

        # The max anim for the title pacman and ghost animations.
        self.max_anim_title_pacman = 6

        # The current anim for the title part 2.
        self.cur_anim_title_2 = 0

        # The max anim for the title part 2.
        self.max_anim_title_2 = 250

        # The current anim for the title part 3.
        self.cur_anim_title_3 = 0

        # The max anim for the title part 3.
        self.max_anim_title_3 = 63

        # The current anim for the title part 4.
        self.cur_anim_title_4 = 0

        # The max anim for the title part 4.
        self.max_anim_title_4 = 20

        # The current anim for the title part 5.
        self.cur_anim_title_5 = 0

        # The max anim for the title part 5.
        self.max_anim_title_5 = 125

        # The input manager for detecting keyboard and mouse input.
        self.input_manager = InputManager(self)

        # The sound manager for playing the music and sound effects.
        self.sound_manager = SoundManager()

        # The pygame clock for managing the time.
        self.pygame_clock = None

        # The backbuffer being rendered to.
        self.backbuffer = None

        # The player game object. AKA Pac-Man.
        self.game_obj_player = None

        # The fruit game object.
        self.game_obj_fruit = None

        # The ghost house entrance game object.
        self.game_obj_ghost_house_entrance = None

        # The portal shot 1.
        self.portal_shot_1 = None

        # The portal shot 2.
        self.portal_shot_2 = None

        # The portal entrance 1.
        self.portal_entrance_1 = None

        # The portal entrance 2.
        self.portal_entrance_2 = None

        # The Pac-Man title animation.
        self.pacman_title_animation = None

        # The blinky title animation.
        self.blinky_title_animation = None

        # The pinky title animation.
        self.pinky_title_animation = None

        # The inky title animation.
        self.inky_title_animation = None

        # The clyde title animation.
        self.clyde_title_animation = None

        # The power pellet title animation.
        self.power_pellet_title_animation = None

        # The name for blinky for the title animation.
        self.blinky_name = None

        # The name for pinky for the title animation.
        self.pinky_name = None

        # The name for inky for the title animation.
        self.inky_name = None

        # The name for clyde for the title animation.
        self.clyde_name = None

        # The game object tiles. AKA walls.
        self.game_objs_tiles = []

        # The game object dots.
        self.game_objs_dots = []

        # The game object pellets.
        self.game_objs_pellets = []

        # The game object ghosts.
        self.game_objs_ghosts = []

        # The game object text boxes.
        self.game_objs_text_boxes = {}

        # The fonts for rendering the text.
        self.fonts = {}

        # The fruit display for displaying the fruit below the map.
        self.fruit_display = {}

        # The lives display for displaying the lives above the map.
        self.lives_display = []

        # The game object title images.
        self.game_objs_title_images = []

        # The game object buttons.
        self.game_objs_buttons = []

        # The a star array of arrays.
        self.a_star_array = []

        # Create the star array.
        for x in range(0, self.a_star_array_rows):
            self.a_star_array.append([])
            for y in range(0, self.a_star_array_columns):
                self.a_star_array[x].append(None)

        # The list of nodes in the a star graph, extracted from the a star array. It also contain a tuple with the x
        # and y coordinate.
        self.a_star_list = []

        # The list of sprite images.
        self.sprite_images = {}

        # The list of high scores.
        self.high_scores = []

        # Create the high scores.

        # The high score file.
        in_file = open("high_scores.bin", "rb")

        # Load all 20 of the high score.
        for x in range(0, 20):
            # The current high score being loaded.
            cur_score = struct.unpack('i', in_file.read(4))[0]

            # Add the high score to the high score list.
            self.high_scores.append(cur_score)

        # Close the high score file.
        in_file.close()

        # Set up the sound manager and load the sounds.
        self.sound_manager.init()
        self.sound_manager.load_sounds()

        # Set up pygame.
        self.setup_pygame()

        # Load the sprite images.
        self.load_sprite_images()

        # Begin the game.

        # Prep the game menu.
        self.setup_menu()

        # Start the main loop.
        self.main_loop()

    def setup_pygame(self):
        """Sets up the pygame programming module."""
        # Create the pygame module.
        pygame.init()

        # Get the pygame clock.
        self.pygame_clock = pygame.time.Clock()

        # The backbuffer of the game.
        self.backbuffer = pygame.display.set_mode(
            (448, 600))

        # Set the caption for the game window.
        pygame.display.set_caption("Pacman")

        # Load the font files.

        # The small font.
        font1 = pygame.font.Font("fonts/PressStart2P.ttf", 12)
        self.fonts["PressStart2P-small"] = font1

        # The big font.
        font2 = pygame.font.Font("fonts/PressStart2P.ttf", 50)
        self.fonts["PressStart2P-big"] = font2

        # The medium font.
        font3 = pygame.font.Font("fonts/PressStart2P.ttf", 32)
        self.fonts["PressStart2P-medium"] = font3

    def load_sprite_images(self):
        """Use XML to create all the game sprites and store them in a dictionary."""

        # Load the sprite sheet image.
        sprite_sheet = pygame.image.load('images/sprites.png')

        # The e tree node for the sprite images.
        e_tree = ETree.parse("images/sprites.xml")

        # The root node of the e tree.
        root = e_tree.getroot()

        # The sprite info xml objects.
        sprite_infos_xml = root.findall('sprite')

        # Create every individual sprite and load it into the sprite image list.
        for sprite_info_xml in sprite_infos_xml:
            # Load the sprite info attributes

            # The name of the sprite.
            name = ""

            # The x position of the sprite.
            x = 0

            # The y position of the sprite.
            y = 0

            # The width of the sprite.
            w = 0

            # The height of the sprite.
            h = 0

            # Load all of the sprite attributes for the current sprite.
            for sprite_attr in sprite_info_xml.attrib:

                # Check for the different kinds of sprite attributes.
                if sprite_attr == 'n':
                    # The name of the sprite.
                    name = sprite_info_xml.get(sprite_attr)
                elif sprite_attr == 'x':
                    # The x position of the sprite.
                    x = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'y':
                    # The y position of the sprite.
                    y = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'w':
                    # The width of the sprite.
                    w = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'h':
                    # The height of the sprite.
                    h = int(sprite_info_xml.get(sprite_attr))

            # The current image of the sprite in the sprite sheet.
            cur_image = sprite_sheet.subsurface(
                pygame.Rect(x, y, w, h))

            # Add the sprite to the sprite image dictionary.
            self.sprite_images[name] = cur_image

    def setup_menu(self):
        """Sets up the menu for the game."""

        # Clear all the game object title images.
        self.game_objs_title_images.clear()

        # Clear all the game object buttons.
        self.game_objs_buttons.clear()

        # Clear all the game object text boxes.
        self.game_objs_text_boxes.clear()

        # Set the defaults for the title animations.
        self.cur_anim_title_1 = 0
        self.cur_anim_title_pacman = 0
        self.cur_anim_title_2 = 0
        self.cur_anim_title_3 = 0
        self.cur_anim_title_4 = 0
        self.cur_anim_title_5 = 0
        self.title_anim_mode = 0

        # The fonts for the text rendering.
        font1 = self.fonts["PressStart2P-big"]
        font2 = self.fonts["PressStart2P-medium"]
        font3 = self.fonts["PressStart2P-small"]

        # The text box for the Pac-Man title.
        text_1 = TextBox(232, 80, False, "PAC-MAN", font1, (255, 255, 150))
        self.game_objs_text_boxes["title1"] = text_1

        # The text box for the Pac-Man Portal title.
        text_2 = TextBox(232, 130, False, "PORTAL", font1, (255, 255, 150))
        self.game_objs_text_boxes["title2"] = text_2

        # The text box for the directions part 1.
        text_3 = TextBox(232, 530, False, "USE THE ARROW KEYS TO MOVE AND", font3, (0, 255, 255))
        self.game_objs_text_boxes["directions1"] = text_3

        # The text box for the directions part 2.
        text_4 = TextBox(232, 550, False, "THE Z AND X KEYS TO FIRE PORTALS.", font3, (0, 255, 255))
        self.game_objs_text_boxes["directions2"] = text_4

        # The text box for the directions part 3.
        text_5 = TextBox(232, 570, False, "TAP ARROW KEYS TO ENTER PORTALS.", font3, (0, 255, 255))
        self.game_objs_text_boxes["directions3"] = text_5

        # The title object portal image.
        o_title = GameObject(152, 130)

        # The image for the portal image.
        o_title.image = self.sprite_images["portal_entrance_2_4.png"]

        # The image rect for the portal image.
        o_title.image_rect = pygame.Rect(152, 130, 128, 128)

        # Add the portal image to the game objects title images list.
        self.game_objs_title_images.append(o_title)

        # The start button for starting the game.
        start_button = Button(232, 400, 0, "START GAME", (100, 100, 100), (200, 200, 200),
                              font2, self.input_manager)
        # Add the start button to the list of buttons.
        self.game_objs_buttons.append(start_button)

        # The high score button for the high scores.
        high_scores_button = Button(232, 460, 1, "HIGH SCORES", (100, 100, 100), (200, 200, 200),
                                    font2, self.input_manager)
        # Add the high score button to the list of buttons.
        self.game_objs_buttons.append(high_scores_button)

        # Create the pacman characters for the title screen animation.
        pacman_t = GameObject(0, 260)

        # The image for the pacman title image.
        pacman_t.image = self.sprite_images["pacman_run1.png"]

        # The image rect for the pacman title image.
        pacman_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)

        # Create the blinky title animation image.
        blinky_t = GameObject(-40, 260)
        blinky_t.image = self.sprite_images["blinky_run_r1.png"]
        blinky_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)
        self.game_objs_title_images.append(blinky_t)

        # Create the pinky title animation image.
        pinky_t = GameObject(-80, 260)
        pinky_t.image = self.sprite_images["pinky_run_r1.png"]
        pinky_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)
        self.game_objs_title_images.append(pinky_t)

        # Create the inky title animation image.
        inky_t = GameObject(-120, 260)
        inky_t.image = self.sprite_images["inky_run_r1.png"]
        inky_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)
        self.game_objs_title_images.append(inky_t)

        # Create the clyde title animation image.
        clyde_t = GameObject(-160, 260)
        clyde_t.image = self.sprite_images["clyde_run_r1.png"]
        clyde_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)
        self.game_objs_title_images.append(clyde_t)

        # Create the power pellet title animation image.
        power_pellet_t = GameObject(360, 268)
        power_pellet_t.image = self.sprite_images["pellet.png"]
        power_pellet_t.image_rect = pygame.Rect(pacman_t.position_x, pacman_t.position_y, 32, 32)
        self.game_objs_title_images.append(power_pellet_t)

        # Set all the references for the title images.
        self.pacman_title_animation = pacman_t
        self.blinky_title_animation = blinky_t
        self.pinky_title_animation = pinky_t
        self.inky_title_animation = inky_t
        self.clyde_title_animation = clyde_t
        self.power_pellet_title_animation = power_pellet_t

    def setup_game(self):
        """Set up the game for gameplay."""

        # Clear all the title screen objects.
        self.game_objs_title_images.clear()
        self.game_objs_buttons.clear()
        self.game_objs_text_boxes.clear()

        # Reset the gameplay variables.
        self.ghost_cur_time_scatter = self.ghost_max_time_scatter
        self.cur_level = 0
        self.dots_eaten = 0
        self.current_score = 0
        self.got_extra_life = False

        # Create the rect for the Pac-Man life display.
        cur_rect = pygame.Rect(0, 0, 32, 32)
        self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_rect))

        # Create another rect for the Pac-Man life display.
        cur_rect2 = pygame.Rect(0, 0, 32, 32)
        self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_rect2))

        # Play the ready song.
        self.sound_manager.play_sound(self.sound_manager.song_ready, 0, 0)

        # Load the map.
        self.load_map(True)

    def setup_high_score_table(self):
        """Sets up the high score table."""

        # Remove the title game objects.
        self.game_objs_title_images.clear()
        self.game_objs_buttons.clear()
        self.game_objs_text_boxes.clear()

        # The fonts for the text boxes and buttons.
        font2 = self.fonts["PressStart2P-medium"]
        font3 = self.fonts["PressStart2P-small"]

        # The text box for the high scores.
        text_1 = TextBox(232, 60, False, "HIGH SCORES", font2, (255, 255, 150))
        self.game_objs_text_boxes["high_scores"] = text_1

        # The offset y for the score images.
        offset_y = 100

        # Render all the scores for the screen.
        for score in self.high_scores:
            # The text box for the score.
            text_2 = TextBox(232, offset_y, False, str(score), font3, (255, 255, 0))
            self.game_objs_text_boxes["score_1" + str(offset_y)] = text_2

            # Increment the offset y by 20.
            offset_y += 20

        # The back button for the high scores.
        high_scores_button = Button(232, 530, 2, "BACK", (100, 100, 100), (200, 200, 200),
                                    font2, self.input_manager)
        self.game_objs_buttons.append(high_scores_button)

    def main_loop(self):
        """The main loop for the game."""

        # Check if the game is still running. If so, loop.
        while self.is_running:

            # Manage the frame rate to 60 fps.
            self.pygame_clock.tick(60)

            # Check the keyboard input events.
            self.input_manager.check_events()

            # Check if the buttons are being hovered over.
            for button in self.game_objs_buttons:
                button.check_was_hovered()

            # Check if the buttons are being pressed.
            if self.input_manager.mouse_button_pressed:
                for button in self.game_objs_buttons:
                    button_pressed = button.check_was_clicked()

                    if button_pressed:
                        if button.button_type == 0:
                            self.game_mode = 1
                            self.sound_manager.play_sound(self.sound_manager.sound1_pacdot_2, 1, 0)
                            self.setup_game()
                        elif button.button_type == 1:
                            self.game_mode = 3
                            self.sound_manager.play_sound(self.sound_manager.sound1_pacdot_2, 1, 0)
                            self.setup_high_score_table()
                        elif button.button_type == 2:
                            self.game_mode = 0
                            self.sound_manager.play_sound(self.sound_manager.sound1_pacdot_2, 1, 0)
                            self.setup_menu()

            # Animate the title screen.
            if self.game_mode == 0:
                self.animate_title_screen()

            # Check every frame if there are ghosts that are reviving. If so, tell blinky to play the ghost revive
            # music.
            found_ghosts_reviving = False

            for ghost in self.game_objs_ghosts:
                if ghost.run_mode == 4:
                    for ghost2 in self.game_objs_ghosts:
                        if ghost2.ghost_type == 0:
                            ghost2.ghosts_reviving = True
                            found_ghosts_reviving = True
                            break
                if found_ghosts_reviving:
                    break

            if not found_ghosts_reviving:
                for ghost in self.game_objs_ghosts:
                    if ghost.ghost_type == 0:
                        ghost.ghosts_reviving = False

            # Check if changing the level or state.
            if self.game_obj_player is not None:
                if self.game_obj_player.lose_life:
                    self.lives -= 1
                    self.dots_eaten = self.game_obj_player.dots_eaten

                    if not len(self.lives_display) == 0:
                        self.lives_display.pop(0)
                    if self.lives > 0:
                        self.load_map(False)
                    else:
                        # Create the game over text.
                        font1 = self.fonts["PressStart2P-small"]

                        text_3 = TextBox(185, 328, False, "GAME", font1, (225, 0, 0))
                        self.game_objs_text_boxes["GAME"] = text_3

                        text_4 = TextBox(260, 328, False, "OVER", font1, (225, 0, 0))
                        self.game_objs_text_boxes["OVER"] = text_4

                        self.game_obj_player = None
                        self.add_new_high_score(self.current_score)
                        self.export_new_high_scores()
                        self.dots_eaten = 0

                elif self.game_obj_player.finished_map_finished_anim:
                    self.cur_level += 1
                    self.dots_eaten = 0

                    if self.ghost_max_time_scatter > 20:
                        self.ghost_max_time_scatter -= 20
                    self.load_map(True)

            # If out of lives, wait until it is time to return to the title screen.
            if self.lives == 0:
                if self.cur_anim_title_5 >= self.max_anim_title_5:
                    self.cur_anim_title_5 = 0
                    self.game_mode = 0
                    self.lives = 3
                    self.game_objs_text_boxes.clear()
                    self.game_obj_player = None
                    self.portal_entrance_2 = None
                    self.portal_entrance_1 = None
                    self.portal_shot_1 = None
                    self.portal_shot_2 = None
                    self.game_obj_fruit = None
                    self.game_objs_pellets.clear()
                    self.game_obj_ghost_house_entrance = None
                    self.game_objs_tiles.clear()
                    self.fruit_display.clear()
                    self.lives_display.clear()
                    self.game_objs_dots.clear()
                    self.cur_anim_title_3 = 0
                    self.cur_anim_title_2 = 0
                    self.cur_anim_title_1 = 0
                    self.cur_anim_title_4 = 0
                    self.title_anim_mode = 0

                    self.setup_menu()
                else:
                    self.cur_anim_title_5 += 1

            # Check if getting an extra life.
            if not self.got_extra_life:
                if self.current_score >= self.extra_life_score:
                    self.lives += 1
                    cur_image_rect = pygame.Rect(0, 0, 32, 32)
                    self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_image_rect))
                    self.got_extra_life = True
                    self.sound_manager.play_sound(self.sound_manager.sound7_extra_life, 7, 0)

            # Update the game objects.

            # Update Pacman.
            if self.game_obj_player is not None:
                self.game_obj_player.update_obj()

            # Check if creating the portal shots.
            if self.game_obj_player is not None and not self.game_obj_player.is_dead and \
                    not self.game_obj_player.finished_map and self.game_obj_player.ready_mode == 2:
                if self.input_manager.pressed_z and self.portal_shot_1 is None:
                    self.portal_shot_1 = PortalShot(int(self.game_obj_player.position_x),
                                                    int(self.game_obj_player.position_y), 0,
                                                    self.sprite_images["portal_shot_1.png"],
                                                    self.game_obj_player.run_direction)
                    self.game_obj_player.portal_shot_1 = self.portal_shot_1
                    self.sound_manager.play_sound(self.sound_manager.sound4_fire_portal, 4, 0)

                elif self.input_manager.pressed_x and self.portal_shot_2 is None:
                    self.portal_shot_2 = PortalShot(int(self.game_obj_player.position_x),
                                                    int(self.game_obj_player.position_y), 1,
                                                    self.sprite_images["portal_shot_2.png"],
                                                    self.game_obj_player.run_direction)
                    self.game_obj_player.portal_shot_2 = self.portal_shot_2
                    self.sound_manager.play_sound(self.sound_manager.sound4_fire_portal, 4, 0)

            # Update the portal shots.
            if self.portal_shot_1 is not None:
                self.portal_shot_1.update_obj()
            if self.portal_shot_2 is not None:
                self.portal_shot_2.update_obj()

            # Update the portals.
            if self.portal_entrance_1 is not None:
                self.portal_entrance_1.update_obj()
            if self.portal_entrance_2 is not None:
                self.portal_entrance_2.update_obj()

            # Update the fruit.
            if self.game_obj_fruit is not None:
                self.game_obj_fruit.update_obj()

            # Update the ghost objects.
            for ghost in self.game_objs_ghosts:
                ghost.update_obj()

            # Perform the collision detection.
            self.collision_detection()

            # Remove game objects that are marked for deletion.
            if self.game_obj_fruit is not None and self.game_obj_fruit.marked_for_deletion:
                self.game_obj_fruit = None

            if self.portal_shot_1 is not None and self.portal_shot_1.marked_for_deletion:
                self.portal_shot_1 = None

            if self.portal_shot_2 is not None and self.portal_shot_2.marked_for_deletion:
                self.portal_shot_2 = None

            if self.portal_entrance_1 is not None and self.portal_entrance_1.marked_for_deletion:
                self.portal_entrance_1 = None
                self.game_obj_player.portal_entrance_1 = None
                for ghost in self.game_objs_ghosts:
                    ghost.portal_entrance_1 = None

            if self.portal_entrance_2 is not None and self.portal_entrance_2.marked_for_deletion:
                self.portal_entrance_2 = None
                self.game_obj_player.portal_entrance_2 = None
                for ghost in self.game_objs_ghosts:
                    ghost.portal_entrance_2 = None

            # Render the game objects.
            self.render_game_objects()

            # If the q key is pressed, exit the game.
            if self.input_manager.pressed_q:
                self.is_running = False

        # Clean up the game system.
        self.clean_up()

    def animate_title_screen(self):
        """Animates the title screen."""

        # Animate different animation sequences based on the title animation mode.
        if self.title_anim_mode == 0:

            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_1 >= self.max_anim_title_1:
                # Set the defaults for the next title animation.
                self.cur_anim_title_1 = 0
                self.title_anim_mode = 1
                self.game_objs_title_images.remove(self.power_pellet_title_animation)
                self.power_pellet_title_animation = None
                self.pacman_title_animation.angle = 180
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_1 += 1

                self.pacman_title_animation.position_x += 2
                self.blinky_title_animation.position_x += 2
                self.pinky_title_animation.position_x += 2
                self.inky_title_animation.position_x += 2
                self.clyde_title_animation.position_x += 2

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                if self.cur_anim_title_pacman == 0 or self.cur_anim_title_pacman == 4:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run1.png"]
                elif self.cur_anim_title_pacman == 1 or self.cur_anim_title_pacman == 3:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run2.png"]
                elif self.cur_anim_title_pacman == 2:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run3.png"]
                elif self.cur_anim_title_pacman == 5:
                    self.pacman_title_animation.image = self.sprite_images["pacman_idle.png"]

                if self.cur_anim_title_pacman == 0:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r1.png"]
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r1.png"]
                    self.inky_title_animation.image = self.sprite_images["inky_run_r1.png"]
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r2.png"]
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r2.png"]
                    self.inky_title_animation.image = self.sprite_images["inky_run_r2.png"]
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r2.png"]

        elif self.title_anim_mode == 1:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_2 >= self.max_anim_title_2:
                # Set the defaults for the next title animation.
                self.cur_anim_title_2 = 0
                self.title_anim_mode = 2
                self.blinky_title_animation.position_x = -32
                self.blinky_title_animation.position_y = 238
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_2 += 1

                self.pacman_title_animation.position_x -= 2
                if self.cur_anim_title_2 < 25:
                    self.blinky_title_animation.position_x -= 0.5
                elif self.cur_anim_title_2 > 75:
                    self.blinky_title_animation.position_x += 4.0

                if self.cur_anim_title_2 < 50:
                    self.pinky_title_animation.position_x -= 0.5
                elif self.cur_anim_title_2 > 100:
                    self.pinky_title_animation.position_x += 4.0

                if self.cur_anim_title_2 < 75:
                    self.inky_title_animation.position_x -= 0.5
                elif self.cur_anim_title_2 > 125:
                    self.inky_title_animation.position_x += 4.0

                if self.cur_anim_title_2 < 100:
                    self.clyde_title_animation.position_x -= 0.5
                elif self.cur_anim_title_2 > 150:
                    self.clyde_title_animation.position_x += 4.0

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                if self.cur_anim_title_pacman == 0 or self.cur_anim_title_pacman == 4:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run1.png"]
                elif self.cur_anim_title_pacman == 1 or self.cur_anim_title_pacman == 3:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run2.png"]
                elif self.cur_anim_title_pacman == 2:
                    self.pacman_title_animation.image = self.sprite_images["pacman_run3.png"]
                elif self.cur_anim_title_pacman == 5:
                    self.pacman_title_animation.image = self.sprite_images["pacman_idle.png"]

                if self.cur_anim_title_pacman == 0:
                    if self.cur_anim_title_2 < 25:
                        self.blinky_title_animation.image = self.sprite_images["blue_run1.png"]
                    if self.cur_anim_title_2 < 50:
                        self.pinky_title_animation.image = self.sprite_images["blue_run1.png"]
                    if self.cur_anim_title_2 < 75:
                        self.inky_title_animation.image = self.sprite_images["blue_run1.png"]
                    if self.cur_anim_title_2 < 100:
                        self.clyde_title_animation.image = self.sprite_images["blue_run1.png"]
                elif self.cur_anim_title_pacman == 3:
                    if self.cur_anim_title_2 < 25:
                        self.blinky_title_animation.image = self.sprite_images["blue_run2.png"]
                    if self.cur_anim_title_2 < 50:
                        self.pinky_title_animation.image = self.sprite_images["blue_run2.png"]
                    if self.cur_anim_title_2 < 75:
                        self.inky_title_animation.image = self.sprite_images["blue_run2.png"]
                    if self.cur_anim_title_2 < 100:
                        self.clyde_title_animation.image = self.sprite_images["blue_run2.png"]

                if self.cur_anim_title_2 == 25:
                    self.blinky_title_animation.image = self.sprite_images["200.png"]
                elif self.cur_anim_title_2 == 50:
                    self.pinky_title_animation.image = self.sprite_images["400.png"]
                elif self.cur_anim_title_2 == 75:
                    self.inky_title_animation.image = self.sprite_images["800.png"]
                    self.blinky_title_animation.image = self.sprite_images["eyes_r.png"]
                elif self.cur_anim_title_2 == 100:
                    self.clyde_title_animation.image = self.sprite_images["1600.png"]
                    self.pinky_title_animation.image = self.sprite_images["eyes_r.png"]
                elif self.cur_anim_title_2 == 125:
                    self.inky_title_animation.image = self.sprite_images["eyes_r.png"]
                elif self.cur_anim_title_2 == 150:
                    self.clyde_title_animation.image = self.sprite_images["eyes_r.png"]

        elif self.title_anim_mode == 2:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_3 >= self.max_anim_title_3:
                # Set the defaults for the next title animation.
                self.cur_anim_title_3 = 0
                self.title_anim_mode = 3

                font1 = self.fonts["PressStart2P-small"]

                text_1 = TextBox(232, 238, False, "\"BLINKY\"", font1, (255, 0, 0))
                self.game_objs_text_boxes["blinky"] = text_1

                self.blinky_name = text_1
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_3 += 1

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                self.blinky_title_animation.position_x += 3.0

                if self.cur_anim_title_pacman == 0:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r2.png"]

        elif self.title_anim_mode == 3:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_4 >= self.max_anim_title_4:
                # Set the defaults for the next title animation.
                self.cur_anim_title_4 = 0
                self.title_anim_mode = 4
                self.pinky_title_animation.position_x = -32
                self.pinky_title_animation.position_y = 270
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_4 += 1

        elif self.title_anim_mode == 4:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_3 >= self.max_anim_title_3:
                # Set the defaults for the next title animation.
                self.cur_anim_title_3 = 0
                self.title_anim_mode = 5

                font1 = self.fonts["PressStart2P-small"]

                text_1 = TextBox(232, 270, False, "\"PINKY\"", font1, (255, 200, 220))
                self.game_objs_text_boxes["pinky"] = text_1

                self.pinky_name = text_1
            else:
                # Update the title animation.
                self.cur_anim_title_3 += 1

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                self.pinky_title_animation.position_x += 3.0

                if self.cur_anim_title_pacman == 0:
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r2.png"]

        elif self.title_anim_mode == 5:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_4 >= self.max_anim_title_4:
                # Set the defaults for the next title animation.
                self.cur_anim_title_4 = 0
                self.title_anim_mode = 6
                self.inky_title_animation.position_x = -32
                self.inky_title_animation.position_y = 302
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_4 += 1

        elif self.title_anim_mode == 6:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_3 >= self.max_anim_title_3:
                # Set the defaults for the next title animation.
                self.cur_anim_title_3 = 0
                self.title_anim_mode = 7

                font1 = self.fonts["PressStart2P-small"]

                text_1 = TextBox(232, 302, False, "\"INKY\"", font1, (0, 255, 255))
                self.game_objs_text_boxes["inky"] = text_1

                self.inky_name = text_1
            else:
                # Update the title animation.
                self.cur_anim_title_3 += 1

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                self.inky_title_animation.position_x += 3.0

                if self.cur_anim_title_pacman == 0:
                    self.inky_title_animation.image = self.sprite_images["inky_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.inky_title_animation.image = self.sprite_images["inky_run_r2.png"]

        elif self.title_anim_mode == 7:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_4 >= self.max_anim_title_4:
                # Set the defaults for the next title animation.
                self.cur_anim_title_4 = 0
                self.title_anim_mode = 8
                self.clyde_title_animation.position_x = -32
                self.clyde_title_animation.position_y = 334
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_4 += 1

        elif self.title_anim_mode == 8:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_3 >= self.max_anim_title_3:
                # Set the defaults for the next title animation.
                self.cur_anim_title_3 = 0
                self.title_anim_mode = 9

                font1 = self.fonts["PressStart2P-small"]

                text_1 = TextBox(232, 334, False, "\"CLYDE\"", font1, (255, 200, 0))
                self.game_objs_text_boxes["clyde"] = text_1

                self.clyde_name = text_1
            else:
                # Update the title animation.
                self.cur_anim_title_3 += 1

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                self.clyde_title_animation.position_x += 3.0

                if self.cur_anim_title_pacman == 0:
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r2.png"]

        elif self.title_anim_mode == 9:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_5 >= self.max_anim_title_5:
                # Set the defaults for the next title animation.
                self.cur_anim_title_5 = 0
                self.title_anim_mode = 10
                self.cur_anim_title_pacman = 0
            else:
                # Update the title animation.
                self.cur_anim_title_5 += 1

        elif self.title_anim_mode == 10:
            # If the title animation is finished, switch to the next title animation.
            if self.cur_anim_title_5 >= self.max_anim_title_5:
                # Set the defaults for the next title animation.
                self.cur_anim_title_5 = 0
                self.title_anim_mode = 0

                power_pellet_t = GameObject(360, 268)
                power_pellet_t.image = self.sprite_images["pellet.png"]
                power_pellet_t.image_rect = pygame.Rect(power_pellet_t.position_x, power_pellet_t.position_y,
                                                        32, 32)
                self.game_objs_title_images.append(power_pellet_t)
                self.power_pellet_title_animation = power_pellet_t

                self.pacman_title_animation.position_x = 0
                self.pacman_title_animation.angle = 0
                self.blinky_title_animation.position_x = -40
                self.blinky_title_animation.position_y = 260
                self.pinky_title_animation.position_x = -80
                self.pinky_title_animation.position_y = 260
                self.inky_title_animation.position_x = -120
                self.inky_title_animation.position_y = 260
                self.clyde_title_animation.position_x = -160
                self.clyde_title_animation.position_y = 260
            else:
                # Update the title animation.
                self.cur_anim_title_5 += 1

                self.game_objs_text_boxes.pop("blinky", None)
                self.blinky_name = None
                self.game_objs_text_boxes.pop("pinky", None)
                self.pinky_name = None
                self.game_objs_text_boxes.pop("inky", None)
                self.inky_name = None
                self.game_objs_text_boxes.pop("clyde", None)
                self.clyde_name = None

                self.blinky_title_animation.position_x += 5.0

                if self.cur_anim_title_5 >= 20:
                    self.pinky_title_animation.position_x += 5.0
                if self.cur_anim_title_5 >= 40:
                    self.inky_title_animation.position_x += 5.0
                if self.cur_anim_title_5 >= 60:
                    self.clyde_title_animation.position_x += 5.0

                if self.cur_anim_title_pacman >= self.max_anim_title_pacman:
                    self.cur_anim_title_pacman = 0
                else:
                    self.cur_anim_title_pacman += 1

                if self.cur_anim_title_pacman == 0:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r1.png"]
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r1.png"]
                    self.inky_title_animation.image = self.sprite_images["inky_run_r1.png"]
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r1.png"]
                elif self.cur_anim_title_pacman == 3:
                    self.blinky_title_animation.image = self.sprite_images["blinky_run_r2.png"]
                    self.pinky_title_animation.image = self.sprite_images["pinky_run_r2.png"]
                    self.inky_title_animation.image = self.sprite_images["inky_run_r2.png"]
                    self.clyde_title_animation.image = self.sprite_images["clyde_run_r2.png"]

    def load_map(self, destroy_dots_and_pellets):
        """Loads the pacman game map."""

        self.game_objs_ghosts.clear()

        if destroy_dots_and_pellets:
            self.game_objs_pellets.clear()
            self.game_objs_dots.clear()

        self.game_objs_tiles.clear()
        self.game_obj_player = None
        self.game_obj_fruit = None
        self.portal_shot_1 = None
        self.portal_shot_2 = None
        self.portal_entrance_1 = None
        self.portal_entrance_2 = None
        self.a_star_list.clear()

        # The map file being read to create the map objects. Use with statement to ensure the file closes after reading
        # everything.
        with open("map.txt", "r") as in_file:
            # The text containing all the characters for the map objects.
            map_text = in_file.read()

            # The current x position of the current map object being read from or the a star node.
            cur_position_x = 8

            # The current y position of the current map object being read from or the a star node.
            cur_position_y = 40

            # Go through every character and create the correct map object from it.
            for char in map_text:
                if not char == '\n':

                    # The current background tile being produced.
                    background_tile1 = None

                    # Choose a different sprite based on the character.
                    if char == '|':
                        background_tile1 = BackgroundTile(self.sprite_images["wls.png"],
                                                          self.sprite_images["wls_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '!':
                        background_tile1 = BackgroundTile(self.sprite_images["wrs.png"],
                                                          self.sprite_images["wrs_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '=':
                        background_tile1 = BackgroundTile(self.sprite_images["wts.png"],
                                                          self.sprite_images["wts_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '~':
                        background_tile1 = BackgroundTile(self.sprite_images["wbs.png"],
                                                          self.sprite_images["wbs_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '-':
                        background_tile1 = BackgroundTile(self.sprite_images["wt.png"],
                                                          self.sprite_images["wt_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '*':
                        background_tile1 = BackgroundTile(self.sprite_images["wb.png"],
                                                          self.sprite_images["wb_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '(':
                        background_tile1 = BackgroundTile(self.sprite_images["wr.png"],
                                                          self.sprite_images["wr_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == ')':
                        background_tile1 = BackgroundTile(self.sprite_images["wl.png"],
                                                          self.sprite_images["wl_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '<':
                        background_tile1 = BackgroundTile(self.sprite_images["wtls.png"],
                                                          self.sprite_images["wtls_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '>':
                        background_tile1 = BackgroundTile(self.sprite_images["wtrs.png"],
                                                          self.sprite_images["wtrs_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'L':
                        background_tile1 = BackgroundTile(self.sprite_images["wbls.png"],
                                                          self.sprite_images["wbls_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'R':
                        background_tile1 = BackgroundTile(self.sprite_images["wbrs.png"],
                                                          self.sprite_images["wbrs_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '/':
                        background_tile1 = BackgroundTile(self.sprite_images["wtl.png"],
                                                          self.sprite_images["wtl_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '\\':
                        background_tile1 = BackgroundTile(self.sprite_images["wtr.png"],
                                                          self.sprite_images["wtr_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'l':
                        background_tile1 = BackgroundTile(self.sprite_images["wbl.png"],
                                                          self.sprite_images["wbl_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'r':
                        background_tile1 = BackgroundTile(self.sprite_images["wbr.png"],
                                                          self.sprite_images["wbr_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'T':
                        background_tile1 = BackgroundTile(self.sprite_images["wltst.png"],
                                                          self.sprite_images["wltst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 't':
                        background_tile1 = BackgroundTile(self.sprite_images["wrtst.png"],
                                                          self.sprite_images["wrtst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '@':
                        background_tile1 = BackgroundTile(self.sprite_images["wbrs2.png"],
                                                          self.sprite_images["wbrs2_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '#':
                        background_tile1 = BackgroundTile(self.sprite_images["wtls2.png"],
                                                          self.sprite_images["wtls2_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '$':
                        background_tile1 = BackgroundTile(self.sprite_images["wtrs2.png"],
                                                          self.sprite_images["wtrs2_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '%':
                        background_tile1 = BackgroundTile(self.sprite_images["wbls2.png"],
                                                          self.sprite_images["wbls2_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '{':
                        background_tile1 = BackgroundTile(self.sprite_images["wtlst.png"],
                                                          self.sprite_images["wtlst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '}':
                        background_tile1 = BackgroundTile(self.sprite_images["wtrst.png"],
                                                          self.sprite_images["wtrst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '[':
                        background_tile1 = BackgroundTile(self.sprite_images["wblst.png"],
                                                          self.sprite_images["wblst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == ']':
                        background_tile1 = BackgroundTile(self.sprite_images["wbrst.png"],
                                                          self.sprite_images["wbrst_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'g':
                        background_tile1 = BackgroundTile(self.sprite_images["wbli.png"],
                                                          self.sprite_images["wbli_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'h':
                        background_tile1 = BackgroundTile(self.sprite_images["wbri.png"],
                                                          self.sprite_images["wbri_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'i':
                        background_tile1 = BackgroundTile(self.sprite_images["wtli.png"],
                                                          self.sprite_images["wtli_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == 'j':
                        background_tile1 = BackgroundTile(self.sprite_images["wtri.png"],
                                                          self.sprite_images["wtri_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '1':
                        background_tile1 = BackgroundTile(self.sprite_images["wtlsg.png"],
                                                          self.sprite_images["wtlsg_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '2':
                        background_tile1 = BackgroundTile(self.sprite_images["wtsgl.png"],
                                                          self.sprite_images["wtsgl_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '3':
                        background_tile1 = BackgroundTile(self.sprite_images["wtsgc.png"],
                                                          self.sprite_images["wtsgc_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '4':
                        background_tile1 = BackgroundTile(self.sprite_images["wtsgr.png"],
                                                          self.sprite_images["wtsgr_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '5':
                        background_tile1 = BackgroundTile(self.sprite_images["wtrsg.png"],
                                                          self.sprite_images["wtrsg_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '6':
                        background_tile1 = BackgroundTile(self.sprite_images["wblsg.png"],
                                                          self.sprite_images["wblsg_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '7':
                        background_tile1 = BackgroundTile(self.sprite_images["wbrsg.png"],
                                                          self.sprite_images["wbrsg_w.png"],
                                                          cur_position_x, cur_position_y, True)
                    elif char == '`':
                        background_tile1 = BackgroundTile(None, None,
                                                          cur_position_x, cur_position_y, True)
                    elif char == '.' and destroy_dots_and_pellets:
                        # The current pacdot being produced.
                        pacdot = Dot(cur_position_x, cur_position_y, self.sprite_images["dot.png"])
                        self.game_objs_dots.append(pacdot)

                    elif char == 'o' and destroy_dots_and_pellets:
                        # The current pellet being produced.
                        pellet = Pellet(cur_position_x, cur_position_y, self.sprite_images["pellet.png"])
                        self.game_objs_pellets.append(pellet)

                    if background_tile1 is not None:
                        self.game_objs_tiles.append(background_tile1)

                    cur_position_x += 16

                    if cur_position_x >= (28 * 16) + 8:
                        cur_position_x = 8
                        cur_position_y += 16

        # Load the a star map.
        with open("nodes.txt", "r") as in_file:
            # The text containing all the characters for the map objects.
            map_text = in_file.read()

            # The current x position of the current map object being read from or the a star node.
            cur_position_x = 8

            # The current y position of the current map object being read from or the a star node.
            cur_position_y = 40

            # Go through every character and create the correct map object from it.
            for char in map_text:

                if not char == '\n':
                    # The current node being produced.
                    cur_node = None

                    if char == '.':
                        cur_node = AStarNode(cur_position_x, cur_position_y)

                    if cur_node is not None:
                        index_x = Ghost.compute_index(cur_position_x)
                        index_y = Ghost.compute_index(cur_position_y)
                        # noinspection PyTypeChecker
                        self.a_star_array[index_x][index_y] = cur_node

                        index_x = int((cur_position_x - 8) / 16)
                        index_y = int((cur_position_y - 8) / 16)

                        self.a_star_array[index_x][index_y] = cur_node
                        self.a_star_list.append((index_x, index_y, cur_node))

                    cur_position_x += 16

                    if cur_position_x >= (28 * 16) + 8:
                        cur_position_x = 8
                        cur_position_y += 16

            # Connect all of the a star nodes together.
            for x in range(0, len(self.a_star_array)):
                for y in range(len(self.a_star_array[x])):
                    # The current node attaching its neighboring nodes.
                    node = self.a_star_array[x][y]

                    # Only attach nodes if the node exists.
                    if node is not None:

                        # The name of the neighboring nodes.
                        node_child_l_index_x = x - 1
                        node_child_l_index_y = y

                        node_child_r_index_x = x + 1
                        node_child_r_index_y = y

                        node_child_u_index_x = x
                        node_child_u_index_y = y - 1

                        node_child_d_index_x = x
                        node_child_d_index_y = y + 1

                        if node_child_l_index_x >= 0:
                            node.child_left = self.a_star_array[node_child_l_index_x][node_child_l_index_y]

                        if node_child_r_index_x < self.a_star_array_rows:
                            node.child_right = self.a_star_array[node_child_r_index_x][node_child_r_index_y]

                        if node_child_u_index_y >= 0:
                            node.child_up = self.a_star_array[node_child_u_index_x][node_child_u_index_y]

                        if node_child_d_index_y < self.a_star_array_columns:
                            node.child_down = self.a_star_array[node_child_d_index_x][node_child_d_index_y]

        # Create the fruit.

        # The fruit position x.
        fruit_position_x = 224

        # The fruit position y.
        fruit_position_y = 326

        fruit_display_rect = pygame.Rect(0, 0, 32, 32)

        if self.cur_level == 0:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 100,
                                        self.sprite_images["fruit_cherry.png"],
                                        self.sprite_images["100.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_cherry.png"], fruit_display_rect)
        elif self.cur_level == 1:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 300,
                                        self.sprite_images["fruit_strawberry.png"],
                                        self.sprite_images["300.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_strawberry.png"], fruit_display_rect)
        elif self.cur_level == 2 or self.cur_level == 3:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 500,
                                        self.sprite_images["fruit_orange.png"],
                                        self.sprite_images["500.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_orange.png"], fruit_display_rect)
        elif self.cur_level == 4 or self.cur_level == 5:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 700,
                                        self.sprite_images["fruit_apple.png"],
                                        self.sprite_images["700.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_apple.png"], fruit_display_rect)
        elif self.cur_level == 6 or self.cur_level == 7:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 1000,
                                        self.sprite_images["fruit_melon.png"],
                                        self.sprite_images["1000.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_melon.png"], fruit_display_rect)
        elif self.cur_level == 8 or self.cur_level == 9:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 2000,
                                        self.sprite_images["fruit_galaxian.png"],
                                        self.sprite_images["2000.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_galaxian.png"], fruit_display_rect)
        elif self.cur_level == 10 or self.cur_level == 11:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 3000,
                                        self.sprite_images["fruit_bell.png"],
                                        self.sprite_images["3000.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_bell.png"], fruit_display_rect)
        elif self.cur_level > 11:
            self.game_obj_fruit = Fruit(fruit_position_x, fruit_position_y, 5000,
                                        self.sprite_images["fruit_key.png"],
                                        self.sprite_images["5000.png"])
            self.fruit_display[self.cur_level] = (self.sprite_images["fruit_key.png"], fruit_display_rect)

        # Create Pacman.
        self.game_obj_player = Player(224, 424, self.dots_eaten, self.input_manager, self.game_objs_tiles,
                                      self.game_objs_dots, self.game_objs_pellets, self.game_obj_fruit,
                                      self.game_objs_ghosts,
                                      self.game_objs_text_boxes, self.sound_manager, self.sprite_images)

        self.game_obj_player.dots_eaten = self.dots_eaten

        if self.cur_level < 9:
            self.game_obj_player.max_anim_ate_pellet -= 64 * self.cur_level
        else:
            self.game_obj_player.max_anim_ate_pellet = 0

        # Create the ghost house entrance.
        self.game_obj_ghost_house_entrance = GhostHouseEntrance(224, 232, self.sprite_images)

        # Create the ghosts.

        # Create Blinky.
        blinky = Ghost(224, 232, 0, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                       self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, None,
                       self.sound_manager, self.sprite_images)

        # Create Pinky.
        pinky = Ghost(224, 280, 1, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                      self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, None,
                      self.sound_manager, self.sprite_images)

        # Create Inky.
        inky = Ghost(192, 280, 2, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                     self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, blinky,
                     self.sound_manager, self.sprite_images)

        # Create Clyde.
        clyde = Ghost(256, 280, 3, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                      self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, None,
                      self.sound_manager, self.sprite_images)

        self.game_objs_ghosts.append(blinky)
        self.game_objs_ghosts.append(pinky)
        self.game_objs_ghosts.append(inky)
        self.game_objs_ghosts.append(clyde)

        # Increase ghost speeds on certain levels.
        if 10 <= self.cur_level > 0:
            for ghost in self.game_objs_ghosts:
                ghost.run_speed += 0.01 * float(self.cur_level)

        # Allow certain ghosts to travel through portals at certain levels.
        if self.cur_level >= 4:
            clyde.can_travel_through_portals = True
        if self.cur_level >= 6:
            inky.can_travel_through_portals = True
        if self.cur_level >= 8:
            blinky.can_travel_through_portals = True
        if self.cur_level >= 10:
            pinky.can_travel_through_portals = True

        # Create the starting text.
        font1 = self.fonts["PressStart2P-small"]

        if self.cur_level == 0 and self.lives == 3:
            text_1 = TextBox(225, 232, False, "PLAYER ONE", font1, (0, 255, 255))
            self.game_objs_text_boxes["PLAYER ONE"] = text_1

        text_2 = TextBox(225, 328, False, "READY!", font1, (255, 255, 0))
        self.game_objs_text_boxes["READY!"] = text_2

        text_3 = TextBox(64, 20, False, "SCORE:", font1, (255, 255, 255))
        self.game_objs_text_boxes["SCORE:"] = text_3

        text_4 = TextBox(256, 20, False, "LIVES:", font1, (255, 255, 255))
        self.game_objs_text_boxes["LIVES:"] = text_4

        text_5 = TextBox(116, 12, True, "0", font1, (255, 255, 0))
        self.game_objs_text_boxes["score"] = text_5

        # Set the ghost images to none if it is the first level with 3 lives.
        if self.cur_level == 0 and self.lives == 3:
            self.game_obj_player.ready_mode = 0
            blinky.image = None
            pinky.image = None
            inky.image = None
            clyde.image = None
        else:
            self.game_obj_player.ready_mode = 1

    def collision_detection(self):
        """Performs the collision detection."""

        # Check for collisions between the player and the walls.
        if self.game_obj_player is not None and not self.game_obj_player.is_traveling:
            for cur_game_obj in self.game_objs_tiles:
                collision_rect_other = cur_game_obj.collision_rect

                if collision_rect_other is not None and \
                        self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                    self.game_obj_player.is_running = False

                    if self.game_obj_player.run_direction == 0:
                        self.game_obj_player.position_x = cur_game_obj.position_x + collision_rect_other.width
                    elif self.game_obj_player.run_direction == 1:
                        self.game_obj_player.position_x = cur_game_obj.position_x - collision_rect_other.width
                    elif self.game_obj_player.run_direction == 2:
                        self.game_obj_player.position_y = cur_game_obj.position_y + collision_rect_other.height
                    elif self.game_obj_player.run_direction == 3:
                        self.game_obj_player.position_y = cur_game_obj.position_y - collision_rect_other.height

        # Check for collisions between the player and the dots.
        if self.game_obj_player is not None:
            for cur_game_obj in self.game_objs_dots:
                collision_rect_other = cur_game_obj.collision_rect

                if collision_rect_other is not None and \
                        self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                    self.game_objs_dots.remove(cur_game_obj)

                    # If all of the dots are eaten, stop the music.
                    if len(self.game_objs_dots) == 0:
                        self.sound_manager.channel_song.stop()

                    self.game_obj_player.dots_eaten += 1
                    self.dots_eaten += 1
                    self.current_score += 10
                    if not self.game_obj_player.ate_dot_1:
                        self.sound_manager.play_sound(self.sound_manager.sound1_pacdot_1, 1, 0)
                        self.game_obj_player.ate_dot_1 = True
                    else:
                        self.sound_manager.play_sound(self.sound_manager.sound1_pacdot_2, 2, 0)
                        self.game_obj_player.ate_dot_1 = False

        # Check for collisions between the player and the pellets.
        if self.game_obj_player is not None:
            for cur_game_obj in self.game_objs_pellets:
                collision_rect_other = cur_game_obj.collision_rect

                if collision_rect_other is not None and \
                        self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                    self.game_objs_pellets.remove(cur_game_obj)
                    self.game_obj_player.ate_pellet = True
                    self.game_obj_player.cur_anim_ate_pellet = 0
                    self.game_obj_player.streak = 0
                    self.current_score += 50

                    # Make all of the ghosts vulnerable to being eaten by pacman.
                    for ghost in self.game_objs_ghosts:
                        # Only turn ghosts blue if they are not traveling and are not reviving.
                        if not ghost.run_mode == 4 and not ghost.run_mode == 2:
                            ghost.is_vulnerable = True
                            ghost.is_blinking = False
                            ghost.run_mode = 3
                            ghost.prev_turn_node = None
                            ghost.switched_mode = True

        # Check for collisions between the player and the ghosts.
        if self.game_obj_player is not None:
            for ghost in self.game_objs_ghosts:
                collision_rect_other = ghost.collision_rect

                if collision_rect_other is not None and \
                        self.game_obj_player.collision_rect.colliderect(collision_rect_other):

                    if not self.game_obj_player.is_dead:
                        if ghost.run_mode == 3:
                            ghost.run_mode = 4
                            ghost.is_vulnerable = False
                            ghost.is_blinking = False
                            ghost.dead = True
                            self.game_obj_player.streak += 1

                            if self.game_obj_player.streak == 1:
                                ghost.image = self.sprite_images["200.png"]
                                self.current_score += 200
                            elif self.game_obj_player.streak == 2:
                                ghost.image = self.sprite_images["400.png"]
                                self.current_score += 400
                            elif self.game_obj_player.streak == 3:
                                ghost.image = self.sprite_images["800.png"]
                                self.current_score += 800
                            elif self.game_obj_player.streak == 4:
                                ghost.image = self.sprite_images["1600.png"]
                                self.current_score += 1600

                            self.game_obj_player.just_ate_ghost = True
                            self.game_obj_player.image = None

                            self.sound_manager.play_sound(self.sound_manager.sound3_eat_ghost, 3, 0)

                            # We only want to collide with one ghost.
                            break

                        elif ghost.run_mode == 0 or ghost.run_mode == 1 or (ghost.run_mode == 2 and
                                                                            not ghost.image == ghost.image_eyes_d):
                            self.game_obj_player.is_dead = True
                            self.game_obj_player.image = self.game_obj_player.image_runr3
                            self.game_obj_player.is_running = False
                            self.game_objs_ghosts.clear()
                            self.game_obj_fruit = None
                            self.portal_shot_1 = None
                            self.portal_shot_2 = None

                            self.sound_manager.channel_song.stop()
                            pygame.time.wait(1200)

                            self.sound_manager.play_sound(self.sound_manager.song_pacman_die, 0, 0)

        # Check for collisions between the player and the fruit.
        if self.game_obj_player is not None:
            if self.game_obj_fruit is not None:
                collision_rect_other = self.game_obj_fruit.collision_rect

                if collision_rect_other is not None and \
                        self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                    if self.game_obj_fruit.despawning:
                        if not self.game_obj_fruit.eaten:
                            self.sound_manager.play_sound(self.sound_manager.sound2_fruit, 2, 0)
                            self.game_obj_fruit.eaten = True
                            self.current_score += self.game_obj_fruit.score

        # Check for collisions between the ghosts and the ghost house entrance.
        for ghost in self.game_objs_ghosts:
            collision_rect_other = ghost.collision_rect

            if collision_rect_other is not None and \
                    self.game_obj_ghost_house_entrance.collision_rect.colliderect(collision_rect_other):
                if ghost.run_mode == 4:
                    ghost.run_mode = 2
                    ghost.run_direction = 3
                    ghost.position_x = 224
                    ghost.spawn_mode = 4

        # Check for collisions between the portal shot and the portal entrances.
        if self.portal_entrance_1 is not None:
            collision_rect_other = self.portal_entrance_1.collision_rect
            if self.portal_shot_1 is not None and \
                    self.portal_shot_1.collision_rect.colliderect(collision_rect_other):
                self.portal_shot_1.marked_for_deletion = True

            if self.portal_shot_2 is not None and \
                    self.portal_shot_2.collision_rect.colliderect(collision_rect_other):
                self.portal_shot_2.marked_for_deletion = True

        if self.portal_entrance_2 is not None:
            collision_rect_other = self.portal_entrance_2.collision_rect
            if self.portal_shot_1 is not None and \
                    self.portal_shot_1.collision_rect.colliderect(collision_rect_other):
                self.portal_shot_1.marked_for_deletion = True

            if self.portal_shot_2 is not None and \
                    self.portal_shot_2.collision_rect.colliderect(collision_rect_other):
                self.portal_shot_2.marked_for_deletion = True

        # Check for collisions between the portal shot and the walls.
        for wall in self.game_objs_tiles:
            collision_rect_other = wall.collision_rect

            # Checks if a portal was already created so that another portal cannot be created.
            portal_created = False

            if collision_rect_other is not None:
                if self.portal_shot_1 is not None and not self.portal_shot_1.marked_for_deletion and \
                        self.portal_shot_1.collision_rect.colliderect(collision_rect_other):
                    if self.portal_entrance_1 is None or \
                            (self.portal_entrance_1 is not None and not self.portal_entrance_1.in_use):
                        self.portal_entrance_1 = PortalEntrance(wall.position_x, wall.position_y, 0,
                                                                self.portal_shot_1.direction,
                                                                self.sprite_images["portal_entrance_1_1.png"],
                                                                self.sprite_images["portal_entrance_1_2.png"],
                                                                self.sprite_images["portal_entrance_1_3.png"])
                        self.game_obj_player.portal_entrance_1 = self.portal_entrance_1
                        for ghost in self.game_objs_ghosts:
                            ghost.portal_entrance_1 = self.portal_entrance_1
                        self.sound_manager.play_sound(self.sound_manager.sound6_generate_portal, 6, 0)
                    self.portal_shot_1 = None
                    portal_created = True

                if not portal_created and \
                        self.portal_shot_2 is not None and not self.portal_shot_2.marked_for_deletion and \
                        self.portal_shot_2.collision_rect.colliderect(collision_rect_other):
                    if self.portal_entrance_2 is None or \
                            (self.portal_entrance_2 is not None and not self.portal_entrance_2.in_use):
                        self.portal_entrance_2 = PortalEntrance(wall.position_x, wall.position_y, 0,
                                                                self.portal_shot_2.direction,
                                                                self.sprite_images["portal_entrance_2_1.png"],
                                                                self.sprite_images["portal_entrance_2_2.png"],
                                                                self.sprite_images["portal_entrance_2_3.png"])
                        self.game_obj_player.portal_entrance_2 = self.portal_entrance_2
                        for ghost in self.game_objs_ghosts:
                            ghost.portal_entrance_2 = self.portal_entrance_2
                        self.sound_manager.play_sound(self.sound_manager.sound6_generate_portal, 6, 0)
                    self.portal_shot_2 = None

        # Check for collisions between the portal shot and the ghosts.
        for ghost in self.game_objs_ghosts:
            collision_rect_other = ghost.collision_rect

            if collision_rect_other is not None:
                if self.portal_shot_1 is not None and \
                        self.portal_shot_1.collision_rect.colliderect(collision_rect_other):
                    self.portal_shot_1 = None

                if self.portal_shot_2 is not None and \
                        self.portal_shot_2.collision_rect.colliderect(collision_rect_other):
                    self.portal_shot_2 = None

        # Check for collisions between the portal entrance and another portal entrance.
        if self.portal_entrance_1 is not None and self.portal_entrance_2 is not None:
            collision_rect_other = self.portal_entrance_1.collision_rect

            if collision_rect_other is not None:
                if self.portal_entrance_2.collision_rect.colliderect(collision_rect_other):
                    self.portal_entrance_1.marked_for_deletion = True

    def render_game_objects(self):
        """Render all the game objects to the screen. Objects are rendered in order from tiles, to dots, to pacman, to
        ghosts."""
        # Fill the background with the color black.
        self.backbuffer.fill((0, 0, 0))

        # Render all of the individual game objects that are tiles.
        self.render_game_obj_group(self.game_objs_tiles, False)

        # Render the portal entrances.
        if self.portal_entrance_1 is not None:
            self.render_game_obj(self.portal_entrance_1, True)

        if self.portal_entrance_2 is not None:
            self.render_game_obj(self.portal_entrance_2, True)

        # Render all of the individual game objects that are dots.
        self.render_game_obj_group(self.game_objs_dots, False)

        # Render all of the individual game objects that are pellets.
        self.render_game_obj_group(self.game_objs_pellets, False)

        # Render the fruit.
        if self.game_obj_fruit is not None:
            self.render_game_obj(self.game_obj_fruit, False)

        # Render Pacman.
        if self.game_obj_player is not None:
            self.render_game_obj(self.game_obj_player, True)

        # Render all of the individual game objects that are ghosts.
        self.render_game_obj_group(self.game_objs_ghosts, False)

        # Render the portal shots.
        if self.portal_shot_1 is not None:
            self.render_game_obj(self.portal_shot_1, True)

        if self.portal_shot_2 is not None:
            self.render_game_obj(self.portal_shot_2, True)

        # Update the score text for rendering.
        if self.game_mode == 1:
            self.game_objs_text_boxes["score"].set_text(str(self.current_score))

        # Render all of the individual game objects that are text boxes.
        for key in self.game_objs_text_boxes:
            cur_text_box = self.game_objs_text_boxes[key]
            self.render_game_obj(cur_text_box, False)

        # Render the fruit display.
        keys = []
        for key in sorted(self.fruit_display):
            keys.append(key)

        # The current fruit position x.
        cur_fruit_pos_x = 430

        # The current fruit position y.
        cur_fruit_pos_y = 575

        # We can only display up to 12 fruit
        while len(keys) > 12:
            keys.pop(0)

        # Render every fruit in the list.
        for key in keys:
            # The current image being rendered.
            cur_image = self.fruit_display[key][0]

            # The rect of the current image being rendered.
            cur_rect = self.fruit_display[key][1]

            cur_rect.centerx = cur_fruit_pos_x
            cur_rect.centery = cur_fruit_pos_y

            cur_fruit_pos_x -= 32

            # Blit the sprite to the backbuffer.
            self.backbuffer.blit(cur_image, cur_rect)

        cur_life_pos_x = 310
        cur_life_pos_y = 20

        # Render the lives the player has.
        for life in self.lives_display:
            # The current image being rendered.
            cur_image = life[0]

            # The rect of the current image being rendered.
            cur_rect = life[1]

            cur_rect.centerx = cur_life_pos_x
            cur_rect.centery = cur_life_pos_y

            cur_life_pos_x += 32

            # Blit the sprite to the backbuffer.
            self.backbuffer.blit(cur_image, cur_rect)

        # Render the title images.
        if self.game_mode == 0:
            self.render_game_obj_group(self.game_objs_title_images, False)
            self.render_game_obj(self.pacman_title_animation, True)

        # Render the buttons.
        self.render_game_obj_group(self.game_objs_buttons, False)

        # Swap the backbuffer.
        pygame.display.flip()

    def render_game_obj_group(self, game_obj_group, apply_rotation):
        """Renders a single game object group."""

        # Loop through every game object and render it.
        for game_obj in game_obj_group:
            self.render_game_obj(game_obj, apply_rotation)

    def render_game_obj(self, game_obj, apply_rotation):
        """Renders a single game object."""

        # If there is no image, don't render it.
        if game_obj.image is not None:
            # Update the object rect for the rendering process.
            game_obj.update_rect()

            # The current image being rendered.
            cur_image = game_obj.image

            # The rect of the current image being rendered.
            cur_rect = game_obj.image_rect

            if apply_rotation:
                # Blit the sprite to the backbuffer.
                self.backbuffer.blit(pygame.transform.rotate(cur_image, game_obj.angle), cur_rect)
            else:
                # Blit the sprite to the backbuffer.
                self.backbuffer.blit(cur_image, cur_rect)

    def add_new_high_score(self, high_score):
        """Adds a new high score to the high score table."""

        # Add the new high score by comparing to other high scores.
        for x in range(0, len(self.high_scores)):
            if high_score >= self.high_scores[x]:
                self.high_scores.insert(x, int(high_score))
                self.high_scores.pop()
                break

    def export_new_high_scores(self):
        """Exports the new high scores to the high scores file."""

        # The out file for the high scores.
        out_file = open("high_scores.bin", "wb")

        for x in range(0, 20):
            cur_score = struct.pack('i', self.high_scores[x])
            out_file.write(cur_score)

        out_file.close()

    @staticmethod
    def clean_up():
        # Exit pygame.
        pygame.quit()
