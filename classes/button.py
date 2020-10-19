import pygame
from utilities.constants import *

offset = 3


class Button():
    def __init__(self, color, x, y, width, height, font, text="", is_locked=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.is_locked = is_locked
        self.small_font = pygame.font.SysFont("notosansmonocjkkr", 15)

    def getXMiddle(self, widthOfObject):
        return self.x + self.width / 2 - widthOfObject / 2

    def getYMiddle(self, heightOfObject):
        return self.y + self.height / 2 - heightOfObject / 2

    def draw(self, window, outline=None, shadow=None, text_color=WHITE):
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
            text = font.render(self.text, 1, text_color)
            # Centers text in the middle of the button
            window.blit(text, (
            self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

        if self.is_locked:
            # Draw a semi-transparant button on top of the previous one when the item is locked
            s = pygame.Surface((self.width, self.height))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((0, 0, 0))  # this fills the entire surface
            window.blit(s, (self.x, self.y))  # (0,0) are the top-left coordinates
            # Draw a lock image on top of the button
            window.blit(LOCK_SMALL, (self.x + 20, self.getYMiddle(LOCK_SMALL.get_height())))

            unlock_text = self.small_font.render("Not available in experimental version", 1, WHITE)
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
            self.color = GREEN
        else:
            self.color = BACKGROUND_GREY
