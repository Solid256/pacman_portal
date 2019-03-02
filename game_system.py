import pygame
import xml.etree.ElementTree as ETree
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


class GameSystem:
    def __init__(self):
        self.game_objs_tiles = []
        self.game_objs_dots = []
        self.game_objs_pellets = []
        self.game_objs_ghosts = []
        self.game_objs_text_boxes = {}
        self.fonts = {}
        self.fruit_display = {}
        self.lives_display = []

        # The columns in the a star array.
        self.a_star_array_rows = 29

        # The rows in the a star array.
        self.a_star_array_columns = 35

        # The a star array of arrays.
        self.a_star_array = []
        for x in range(0, self.a_star_array_rows):
            self.a_star_array.append([])
            for y in range(0, self.a_star_array_columns):
                self.a_star_array[x].append(None)

        # The list of nodes in the a star graph, extracted from the a star array. It also contain a tuple with the x
        # and y coordinate.
        self.a_star_list = []
        self.sprite_images = {}
        self.input_manager = InputManager(self)
        self.pygame_clock = None
        self.backbuffer = None
        self.game_obj_player = None
        self.game_obj_fruit = None
        self.game_obj_ghost_house_entrance = None
        self.portal_shot_1 = None
        self.portal_shot_2 = None
        self.portal_entrance_1 = None
        self.portal_entrance_2 = None
        self.is_running = True
        self.lives = 3
        self.ghost_max_time_scatter = 400
        self.ghost_cur_time_scatter = self.ghost_max_time_scatter
        self.cur_level = 0

        # The number of dots Pacman has eaten.
        self.dots_eaten = 0

        # The current score from the current playthrough.
        self.current_score = 0

        # Checks if the player got an extra life.
        self.got_extra_life = False

        # The score needed to get an extra life. It is 10,000, just like in the original Pacman.
        self.extra_life_score = 10000

        # Begin the game.
        self.setup_pygame()
        self.load_sprite_images()

        cur_rect = pygame.Rect(0, 0, 32, 32)
        self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_rect))

        cur_rect2 = pygame.Rect(0, 0, 32, 32)
        self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_rect2))

        self.load_map(True)
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

        pygame.display.set_caption("Pacman")

        # Load the font files.
        font1 = pygame.font.Font("fonts/PressStart2P.ttf", 12)
        self.fonts["PressStart2P.ttf"] = font1

    def load_sprite_images(self):
        """Use XML to create all the game sprites and store them in a dictionary."""

        # Load the sprite sheet image.
        sprite_sheet = pygame.image.load('images/sprites.png')

        e_tree = ETree.parse("images/sprites.xml")
        root = e_tree.getroot()

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

            for sprite_attr in sprite_info_xml.attrib:
                if sprite_attr == 'n':
                    name = sprite_info_xml.get(sprite_attr)
                elif sprite_attr == 'x':
                    x = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'y':
                    y = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'w':
                    w = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'h':
                    h = int(sprite_info_xml.get(sprite_attr))

            cur_image = sprite_sheet.subsurface(
                pygame.Rect(x, y, w, h))

            self.sprite_images[name] = cur_image

    def main_loop(self):
        """The main loop for the game."""

        # Check if the game is still running. If so, loop.
        while self.is_running:

            # Manage the frame rate to 60 fps.
            self.pygame_clock.tick(60)

            # Check the keyboard input events.
            self.input_manager.check_events()

            # Check if changing the level or state.
            if self.game_obj_player.lose_life:
                self.lives -= 1
                if not len(self.lives_display) == 0:
                    self.lives_display.pop(0)
                if self.lives > 0:
                    self.load_map(False)
                else:
                    self.game_obj_player.ready_mode = 3

                    # Create the game over text.
                    font1 = self.fonts["PressStart2P.ttf"]

                    text_3 = TextBox(185, 328, False, "GAME", font1, (225, 0, 0))
                    self.game_objs_text_boxes["GAME"] = text_3

                    text_4 = TextBox(260, 328, False, "OVER", font1, (225, 0, 0))
                    self.game_objs_text_boxes["OVER"] = text_4

                    self.game_obj_player.image = None

            elif self.game_obj_player.finished_map_finished_anim:
                self.cur_level += 1
                self.dots_eaten = 0

                if self.ghost_max_time_scatter > 20:
                    self.ghost_max_time_scatter -= 20
                self.load_map(True)

            # Check if getting an extra life.
            if not self.got_extra_life:
                if self.current_score >= self.extra_life_score:
                    self.lives += 1
                    cur_image_rect = pygame.Rect(0, 0, 32, 32)
                    self.lives_display.append((self.sprite_images["pacman_run2.png"], cur_image_rect))
                    self.got_extra_life = True

            # Update the game objects.

            # Update Pacman.
            if self.game_obj_player is not None:
                self.game_obj_player.update_obj()

            # Check if creating the portal shots.
            if self.game_obj_player.ready_mode == 2:
                if self.input_manager.pressed_z and self.portal_shot_1 is None:
                    self.portal_shot_1 = PortalShot(int(self.game_obj_player.position_x),
                                                    int(self.game_obj_player.position_y), 0,
                                                    self.sprite_images["portal_shot_1.png"],
                                                    self.game_obj_player.run_direction)
                    self.game_obj_player.portal_shot_1 = self.portal_shot_1

                elif self.input_manager.pressed_x and self.portal_shot_2 is None:
                    self.portal_shot_2 = PortalShot(int(self.game_obj_player.position_x),
                                                    int(self.game_obj_player.position_y), 1,
                                                    self.sprite_images["portal_shot_2.png"],
                                                    self.game_obj_player.run_direction)
                    self.game_obj_player.portal_shot_2 = self.portal_shot_2

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
                                      self.game_objs_text_boxes, self.sprite_images)

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
                      self.sprite_images)

        # Create Pinky.
        pinky = Ghost(224, 280, 1, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                      self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, None,
                      self.sprite_images)

        # Create Inky.
        inky = Ghost(192, 280, 2, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                     self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, blinky,
                     self.sprite_images)

        # Create Clyde.
        clyde = Ghost(256, 280, 3, self.ghost_cur_time_scatter, self.game_obj_player, self.a_star_array,
                      self.a_star_list, self.game_objs_tiles, self.game_obj_ghost_house_entrance, None,
                      self.sprite_images)

        self.game_objs_ghosts.append(blinky)
        '''self.game_objs_ghosts.append(pinky)
        self.game_objs_ghosts.append(inky)
        self.game_objs_ghosts.append(clyde)'''

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
        font1 = self.fonts["PressStart2P.ttf"]

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
        for cur_game_obj in self.game_objs_dots:
            collision_rect_other = cur_game_obj.collision_rect

            if collision_rect_other is not None and \
                    self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                self.game_objs_dots.remove(cur_game_obj)
                self.game_obj_player.dots_eaten += 1
                self.dots_eaten += 1
                self.current_score += 10

        # Check for collisions between the player and the pellets.
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
                        pygame.time.wait(1200)

        # Check for collisions between the player and the fruit.
        if self.game_obj_fruit is not None:
            collision_rect_other = self.game_obj_fruit.collision_rect

            if collision_rect_other is not None and \
                    self.game_obj_player.collision_rect.colliderect(collision_rect_other):
                if self.game_obj_fruit.despawning:
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

        # Debug rendering for the ghost's a star path.

        # Debug rendering for the ghost house.
        '''if self.game_obj_ghost_house_entrance is not None:
            cur_image = self.sprite_images["debug_2.png"]
            cur_rect = cur_image.get_rect()
            cur_rect.centerx = self.game_obj_ghost_house_entrance.position_x
            cur_rect.centery = self.game_obj_ghost_house_entrance.position_y
            self.backbuffer.blit(cur_image, cur_rect)'''

        # Render the ghost's path.
        for ghost in self.game_objs_ghosts:
            '''for node in ghost.node_path:
                cur_image = self.sprite_images["debug_1.png"]
                cur_rect = cur_image.get_rect()
                cur_rect.centerx = node.position_x
                cur_rect.centery = node.position_y
                self.backbuffer.blit(cur_image, cur_rect)'''

            # Render the ghost's start index.
            '''cur_image = self.sprite_images["debug_1.png"]
            cur_rect = cur_image.get_rect()
            cur_rect.centerx = ghost.a_star_ghost_index_x * 16 + 8
            cur_rect.centery = ghost.a_star_ghost_index_y * 16 + 8
            self.backbuffer.blit(cur_image, cur_rect)

            # Render the ghost's end index.
            cur_image = self.sprite_images["debug_2.png"]
            cur_rect = cur_image.get_rect()
            cur_rect.centerx = ghost.a_star_end_index_x * 16 + 8
            cur_rect.centery = ghost.a_star_end_index_y * 16 + 8
            self.backbuffer.blit(cur_image, cur_rect)'''

        # Swap the backbuffer.
        pygame.display.flip()

    def render_game_obj_group(self, game_obj_group, apply_rotation):
        for game_obj in game_obj_group:
            self.render_game_obj(game_obj, apply_rotation)

    def render_game_obj(self, game_obj, apply_rotation):
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

    @staticmethod
    def clean_up():
        # Exit pygame.
        pygame.quit()
