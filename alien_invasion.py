import pygame
from pygame.sprite import Group

from settings import Settings
import game_functions as gf
from ship import Ship
from alien import Alien
from boom import Boom
from images import Images

def run_game():
	# Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Avengers Assemble")

    #Make a ship
    ship = Ship(ai_settings, screen)
    # Make an alien.
    alien = Alien(ai_settings, screen)
    image = Images(ai_settings, screen)
    
    bullets = Group()
    aliens = Group()
    booms=Group()

    # Create the fleet of aliens.
    

    

	# Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship,bullets,image)
        gf.update_screen(ai_settings, screen ,ship,aliens, bullets,booms
        ,image)
        if ai_settings.state:
            ship.update(bullets)
            gf.update_bullets(ai_settings, screen, ship,
                              bullets,aliens,booms)
            gf.update_aliens(aliens, ai_settings,screen,ship,bullets,image)
            gf.update_speed(ai_settings, screen ,ship,aliens, bullets,booms
        ,image)
            gf.update_boom(booms,ai_settings)



run_game()

