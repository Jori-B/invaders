from utilities.constants import *
import pygame

def collide(obj1, obj2):
    # distance top left hand corner ojbect 2 - 1
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # src function overlap determines if two imgs' masks are overlapping
    # it returns and (x,y) collision point if they are overlapping, else none
    # Convert the floating point pixels values we get from the sharp images to integers
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def get_middle_x(object):
    if isinstance(object, int):
        return WIDTH / 2 - object / 2
    else:
        return WIDTH / 2 - object.get_width() / 2

def render_multi_line(text, x, y, fsize, font):
    lines = text.splitlines()
    x_all = 0
    for i, l in enumerate(lines):
        label = font.render(l, 1, WHITE)
        if not x_all:
            x_all = get_middle_x(label)
        WINDOW.blit(label, (x_all, y + fsize * i))
        max_y = y + fsize * i
    return max_y