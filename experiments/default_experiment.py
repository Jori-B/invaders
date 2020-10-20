
import pandas as pd
from classes.button import Button
from classes.rectangle import Rectangle
from classes.model import Model
from slimstampen.spacingmodel import Response
from utilities.constants import *
from utilities.main_functions import *
from classes.saveData import *

MAX_ANS_LEN = 10

# initialize font usage
pygame.font.init()
pygame.init()

# How big is our window going to be, dimensions depend on the screen preventing windows to be too big
infoObject = pygame.display.Info()

# The minutes and seconds when someone started are defined globally. Namely, if someone pressed the
# menu during the game, then the minutes and seconds should still count as having passed.
minutes_start = 11
seconds_start = 59
start_ticks = 0

def default_main(group_num):
    global minutes_start
    global seconds_start
    global start_ticks

    # Dictates if while loop is going to run
    run = True
    # Amount of frames per second (checking if character is moving once every second)
    FPS = 60

    main_font = pygame.font.SysFont("notosansmonocjkkr", 30)

    if group_num == 1:
        block = 1
        trial_nr = 0
    else:
        block = 2
        if os.path.isfile("Save_Data/temp_game_data.csv"):
            trial_nr = pd.read_csv("Save_Data/temp_game_data.csv").shape[0]
    game_data = pd.DataFrame()
    is_gamification = False

    # Define reference to Model class
    model = Model()
    if not default_main.has_been_called:
        model.add_facts_for_block(group_number=group_num, block=block)
    default_main.has_been_called = True

    clock = pygame.time.Clock()

    if start_ticks == 0:
        start_ticks = pygame.time.get_ticks()  # starter tick

    answering_question = False

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

        timer = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds since the start
        minutes = minutes_start - int(timer / 60)  # divide seconds by 60 to get the amount of minutes
        seconds = (seconds_start - int(timer)) % 60  # % the seconds passed so that only seconds are shown

        WINDOW.blit(BACKGROUND, (0, 0))

        # If the specified time is up the user should switch to the break screen
        # The second statement is a failsafe for when the time.sleep() function cause the timer to run back to 59 sec again
        if (minutes <= 0 and seconds <= 0) or (minutes <= 0 and seconds_start - int(timer) < 0):
            if not game_data.empty:
                model_data = model.save_model_data()
                save_data = pd.merge(model_data, game_data, on='trial', how='outer')
                save_data.to_csv(PATH, index=False)
            save_full_experiment_data()
            print("Experiment done")
            # code = "0000"
            run = False
            return True

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
            new_fact = model.get_next_fact(group_number=group_num, block=block)
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
                        d = {'trial': trial_nr, 'block': block, 'group_number': group_num,
                             'is_gamification': [is_gamification], 'answer_given': string}

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
    return False

default_main.has_been_called = False


def default_main_menu(group_num):

    done = False

    button_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    button_width = 400
    button_height = 80
    button_x = WIDTH / 2 - button_width / 2
    start_button_y = 3 * HEIGHT / 4
    start_button = Button(BACKGROUND_GREY, button_x, start_button_y, button_width,
                          button_height, button_font, "Start game!")
    if group_num == 1:
        explanation_general = "This is the standard SlimStampen block of the experiment. \n\n" \
                              "In the upcoming block you will solve multiplication questions. \n" \
                              "After 12 minutes there is a break in which you will be asked. \n" \
                              "to fill out a questionnaire about you experience with the \n" \
                              "task and the SlimStampen program. \n" \
                              "Have fun and good luck!"
    else:
        explanation_general = "Next is the standard SlimStampen block of the experiment. \n\n" \
                              "In the upcoming block you will again solve multiplication \n" \
                              "questions. After 12 minutes you will again to be asked \n" \
                              "to fill out a questionnaire about you experience with the \n" \
                              "task and the SlimStampen program. \n" \
                              "Have fun and good luck!"

    font_size = 25
    explanation_font_general = pygame.font.SysFont("Arial", font_size)
    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        start_button.draw(WINDOW, WHITE)
        WINDOW.blit(GHOST_BOY, (get_middle_x(GHOST_BOY), HEIGHT / 2 - 30))
        render_multi_line(explanation_general, 200, 50, font_size + 5, explanation_font_general)
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                pygame.quit()
                sys.exit()
                run = False
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                start_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isHovered(position):
                    return default_main(group_num)

    # pygame.quit()
    return False

#default_main_menu()
