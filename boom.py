import pygame
from pygame.sprite import Sprite


class Boom(Sprite):
	def __init__(self,screen,alien):
		super(Boom, self).__init__()
		self.screen=screen
		# Load the ship image, and get its rect.
		self.image = pygame.image.load('img/boom.bmp')
		self.rect = self.image.get_rect()
		self.rect.centerx=alien.rect.centerx
		self.rect.centery=alien.rect.centery
		self.time = pygame.time.get_ticks()
        
		
		 
	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)


