from utilities.constants import *

class Move(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = MOVE_ANIMATION[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # If we are at the last picture of the animation
            if self.frame == len(MOVE_ANIMATION[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = MOVE_ANIMATION[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center