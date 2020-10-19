from classes.button import Button
from utilities.constants import *


# Inherits from button (so all the things from player are also in player)
class MenuButton(Button):
    def __init__(self, color, x, y, width, height, font):
        # Use button's initialization method
        super().__init__(color, x, y, width, height, font)

    # Overwriting the draw method of button
    def draw(self, window, outline, shadow=None):
        # Draw a rectangle with an outline
        pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)

        offset = 3
        if shadow:
            # Draw a shadow below the button
            pygame.draw.rect(window, BLACK, (self.x + offset, self.y + offset, self.width, self.height), 0)

        # Draw the button
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        # draw a straight line
        for height in range(1, 4):
            startpos = (self.x + (self.width / 5), self.y + self.height * (height / 4))
            endpos = (self.x + self.width - (self.width / 5), self.y + self.height * (height / 4))
            pygame.draw.line(window, WHITE, startpos, endpos, 2)



