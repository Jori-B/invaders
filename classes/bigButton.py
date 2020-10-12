# Should be inherited from button

import pygame
from utilities.constants import *

offset = 3

class BigButton():
    def __init__(self, color, x, y, width, height, font, img, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.img = img

    def draw(self, window, outline=None, shadow=None):
        # To draw the button, this method is called
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 3)

        if shadow:
            # Draw a shadow below the button
            pygame.draw.rect(window, BLACK, (self.x + offset, self.y + offset, self.width, self.height), 0)
        # Draw the button
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.img != None:
            window.blit(self.img, (
            self.x + self.width / 2 - self.img.get_width() / 2, self.y + self.height - self.img.get_height() - 50))

        if self.text != "":
            font = self.font
            text = font.render(self.text, 1, WHITE)
            # Centers text in the middle of the button
            window.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + text.get_height()))

    def isHovered(self, position):
        X = 0
        Y = 1
        # Position is the mouse position or a tuple of (x, y) coordinates
        if self.x < position[X] < self.x + self.width:
            if self.y < position[Y] < self.y + self.height:
                return True
        return False

