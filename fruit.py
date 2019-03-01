from game_object import GameObject
import random

import pygame


class Fruit(GameObject):
    def __init__(self, x, y, score, fruit_image, score_image):
        super(Fruit, self).__init__(x, y)
        self.fruit_image = fruit_image
        self.score_image = score_image
        self.image = None
        self.score = score
        self.cur_spawn_time = 0
        self.position_x = x
        self.position_y = y

        random.seed()

        self.max_spawn_time = 500 + random.randint(-100, 100)
        self.cur_despawn_time = 0
        self.max_despawn_time = 600 + random.randint(-50, 50)
        self.spawning = True
        self.despawning = False
        self.eaten = False
        self.cur_eaten_time = 0
        self.max_eaten_time = 50

        self.image_rect = pygame.Rect(x - 16, y - 16, 32, 32)

        self.collision_rect = pygame.Rect(x - 4, y - 4, 8, 8)

        self.collision_rect.centerx = self.position_x
        self.collision_rect.centery = self.position_y

    def update_obj(self):
        if not self.eaten:
            if self.spawning:
                if self.cur_spawn_time >= self.max_spawn_time:
                    self.despawning = True
                    self.spawning = False
                    self.image = self.fruit_image
                self.cur_spawn_time += 1

            if self.despawning:
                if self.cur_despawn_time >= self.max_despawn_time:
                    self.despawning = False
                    self.image = None
                else:
                    self.cur_despawn_time += 1
        else:
            self.image = self.score_image

            if self.cur_eaten_time >= self.max_eaten_time:
                self.image = None
                self.cur_eaten_time = self.max_eaten_time
            else:
                self.cur_eaten_time += 1
