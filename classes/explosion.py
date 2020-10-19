from utilities.constants import *
from classes.text import Text

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, score):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = EXPLOSION_ANIMATION[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.score = score



    def update(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # If we are at the last picture of the animation
            if self.frame == len(EXPLOSION_ANIMATION[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = EXPLOSION_ANIMATION[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                if self.score:
                    score_font = pygame.font.SysFont("Arial", 25)
                    score_font_rendered = score_font.render("+" + str(self.score), 1, WHITE)
                    width_text = score_font_rendered.get_width()
                    x, y = self.rect.center
                    WINDOW.blit(score_font_rendered, (x - width_text/2, y + 40))
