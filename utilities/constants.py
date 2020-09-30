import os
import pygame

# WIDTH, HEIGHT = infoObject.current_w-20, infoObject.current_h-40
WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# TODO: This should probably go somewhere else
pygame.display.set_caption("Multiplication Invaders")
# A way to completely go full screen (however when using two displays it, just like the above, it grows too big
# src.display.set_mode((0, 0), src.FULLSCREEN)

# Colors
BLACK = (0, 0, 0, 0.5)
BLACK_NON_TRANSPARENT = (0, 0, 0)
WHITE = (225, 225, 255)
PURPLE = (108, 99, 255)
DARK_BLUE = (83, 109, 254)
RED = (245, 0, 87)
LIGHT_BLUE = (0, 176, 255)
GREEN = (0, 191, 166)
ORANGE = (249, 168, 38)


# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

# Answer Box
ANSWER_BOX = pygame.image.load(os.path.join("assets", "answer_button.png"))

# Explosion dictionary (dic: has names instead of numbers) animation which is looped through in small and large scale
EXPLOSION_ANIMATION = {}
EXPLOSION_ANIMATION['small'] = []
EXPLOSION_ANIMATION['large'] = []
# Images are numbered so we can loop through them
for i in range(9):
    file_name = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join("assets/explosion", file_name)).convert()
    img.set_colorkey(BLACK_NON_TRANSPARENT)
    img_large = pygame.transform.scale(img, (75, 75))
    EXPLOSION_ANIMATION['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    # TODO: Small explosion should be used for when alien hits spaceship
    EXPLOSION_ANIMATION['small'].append(img_small)

all_sprites = pygame.sprite.Group()

