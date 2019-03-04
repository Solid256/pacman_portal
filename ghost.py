from game_object import GameObject

import pygame
import random


class Ghost(GameObject):
    def __init__(self, x, y, ghost_type, max_time_scatter, pacman, a_star_array, a_star_list, walls,
                 ghost_house_entrance, blinky, sound_manager, sprites):
        """The init function for initializing the default values."""
        super(Ghost, self).__init__(x, y)
        self.is_vulnerable = False
        self.is_blinking = False
        self.blink_anim_toggle = True
        self.can_travel_through_portals = False

        # Checks if the ghost is running or not.
        self.is_running = True

        self.end_node_reached = False

        self.teleporting = False

        # Checks if the ghost has switched run mode. It is only reset to false after the ghost has gotten a chance to
        # change direction and gather a new previous corner node.
        self.switched_mode = False

        # Checks if the ghost is dead.
        self.dead = False

        self.clyde_switch_mode_1 = False

        self.active = False

        self.in_portal = False
        self.leaving_portal = False

        # Checks if there are ghosts reviving.
        self.ghosts_reviving = False

        self.ghost_type = ghost_type
        self.max_mode_switch_0 = 400
        self.max_mode_switch_1 = max_time_scatter
        self.cur_mode_switch = 0
        self.extra_movement = 0
        self.clyde_wait = 0

        # The direction that the ghost is running.
        # 0 - left.
        # 1 - right.
        # 2 - up.
        # 3 - down.
        self.run_direction = 0

        # The running mode.
        # 0 - scatter.
        # 1 - chase.
        # 2 - travel.
        # 3 - flee.
        # 4 - revive.
        self.run_mode = 1

        # The spawn mode.
        # 0 - No spawn.
        # 1 - Moving left or right.
        # 2 - Moving up.
        # 3 - Wavering.
        # 4 - Moving down.
        self.spawn_mode = 0

        # The running speed of the ghost.
        self.run_speed = 1.8

        # The traveling speed of the ghost.
        self.traveling_speed = 1.5

        # The vulnerable speed of the ghost.
        self.vulnerable_speed = 1.0

        # The revive speed of the ghost.
        self.revive_speed = 3.0

        # The current speed being used.
        self.current_speed = self.run_speed

        # The current run mode being managed by the random timer.
        self.timed_run_mode = 1

        # The previous run mode. Used to check if the run mode has changed.
        self.prev_run_mode = 1

        # The current scatter position for the scatter and flee modes.
        self.scatter_index_x = 0
        self.scatter_index_y = 0

        # The scatter positions for the scatter and flee modes.
        self.scatter_tl_index_x = self.compute_index(24)
        self.scatter_tl_index_y = self.compute_index(40)

        self.scatter_tr_index_x = self.compute_index(424)
        self.scatter_tr_index_y = self.compute_index(40)

        self.scatter_dl_index_x = self.compute_index(24)
        self.scatter_dl_index_y = self.compute_index(552)

        self.scatter_dr_index_x = self.compute_index(424)
        self.scatter_dr_index_y = self.compute_index(552)

        # The current animation for the running animation.
        self.cur_anim_run = 0

        # The maximum animation for the running animation.
        self.max_anim_run = 16

        # The start point a star indices for the ghosts.
        self.a_star_ghost_index_x = 0
        self.a_star_ghost_index_y = 0

        # The end point a star indices for the ghosts.
        self.a_star_end_index_x = 0
        self.a_star_end_index_y = 0

        # The maximum number of nodes found. This is to prevent the a star algorithm from becoming too slow.
        self.max_num_of_nodes_found = 256

        self.cur_anim_portal = 0
        self.max_anim_portal = 6
        self.portal_index = 0
        # Checks if blinky is playing a song.
        # 0 - No song.
        # 1 - Blinky 1.
        # 2 - Blinky 2.
        # 3 - Blinky 3.
        # 4 - Flee.
        # 5 - Revive.
        self.blinky_play_sound = 0

        self.pacman = pacman
        self.a_star_array = a_star_array
        self.a_star_list = a_star_list
        self.walls = walls
        self.ghost_house_entrance = ghost_house_entrance
        self.portal_entrance_1 = None
        self.portal_entrance_2 = None
        self.blinky = blinky
        self.sound_manager = sound_manager
        self.sprites = sprites
        self.prev_turn_node = None

        # Set up the random seed.
        random.seed()

        # Choose the correct ghost images based on the ghost type.
        if self.ghost_type == 0:
            self.image_run_l1 = sprites["blinky_run_l1.png"]
            self.image_run_l2 = sprites["blinky_run_l2.png"]

            self.image_run_r1 = sprites["blinky_run_r1.png"]
            self.image_run_r2 = sprites["blinky_run_r2.png"]

            self.image_run_u1 = sprites["blinky_run_u1.png"]
            self.image_run_u2 = sprites["blinky_run_u2.png"]

            self.image_run_d1 = sprites["blinky_run_d1.png"]
            self.image_run_d2 = sprites["blinky_run_d2.png"]

        elif self.ghost_type == 1:
            self.image_run_l1 = sprites["pinky_run_l1.png"]
            self.image_run_l2 = sprites["pinky_run_l2.png"]

            self.image_run_r1 = sprites["pinky_run_r1.png"]
            self.image_run_r2 = sprites["pinky_run_r2.png"]

            self.image_run_u1 = sprites["pinky_run_u1.png"]
            self.image_run_u2 = sprites["pinky_run_u2.png"]

            self.image_run_d1 = sprites["pinky_run_d1.png"]
            self.image_run_d2 = sprites["pinky_run_d2.png"]

            self.spawn_mode = 2
            self.run_mode = 2
            self.run_direction = 2

        elif self.ghost_type == 2:
            self.image_run_l1 = sprites["inky_run_l1.png"]
            self.image_run_l2 = sprites["inky_run_l2.png"]

            self.image_run_r1 = sprites["inky_run_r1.png"]
            self.image_run_r2 = sprites["inky_run_r2.png"]

            self.image_run_u1 = sprites["inky_run_u1.png"]
            self.image_run_u2 = sprites["inky_run_u2.png"]

            self.image_run_d1 = sprites["inky_run_d1.png"]
            self.image_run_d2 = sprites["inky_run_d2.png"]

            self.spawn_mode = 3
            self.run_mode = 2
            self.run_direction = 3

        elif self.ghost_type == 3:
            self.image_run_l1 = sprites["clyde_run_l1.png"]
            self.image_run_l2 = sprites["clyde_run_l2.png"]

            self.image_run_r1 = sprites["clyde_run_r1.png"]
            self.image_run_r2 = sprites["clyde_run_r2.png"]

            self.image_run_u1 = sprites["clyde_run_u1.png"]
            self.image_run_u2 = sprites["clyde_run_u2.png"]

            self.image_run_d1 = sprites["clyde_run_d1.png"]
            self.image_run_d2 = sprites["clyde_run_d2.png"]

            self.spawn_mode = 3
            self.run_mode = 2
            self.run_direction = 3

        self.image_blue_run1 = sprites["blue_run1.png"]
        self.image_blue_run2 = sprites["blue_run2.png"]
        self.image_blue_run3 = sprites["blue_run3.png"]
        self.image_blue_run4 = sprites["blue_run4.png"]

        self.image_eyes_d = sprites["eyes_d.png"]
        self.image_eyes_u = sprites["eyes_u.png"]
        self.image_eyes_l = sprites["eyes_l.png"]
        self.image_eyes_r = sprites["eyes_r.png"]

        self.image = self.image_run_l1

        # The original rect of the original sprite image.
        original_rect = self.image.get_rect()

        self.image_rect = pygame.Rect(x - 16, y - 16, original_rect.width, original_rect.height)

        # The collision rect.
        self.collision_rect = pygame.Rect(x - 8, y - 8, 16, 16)

        # The node path for the ghost to travel on.
        self.node_path = []

        # The predecessors of the child nodes.
        self.predecessors = {}

    def update_obj(self):
        if self.active:
            # Check whether or not to start playing music.
            if not self.pacman.ate_pellet and not self.ghosts_reviving:
                if self.pacman.dots_eaten < 100:
                    if not self.blinky_play_sound == 1:
                        self.blinky_play_sound = 1
                        self.sound_manager.play_sound(self.sound_manager.song_blinky_1, 0, -1)
                elif 200 > self.pacman.dots_eaten >= 100:
                    if not self.blinky_play_sound == 2:
                        self.blinky_play_sound = 2
                        self.sound_manager.play_sound(self.sound_manager.song_blinky_2, 0, -1)
                elif self.pacman.dots_eaten >= 200:
                    if not self.blinky_play_sound == 3:
                        self.blinky_play_sound = 3
                        self.sound_manager.play_sound(self.sound_manager.song_blinky_3, 0, -1)
            elif not self.ghosts_reviving:
                if not self.blinky_play_sound == 4:
                    self.blinky_play_sound = 4
                    self.sound_manager.play_sound(self.sound_manager.song_flee, 0, -1)
            else:
                if not self.blinky_play_sound == 5:
                    self.blinky_play_sound = 5
                    self.sound_manager.play_sound(self.sound_manager.song_revive, 0, -1)

            self.extra_movement = 0.0

            # Check if switching to a different mode.
            if self.timed_run_mode == 0 and self.cur_mode_switch > self.max_mode_switch_1:
                self.timed_run_mode = 1
                self.cur_mode_switch = 0
            elif self.timed_run_mode == 1 and self.cur_mode_switch > self.max_mode_switch_0:
                self.timed_run_mode = 0
                self.cur_mode_switch = 1

            self.cur_mode_switch += 1

            # Switch to the next timed run mode when ready. You cannot do this when in traveling or flee or revive mode.
            if not self.run_mode == 2 and not self.run_mode == 3 and not self.run_mode == 4:
                # If the ghost is blinky, and 90 dots are eaten, go into Cruise Elroy mode.
                if self.pacman.dots_eaten >= 90 and self.ghost_type == 0:
                    self.run_mode = 1
                else:
                    self.run_mode = self.timed_run_mode

            # Change the run mode to traveling if the ghost is trying to teleport horizontally.
            if self.position_x < 0 or self.position_x > 440:
                self.run_mode = 2
                self.teleporting = True
            elif self.teleporting:
                self.teleporting = False
                self.run_mode = self.timed_run_mode

            # Check if the run mode has been switched.
            if not self.prev_run_mode == self.run_mode:
                self.switched_mode = True
                self.prev_run_mode = self.run_mode
                self.prev_turn_node = None

            # Teleport the ghost on the other side of the screen if the ghost leaves the screen horizontally.
            if self.position_x < -16:
                self.position_x = 480
            elif self.position_x > 480:
                self.position_x = -16

            self.a_star_ghost_index_x = int(int(self.position_x) / 16)
            self.a_star_ghost_index_y = int(int(self.position_y) / 16)

            # Find out which direction to run by using the a star algorithm.
            if not self.run_mode == 2:
                found_wall_1 = False
                found_wall_2 = False

                # If a previous turn node wasn't found, just let the a star algorithm run. Otherwise check for turning
                # corners.
                if self.prev_turn_node is None:
                    self.run_direction = self.a_star()
                else:
                    # First check if you actually have to use the a star algorithm. Check for multiple turning paths.
                    if self.run_direction == 0 or self.run_direction == 1:
                        wall_index_other_1 = self.a_star_ghost_index_y + 1
                        wall_index_other_2 = self.a_star_ghost_index_y - 1

                        for cur_wall in self.walls:
                            wall_x_index = self.compute_index(cur_wall.position_x)
                            wall_y_index = self.compute_index(cur_wall.position_y)

                            if wall_x_index == self.a_star_ghost_index_x and wall_y_index == wall_index_other_1:
                                found_wall_1 = True
                            elif wall_x_index == self.a_star_ghost_index_x and wall_y_index == wall_index_other_2:
                                found_wall_2 = True
                    else:
                        wall_index_other_1 = self.a_star_ghost_index_x + 1
                        wall_index_other_2 = self.a_star_ghost_index_x - 1

                        for cur_wall in self.walls:
                            wall_x_index = self.compute_index(cur_wall.position_x)
                            wall_y_index = self.compute_index(cur_wall.position_y)

                            if wall_x_index == wall_index_other_1 and wall_y_index == self.a_star_ghost_index_y:
                                found_wall_1 = True
                            elif wall_x_index == wall_index_other_2 and wall_y_index == self.a_star_ghost_index_y:
                                found_wall_2 = True

                    # Only allow the a star algorithm if turning a corner that is different from the previous corner.
                    if (not self.prev_turn_node[0] == self.a_star_ghost_index_x or
                            not self.prev_turn_node[1] == self.a_star_ghost_index_y):
                        # If the wall was not found, allow the a star algorithm to take place.
                        if not found_wall_1 or not found_wall_2:

                            ghost_aligned_position_x = self.a_star_ghost_index_x * 16 + 8
                            ghost_aligned_position_y = self.a_star_ghost_index_y * 16 + 8

                            # Check for the existence of a portal. If one exists, go right ahead and decide to either go
                            # through the portal or follow the a star algorithm.
                            # Check if Pac-Man is entering a portal. If so make the player start traveling.
                            if self.can_travel_through_portals and \
                                    not self.run_mode == 2 and \
                                    not self.run_mode == 3 and \
                                    not self.run_mode == 4 and \
                                    self.portal_entrance_1 is not None and \
                                    self.portal_entrance_2 is not None and \
                                    not self.in_portal and \
                                    not self.leaving_portal and \
                                    not self.portal_entrance_1.in_use and \
                                    not self.portal_entrance_2.in_use:

                                # The chance that the ghost will go through the portal.
                                chance_portal = random.randint(0, 3)

                                if chance_portal >= 2:
                                    if self.portal_entrance_1.direction == 0:
                                        ghost_aligned_position_x -= 16
                                    if self.portal_entrance_1.direction == 1:
                                        ghost_aligned_position_x += 16
                                    if self.portal_entrance_1.direction == 2:
                                        ghost_aligned_position_y -= 16
                                    if self.portal_entrance_1.direction == 3:
                                        ghost_aligned_position_y += 16

                                    if ghost_aligned_position_x == self.portal_entrance_1.position_x and \
                                            ghost_aligned_position_y == self.portal_entrance_1.position_y:

                                        self.portal_entrance_1.in_use = True
                                        self.portal_entrance_2.in_use = True
                                        self.run_mode = 2
                                        self.in_portal = True
                                        self.portal_index = 0
                                        self.run_direction = self.portal_entrance_1.direction

                                    else:
                                        ghost_aligned_position_x = self.a_star_ghost_index_x * 16 + 8
                                        ghost_aligned_position_y = self.a_star_ghost_index_y * 16 + 8

                                        if self.portal_entrance_2.direction == 0:
                                            ghost_aligned_position_x -= 16
                                        if self.portal_entrance_2.direction == 1:
                                            ghost_aligned_position_x += 16
                                        if self.portal_entrance_2.direction == 2:
                                            ghost_aligned_position_y -= 16
                                        if self.portal_entrance_2.direction == 3:
                                            ghost_aligned_position_y += 16

                                        if ghost_aligned_position_x == self.portal_entrance_2.position_x and \
                                                ghost_aligned_position_y == self.portal_entrance_2.position_y:

                                            self.portal_entrance_1.in_use = True
                                            self.portal_entrance_2.in_use = True
                                            self.run_mode = 2
                                            self.in_portal = True
                                            self.portal_index = 1
                                            self.run_direction = self.portal_entrance_2.direction

                            if not self.run_mode == 2:
                                self.run_direction = self.a_star()

            # Check if changing direction for the portal animations.
            if self.run_mode == 2:
                if self.in_portal:
                    if self.cur_anim_portal >= self.max_anim_portal:
                        self.cur_anim_portal = 0
                        self.leaving_portal = True
                        self.in_portal = False

                        cur_portal = self.portal_entrance_1

                        if self.portal_index == 0:
                            cur_portal = self.portal_entrance_2

                        self.run_direction = cur_portal.direction

                        if cur_portal.direction == 0:
                            self.run_direction = 1
                        if cur_portal.direction == 1:
                            self.run_direction = 0
                        if cur_portal.direction == 2:
                            self.run_direction = 3
                        if cur_portal.direction == 3:
                            self.run_direction = 2

                        self.position_x = cur_portal.position_x
                        self.position_y = cur_portal.position_y

                        self.sound_manager.play_sound(self.sound_manager.sound5_enter_portal, 5, 0)
                    else:
                        self.cur_anim_portal += 1

                elif self.leaving_portal:
                    if self.cur_anim_portal >= self.max_anim_portal:
                        self.cur_anim_portal = 0
                        self.leaving_portal = False
                        self.run_mode = self.timed_run_mode
                        self.portal_entrance_1.in_use = False
                        self.portal_entrance_2.in_use = False
                        self.prev_turn_node = None
                    else:
                        self.cur_anim_portal += 1

            if self.is_running:
                if self.run_mode == 2:
                    self.current_speed = self.traveling_speed
                elif self.run_mode == 3:
                    self.current_speed = self.vulnerable_speed
                elif self.run_mode == 4:
                    self.current_speed = self.revive_speed
                else:
                    self.current_speed = self.run_speed
                    if self.ghost_type == 0:
                        if self.pacman.dots_eaten >= 100:
                            self.current_speed += 0.1
                            if self.pacman.dots_eaten >= 200:
                                self.current_speed += 0.1

                if self.run_direction == 0:
                    self.position_x -= self.current_speed + self.extra_movement
                elif self.run_direction == 1:
                    self.position_x += self.current_speed + self.extra_movement
                elif self.run_direction == 2:
                    self.position_y -= self.current_speed + self.extra_movement
                elif self.run_direction == 3:
                    self.position_y += self.current_speed + self.extra_movement

            # Process the ghost animation.
            if self.cur_anim_run >= self.max_anim_run:
                self.cur_anim_run = 0
                if self.blink_anim_toggle:
                    self.blink_anim_toggle = False
                elif not self.blink_anim_toggle:
                    self.blink_anim_toggle = True

            if self.dead:
                if self.run_direction == 0:
                    self.image = self.image_eyes_l
                elif self.run_direction == 1:
                    self.image = self.image_eyes_r
                elif self.run_direction == 2:
                    self.image = self.image_eyes_u
                elif self.run_direction == 3:
                    self.image = self.image_eyes_d

            elif self.cur_anim_run == 0:
                if not self.is_vulnerable:
                    if self.run_direction == 0:
                        self.image = self.image_run_l1
                    elif self.run_direction == 1:
                        self.image = self.image_run_r1
                    elif self.run_direction == 2:
                        self.image = self.image_run_u1
                    elif self.run_direction == 3:
                        self.image = self.image_run_d1
                elif self.run_mode == 3:
                    if not self.is_blinking or not self.blink_anim_toggle:
                        self.image = self.image_blue_run1
                    else:
                        self.image = self.image_blue_run3

            elif self.cur_anim_run == 8:
                if not self.is_vulnerable:
                    if self.run_direction == 0:
                        self.image = self.image_run_l2
                    elif self.run_direction == 1:
                        self.image = self.image_run_r2
                    elif self.run_direction == 2:
                        self.image = self.image_run_u2
                    elif self.run_direction == 3:
                        self.image = self.image_run_d2
                elif self.run_mode == 3:
                    if not self.is_blinking or not self.blink_anim_toggle:
                        self.image = self.image_blue_run2
                    else:
                        self.image = self.image_blue_run4

            self.cur_anim_run += 1

            # Process the spawn mode, if there is one.
            if self.spawn_mode == 1:
                if self.ghost_type == 2:
                    if self.position_x > 224:
                        self.spawn_mode = 2
                        self.position_x = 224
                        self.run_direction = 2
                else:
                    if self.position_x < 224:
                        self.spawn_mode = 2
                        self.position_x = 224
                        self.run_direction = 2

            elif self.spawn_mode == 2:
                if self.position_y < 238:
                    self.spawn_mode = 0
                    self.run_mode = self.timed_run_mode
                    self.position_x = 224
                    self.position_y = 238

            elif self.spawn_mode == 3:
                if self.position_y < 270:
                    self.run_direction = 3
                elif self.position_y > 288:
                    self.run_direction = 2
                if self.ghost_type == 2:
                    if self.pacman.dots_eaten >= 30:
                        self.spawn_mode = 1
                        self.run_direction = 1
                else:
                    if self.pacman.dots_eaten >= 90:
                        if self.clyde_wait == 16:
                            self.spawn_mode = 1
                            self.run_direction = 0
                        else:
                            self.clyde_wait += 1

            elif self.spawn_mode == 4:
                if self.position_y > 290:
                    self.spawn_mode = 2
                    self.run_direction = 2
                    self.dead = False

            # Update the collision rect object.
            self.collision_rect.centerx = self.position_x
            self.collision_rect.centery = self.position_y

    def a_star(self):

        self.end_node_reached = False
        self.node_path.clear()
        self.predecessors.clear()

        # First, determine the position of the ghost in the a star map.
        self.a_star_ghost_index_x = int(int(self.position_x) / 16)
        self.a_star_ghost_index_y = int(int(self.position_y) / 16)

        # Check if scattering. If so, move over to the scatter position. If chasing, move over to Pacman's position.
        if self.run_mode == 0:
            # Choose the correct scatter position. They are at the corners of the game window.
            if self.ghost_type == 0:
                self.scatter_index_x = self.scatter_tr_index_x
                self.scatter_index_y = self.scatter_tr_index_y
            elif self.ghost_type == 1:
                self.scatter_index_x = self.scatter_tl_index_x
                self.scatter_index_y = self.scatter_tl_index_y
            elif self.ghost_type == 2:
                self.scatter_index_x = self.scatter_dr_index_x
                self.scatter_index_y = self.scatter_dr_index_y
            elif self.ghost_type == 3:
                self.scatter_index_x = self.scatter_dl_index_x
                self.scatter_index_y = self.scatter_dl_index_y

            self.a_star_end_index_x = self.scatter_index_x
            self.a_star_end_index_y = self.scatter_index_y

        elif self.run_mode == 1:
            if self.ghost_type == 1:
                pacman_extended_position_x = int(int(self.pacman.position_x / 16) * 16) + 8
                pacman_extended_position_y = int(int(self.pacman.position_y / 16) * 16) + 8
                pacman_extended_position_wall_x = pacman_extended_position_x
                pacman_extended_position_wall_y = pacman_extended_position_y
                pacman_extended_position_wall2_x = pacman_extended_position_x
                pacman_extended_position_wall2_y = pacman_extended_position_y
                pacman_extended_position_wall3_x = pacman_extended_position_x
                pacman_extended_position_wall3_y = pacman_extended_position_y
                if self.pacman.run_direction == 0:
                    pacman_extended_position_x -= 64
                    pacman_extended_position_wall_x -= 48
                    pacman_extended_position_wall2_x -= 32
                    pacman_extended_position_wall3_x -= 16
                elif self.pacman.run_direction == 1:
                    pacman_extended_position_x += 64
                    pacman_extended_position_wall_x += 48
                    pacman_extended_position_wall2_x += 32
                    pacman_extended_position_wall3_x += 16
                elif self.pacman.run_direction == 2:
                    pacman_extended_position_y -= 64
                    pacman_extended_position_wall_y -= 48
                    pacman_extended_position_wall2_y -= 32
                    pacman_extended_position_wall3_y -= 16
                elif self.pacman.run_direction == 3:
                    pacman_extended_position_y += 64
                    pacman_extended_position_wall_y += 48
                    pacman_extended_position_wall2_y += 32
                    pacman_extended_position_wall3_y += 16

                found_wall = False

                # Check if a wall is in the way of the extended pacman position:
                for wall in self.walls:
                    if wall.position_x == pacman_extended_position_x and \
                            wall.position_y == pacman_extended_position_y:
                        found_wall = True
                        break
                    if wall.position_x == pacman_extended_position_wall_x and \
                            wall.position_y == pacman_extended_position_wall_y:
                        found_wall = True
                        break
                    if wall.position_x == pacman_extended_position_wall2_x and \
                            wall.position_y == pacman_extended_position_wall2_y:
                        found_wall = True
                        break
                    if wall.position_x == pacman_extended_position_wall3_x and \
                            wall.position_y == pacman_extended_position_wall3_y:
                        found_wall = True
                        break

                # Check if the position is the same as the ghost. If so, pretend it is a wall.
                if pacman_extended_position_x == self.a_star_ghost_index_x * 16 + 8 and \
                        pacman_extended_position_y == self.a_star_ghost_index_y * 16 + 8:
                    found_wall = True
                elif pacman_extended_position_wall_x == self.a_star_ghost_index_x * 16 + 8 and \
                        pacman_extended_position_wall_y == self.a_star_ghost_index_y * 16 + 8:
                    found_wall = True
                elif pacman_extended_position_wall2_x == self.a_star_ghost_index_x * 16 + 8 and \
                        pacman_extended_position_wall2_y == self.a_star_ghost_index_y * 16 + 8:
                    found_wall = True
                elif pacman_extended_position_wall3_x == self.a_star_ghost_index_x * 16 + 8 and \
                        pacman_extended_position_wall3_y == self.a_star_ghost_index_y * 16 + 8:
                    found_wall = True

                if found_wall:
                    self.a_star_end_index_x = int(int(min(447, max(0, self.pacman.position_x))) / 16)
                    self.a_star_end_index_y = int(int(self.pacman.position_y) / 16)
                else:
                    self.a_star_end_index_x = int(int(min(447, max(0, pacman_extended_position_x))) / 16)
                    self.a_star_end_index_y = int(int(pacman_extended_position_y) / 16)
            elif self.ghost_type == 2:
                pacman_extended_position_x = int(int(self.pacman.position_x / 16) * 16) + 8
                pacman_extended_position_y = int(int(self.pacman.position_y / 16) * 16) + 8

                if self.pacman.run_direction == 0:
                    pacman_extended_position_x -= 32
                elif self.pacman.run_direction == 1:
                    pacman_extended_position_x += 32
                elif self.pacman.run_direction == 2:
                    pacman_extended_position_y -= 32
                elif self.pacman.run_direction == 3:
                    pacman_extended_position_y += 32

                blinky_position_x = int(int(self.blinky.position_x / 16) * 16) + 8
                blinky_position_y = int(int(self.blinky.position_y / 16) * 16) + 8

                blinky_vec_x = pacman_extended_position_x - blinky_position_x
                blinky_vec_y = pacman_extended_position_y - blinky_position_y

                blinky_vec_x *= 2
                blinky_vec_y *= 2

                blinky_vec_x += blinky_position_x
                blinky_vec_y += blinky_position_y

                if blinky_vec_x > 456:
                    blinky_vec_x = 456
                elif blinky_vec_x < 8:
                    blinky_vec_x = 8

                if blinky_vec_y > 520:
                    blinky_vec_y = 520
                elif blinky_vec_y < 56:
                    blinky_vec_y = 56

                found_wall = False

                # Check if a wall is in the way of the extended pacman position:
                for wall in self.walls:
                    if wall.position_x == blinky_vec_x and wall.position_y == blinky_vec_y:
                        found_wall = True
                        break

                # Check if the position is the same as the ghost. If so, pretend it is a wall.
                if blinky_vec_x == self.a_star_ghost_index_x * 16 + 8 and \
                        blinky_vec_y == self.a_star_ghost_index_y * 16 + 8:
                    found_wall = True

                # Check if the position is in the same position as an actual node. If not, pretend it is a wall.
                if self.a_star_array[self.compute_index(blinky_vec_x)][self.compute_index(blinky_vec_x)] is None:
                    found_wall = True

                if found_wall:
                    self.a_star_end_index_x = int(int(min(447, max(0, self.pacman.position_x))) / 16)
                    self.a_star_end_index_y = int(int(self.pacman.position_y) / 16)
                else:
                    self.a_star_end_index_x = int(int(min(447, max(0, blinky_vec_x))) / 16)
                    self.a_star_end_index_y = int(int(blinky_vec_y) / 16)

            elif self.ghost_type == 3:
                if abs(self.position_x - self.pacman.position_x) < 128.0 and \
                        abs(self.position_y - self.pacman.position_y) < 128.0:
                    # Choose the correct scatter position. They are at the corners of the game window.
                    self.scatter_index_x = self.scatter_dl_index_x
                    self.scatter_index_y = self.scatter_dl_index_y
                    self.a_star_end_index_x = self.scatter_index_x
                    self.a_star_end_index_y = self.scatter_index_y
                    if not self.clyde_switch_mode_1:
                        self.prev_turn_node = None
                        self.clyde_switch_mode_1 = True
                        self.switched_mode = True
                else:
                    self.a_star_end_index_x = int(int(min(447, max(0, self.pacman.position_x))) / 16)
                    self.a_star_end_index_y = int(int(self.pacman.position_y) / 16)

                    if self.clyde_switch_mode_1:
                        self.prev_turn_node = None
                        self.clyde_switch_mode_1 = False
                        self.switched_mode = True

            else:
                self.a_star_end_index_x = int(int(min(447, max(0, self.pacman.position_x))) / 16)
                self.a_star_end_index_y = int(int(self.pacman.position_y) / 16)

        elif self.run_mode == 3:
            self.a_star_end_index_x = int(int(min(447, max(0, self.pacman.position_x))) / 16)
            self.a_star_end_index_y = int(int(self.pacman.position_y) / 16)

            if self.a_star_end_index_x > self.a_star_ghost_index_x:
                if self.a_star_end_index_y > self.a_star_ghost_index_y:
                    self.scatter_index_x = self.scatter_tl_index_x
                    self.scatter_index_y = self.scatter_tl_index_y
                else:
                    self.scatter_index_x = self.scatter_dl_index_x
                    self.scatter_index_y = self.scatter_dl_index_y
            else:
                if self.a_star_end_index_y > self.a_star_ghost_index_y:
                    self.scatter_index_x = self.scatter_tr_index_x
                    self.scatter_index_y = self.scatter_tr_index_y
                else:
                    self.scatter_index_x = self.scatter_dr_index_x
                    self.scatter_index_y = self.scatter_dr_index_y

            self.a_star_end_index_x = self.scatter_index_x
            self.a_star_end_index_y = self.scatter_index_y

        elif self.run_mode == 4:
            self.a_star_end_index_x = int(int(min(447, max(0, self.ghost_house_entrance.position_x))) / 16)
            self.a_star_end_index_y = int(int(self.ghost_house_entrance.position_y) / 16)

        # A very large number.
        infinity = 99999

        # The number of nodes found.
        num_of_nodes_found = 0

        # Set the distances for the nodes and compute the H values. Also set them to not visited.
        for cur_node_tuple in self.a_star_list:

            index_x = cur_node_tuple[0]
            index_y = cur_node_tuple[1]
            cur_node = cur_node_tuple[2]

            cur_node.value_f = infinity

            # Set all nodes to not visited for the next time the a star algorithm is run.
            cur_node.visited = False

            # Compute the H value for all the nodes.
            cur_node.value_h = abs(index_x - self.a_star_end_index_x) + abs(index_y - self.a_star_end_index_y)

        # The starting node.
        starting_node = self.a_star_array[self.a_star_ghost_index_x][self.a_star_ghost_index_y]

        # Set the distance for the starting node.
        starting_node.value_f = starting_node.value_h

        # Used for checking which children to check distances for.
        use_left_child = True
        use_right_child = True
        use_up_child = True
        use_down_child = True

        # Checks if the first node was already used.
        first_node_used = False

        # Use the greedy algorithm to find the shortest path. Finish once all nodes are visited.
        while num_of_nodes_found < self.max_num_of_nodes_found:

            # The minimum node key.
            min_node_index_x = -1
            min_node_index_y = -1

            # Find the smallest node.
            for cur_node_tuple in self.a_star_list:
                index_x = cur_node_tuple[0]
                index_y = cur_node_tuple[1]
                cur_node = cur_node_tuple[2]

                # Don't choose a node that is already visited or does not exist.
                if cur_node is not None and not cur_node.visited:
                    if min_node_index_x == -1:
                        min_node_index_x = index_x
                        min_node_index_y = index_y

                        # Prevent the ghost from turning around in reverse. If just switched running modes, then
                        # allow the ghost to turn around.
                        if not first_node_used:

                            if not self.switched_mode:
                                if self.run_direction == 0:
                                    use_right_child = False
                                elif self.run_direction == 1:
                                    use_left_child = False
                                elif self.run_direction == 2:
                                    use_down_child = False
                                elif self.run_direction == 3:
                                    use_up_child = False

                            first_node_used = True

                    elif cur_node.value_f < self.a_star_array[min_node_index_x][min_node_index_y].value_f:
                        min_node_index_x = index_x
                        min_node_index_y = index_y

            # Update the distances for the child nodes.
            cur_min_node = self.a_star_array[min_node_index_x][min_node_index_y]

            # The child node from the min node.
            child_node = cur_min_node.child_left
            if child_node is not None:
                if use_left_child:
                    if self.check_child(min_node_index_x, min_node_index_y, cur_min_node, child_node):
                        num_of_nodes_found += 1
                        break
                else:
                    use_left_child = True

            child_node = cur_min_node.child_right
            if child_node is not None:
                if use_right_child:
                    if self.check_child(min_node_index_x, min_node_index_y, cur_min_node, child_node):
                        num_of_nodes_found += 1
                        break
                else:
                    use_right_child = True

            child_node = cur_min_node.child_up
            if child_node is not None:
                if use_up_child:
                    if self.check_child(min_node_index_x, min_node_index_y, cur_min_node, child_node):
                        num_of_nodes_found += 1
                        break
                else:
                    use_up_child = True

            child_node = cur_min_node.child_down
            if child_node is not None:
                if use_down_child:
                    if self.check_child(min_node_index_x, min_node_index_y, cur_min_node, child_node):
                        num_of_nodes_found += 1
                        break
                else:
                    use_down_child = True

            num_of_nodes_found += 1
            cur_min_node.visited = True

        if self.end_node_reached:
            # Construct the path to the destination.

            cur_path_node_index_x = self.a_star_end_index_x
            cur_path_node_index_y = self.a_star_end_index_y

            cur_path_node = self.a_star_array[cur_path_node_index_x][cur_path_node_index_y]

            self.node_path.append(cur_path_node)

            cur_predecessor = None

            if (cur_path_node_index_x, cur_path_node_index_y) in self.predecessors:
                cur_predecessor = self.predecessors[(cur_path_node_index_x, cur_path_node_index_y)]

            while cur_predecessor is not None:
                self.node_path.append(self.a_star_array[cur_predecessor[0]][cur_predecessor[1]])
                if cur_predecessor in self.predecessors:
                    cur_predecessor = self.predecessors[cur_predecessor]
                else:
                    break

            if len(self.node_path) >= 2:
                cur_dir_node = self.node_path[len(self.node_path) - 1]
                next_dir_node = self.node_path[len(self.node_path) - 2]

                dir_node_x = next_dir_node.position_x - cur_dir_node.position_x
                dir_node_y = next_dir_node.position_y - cur_dir_node.position_y

                cur_path_node_index_x = self.compute_index(cur_dir_node.position_x)
                cur_path_node_index_y = self.compute_index(cur_dir_node.position_y)

                # Find out which direction to run.

                # Checks if the ghost can change direction.
                change_direction = False

                # First, check if the ghost can switch on its own tile.
                if self.prev_turn_node is None or \
                        (not self.prev_turn_node[0] == cur_path_node_index_x or
                         not self.prev_turn_node[1] == cur_path_node_index_y):
                    if self.run_direction == 0:
                        if self.position_x < cur_dir_node.position_x:
                            self.extra_movement = 0.0
                            change_direction = True

                    elif self.run_direction == 1:
                        if self.position_x > cur_dir_node.position_x:
                            self.extra_movement = 0.0
                            change_direction = True

                    elif self.run_direction == 2:
                        if self.position_y < cur_dir_node.position_y:
                            self.extra_movement = 0.0
                            change_direction = True

                    elif self.run_direction == 3:
                        if self.position_y > cur_dir_node.position_y:
                            self.extra_movement = 0.0
                            change_direction = True

                if change_direction:
                    # Update the previous turn node.
                    self.prev_turn_node = (cur_path_node_index_x, cur_path_node_index_y)
                    return self.check_a_star_wall(cur_dir_node, dir_node_x, dir_node_y, cur_dir_node.position_x,
                                                  cur_dir_node.position_y)

                else:
                    return self.run_direction
            else:
                return self.run_direction

        else:
            return self.run_direction

    def check_child(self, min_node_index_x, min_node_index_y, cur_min_node, child_node):
        # Update the node distances for the child nodes.
        if not child_node.visited:

            child_node_index_x = self.compute_index(child_node.position_x)
            child_node_index_y = self.compute_index(child_node.position_y)

            child_node_key = (child_node_index_x, child_node_index_y)

            child_node.value_g = cur_min_node.value_g + 1

            # The F value for the a star algorithm.
            value_f = child_node.value_g + child_node.value_h

            # If the f value is smaller than the child node, then update the f value for the child node.
            if value_f + cur_min_node.value_f < child_node.value_f:
                child_node.value_f = value_f

            self.predecessors[child_node_key] = (min_node_index_x, min_node_index_y)

            # Check if the end node has been reached.
            if child_node_index_x == self.a_star_end_index_x and child_node_index_y == self.a_star_end_index_y:
                child_node.value_f = value_f

                self.end_node_reached = True

                cur_min_node.visited = True

                return True

        return False

    def check_a_star_wall(self, cur_dir_node, dir_node_x, dir_node_y, a_star_ghost_position_x, a_star_ghost_position_y):
        # Get the wall that could potentially collide with the point.
        wall = None

        wall_coord_x = cur_dir_node.position_x + dir_node_x
        wall_coord_y = cur_dir_node.position_y + dir_node_y

        for cur_wall in self.walls:
            if cur_wall.position_x == wall_coord_x and cur_wall.position_y == wall_coord_y:
                wall = cur_wall
                break

        if wall is not None:
            # Find out what other directions the ghost can take. Allow the ghost to switch direction 180 degrees if the
            # run mode has been switched.
            if self.switched_mode:
                self.switched_mode = False
                if cur_dir_node.child_left is not None and not dir_node_x < 0:
                    self.position_y = a_star_ghost_position_y
                    return 0
                if cur_dir_node.child_right is not None and not dir_node_x > 0:
                    self.position_y = a_star_ghost_position_y
                    return 1
                if cur_dir_node.child_up is not None and not dir_node_y < 0:
                    self.position_x = a_star_ghost_position_x
                    return 2
                if cur_dir_node.child_down is not None and not dir_node_y > 0:
                    self.position_x = a_star_ghost_position_x
                    return 3
            else:
                if cur_dir_node.child_left is not None and not dir_node_x < 0:
                    if not self.run_direction == 1:
                        self.position_y = a_star_ghost_position_y
                        return 0
                if cur_dir_node.child_right is not None and not dir_node_x > 0:
                    if not self.run_direction == 0:
                        self.position_y = a_star_ghost_position_y
                        return 1
                if cur_dir_node.child_up is not None and not dir_node_y < 0:
                    if not self.run_direction == 3:
                        self.position_x = a_star_ghost_position_x
                        return 2
                if cur_dir_node.child_down is not None and not dir_node_y > 0:
                    if not self.run_direction == 2:
                        self.position_x = a_star_ghost_position_x
                        return 3
        else:
            # Find out which direction to switch to. Also lock the ghost onto the x or y axis of the path. Allow the
            # ghost to switch direction 180 degrees if the run mode has been switched.
            if self.switched_mode:
                self.switched_mode = False
                if dir_node_x < 0:
                    self.position_y = a_star_ghost_position_y
                    return 0
                elif dir_node_x > 0:
                    self.position_y = a_star_ghost_position_y
                    return 1
                elif dir_node_y < 0:
                    self.position_x = a_star_ghost_position_x
                    return 2
                elif dir_node_y > 0:
                    self.position_x = a_star_ghost_position_x
                    return 3
                else:
                    return self.run_direction
            else:
                if dir_node_x < 0 and not self.run_direction == 1 and not self.run_direction == 0:
                    self.position_y = a_star_ghost_position_y
                    return 0
                elif dir_node_x > 0 and not self.run_direction == 0 and not self.run_direction == 1:
                    self.position_y = a_star_ghost_position_y
                    return 1
                elif dir_node_y < 0 and not self.run_direction == 3 and not self.run_direction == 2:
                    self.position_x = a_star_ghost_position_x
                    return 2
                elif dir_node_y > 0 and not self.run_direction == 2 and not self.run_direction == 3:
                    self.position_x = a_star_ghost_position_x
                    return 3
                else:
                    return self.run_direction

    @staticmethod
    def compute_index(position_i):
        return int(int(position_i - 8) / 16)
