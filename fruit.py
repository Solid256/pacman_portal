from game_object import GameObject
import random

import pygame


class Fruit(GameObject):
    def __init__(self, x, y, score, fruit_image, score_image):
        """The init function for initializing the default values."""
        super(Fruit, self).__init__(x, y)

        # Checks if the fruit is spawning.
        self.spawning = True

        # Checks if the fruit is despawning.
        self.despawning = False

        # Checks if the fruit is eaten.
        self.eaten = False

        # Set the random seed for creating random integers.
        random.seed()

        # The current spawn time for the fruit to spawn.
        self.cur_spawn_time = 0

        # The max spawn time for the fruit to appear.
        self.max_spawn_time = 500 + random.randint(-100, 100)

        # The current spawn time for the fruit to appear.
        self.cur_despawn_time = 0

        # The max despawn time for the fruit to disappear.
        self.max_despawn_time = 600 + random.randint(-50, 50)

        # The score of the fruit.
        self.score = score

        # The current time for being eaten.
        self.cur_eaten_time = 0

        # The maximum time for being eaten.
        self.max_eaten_time = 50

        # The position x for the fruit.
        self.position_x = x

        # The position y for the fruit.
        self.position_y = y

        # The image for the fruit.
        self.fruit_image = fruit_image

        # The image for the score.
        self.score_image = score_image

        # The image being used for rendering.
        self.image = None

        # The image rect for the fruit image.
        self.image_rect = pygame.Rect(x - 16, y - 16, 32, 32)

        # The collision rect for the fruit image.
        self.collision_rect = pygame.Rect(x - 4, y - 4, 8, 8)

        # Set the collision rect position x.
        self.collision_rect.centerx = self.position_x

        # Set the collision rect position y.
        self.collision_rect.centery = self.position_y

    def update_obj(self):
        """Used for updating the game object."""

        # If the fruit was not eaten, decide when to spawn the fruit.
        if not self.eaten:

            # Only spawn the fruit once it is spawning.
            if self.spawning:

                # If the current spawn time is larger than or equal to the max spawn time, spawn the fruit.
                if self.cur_spawn_time >= self.max_spawn_time:

                    # Set the fruit despawning to true.
                    self.despawning = True

                    # Set the fruit spawning to false.
                    self.spawning = False

                    # Set the fruit image so that it appears on the screen.
                    self.image = self.fruit_image

                else:
                    # Increment the spawn time.
                    self.cur_spawn_time += 1

            # If the fruit is despawning, check if it has despawned.
            if self.despawning:

                # Check if the current despawn time is larger than or equal to the max despawn time.
                if self.cur_despawn_time >= self.max_despawn_time:

                    # Set despawning to false.
                    self.despawning = False

                    # Set the image to none to make the fruit disappear.
                    self.image = None
                else:
                    # increment the current despawn time.
                    self.cur_despawn_time += 1
        else:
            # If eaten, set the fruit image to the score image.
            self.image = self.score_image

            # If the current eaten time is larger than or equal to the maximum eaten time, then set the image to none.
            if self.cur_eaten_time >= self.max_eaten_time:

                # Set the image to none to make the fruit score disappear.
                self.image = None

                # Set the current eaten time to the maximum eaten time.
                self.cur_eaten_time = self.max_eaten_time
            else:
                # Increment the current eaten time.
                self.cur_eaten_time += 1
