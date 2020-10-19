import os
import pygame
import time
import random
import string

# WIDTH, HEIGHT = infoObject.current_w-20, infoObject.current_h-40
WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# TODO: This should probably go somewhere else
pygame.display.set_caption("Multiplication Invaders")
# A way to completely go full screen (however when using two displays it, just like the above, it grows too big
# src.display.set_mode((0, 0), src.FULLSCREEN)

WELCOME_TEXT = pygame.image.load(os.path.join("assets", "welcome_msg.png"))
GHOST_BOY = pygame.image.load(os.path.join("assets", "mascot.png"))
MENU_TEXT = pygame.image.load(os.path.join("assets/menu", "header.png"))
MENU_SHIP = pygame.image.load(os.path.join("assets/menu", "menu_ship.png"))
# Colors
BACKGROUND_GREY = (59, 56, 56, 0)
BACKGROUND_WHITE = (255, 255, 255,0)
BLACK = (0, 0, 0, 0.5)
BLACK_NON_TRANSPARENT = (0, 0, 0)
WHITE = (255, 255, 255)
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
# PLAYER_SHIP = pygame.image.load(os.path.join("assets/ships", "lord_nelson_purple.png"))
def choose_ship(name, color):
    ship_img_string = name + "_" + color + ".png"
    return pygame.image.load(os.path.join("assets/ships", ship_img_string))

NELSON = pygame.image.load(os.path.join("assets/ships", "lord_nelson_purple.png"))
COMMANDER = pygame.image.load(os.path.join("assets/ships", "commander_cosmonaut_purple.png"))
POINTY_BOY = pygame.image.load(os.path.join("assets/ships", "pointy_boy_purple.png"))
DONUT = pygame.image.load(os.path.join("assets/ships", "donut_warrior_purple.png"))


# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow_1.png"))

# Heart icon
LIFE = pygame.image.load(os.path.join("assets", "heart.png"))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))
BACKGROUND_SLIM = pygame.transform.scale(pygame.image.load(os.path.join("assets", "WhiteWallpaper.png")), (WIDTH, HEIGHT))

NUMPAD = pygame.image.load(os.path.join("assets", "keypad.png"))
SPACEBAR = pygame.image.load(os.path.join("assets", "spacebar.png"))

# Answer Box
ANSWER_BOX = pygame.image.load(os.path.join("assets", "answer_button.png"))
CORRECT_IMG = pygame.image.load(os.path.join("assets", "correct.png"))
INCORRECT_IMG = pygame.image.load(os.path.join("assets", "incorrect.png"))

LOCK = pygame.image.load(os.path.join("assets", "padlock.png"))
LOCK_SMALL = pygame.image.load(os.path.join("assets", "padlock_small.png"))

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

DISAPPEAR_ANIMATION = {}
DISAPPEAR_ANIMATION['small'] = []
DISAPPEAR_ANIMATION['large'] = []
# Images are numbered so we can loop through them
for i in range(5):
    file_name = 'spaceshipPuff0{}.png'.format(i)
    img = pygame.image.load(os.path.join("assets/disappear", file_name)).convert()
    img.set_colorkey(BLACK_NON_TRANSPARENT)
    img_large = pygame.transform.scale(img, (75, 75))
    DISAPPEAR_ANIMATION['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    # TODO: Small explosion should be used for when alien hits spaceship
    DISAPPEAR_ANIMATION['small'].append(img_small)

all_sprites = pygame.sprite.Group()

REAPPEAR_ANIMATION = {}
REAPPEAR_ANIMATION['small'] = []
REAPPEAR_ANIMATION['large'] = []
# Images are numbered so we can loop through them
for i in range(5):
    file_name = 'spaceshipPuff0{}.png'.format(5-i)
    img = pygame.image.load(os.path.join("assets/disappear", file_name)).convert()
    img.set_colorkey(BLACK_NON_TRANSPARENT)
    img_large = pygame.transform.scale(img, (75, 75))
    REAPPEAR_ANIMATION['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    # TODO: Small explosion should be used for when alien hits spaceship
    REAPPEAR_ANIMATION['small'].append(img_small)

all_sprites = pygame.sprite.Group()

MOVE_ANIMATION = {}
MOVE_ANIMATION['small'] = []
MOVE_ANIMATION['large'] = []
# Images are numbered so we can loop through them
for i in range(5):
    file_name = 'spaceshipPuff0{}.png'.format(i)
    img = pygame.image.load(os.path.join("assets/moveup", file_name)).convert()
    img.set_colorkey(BLACK_NON_TRANSPARENT)
    img_large = pygame.transform.scale(img, (75, 75))
    MOVE_ANIMATION['large'].append(img_large)
    img_small = pygame.transform.scale(img, (32, 32))
    # TODO: Small explosion should be used for when alien hits spaceship
    MOVE_ANIMATION['small'].append(img_small)

all_sprites = pygame.sprite.Group()

START_TIME = int(round(time.time() * 1000))
PATH = "Save_Data/temp_merged_save_data.csv"
FINAL_PATH = f"Save_Data/experiment_data_subject_{random.choice(string.ascii_letters)}{START_TIME % 1000}.csv"

ID_CODE_1 = f"{random.choice(string.ascii_letters)}{START_TIME % 1000}"
ID_CODE_2 = f"{random.choice(string.ascii_letters)}{START_TIME % 1001}"
while ID_CODE_1 == ID_CODE_2:
    ID_CODE_2 = f"{random.choice(string.ascii_letters)}{START_TIME % 1001}"
