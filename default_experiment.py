# Based on https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=UnityCoin
import random
import numpy as np
import pandas as pd
from classes.button import Button
from classes.bigButton import BigButton
from classes.rectangle import Rectangle
from classes.player import Player
from classes.enemy import Enemy
from classes.explosion import Explosion
from classes.disappear import Disappear
from classes.reappear import Reappear
from classes.move import Move
from classes.model import Model
from slimstampen.spacingmodel import Response
from utilities.constants import *
from utilities.main_functions import *

# import utility

MAX_ANS_LEN = 10

# initialize font usage
pygame.font.init()
pygame.init()

# How big is our window going to be, dimensions depend on the screen preventing windows to be too big
infoObject = pygame.display.Info()


def main():
    # Dictates if while loop is going to run
    run = True
    # Amount of frames per second (checking if character is moving once every second)
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    lost_font = pygame.font.SysFont("notosansmonocjkkr", 60)
    # If you want to know which fonts are available
    # print(src.font.get_fonts())

    # Define reference to Model class
    model = Model()

    block = 1  # else: block = 2
    game_data = pd.DataFrame()
    trial_nr = 0
    is_gamification = False

    clock = pygame.time.Clock()

    answering_question = False
    enemy_hit = None

    def show_answer(is_correct, answer, x, y):

        if is_correct:
            text = "Correct!"
            correct_img = CORRECT_IMG
            main_font_size = 30
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, main_font, False, text)
            correct_box.draw(WINDOW, None, False)
        else:
            text = "Incorrect! Answer was: "
            correct_img = INCORRECT_IMG
            main_font_size = 20
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            answer_font = pygame.font.SysFont("notosansmonocjkkr", 30)

            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, answer_font, True, text,
                                    str(answer), )
            correct_box.draw(WINDOW, None, False)

        WINDOW.blit(correct_img, (
            x, y + 15,
            correct_img.get_width() + 50, correct_img.get_height()))

        pygame.display.update()
        # Show the correct answer for 2 seconds
        time.sleep(3)

    while run:
        clock.tick(FPS)
        WINDOW.blit(BACKGROUND_SLIM, (0, 0))

        # No more lives or health then you lost
        # If there are no more enemies on screen then

        # Check for all events (keypresses, mouseclick, etc.
        events = pygame.event.get()
        for event in events:
            # if the 'x' on the right top is pressed the game is quit
            if event.type == pygame.QUIT:
                # Merge and save data from model and game in case the game is completely closed
                if not game_data.empty:
                    model_data = model.save_model_data()
                    save_data = pd.merge(model_data, game_data, on='trial', how='outer')
                    save_data.to_csv(PATH, index=False)
                # YOU COULD CHANGE THIS TO quit() to press 'x' and quit the program
                run = False

        # Laser velocity needs to be negative since the y value is lower upwards the screen, meaning laser will go up
        # TODO: Extra parameter SlimStampen question
        # has_hit_enemy, enemy = player.move_lasers(-laser_velocity, enemies, WINDOW)
        if not answering_question:

            # Record question onset time
            question_onset_time_for_RT_calc = int(round(time.time() * 1000))
            question_onset_time = question_onset_time_for_RT_calc - START_TIME
            # Get a new question from the model
            new_fact = model.get_next_fact()
            answer = f"{new_fact[2]}"
            present_alt_question = int(random.uniform(0.001, 1.999))
            if present_alt_question == 0:
                question = f"{new_fact[1]} = "
            else:
                question = f"{new_fact[3]} = "
            # TODO: Add multiplication showing and check if answer is correct or wrong
            main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
            string = ""

            answering_question = True

        if answering_question:

            # Slow down enemies by 50% while answering a question
            code_text = str("Enter the answer below")
            x = WIDTH / 2 - ANSWER_BOX.get_width() / 2
            y = HEIGHT / 2 - ANSWER_BOX.get_height() / 2
            width = 400
            height = 150

            correct_box = Rectangle(WHITE, x, y, width, height, main_font, main_font, True, code_text, str(question),
                                    RED, BLACK_NON_TRANSPARENT)
            correct_box.draw(WINDOW, None, False)

            txt_surface = main_font.render(string, True, pygame.Color('black'))
            txt_y = y + (height / 4) * 3 - (txt_surface.get_height() / 4) * 3 - 5
            WINDOW.blit(
                txt_surface,
                (
                    width + 150 + 100, txt_y  # heigth + 237.25
                )
            )

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        # Record response time
                        response_time = int(round(time.time() * 1000)) - question_onset_time_for_RT_calc
                        # Log the response
                        # Stringify answer instead of typecasting string as int (since a string might not
                        # be castable)
                        if str(answer) == string:
                            print("Correct!")
                            resp = Response(new_fact, question_onset_time, response_time, True)
                            model.m.register_response(resp)
                            # kill_enemy(enemy_hit)
                        else:
                            print("Wrong! The correct answer was " + str(answer))
                            resp = Response(new_fact, question_onset_time, response_time, False)
                            model.m.register_response(resp)
                            # runaway_enemy(enemy_hit, enemies, WINDOW)

                        if os.path.isfile('Save_Data/temp_basic_slimstampen_data.csv'):
                            game_data = pd.read_csv('Save_Data/temp_basic_slimstampen_data.csv')
                            trial_nr = game_data['trial'].iloc[-1]
                        trial_nr += 1
                        d = {'trial': trial_nr, 'block': block, 'is_gamification': [is_gamification],
                             'answer_given': string}

                        if game_data.empty:
                            game_data = pd.DataFrame(data=d)
                        else:
                            game_data = game_data.append(d, ignore_index=True)
                            game_data.to_csv("Save_Data/temp_basic_slimstampen_data.csv", index=False)

                        show_answer(str(answer) == string, answer, x, y + ANSWER_BOX.get_height())

                        # Update enemy velocity according to the amount of facts that have been seen
                        # enemy_velocity = 0.5 + (
                        # model.get_count_seen_facts(int(round(time.time() * 1000)) - START_TIME) * 0.1)

                        answering_question = False
                        enemy_hit = None

                        string = ''
                    elif event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    elif len(string) < MAX_ANS_LEN and 48 <= event.key <= 57:
                        string += str(event.key - 48)

        pygame.display.update()


def main_menu():
    button_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    button_width = 400
    button_height = 80
    button_x = WIDTH / 2 - button_width / 2
    start_button_y = 3 * HEIGHT / 4
    start_button = Button(BACKGROUND_GREY, button_x, start_button_y, button_width,
                          button_height, button_font, "Start game!")

    run = True
    while run:

        WINDOW.blit(BACKGROUND_SLIM, (0, 0))
        start_button.draw(WINDOW, WHITE)

        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                run = False
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                start_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isHovered(position):
                    main()
    pygame.quit()


def save_full_experiment_data():
    if os.path.isfile(PATH):
        experiment_data = pd.read_csv(PATH)
        # if os.path.isfile(FINAL_PATH):
        #     old_experiment_data = pd.read_csv(FINAL_PATH)
        #     experiment_data = old_experiment_data.append(experiment_data, ignore_index=True)
        os.remove(PATH)
        experiment_data.to_csv(FINAL_PATH, index=False)


if os.path.isfile('Save_Data/temp_basic_slimstampen_data.csv'):
    os.remove("Save_Data/temp_basic_slimstampen_data.csv")

main_menu()
