import pygame, sys, random
from pygame.locals import *
from assets import *
from pygame.sprite import Sprite, Group

FPS = 60
BLANK = None

pygame.display.set_caption("Space Invaders")

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


# Class for Game
class Game:
    def __init__(self, Invader_group, SpaceShip, Projectile_group_inv, Projectile_group_spa):
        # Create a game class with all the groups
        self.invader_group = Invader_group
        self.projectile_group_invaders = Projectile_group_inv
        self.projectile_group_spaceship = Projectile_group_spa
        self.spaceship = SpaceShip
        self.game_active = True

    def update(self, DISPLAY_SURFACE):
        self.projectile_invader_collision()
        
        for invader in self.invader_group:
            invader.update(self)

        self.projectile_movement()
        spaceship_collision(self)
        
    def projectile_invader_collision(self):
        collisions = pygame.sprite.groupcollide(self.projectile_group_spaceship, self.invader_group, True, True)
        
        for invader_list in collisions.values():
            for invader in invader_list:
                invader.kill()
                
    def projectile_movement(self):
        if self.game_active:
            self.projectile_group_invaders.update()
            self.projectile_group_invaders.draw(DISPLAY_SURFACE)

            self.projectile_group_spaceship.update()
            self.projectile_group_spaceship.draw(DISPLAY_SURFACE)


# Class for SpaceShip

class SpaceShip(pygame.sprite.Sprite):  # Here we are inheriting from the pygame.sprite.Sprite class
    def __init__(self):
        super().__init__()
        # The order of self.image: load image -> resize image -> rotate image
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(SPACESHIP_IMG).convert_alpha(), (
        int(WINDOW_WIDTH * 0.15), int(WINDOW_WIDTH * 0.15))), 180.0)
        # The order of self.rect: get rect from image -> set rect position
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 75))
        self.health = 3


# Class for Invader 
class Invader(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        # Same order as SpaceShip
        self.image = pygame.transform.scale(pygame.image.load(INVADER_IMG).convert_alpha(),
                                            (int(WINDOW_WIDTH * 0.10), int(WINDOW_WIDTH * 0.10)))
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def update(self, game: Game):
        if random.randint(0, 1000) == 1:
            # Create a projectile
            shoot_projectile(game=game, position=(self.x, self.y), direction=1, speed=4)


# Class for Projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, direction, speed):
        super().__init__()
        # create a surface with the size of 5x10
        self.image = pygame.Surface((5, 10))
        # fill the surface with red color
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=position)
        self.speed = direction * speed

    def update(self):
        """"Move projectile by given distance of speed"""
        self.rect.y += self.speed
        # If projectile goes off the screen, remove it
        if self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT:
            self.kill()  # Remove the projectile if it goes off the screen


def handle_keypress(event, game: Game):
    # check if the key pressed is left or right
    if event == pygame.K_LEFT:
        game.spaceship.rect.x -= 10
    elif event == pygame.K_RIGHT:
        game.spaceship.rect.x += 10
    elif event == pygame.K_SPACE:
        if not game.projectile_group_spaceship.sprites():
            shoot_projectile(game, position=game.spaceship.rect.midtop, direction=-1)


def shoot_projectile(game: Game, position, direction, speed=10):
    # Create a projectile and add it to the projectile group
    projectile = Projectile(position, direction, speed)
    if direction == 1:
        game.projectile_group_invaders.add(projectile)
    elif direction == -1:
        game.projectile_group_spaceship.add(projectile)


def terminate():
    # End pygame and programme
    pygame.quit()
    sys.exit()


def load_background(DISPLAY_SURFACE):
    # Load the background image and scale it to the size of the window
    DISPLAY_SURFACE.blit(source=pygame.transform.scale(pygame.image.load(BACKGROUND_IMG).convert_alpha(),
                                                       size=(WINDOW_HEIGHT, WINDOW_HEIGHT)),
                         dest=(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH))


def spaceship_collision(game: Game):
    value = pygame.sprite.spritecollide(sprite=game.spaceship, group=game.projectile_group_invaders, dokill=True)
    if value:
        game.spaceship.health -= 1
        if game.spaceship.health == 0:
            print(game.spaceship.health)
            """ -- -- -- -- Place for an end of the game -- -- -- -- """
            game.game_active = False

def title_screen_animation(game: Game):
    invader_sprite_group = pygame.sprite.Group()
    for _ in range(10):
        invader = Invader(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        invader_sprite_group.add(invader)

    font = pygame.font.Font(FONT_PATH, BASIC_FONT_SIZE)
    game_title=font.render("Space Invaders",True,(255,255,255))
    start_text=font.render("Press SPACE to Start",True,(255,255,255))

    highlighted_surface_title = pygame.Surface((game_title.get_width(), game_title.get_height()))
    highlighted_surface_title.fill((0, 0, 0))
    highlighted_surface_start = pygame.Surface((start_text.get_width(), start_text.get_height()))
    highlighted_surface_start.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.QUIT:
                pygame.quit()

        load_background(DISPLAY_SURFACE=DISPLAY_SURFACE)
        invader_sprite_group.update(game)
        invader_sprite_group.draw(DISPLAY_SURFACE)

        for invader in invader_sprite_group:
            invader.rect.x += 1
            if invader.rect.left > WINDOW_WIDTH:
                invader.rect.right = 0
            """invader.rect.x += random.randint(-1, 1)
            invader.rect.y += random.randint(-1, 1)
            invader.rect.x = max(0, min(invader.rect.x, WINDOW_WIDTH - invader.rect.width))
            invader.rect.y = max(0, min(invader.rect.y, WINDOW_HEIGHT - invader.rect.height))"""

        DISPLAY_SURFACE.blit(highlighted_surface_title, (WINDOW_WIDTH // 2 - game_title.get_width() // 2, 200))
        DISPLAY_SURFACE.blit(game_title, (WINDOW_WIDTH // 2 - game_title.get_width() // 2, 200))
        
        DISPLAY_SURFACE.blit(highlighted_surface_start, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, 300))
        DISPLAY_SURFACE.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, 300))

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS, BLANK

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    load_background(DISPLAY_SURFACE=DISPLAY_SURFACE)

    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)


    
    spaceship = SpaceShip()
    invaders_list = [Invader(x_pos=x * 85, y_pos=y * 60) for x in range(1, 7) for y in range(1, 4)]
    invader_sprite_group = Group()
    for invader in invaders_list:
        invader_sprite_group.add(invader)

    # Create the game object
    main_game = Game(Invader_group=invader_sprite_group, SpaceShip=spaceship, Projectile_group_inv=Group(),
                     Projectile_group_spa=Group())
    title_screen_animation(game=main_game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.KEYDOWN:
                handle_keypress(event=event.key, game=main_game)

        load_background(DISPLAY_SURFACE=DISPLAY_SURFACE)
        DISPLAY_SURFACE.blit(spaceship.image, spaceship.rect)
        invader_sprite_group.draw(DISPLAY_SURFACE)

        # Update and draw projectiles
        main_game.update(DISPLAY_SURFACE=DISPLAY_SURFACE)  # Update projectile positions

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
