import pygame

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1400
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)
        
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 12
        self.bg=pygame.image.load('img/space.png')
        self.bg_rect=self.bg.get_rect()

        self.this_row=0
        
        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,255,255
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed_factor = 8
        
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        self.boom_time=1000
     
        self.lives=3
        self.images=3
        self.state=False
        self.win=0
        self.final=True
        self.hit=False
        self.time = pygame.time.get_ticks()
