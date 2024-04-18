import pygame
from pygame.locals import *
import sys
import random
from assets import *  # Assuming you have defined SPACESHIP_IMG and INVADER_IMG in assets.py
from pygame.sprite import Sprite, Group

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60
BLANK = None

# constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# global variable to be used in multiple functions, default value is None
FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None
BASIC_FONT_SIZE = 30
BUTTONS = None


# Main idea is to create a class with attributes of Sprite
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(SPACESHIP_IMG).convert_alpha(), (int(WINDOW_WIDTH * 0.2), int(WINDOW_WIDTH * 0.2))), 180.0)
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT-75))
    

class Invader(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.image = pygame.transform.scale(pygame.image.load(INVADER_IMG).convert_alpha(), (int(WINDOW_WIDTH * 0.10), int(WINDOW_WIDTH * 0.10)))
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    
class Game:
    def __init__(self, Invader_group, SpaceShip: SpaceShip, Projectile_group):
        self.invader_group = Invader_group
        self.spaceship = SpaceShip
        self.projectile_group = Projectile_group


class Projectile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Adjust the size as needed
        self.image.fill((255, 0, 0))  # Red color for the projectile
        self.rect = self.image.get_rect(midbottom=position)
        self.speed = 10  # Adjust the speed of the projectile as needed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()  # Remove the projectile if it goes off the screen



def handle_keypress(event, game: Game):
    if event == pygame.K_LEFT:
        game.spaceship.rect.x -= 10
    elif event == pygame.K_RIGHT:
        game.spaceship.rect.x += 10
    elif event == pygame.K_SPACE:
        shoot_projectile(game)


def shoot_projectile(game: Game):
    projectile = Projectile(game.spaceship.rect.midtop)
    game.invader_group.add(projectile)
    

def terminate():
    pygame.quit()
    sys.exit()    


def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS, BLANK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    spaceship = SpaceShip()
    invaders_list = [Invader(x_pos=x*85, y_pos= y*60) for x in range(1,7) for y in range(1,4)]
    invader_sprite_group = Group()
    for invader in invaders_list:
        invader_sprite_group.add(invader)

    projectile_sprite_group = Group()  # Create a sprite group for projectiles

    main_game = Game(Invader_group=invader_sprite_group, SpaceShip=spaceship, Projectile_group = projectile_sprite_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.KEYDOWN:
                handle_keypress(event=event.key, game=main_game)

        DISPLAY_SURFACE.fill((0, 0, 0))
        DISPLAY_SURFACE.blit(spaceship.image, spaceship.rect)
        invader_sprite_group.draw(DISPLAY_SURFACE)

        # Update and draw projectiles
        projectile_sprite_group.update()
        projectile_sprite_group.draw(DISPLAY_SURFACE)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
