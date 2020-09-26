import pygame
from utilities.constants import *

offset = 3

class Button():
    def __init__(self, color, x, y, width, height, font, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self, window, outline=None):
        # To draw the button, this method is called
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        # Draw a shadow below the button
        pygame.draw.rect(window, BLACK, (self.x + offset, self.y + offset, self.width, self.height), 0)
        # Draw the button
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)


        if self.text != "":
            font = self.font
            text = font.render(self.text, 1, WHITE)
            # Centers text in the middle of the button
            window.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))

    def isHovered(self, position):
        X = 0
        Y = 1
        # Position is the mouse position or a tuple of (x, y) coordinates
        if position[X] > self.x and position[X] < self.x + self.width:
            if position[Y] > self.y and position[Y] < self.y + self.height:
                return True
        return False

