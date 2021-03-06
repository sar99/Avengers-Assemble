import sys
import pygame
import random

from bullet import Bullet
from alien import Alien
from time import sleep
from boom import Boom
from images import Images

def check_keydown_events(event, ai_settings, screen, ship,bullets,images):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_RETURN:
        if ai_settings.images>=0:
            images.change_image()
    elif event.key == pygame.K_q:
        sys.exit()


    

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship,bullets,images):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship,bullets
            ,images)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)



def update_screen(ai_settings, screen,ship, aliens, bullets,booms,images):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.blit(ai_settings.bg,ai_settings.bg_rect)
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    booms.draw(screen)
    images.blitme()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        new_bullet.bullet_sound.play()
        bullets.add(new_bullet)
        

def update_bullets(ai_settings, screen, ship, bullets,aliens,booms):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    #collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for bullet in bullets.sprites():
        for alien in aliens.sprites():
            if (bullet.rect.top <= alien.rect.bottom) and (
            bullet.rect.left>=alien.rect.left) and (
            bullet.rect.right<=alien.rect.right) and (
            bullet.rect.top > alien.rect.top):
                alien.life-=1
                bullets.remove(bullet)
                if alien.life==0:
                    boom = Boom(screen,alien)
                    alien.boom_sound.play()
                    booms.add(boom)
                    if len(aliens)<2:
                        aliens.empty()
                    else:
                        aliens.remove(alien)
                else:
                    alien.bump_sound.play()


    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    ai_settings.this_row+=ai_settings.fleet_drop_speed

            
            
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height  #+ 2 * alien.rect.height * row_number
    aliens.add(alien)



def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens.
    #for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
        r = random.randrange(0,1000)
        if r%3==0 or r%5==0 or r%4==0:
            create_alien(ai_settings, screen, aliens, alien_number)

def ship_hit(ai_settings, screen, ship, aliens, bullets,images):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    ai_settings.lives -= 1
    ai_settings.hit=True
    if ai_settings.lives<=0:
        ai_settings.final=False
        end_game(ai_settings,screen,images)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    sleep(0.5)
    # Create a new fleet and center the ship.
    
    ship.rect.centerx=screen.get_rect().centerx


    


def update_aliens(aliens , ai_settings,screen,ship,bullets,images):
    """Update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update(ai_settings,screen,ship,aliens)
    if not aliens:
        ai_settings.this_row=0
        create_fleet(ai_settings, screen, ship, aliens)
        if not ai_settings.hit:
            ai_settings.win+=1
        ai_settings.hit=False
        if(ai_settings.win==3):
            ai_settings.final=True
            end_game(ai_settings,screen,images)
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, aliens, bullets,images)
    for alien in aliens.sprites():
        if alien.rect.bottom>=ai_settings.screen_height:
            ship_hit(ai_settings, screen, ship, aliens, bullets,images)
            break

def update_boom(booms,ai_settings):
	tick=pygame.time.get_ticks()
	for boom in booms.sprites():
		if tick-boom.time>=ai_settings.boom_time:
			booms.remove(boom)


def update_speed(ai_settings, screen ,ship,aliens, bullets,booms
        ,image):
    tick=pygame.time.get_ticks()
    if tick-ai_settings.time>40000:
        ai_settings.ship_speed_factor*=1.1 
        ai_settings.bullet_speed_factor*=1.1
        ai_settings.alien_speed_factor*=1.1
        ai_settings.fleet_drop_speed*=1.1
        ai_settings.bullets_allowed+=1
        ai_settings.time=pygame.time.get_ticks()


def end_game(ai_settings,screen,images):
    ai_settings.state=False
    images.image=pygame.image.load('img/lose.bmp')
    if ai_settings.final:
	    images.image=pygame.image.load('img/win.bmp')

        
