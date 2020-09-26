from classes.ship import Ship
from classes.laser import Laser
from utilities.constants import *


class Enemy(Ship):
    # Pass a color to the color map to get the corresponding img
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    # Enemies also have a color attribute
    def __init__(self, x, y, color, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Move the ship downward when this is called
    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        # Only shoot laser if the cooldown counter is 0
        if self.cool_down_counter == 0:
            # Offset the laser x position a little so it comes from the center of the enemy ship
            laser = Laser(self.x + 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1