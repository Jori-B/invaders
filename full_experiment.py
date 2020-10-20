from experiments.invaders import *
from experiments.default_experiment import *
import pygame
import random
import numpy as np
import pandas as pd
from classes.button import Button
from classes.bigButton import BigButton
from classes.rectangle import Rectangle
from utilities.constants import *
from utilities.main_functions import *
from classes.endScreen import *
from classes.saveData import *

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
                    group_num = 1


                    done = default_main_menu(group_num)

                    print("FULL EXPERIMENT")
                    print(done)

                    if done == True:

                    # TODO: add break 
                        break_screen(group_num, "0000")
                        main_menu(group_num)
                        end_screen("1")
                        exit()
                elif two_button.isHovered(position):
                    group_num = 2
                    # This should be removed?
                    done = main_menu(group_num)

                    print("FULL EXPERIMENT")
                    print(done)

                    if done == True:
                    # TODO: add break 
                        break_screen(group_num, "0000")

                        default_main_menu(group_num)
                        end_screen("2")
                        exit()



def break_screen(group_number, questionnaire_code):
    font_size = 25
    break_font = pygame.font.SysFont("Arial", font_size)
    link_font = pygame.font.SysFont("Arial", font_size * 2)
    break_text = "You can now take a short break. During this break,\n" \
                 "we ask you to fill out a questionnaire.\n" \
                 f"In it, pease enter \"{ID_CODE_1}\" under Experiment Code.\n" \
                 "Go to the questionnaire using the following link: "
    link_text = "https://forms.gle/" + str(questionnaire_code)
    link_label = link_font.render(link_text, 1, WHITE)
    max_y_text = render_multi_line(break_text, 150, 70, font_size + 5, break_font)
    link_y = max_y_text + link_label.get_height()
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    button_width = 180
    button_height = 60
    img_y = link_y + 100


    continue_text = "After filling in the questionnaire, press continue"
    continue_label = break_font.render(continue_text, 1, DARK_BLUE)
    continue_text_y = img_y + GHOST_BOY.get_height() + continue_label.get_height() * 2

    continue_btn_y = continue_text_y + continue_label.get_height() * 3

    continue_btn = Button(BACKGROUND_GREY, get_middle_x(button_width), continue_btn_y,
                          button_width, button_height, button_font, "Continue")


    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        render_multi_line(break_text, 150, 50, font_size + 5, break_font)
        WINDOW.blit(link_label,
                    (get_middle_x(link_label), link_y))
        WINDOW.blit(GHOST_BOY, (get_middle_x(GHOST_BOY), img_y))
        WINDOW.blit(continue_label,
                    (get_middle_x(continue_label), continue_text_y))
        continue_btn.draw(WINDOW, WHITE)

        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                continue_btn.hoverEffect(position)

            # if continue button is pressed then start the next phase of the experiment
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Based on the condition bring the user to someplace
                if continue_btn.isHovered(position):
                    run = False
                    # if group_number == 1:
                    #     main(group_number)
                    #     print("main(group_num=group_number)")
                    # if group_number == 2:
                    #     default_experiment(group_number)
                    #     print("default_experiment(group_num=group_number)")

full_exp_main_menu()



