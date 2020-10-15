import pygame
from utilities.main_functions import *

class Laser:
    def __init__(self, x, y, img):
        # TODO: These coordinates need to be placed in the center of the space ship
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        # Return a false value when the y position is higher than the height of screen (starts at top with 0)
        return not(self.y <= height and self.y >= -30)

    def collision(self, obj):
        # Is an object colliding with the object that called the function
        return collide(self, obj)