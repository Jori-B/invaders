from utilities.constants import *

offset = 3

# TODO: Button should inherit from rectangle
class Rectangle():
    def __init__(self, color, x, y, width, height, font, font2, has_two_texts, text="", text2=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text2 = text2
        self.has_two_texts = has_two_texts
        self.font = font
        self.font2 = font2

    def draw(self, window, outline=None):
        # To draw the rectangle, this method is called
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        # Draw a shadow below the rectangle
        pygame.draw.rect(window, BLACK, (self.x + offset, self.y + offset, self.width, self.height), 0)
        # Draw the button
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)


        if self.text != "":
            font = self.font
            text = font.render(self.text, 1, BLACK_NON_TRANSPARENT)

            if not self.has_two_texts:
                # Centers text in the middle of the box
                window.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))
            else:
                # Put the text in the top and bottom
                window.blit(text, (
                self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 4 - text.get_height() / 4))
                text2 = self.font2.render(self.text2, 1, RED)
                window.blit(text2, (
                    self.x + self.width / 2 - text.get_width() / 2, self.y + (self.height / 4) * 3 - (text.get_height() / 4) * 3 - 5) )