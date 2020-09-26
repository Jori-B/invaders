import pygame

def collide(obj1, obj2):
    # distance top left hand corner ojbect 2 - 1
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # src function overlap determines if two imgs' masks are overlapping
    # it returns and (x,y) collision point if they are overlapping, else none
    # Convert the floating point pixels values we get from the sharp images to integers
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None
