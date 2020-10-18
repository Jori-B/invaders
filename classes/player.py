import random
from classes.ship import Ship
from utilities.constants import *


# Inherits from player (so all the things from player are also in player)
class Player(Ship):
    def __init__(self, x, y, ship, stats, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)

        self.ship_img = ship
        self.laser_img = pygame.image.load(
            os.path.join("assets", "pixel_laser_yellow_" + str(stats.laser_width) + ".png"))
        # Mask for pixel perfect collision instead of square collision box
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    shots_fired = 'NA'

    # Checks whether laser hit an enemy
    def move_lasers(self, velocity, objs, window):
        # When you move the lasers check if cooldown is finished
        self.shots_fired = self.cooldown()
        # For each laser that the player has
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # For each enemy in the objects list if it collides with the laser remove it
                for obj in objs:
                    if laser.collision(obj):

                        # Make sure that the laser you want to remove actually exists in the list
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        return True, obj
        return False, "no enemy shot"

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # Red rectangle
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 20,
                                               self.ship_img.get_width(), 10))
        # Green rectangle
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 20,
                                               self.ship_img.get_width() * (self.health / self.max_health), 10))


