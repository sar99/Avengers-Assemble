import pygame
from pygame.sprite import Sprite

import game_functions as gf

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.life=3
        self.bump_sound=pygame.mixer.Sound('sound/bump.wav')
        self.boom_sound=pygame.mixer.Sound('sound/boom.wav') 
         

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load('img/spaceship.bmp')
        self.image1 = pygame.image.load('img/spaceship_red.bmp')
        self.image2 = pygame.image.load('img/spaceship_darkred.bmp')


        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.left = 0
        self.rect.top = 0

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True    


    def update(self,ai_settings,screen,ship,aliens):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        if(self.life==2):
            self.image=self.image1
        elif(self.life==1):
            self.image=self.image2
        if (ai_settings.this_row>=self.rect.height):
            ai_settings.this_row=0
            gf.create_fleet(ai_settings, screen, ship, aliens)
            
    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
