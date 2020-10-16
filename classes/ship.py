from classes.laser import Laser
from utilities.constants import *

# Abstract class (no usage only inheriting from it). Namely, enemy and player player are both similar
class Ship:
    # Half a second since FPS is 60
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.health = health
        # Cool down is so that the user can't just spam the laser
        self.cool_down_counter = 0

    def draw(self, window):
        # Draw something red on the window, where it's going to be and how wide , 0 means filling in
        # src.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Is used for player and the enemy, however in player it checks wheter it hit an enemy
    def move_lasers(self, velocity, obj):
        # When you move the lasers check if cooldown is finished
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # Every time player is hit 10 hitpoints are removed
                obj.health -= 10
                # After a hit the laser needs to be removed again
                self.lasers.remove(laser)

    def stop_lasers(self):

        for laser in self.lasers.copy():
            del laser

        self.lasers = []


    # Handles counting the cooldown, before a laser can be shot again
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        # Only shoot laser if the cooldown counter is 0
        if self.cool_down_counter == 0:
            # if self.ship_img.get_width()<=100:
            laser = Laser(self.x+(abs(self.ship_img.get_width())/2) - (self.laser_img.get_width() / 2), self.y, self.laser_img)
            # else:
            #     laser = Laser(self.x+(abs(self.ship_img.get_width())/2), self.y, self.laser_img)

            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
