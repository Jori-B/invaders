# Should be inherited from button

import pygame
from utilities.constants import *
from classes.stats import Stats

offset = 3


class BigButton:
    def __init__(self, color, x, y, width, height, font, img, show_stats=False, ship="", text="", is_locked=False, unlock_text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.img = img
        self.show_stats = show_stats
        self.is_locked = is_locked
        self.small_font = pygame.font.SysFont("notosansmonocjkkr", 25)
        if is_locked:
            self.unlock_text = unlock_text
        if show_stats:
            self.stats = Stats(ship)

    def getXMiddle(self, widthOfObject):
        return self.x + self.width / 2 - widthOfObject / 2

    def getYMiddle(self, heightOfObject):
        return self.y + self.height / 2 - heightOfObject / 2

    def drawStatBar(self, bar_x, bar_y, bar_height, current_stat, window):
        bar_width = self.width * (2 / 5)
        # Since there are 4 levels of stats height, 1/4th of the bar width indicates level 1
        stat_bar_width = (1/4) * bar_width
        # This number is then multiplied by the current stat's level [1, 2, 3, 4]
        if current_stat == "speed":
            stat_bar_width = self.stats.ship_speed * stat_bar_width
        if current_stat == "width":
            stat_bar_width = self.stats.laser_width * stat_bar_width
        if current_stat == "laser_speed":
            stat_bar_width = self.stats.laser_speed * stat_bar_width
        # Black rectangle
        pygame.draw.rect(window, BLACK_NON_TRANSPARENT, (bar_x, bar_y + bar_height / 2,
                                                         bar_width, bar_height))
        # Green rectangle: indicates the level of stats
        pygame.draw.rect(window, GREEN, (bar_x, bar_y + bar_height / 2,
                                         stat_bar_width, bar_height))

    def draw(self, window, outline=None, shadow=None):
        # To draw the button, this method is called
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)

        if shadow:
            # Draw a shadow below the button
            pygame.draw.rect(window, BLACK, (self.x + offset, self.y + offset, self.width, self.height), 0)

        # Draw the button
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = self.font
            text = font.render(self.text, 1, WHITE)
            # Centers text in the middle of the button
            window.blit(text, (self.getXMiddle(text.get_width()), self.y + text.get_height()))

            if self.show_stats:

                stats_x = self.x + 20
                speed_text_y = self.y + text.get_height() * 3
                laser_width_text_y = speed_text_y + 50
                laser_speed_text_y = laser_width_text_y + 50
                speed_text = self.small_font.render("Speed:", 1, WHITE)
                laser_width_text = self.small_font.render("Laser size:", 1, WHITE)
                laser_speed_text = self.small_font.render("Laser speed:", 1, WHITE)
                # Centers text in the middle of the button
                window.blit(speed_text, (stats_x, speed_text_y))
                window.blit(laser_width_text, (stats_x, laser_width_text_y))
                window.blit(laser_speed_text, (stats_x, laser_speed_text_y))
                # Set the bars next to the stats text (laser speed has the largest width so it is used to indicate x)
                bar_x = stats_x + laser_speed_text.get_width() + 10
                bar_height = text.get_height() / 2

                self.drawStatBar(bar_x, speed_text_y, bar_height, "speed", window)
                self.drawStatBar(bar_x, laser_width_text_y, bar_height, "width", window)
                self.drawStatBar(bar_x, laser_speed_text_y, bar_height, "laser_speed", window)


        if self.img is not None:
            window.blit(self.img, (self.getXMiddle(self.img.get_width()), self.y + self.height - self.img.get_height() - 50))

        if self.is_locked:
            # Draw a semi-transparant button on top of the previous one when the item is locked
            s = pygame.Surface((self.width, self.height))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((0, 0, 0))  # this fills the entire surface
            window.blit(s, (self.x, self.y))  # (0,0) are the top-left coordinates
            # Draw a lock image on top of the button
            window.blit(LOCK, (self.getXMiddle(LOCK.get_width()), self.getYMiddle(LOCK.get_height())))

            unlock_text = self.small_font.render(self.unlock_text, 1, WHITE)
            unlock_text_y = self.y + self.height + unlock_text.get_height() / 2
            window.blit(unlock_text, (self.getXMiddle(unlock_text.get_width()), unlock_text_y))



    def isHovered(self, position):
        X = 0
        Y = 1
        # Position is the mouse position or a tuple of (x, y) coordinates
        if self.x < position[X] < self.x + self.width:
            if self.y < position[Y] < self.y + self.height:
                return True
        return False

    def hoverEffect(self, position):
        if self.isHovered(position):
            self.color = DARK_BLUE
        else:
            self.color = BACKGROUND_GREY
