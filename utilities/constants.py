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