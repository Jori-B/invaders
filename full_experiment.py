import random
import numpy as np
import pandas as pd
from classes.button import Button
from classes.bigButton import BigButton
from classes.rectangle import Rectangle
from utilities.constants import *
from utilities.main_functions import *
from default_experiment import *
from invaders import *
import sys

pygame.font.init()
pygame.init()

def full_exp_main_menu():

    font_size = 35
    explanation_font = pygame.font.SysFont("Arial", font_size)

    welcome_text = "WELCOME TO THIS EXPERIMENT ! "
    welcome_text_label = explanation_font.render(welcome_text, 1, DARK_BLUE)
    select_group = "Please select your group number: " 
    select_group_label = explanation_font.render(select_group, 1, WHITE)

    button_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    button_width = 200
    button_height = 80
    one_x = 2 * WIDTH / 6 - button_width / 2
    one_y = 2 * HEIGHT / 3
    one_button= Button(BACKGROUND_GREY, one_x, one_y, button_width,
                          button_height, button_font, " 1 ")

    two_x = 4 * WIDTH / 6 - button_width / 2
    two_y = 2 * HEIGHT / 3
    two_button= Button(BACKGROUND_GREY, two_x, two_y, button_width,
                          button_height, button_font, " 2 ")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        # WINDOW.blit(welcome_text_label, (get_middle_x(welcome_text_label), HEIGHT/3))
        WINDOW.blit(WELCOME_TEXT, (get_middle_x(WELCOME_TEXT), HEIGHT / 3))
        WINDOW.blit(select_group_label, (get_middle_x(select_group_label), HEIGHT/3 + 80))

        one_button.draw(WINDOW, WHITE)
        two_button.draw(WINDOW, WHITE)

        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                # save_full_experiment_data()

                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                one_button.hoverEffect(position)
                two_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if one_button.isHovered(position):
                    default_main_menu()

                    # TODO: add break 

                    main_menu()
                elif two_button.isHovered(position):
                    # This should be removed?
                    main_menu()


                    # TODO: add break 

                    default_main_menu()



full_exp_main_menu()