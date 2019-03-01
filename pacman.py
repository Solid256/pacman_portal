import pygame

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, dots_eaten, input_manager, game_objs_tiles, game_objs_dots, game_objs_pellets,
                 game_obj_fruit, game_objs_ghosts, game_objs_text_boxes, sprites):
        super(Player, self).__init__(x, y)
        self.sprites = sprites
        self.input_manager = input_manager
        self.game_objs_tiles = game_objs_tiles
        self.game_objs_dots = game_objs_dots
        self.game_objs_pellets = game_objs_pellets
        self.game_obj_fruit = game_obj_fruit
        self.portal_shot_1 = None
        self.portal_shot_2 = None
        self.portal_entrance_1 = None
        self.portal_entrance_2 = None
        self.game_objs_ghosts = game_objs_ghosts
        self.text_boxes = game_objs_text_boxes

        self.image_idle = sprites["pacman_idle.png"]
        self.image_runr1 = sprites["pacman_run1.png"]
        self.image_runr2 = sprites["pacman_run2.png"]
        self.image_runr3 = sprites["pacman_run3.png"]

        self.image_die1 = sprites["pacman_die1.png"]
        self.image_die2 = sprites["pacman_die2.png"]
        self.image_die3 = sprites["pacman_die3.png"]
        self.image_die4 = sprites["pacman_die4.png"]
        self.image_die5 = sprites["pacman_die5.png"]
        self.image_die6 = sprites["pacman_die6.png"]
        self.image_die7 = sprites["pacman_die7.png"]
        self.image_die8 = sprites["pacman_die8.png"]
        self.image_die9 = sprites["pacman_die9.png"]
        self.image_die10 = sprites["pacman_die10.png"]
        self.image_die11 = sprites["pacman_die11.png"]
        self.image_die12 = sprites["pacman_die12.png"]
        self.image_die13 = sprites["pacman_die13.png"]
        self.image_die14 = sprites["pacman_die14.png"]
        self.image_die15 = sprites["pacman_die15.png"]
        self.image_die16 = sprites["pacman_die16.png"]

        self.image = self.image_idle

        # The original rect of the original sprite image.
        original_rect = self.image.get_rect()

        self.image_rect = pygame.Rect(x - 16, y - 16, original_rect.width, original_rect.height)

        # The collision rect.
        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        # The running speed of Pacman.
        self.run_speed = 2.0

        # Checks if Pacman is running or not.
        self.is_running = True

        # Checks if Pacman is traveling or not.
        self.is_traveling = False

        # Checks if Pacman is dead or not.
        self.is_dead = False

        # The running direction of Pacman.
        # 0 - left.
        # 1 - right.
        # 2 - up.
        # 3 - down.
        self.run_direction = 1

        # The current animation frame for the running animation.
        self.cur_anim_frame_run = 0

        # The maximum animation frame for the running animation.
        self.max_anim_frame_run = 6

        # The angle at which to display the current pacman sprite.
        self.angle = 0

        # The current animation frame for the death animation.
        self.cur_anim_death = 95

        # The maximum animation frame for the death animation.
        self.max_anim_death = 96

        # Checks if the death animation is running.
        self.run_anim_death = False

        # Checks if losing a life and/or restarting a level.
        self.lose_life = False

        # Checks if pacman has eaten the pellet.
        self.ate_pellet = False

        # The current animation frame for the ate pellet animation.
        self.cur_anim_ate_pellet = 0

        # The current animation frame for the ate pellet animation. This shrinks by 64 after every level. On the 9th
        # level, power pellets become useless, just like in the original pacman.
        self.max_anim_ate_pellet = 512

        # How many ghosts the player has eaten with a single power pellet.
        self.streak = 0

        # Checks if the player has just eaten a ghost.
        self.just_ate_ghost = False

        # The number of dots Pacman has eaten.
        self.dots_eaten = dots_eaten

        # Checks if the map was finished.
        self.finished_map = False

        self.finished_map_waiting = True

        self.cur_finished_map_anim = 0
        self.max_finished_map_anim = 120

        self.finished_map_finished_anim = False

        self.cur_ready1_anim = 0
        self.max_ready1_anim = 128
        self.cur_ready2_anim = 0
        self.max_ready2_anim = 128

        # The ready mode for starting the level.
        # 0 - First level not ready part 1.
        # 1 - Not ready part 2. Every other level part 1.
        # 2 - Ready!
        # 3 - Game over!
        self.ready_mode = 0

    def update_obj(self):

        # Check if the intro sequence is occuring:

        if self.ready_mode == 0:
            self.image = None
            if self.cur_ready1_anim >= self.max_ready1_anim:
                self.ready_mode = 1
                self.cur_ready1_anim = 0
                self.text_boxes.pop("PLAYER ONE", None)
                self.image = self.image_idle

            self.cur_ready1_anim += 1

        elif self.ready_mode == 1:
            for ghost in self.game_objs_ghosts:
                if ghost.ghost_type == 0:
                    ghost.image = ghost.image_run_l1
                elif ghost.ghost_type == 1:
                    ghost.image = ghost.image_run_d1
                elif ghost.ghost_type == 2 or ghost.ghost_type == 3:
                    ghost.image = ghost.image_run_u1

            if self.cur_ready1_anim > self.max_ready1_anim:
                self.ready_mode = 2
                self.cur_ready1_anim = 0
                self.text_boxes.pop("READY!", None)
                self.image = self.image_runr1
                for ghost in self.game_objs_ghosts:
                    ghost.active = True

            self.cur_ready1_anim += 1

        elif self.ready_mode == 2:
            # Check if the map was finished.
            if self.finished_map:
                if self.finished_map_waiting:
                    pygame.time.wait(1200)
                    self.game_objs_ghosts.clear()

                    if self.game_obj_fruit is not None:
                        self.game_obj_fruit.marked_for_deletion = True

                    if self.portal_shot_1 is not None:
                        self.portal_shot_1.marked_for_deletion = True

                    if self.portal_shot_2 is not None:
                        self.portal_shot_2.marked_for_deletion = True

                    if self.portal_entrance_1 is not None:
                        self.portal_entrance_1.marked_for_deletion = True

                    if self.portal_entrance_2 is not None:
                        self.portal_entrance_2.marked_for_deletion = True

                self.finished_map_waiting = False

                if self.cur_finished_map_anim >= self.max_finished_map_anim:
                    self.finished_map_finished_anim = True
                else:
                    if self.cur_finished_map_anim == 0 or \
                        self.cur_finished_map_anim == 30 or \
                        self.cur_finished_map_anim == 60 or \
                            self.cur_finished_map_anim == 90:
                        for wall in self.game_objs_tiles:
                            wall.image = wall.white_tile_image

                    elif self.cur_finished_map_anim == 15 or \
                        self.cur_finished_map_anim == 45 or \
                        self.cur_finished_map_anim == 75 or \
                            self.cur_finished_map_anim == 105:
                        for wall in self.game_objs_tiles:
                            wall.image = wall.tile_image

                    self.cur_finished_map_anim += 1

            # Check if the player just ate a ghost. If so, freeze the game temporarily.
            if self.just_ate_ghost:
                pygame.time.wait(800)
                self.just_ate_ghost = False

            # Processing for when the player isn't dead.
            if not self.is_dead:
                # Check if all the pacdots and pellets are eaten.
                if len(self.game_objs_dots) == 0 and len(self.game_objs_pellets) == 0:
                    # Freeze the game and end it.
                    self.is_running = False
                    self.image = self.image_runr2
                    self.finished_map = True

                    self.game_obj_fruit = None
                    self.portal_shot_1 = None
                    self.portal_shot_2 = None
                else:
                    # Checks if the player is able to change direction.
                    is_able_change_direction = True

                    # Check if the player is traveling or not.
                    if self.position_x < 8 or self.position_x > 440:
                        self.is_traveling = True
                    else:
                        self.is_traveling = False

                    # Only allow player input if pacman isn't traveling.
                    if not self.is_traveling:
                        if self.input_manager.pressed_left:
                            # Check if a wall is blocking the way.

                            # The x coordinate of the collision point 1.
                            col_point1_x = self.position_x - 12

                            # The y coordinate of the collision point 1.
                            col_point1_y = self.position_y + 7

                            # The x coordinate of the collision point 2.
                            col_point2_x = self.position_x - 12

                            # The y coordinate of the collision point 2.
                            col_point2_y = self.position_y - 7

                            for tile in self.game_objs_tiles:
                                if tile.collision_rect.collidepoint(col_point1_x, col_point1_y) or \
                                        tile.collision_rect.collidepoint(col_point2_x, col_point2_y):
                                    is_able_change_direction = False
                                    break

                            if is_able_change_direction:
                                self.run_direction = 0
                                self.is_running = True
                                self.angle = 180

                        elif self.input_manager.pressed_right:
                            # Check if a wall is blocking the way.

                            # The x coordinate of the collision point 1.
                            col_point1_x = self.position_x + 12

                            # The y coordinate of the collision point 1.
                            col_point1_y = self.position_y + 7

                            # The x coordinate of the collision point 2.
                            col_point2_x = self.position_x + 12

                            # The y coordinate of the collision point 2.
                            col_point2_y = self.position_y - 7

                            for tile in self.game_objs_tiles:
                                if tile.collision_rect.collidepoint(col_point1_x, col_point1_y) or \
                                        tile.collision_rect.collidepoint(col_point2_x, col_point2_y):
                                    is_able_change_direction = False
                                    break

                            if is_able_change_direction:
                                self.run_direction = 1
                                self.is_running = True
                                self.angle = 0

                        elif self.input_manager.pressed_up:
                            # Check if a wall is blocking the way.

                            # The x coordinate of the collision point 1.
                            col_point1_x = self.position_x + 7

                            # The y coordinate of the collision point 1.
                            col_point1_y = self.position_y - 12

                            # The x coordinate of the collision point 2.
                            col_point2_x = self.position_x - 7

                            # The y coordinate of the collision point 2.
                            col_point2_y = self.position_y - 12

                            for tile in self.game_objs_tiles:
                                if tile.collision_rect.collidepoint(col_point1_x, col_point1_y) or \
                                        tile.collision_rect.collidepoint(col_point2_x, col_point2_y):
                                    is_able_change_direction = False
                                    break

                            if is_able_change_direction:
                                self.run_direction = 2
                                self.is_running = True
                                self.angle = 90

                        elif self.input_manager.pressed_down:
                            # Check if a wall is blocking the way.

                            # The x coordinate of the collision point 1.
                            col_point1_x = self.position_x + 7

                            # The y coordinate of the collision point 1.
                            col_point1_y = self.position_y + 12

                            # The x coordinate of the collision point 2.
                            col_point2_x = self.position_x - 7
                            col_point2_y = self.position_y + 12

                            for tile in self.game_objs_tiles:
                                if tile.collision_rect.collidepoint(col_point1_x, col_point1_y) or \
                                        tile.collision_rect.collidepoint(col_point2_x, col_point2_y):
                                    is_able_change_direction = False
                                    break

                            if is_able_change_direction:
                                self.run_direction = 3
                                self.is_running = True
                                self.angle = 270

                    if self.is_running:
                        if self.run_direction == 0:
                            self.position_x -= self.run_speed
                        elif self.run_direction == 1:
                            self.position_x += self.run_speed
                        elif self.run_direction == 2:
                            self.position_y -= self.run_speed
                        elif self.run_direction == 3:
                            self.position_y += self.run_speed

                    # Check if Pacman is teleporting through both sides of the screen.
                    if self.position_x < -16:
                        self.position_x = 480
                    elif self.position_x > 480:
                        self.position_x = -16

                    self.collision_rect.centerx = self.position_x
                    self.collision_rect.centery = self.position_y

                    # Update the player animation.
                    if self.is_running:
                        if self.cur_anim_frame_run >= self.max_anim_frame_run:
                            self.cur_anim_frame_run = 0

                        self.cur_anim_frame_run += 1

                        if self.cur_anim_frame_run == 0 or self.cur_anim_frame_run == 4:
                            self.image = self.image_runr1
                        elif self.cur_anim_frame_run == 1 or self.cur_anim_frame_run == 3:
                            self.image = self.image_runr2
                        elif self.cur_anim_frame_run == 2:
                            self.image = self.image_runr3
                        elif self.cur_anim_frame_run == 5:
                            self.image = self.image_idle
                    else:
                        self.image = self.image_runr3

                # Do power pellet stuff.
                if self.ate_pellet:
                    # Update the player power pellet animation.

                    # Check if the ghosts should start blinking.
                    if self.cur_anim_ate_pellet >= self.max_anim_ate_pellet - 192:
                        # Make ghosts start blinking. Set their run mode to flee.
                        for ghost in self.game_objs_ghosts:
                            ghost.is_blinking = True

                    # Check if the power pellet should run out.
                    if self.cur_anim_ate_pellet >= self.max_anim_ate_pellet:
                        self.cur_anim_ate_pellet = 0
                        self.ate_pellet = False
                        self.streak = 0

                        # Make ghosts invulnerable again. Set their run mode to chase.
                        for ghost in self.game_objs_ghosts:

                            # Only do this if their run mode is equal to 3.
                            if ghost.run_mode == 3:
                                ghost.is_blinking = False
                                ghost.is_vulnerable = False
                                ghost.run_mode = ghost.timed_run_mode
                                ghost.prev_turn_node = None
                                ghost.switched_mode = True

                    # Increment the ate pellet animation if still eating ghosts.
                    if self.ate_pellet:
                        self.cur_anim_ate_pellet += 1

            else:
                # Do death stuff.

                # Update the player death animation.
                if self.cur_anim_death >= self.max_anim_death:
                    self.cur_anim_death = 0
                    self.angle = 0

                    if self.run_anim_death:
                        self.lose_life = True

                    self.run_anim_death = True

                self.cur_anim_death += 1

                if self.run_anim_death and not self.lose_life:
                    if self.cur_anim_death == 1:
                        self.image = self.image_die1
                    elif self.cur_anim_death == 6:
                        self.image = self.image_die2
                    elif self.cur_anim_death == 12:
                        self.image = self.image_die3
                    elif self.cur_anim_death == 18:
                        self.image = self.image_die4
                    elif self.cur_anim_death == 24:
                        self.image = self.image_die5
                    elif self.cur_anim_death == 30:
                        self.image = self.image_die6
                    elif self.cur_anim_death == 36:
                        self.image = self.image_die7
                    elif self.cur_anim_death == 42:
                        self.image = self.image_die8
                    elif self.cur_anim_death == 48:
                        self.image = self.image_die9
                    elif self.cur_anim_death == 54:
                        self.image = self.image_die10
                    elif self.cur_anim_death == 60:
                        self.image = self.image_die11
                    elif self.cur_anim_death == 66:
                        self.image = self.image_die12
                    elif self.cur_anim_death == 72:
                        self.image = self.image_die13
                    elif self.cur_anim_death == 78:
                        self.image = self.image_die14
                    elif self.cur_anim_death == 84:
                        self.image = self.image_die15
                    elif self.cur_anim_death == 90:
                        self.image = self.image_die16
        else:
            if self.cur_ready1_anim >= self.max_ready1_anim:
                self.cur_ready1_anim = 0
