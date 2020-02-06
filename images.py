import pygame
import game_functions as gf


class Images():

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.image = pygame.image.load('img/page2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def change_image(self):

        if self.ai_settings.images==3:
            self.image = pygame.image.load('img/page1.png')
            self.ai_settings.images-=1
        elif self.ai_settings.images==2:
            self.image = pygame.image.load('img/page3.png')
            self.ai_settings.images-=1
        elif self.ai_settings.images==1:
            self.image = pygame.image.load('img/page4.bmp')
            self.ai_settings.images-=1
        elif self.ai_settings.images==0:
            self.image = pygame.image.load('img/blank.png')
            self.ai_settings.state=True
            self.ai_settings.images-=1
            
    def blitme(self):
        self.screen.blit(self.image, self.rect)
