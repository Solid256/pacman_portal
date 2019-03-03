import pygame


class SoundManager:
    def __init__(self):
        self.song_ready = None
        self.song_blinky_1 = None
        self.song_blinky_2 = None
        self.song_blinky_3 = None
        self.song_flee = None
        self.song_revive = None
        self.song_pacman_die = None
        self.sound1_pacdot_1 = None
        self.sound1_pacdot_2 = None
        self.sound2_fruit = None
        self.sound3_eat_ghost = None
        self.sound4_fire_portal = None
        self.sound5_enter_portal = None
        self.sound6_generate_portal = None
        self.sound7_extra_life = None

        self.channel_song = None
        self.channel_1 = None
        self.channel_2 = None
        self.channel_3 = None
        self.channel_4 = None
        self.channel_5 = None
        self.channel_6 = None
        self.channel_7 = None

    def init(self):
        # Initialize the mixer with mono sound and a 4096 size music buffer.
        pygame.mixer.init(44100, -16, 1, 1024)

        self.channel_song = pygame.mixer.Channel(0)
        self.channel_1 = pygame.mixer.Channel(1)
        self.channel_2 = pygame.mixer.Channel(2)
        self.channel_3 = pygame.mixer.Channel(3)
        self.channel_4 = pygame.mixer.Channel(4)
        self.channel_5 = pygame.mixer.Channel(5)
        self.channel_6 = pygame.mixer.Channel(6)
        self.channel_7 = pygame.mixer.Channel(7)

    def load_sounds(self):
        # Load all of the sounds and music.

        self.song_ready = pygame.mixer.Sound("audio/pacman_ready.ogg")
        self.song_blinky_1 = pygame.mixer.Sound("audio/blinky_1.ogg")
        self.song_blinky_2 = pygame.mixer.Sound("audio/blinky_2.ogg")
        self.song_blinky_3 = pygame.mixer.Sound("audio/blinky_3.ogg")
        self.song_flee = pygame.mixer.Sound("audio/flee.ogg")
        self.song_revive = pygame.mixer.Sound("audio/revive.ogg")
        self.song_pacman_die = pygame.mixer.Sound("audio/pacman_die.ogg")
        self.sound1_pacdot_1 = pygame.mixer.Sound("audio/pacdot_1.ogg")
        self.sound1_pacdot_2 = pygame.mixer.Sound("audio/pacdot_2.ogg")
        self.sound2_fruit = pygame.mixer.Sound("audio/eat_fruit.ogg")
        self.sound3_eat_ghost = pygame.mixer.Sound("audio/eat_ghost.ogg")
        self.sound4_fire_portal = pygame.mixer.Sound("audio/portal_shot.ogg")
        self.sound5_enter_portal = pygame.mixer.Sound("audio/portal_enter.ogg")
        self.sound6_generate_portal = pygame.mixer.Sound("audio/portal_open.ogg")
        self.sound7_extra_life = pygame.mixer.Sound("audio/extra_life.ogg")

    def play_sound(self, sound, channel_index, loop):
        if channel_index == 0:
            self.channel_song.play(sound, loop)
        if channel_index == 1:
            self.channel_1.play(sound, loop)
        if channel_index == 2:
            self.channel_2.play(sound, loop)
        if channel_index == 3:
            self.channel_3.play(sound, loop)
        if channel_index == 4:
            self.channel_4.play(sound, loop)
        if channel_index == 5:
            self.channel_5.play(sound, loop)
        if channel_index == 6:
            self.channel_6.play(sound, loop)
        if channel_index == 7:
            self.channel_7.play(sound, loop)
