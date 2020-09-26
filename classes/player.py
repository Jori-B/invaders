from classes.ship import Ship
from utilities.constants import *

# Inherits from player (so all the things from player are also in player)
class Player(Ship):
    def __init__(self, x, y, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Mask for pixel perfect collision instead of square collision box
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # Checks whether laser hit an enemy
    def move_lasers(self, velocity, objs, window):
        # When you move the lasers check if cooldown is finished
        self.cooldown()
        # For each laser that the player has
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # For each enemy in the objects list if it collides with the laser remove it
                for obj in objs:
                    if laser.collision(obj):
                        # TODO: Add multiplication showing and check if answer is correct or wrong
                        main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
                        answer = ""
                        answer_label = main_font.render(f"4 x 6 = {answer}", 1, (0, 0, 0))
                        upper_label = main_font.render(f"Enter the kill code below", 1, (152, 76, 62))
                        string = ""
                        # src.draw.rect(WINDOW,(0,0,255),(WIDTH/2 - answer_label.get_width()/2, HEIGHT/2 - answer_label.get_height()/2,answer_label.get_width()+50,answer_label.get_height()))
                        window.blit(ANSWER_BOX, (
                        WIDTH / 2 - ANSWER_BOX.get_width() / 2, HEIGHT / 2 - ANSWER_BOX.get_height() / 2,
                        ANSWER_BOX.get_width() + 50, ANSWER_BOX.get_height()))
                        window.blit(answer_label, (
                        WIDTH / 2 - ANSWER_BOX.get_width() / 2 + 30, HEIGHT / 2 + answer_label.get_height() / 4))
                        window.blit(upper_label, (
                        WIDTH / 2 - ANSWER_BOX.get_width() / 2 + 30, HEIGHT / 2 - 1.5 * answer_label.get_height()))
                        pygame.display.update()

                        while True:
                            event = pygame.event.poll()
                            keys = pygame.key.get_pressed()

                            if event.type == pygame.KEYDOWN:
                                key = pygame.key.name(event.key)  # Returns string id of pressed key.

                                if len(key) == 1:  # This covers all letters and numbers not on numpad.
                                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                                        # if  # Include any other shift characters here.
                                        # else:
                                        string += key.upper()
                                    else:
                                        string += key
                                # elif  # Include any other characters here.
                                elif key == "backspace":
                                    # TODO: Make this work by erasing the current string
                                    string = string[:-1]
                                elif event.key == pygame.K_RETURN:  # Finished typing.
                                    break

                                text = main_font.render(string, 1, (108, 99, 255))
                                window.blit(text, (WIDTH / 2 - answer_label.get_width() / 2 + 40,
                                                   HEIGHT / 2 + answer_label.get_height() / 4))
                                pygame.display.update()

                        objs.remove(obj)
                        # Make sure that the laser you want to remove actually exists in the list
                        if laser in self.lasers:
                            self.lasers.remove(laser)

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
