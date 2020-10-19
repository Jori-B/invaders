# Based on https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=UnityCoin
import random
import os
import sys
import pandas as pd
import numpy as np
from classes.button import Button
from classes.bigButton import BigButton
from classes.menuButton import MenuButton
from classes.rectangle import Rectangle
from classes.player import Player
from classes.enemy import Enemy
from classes.explosion import Explosion
from classes.disappear import Disappear
from classes.reappear import Reappear
from classes.move import Move
from classes.model import Model
from classes.stats import Stats
from slimstampen.spacingmodel import Response
from classes.aboutScreen import *
from utilities.constants import *
from utilities.main_functions import *

MAX_ANS_LEN = 10

# initialize font usage
pygame.font.init()
pygame.init()

# How big is our window going to be, dimensions depend on the screen preventing windows to be too big
infoObject = pygame.display.Info()

# The minutes and seconds when someone started are defined globally. Namely, if someone pressed the
# menu during the game, then the minutes and seconds should still count as having passed.
minutes_start = 0
seconds_start = 2
start_ticks = 0


def create_new_player(ship, stats):
    player = Player(WIDTH / 2, HEIGHT, ship, stats)
    # Center the ship on screen
    player.x -= (player.get_width() / 2)
    player.y -= (player.get_height() + 50)
    return player


def main(ship, ship_name, ship_color, group_num):
    global minutes_start
    global seconds_start
    global start_ticks

    # Dictates if while loop is going to run
    run = True
    # Amount of frames per second (checking if character is moving once every second)
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    # lost_font = pygame.font.SysFont("notosansmonocjkkr", 60)
    # If you want to know which fonts are available
    # print(src.font.get_fonts())

    # Setting variables for data recording
    # if this_is_the_first_block:
    if group_num == 1:
        block = 2
    else:
        block = 1
    game_data = pd.DataFrame()
    trial_nr = 0
    temp_shots_fired = 0
    temp_lives = lives
    is_gamification = True

    # Define reference to Model class
    model = Model()
    if not main.has_been_called:
        model.add_facts_for_block(group_number=group_num, block=block)
    main.has_been_called = True

    enemies = []
    # Every level a new wave will be created of 5 enemies
    wave_length = 5
    enemy_velocity = 0.5
    stats = Stats(ship_name)

    # How fast the player can move every time you press the key a max of 5 pixels to move
    player_velocity = 4 + stats.ship_speed
    laser_velocity = 4
    player_laser_velocity = 3 + stats.laser_speed

    # Define a player space ship at location
    player = create_new_player(ship, stats)

    clock = pygame.time.Clock()

    if start_ticks == 0:
        start_ticks = pygame.time.get_ticks()  # starter tick

    lost = False
    lost_count = 0

    correct_count = 0
    total_count = 0
    score = 0

    answering_question = False
    enemy_hit = None

    def show_answer(is_correct, answer, x, y):

        if is_correct:
            text = "Correct!"
            correct_img = CORRECT_IMG
            main_font_size = 30
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, main_font, False, text)
            correct_box.draw(WINDOW, None, True)

        else:
            text = "Incorrect! Answer was: "
            correct_img = INCORRECT_IMG
            main_font_size = 20
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            answer_font = pygame.font.SysFont("notosansmonocjkkr", 30)

            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, answer_font, True, text,
                                    str(answer))
            correct_box.draw(WINDOW, None, True)

        WINDOW.blit(correct_img, (
            x, y + 15,
            correct_img.get_width() + 50, correct_img.get_height()))

        pygame.display.update()
        # Show the correct answer for a couple of seconds
        if is_correct:
            # Less time for when the answer is correct
            time.sleep(1)
        else:
            time.sleep(3)

    def explode_object(object, is_enemy, score=False):
        object_center_loc = (object.x + object.get_width() / 2, object.y + object.get_height() / 2)
        explosion = Explosion(object_center_loc, 'large', score)
        all_sprites.add(explosion)
        if is_enemy:
            enemies.remove(object)

    def runaway_enemy(enemy, enemies, surface):
        enemy_center_loc = [enemy.x + enemy.get_width() / 2, enemy.y + enemy.get_height() / 2]
        new_loc = enemy_center_loc
        enemies.remove(enemy)
        disappear = Disappear(enemy_center_loc, 'large')
        all_sprites.add(disappear)

        new_enemy_center_loc = [enemy_center_loc[0], enemy_center_loc[1] - 200]

        for enemy_check in enemies:
            enemy_check_loc = (
                enemy_check.x + enemy_check.get_width() / 2, enemy_check.y + enemy_check.get_height() / 2)

            diff_x = abs(new_enemy_center_loc[0] - enemy_check_loc[0])
            diff_y = abs(new_enemy_center_loc[1] - enemy_check_loc[1])

            if (diff_y <= (enemy_check.get_height() + 100) and diff_x <= (enemy_check.get_height() + 100)):

                while diff_y <= (enemy_check.get_height() + 100):
                    new_enemy_center_loc[1] -= 100

                    diff_y = abs(new_enemy_center_loc[1] - enemy_check_loc[1])

        while abs(new_enemy_center_loc[1] - enemy_center_loc[1]) > 5:
            new_loc[1] -= 5
            move_up = Move(new_loc, 'large')
            all_sprites.add(move_up)

        reappear = Reappear(new_enemy_center_loc, 'large')
        all_sprites.add(reappear)
        reapp_enemy = Enemy(new_enemy_center_loc[0] - enemy.get_width() / 2,
                            new_enemy_center_loc[1] - enemy.get_height() / 2, enemy.color)
        enemies.append(reapp_enemy)

    menu_x = 20
    menu_btn = MenuButton(BACKGROUND_GREY, menu_x, 20, 30, 30, "")

    def redraw_window():
        # Draw the background img at coordinate: 0,0 (which is the top left)

        all_sprites.update()
        all_sprites.draw(WINDOW)
        # Draw the menu button
        for event in events:
            position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                menu_btn.hoverEffect(position)
            # if menu button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.isHovered(position):
                    # Merge and save data from model and game in case the game is completely closed
                    if not game_data.empty:
                        model_data = model.save_model_data()
                        save_data = pd.merge(model_data, game_data, on='trial', how='outer')
                        save_data.to_csv(PATH, index=False)
                    main_menu(group_num)
        # Draw text (f strings embed variables)
        lives_label = main_font.render(f"Lives: ", 1, WHITE)
        correct_label = main_font.render(f"Solved {correct_count} of {total_count}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)
        score_label = main_font.render(f"Score: {score}", 1, WHITE)
        # Top left hand corner plus a little offset for room for the menu button
        lives_label_x = 10 + menu_btn.width * 2
        WINDOW.blit(lives_label, (lives_label_x, 10))
        # Draw an amount of hearts in the top left corner indicating the amount of lives
        for life_cnt in range(1, lives + 1):
            WINDOW.blit(LIFE, (
                lives_label_x + lives_label.get_width() + life_cnt * 10 + ((life_cnt - 1) * LIFE.get_width()),
                10 + LIFE.get_height() / 4))
        offset_right = 20
        offset = 50
        # Top right hand corner (width screen minus width of label minus 10 pixels offset)
        score_x = WIDTH - score_label.get_width() - offset_right
        level_x = score_x - level_label.get_width() - offset
        correct_x = level_x - correct_label.get_width() - offset
        WINDOW.blit(score_label, (score_x, 10))
        WINDOW.blit(level_label, (level_x, 10))
        WINDOW.blit(correct_label, (correct_x, 10))

        menu_btn.draw(WINDOW, WHITE)

        seconds_string = str(seconds)
        if seconds < 10:
            seconds_string = "0" + seconds_string

        timer_label = main_font.render(f"Time left: {str(minutes)} : {seconds_string}", 1, WHITE)
        WINDOW.blit(timer_label, (menu_x, HEIGHT - timer_label.get_height() - 20))
        # Draw all enemies (before you initialize the player so the player goes over them)
        for enemy in enemies:
            enemy.draw(WINDOW)
        # Draw the player
        player.draw(WINDOW)

    # Create one background on top of another background and move both downwards to make it seem like you're moving
    # through space
    y_background_new = -HEIGHT
    y_background = 0
    while run:
        clock.tick(FPS)

        timer = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds since the start
        minutes = minutes_start - int(timer / 60)  # divide seconds by 60 to get the amount of minutes
        seconds = (seconds_start - int(timer)) % 60  # % the seconds passed so that only seconds are shown

        # Move background downwards
        WINDOW.blit(BACKGROUND, (0, y_background_new))
        WINDOW.blit(BACKGROUND, (0, y_background))
        y_background += 0.3
        y_background_new += 0.3
        if y_background_new == 0:
            y_background_new = -HEIGHT
            y_background = 0

        # No more lives or health then you lost
        if lives <= 0:
            lost = True
            lost_count += 1
        # When the player has no health left, spawn a new player. But not if they have lost already
        if player.health <= 0 and not lost:
            # Explode the ship when health goes below zero
            explode_object(player, False)
            if lives > 0:
                # Create a new ship
                player = create_new_player(ship, stats)
            lives -= 1
        # If the specified time is up the user should switch to the break sceen
        if minutes == 0 and seconds == 0:
            print("Experiment done")
            run = False
        if lost:
            # FPS * 3 = 3 sec
            # So for 3 seconds, show a "You lost message"
            if lost_count > FPS * 3:
                #     run = False
                lost_screen(ship, ship_name, ship_color, group_num)
                run = False
            else:
                for enemy in enemies:
                    explode_object(enemy, True)
                continue

        # If there are no more enemies on screen then
        if len(enemies) == 0 or len(enemies) == 1:
            level += 1
            y_background = 0
            y_background_new = - HEIGHT
            wave_length += 3
            spawn_box = random.sample(range(1, 6), 5)

            x_boundaries = np.arange(70, WIDTH - 70, (WIDTH - 145) / 3).astype(int)  # range 1,2,3
            y_boundaries = np.arange(10, HEIGHT - 10, (HEIGHT - 25) / 2).astype(int)  # range 4,5,6

            for i in range(3):
                if spawn_box[i] <= 3:
                    enemy = Enemy(random.randrange(x_boundaries[i], x_boundaries[i + 1] - 20),
                                  random.randrange(-y_boundaries[2], -y_boundaries[1] - 10),
                                  random.choice(["red", "blue", "green"]))
                else:
                    enemy = Enemy(random.randrange(x_boundaries[i - 4], x_boundaries[i - 3] - 20),
                                  random.randrange(-y_boundaries[1] - 10, -y_boundaries[0]),
                                  random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

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
                save_full_experiment_data()
                # YOU COULD CHANGE THIS TO quit() to press 'x' and quit the program
                run = False
                pygame.quit()
                sys.exit()
                break

        # check and get all keyboard keys that are pressed

        if not answering_question:

            keys = pygame.key.get_pressed()

            # Key to move and don't let the player move off screen
            if keys[pygame.K_LEFT] and player.x + player_velocity > 0:
                # Move to the left
                player.x -= player_velocity
            # Adding 50 for width of the player's spaceship
            if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
                # Move to the right
                player.x += player_velocity
            if keys[pygame.K_UP] and player.y + player_velocity > 0:
                # Move up
                player.y -= player_velocity
            if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT:
                # Move down
                player.y += player_velocity
            if keys[pygame.K_SPACE]:
                player.shoot()

        # Move the enemies downwards all the time, [:] means a copy of the list (just to be sure nothing bad happens)
        for enemy in enemies[:]:

            if not answering_question or enemy is not enemy_hit:

                enemy.move(enemy_velocity)
                # Check if laser hit the player
                enemy.move_lasers(laser_velocity, player)
                # Roughly every 2 sec an enemy should shoot, randomly determined
                if random.randrange(0, 2 * 60) == 1 and not answering_question:
                    enemy.shoot()
                # When the player collides with the enemy the enemy is removed and player's health reduces
                elif collide(enemy, player):
                    player.health -= 50
                    explode_object(enemy, True)

                # If the enemy moves off the bottom of the screen reduce player's health by half
                if enemy.y + enemy.get_height() > HEIGHT:
                    player.health -= 50
                    explode_object(enemy, True)

        redraw_window()

        # Laser velocity needs to be negative since the y value is lower upwards the screen, meaning laser will go up
        # TODO: Extra parameter SlimStampen question
        has_hit_enemy, enemy = player.move_lasers(-player_laser_velocity, enemies, WINDOW)
        if has_hit_enemy and not answering_question:

            enemy_hit = enemy
            # Increase the player's score when they hit an enemy
            score += 50
            for enemy in enemies[:]:
                enemy.stop_lasers()

            player.stop_lasers()

            enemy_hit.stop_lasers()

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
            main_font = pygame.font.SysFont("notosansmonocjkkr", 25)
            string = ""

            answering_question = True

        if answering_question:

            # Slow down enemies by 50% while answering a question
            enemy_velocity = (0.5 + (model.get_count_seen_facts(int(round(time.time() * 1000)) - START_TIME) * 0.1)) / 2

            code_text = str("Enter the kill code below")
            x = WIDTH / 2 - ANSWER_BOX.get_width() / 2
            y = HEIGHT / 2 - ANSWER_BOX.get_height() / 2
            width = 400
            height = 150

            correct_box = Rectangle(WHITE, x, y, width, height, main_font, main_font, True, code_text, str(question),
                                    RED, BLACK_NON_TRANSPARENT)

            correct_box.draw(WINDOW, None, True)

            txt_surface = main_font.render(string, True, pygame.Color('black'))
            txt_y = y + (height / 4) * 3 - (txt_surface.get_height() / 4) * 3 - 5
            WINDOW.blit(
                txt_surface,
                (
                    width + 150 + 100, txt_y  # heigth + 237.25
                )
            )

            for event in events:

                # if pressing quit 'x' then stop
                if event.type == pygame.QUIT:
                    save_full_experiment_data()
                    run = False
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        # Record response time
                        response_time = int(round(time.time() * 1000)) - question_onset_time_for_RT_calc

                        is_correct = (str(answer) == string)
                        if is_correct:
                            bonus_score = 0
                            # Max response time is 10 seconds -> 10.000 ms
                            if response_time < 10000:
                                # ( 10.000 ms - response time in ms ) / 100 = bonus score
                                # So if the player responds within 10 seconds they get a bonus
                                # Make the bonus score an int so that it's got no decimal places
                                bonus_score = int((10000 - response_time) / 100)
                            points_added = 50 + bonus_score
                            score = score + points_added
                            correct_count += 1
                        total_count += 1
                        # Log the response
                        # Stringify answer instead of typecasting string as int (since a string might not
                        # be castable)
                        if is_correct:
                            print("Correct!")
                            resp = Response(new_fact, question_onset_time, response_time, True)
                            model.m.register_response(resp)
                            explode_object(enemy_hit, True, points_added)
                        else:
                            print("Wrong! The correct answer was " + str(answer))
                            resp = Response(new_fact, question_onset_time, response_time, False)
                            model.m.register_response(resp)
                            runaway_enemy(enemy_hit, enemies, WINDOW)

                        # Record game data
                        enemies_on_screen = 0
                        for each_enemy in enemies[:]:
                            if each_enemy.y > 0:
                                enemies_on_screen += 1

                        if temp_lives != lives:
                            temp_shots_fired = 0

                        if os.path.isfile('Save_Data/temp_game_data.csv'):
                            game_data = pd.read_csv('Save_Data/temp_game_data.csv')
                            trial_nr = game_data['trial'].iloc[-1]
                        trial_nr += 1
                        d = {'trial': trial_nr, 'block': block, 'group_number': group_num, 'ID_code_1': ID_CODE_1,
                             'ID_code_2': ID_CODE_2, 'is_gamification': is_gamification, 'answer_given': string,
                             'shots_fired': player.shots_fired - temp_shots_fired,
                             'shots_fired_total': player.shots_fired, 'ship_name': ship_name,
                             'ship_color': [ship_color], 'lives': lives, 'level': level,
                             'enemies_on_screen': enemies_on_screen + 1}
                        temp_shots_fired = player.shots_fired
                        temp_lives = lives
                        if game_data.empty:
                            game_data = pd.DataFrame(data=d)
                        else:
                            game_data = game_data.append(d, ignore_index=True)
                            game_data.to_csv("Save_Data/temp_game_data.csv", index=False)

                        show_answer(is_correct, answer, x, y + ANSWER_BOX.get_height())

                        # Update enemy velocity according to the amount of facts that have been seen
                        enemy_velocity = 0.5 + (
                                model.get_count_seen_facts(int(round(time.time() * 1000)) - START_TIME) * 0.05)

                        answering_question = False
                        enemy_hit = None

                        string = ''
                    elif event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    elif len(string) < MAX_ANS_LEN and 48 <= event.key <= 57:
                        string += str(event.key - 48)

        pygame.display.update()


main.has_been_called = False


# When run is set to false the system comes here
# TODO: The app should bring the user to a new instance of the menu


def main_menu(group_num):
    button_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    button_width = 400
    button_height = 80
    button_x = WIDTH - 1.3 * button_width
    start_button_y = 130
    start_button = Button(BACKGROUND_GREY, button_x, start_button_y, button_width,
                          button_height, button_font, "Start game!")
    upgrade_button = Button(BACKGROUND_GREY, button_x, start_button_y + 140, button_width,
                            button_height, button_font, "Upgrades", True)
    settings_button = Button(BACKGROUND_GREY, button_x, start_button_y + 280,
                             button_width,
                             button_height, button_font, "Settings", True)
    about_button = Button(BACKGROUND_GREY, button_x, start_button_y + 420, button_width,
                          button_height, button_font, "About")
    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        start_button.draw(WINDOW, WHITE)
        upgrade_button.draw(WINDOW, WHITE)
        settings_button.draw(WINDOW, WHITE)
        about_button.draw(WINDOW, WHITE)
        menu_x = 80
        WINDOW.blit(MENU_TEXT, (menu_x, HEIGHT / 2 - MENU_TEXT.get_height()))
        WINDOW.blit(MENU_SHIP, (menu_x + 0.5 * MENU_TEXT.get_width() - 0.5 * MENU_SHIP.get_width(), HEIGHT / 2 + 50))
        # WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                start_button.hoverEffect(position)
                upgrade_button.hoverEffect(position)
                about_button.hoverEffect(position)
                settings_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isHovered(position):
                    # initialize ship
                    choose_fighter(group_num)
                if about_button.isHovered(position):
                    about_screen()


def lost_screen(ship, ship_name, ship_color, group_num):
    lost_font = pygame.font.SysFont("notosansmonocjkkr", 60)
    lost_label = lost_font.render("You Lost!", 1, WHITE)
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    button_width = 180
    button_height = 60
    menu_button = Button(BACKGROUND_GREY, WIDTH / 2 - 1.5 * button_width, HEIGHT / 2 + lost_label.get_height(),
                         button_width, button_height, button_font,
                         "Menu")
    restart_button = Button(BACKGROUND_GREY, WIDTH / 2 + button_width / 2, HEIGHT / 2 + lost_label.get_height(),
                            button_width, button_height, button_font,
                            "Try again")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        WINDOW.blit(lost_label,
                    (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2 - lost_label.get_height()))
        menu_button.draw(WINDOW, WHITE)
        restart_button.draw(WINDOW, WHITE)

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
                restart_button.hoverEffect(position)
                menu_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Setting run to false bring you back to menu
                if menu_button.isHovered(position):
                    main_menu(group_num)
                    run = False
                # Restart the game
                if restart_button.isHovered(position):
                    main(ship, ship_name, ship_color, group_num)



def show_explanation(ship, chosen_ship, color, group_num):
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    back_button = Button(BACKGROUND_GREY, WIDTH * (1 / 21), button_font.get_height(), 150, 50, button_font, "< Back")

    font_size = 25
    explanation_font_general = pygame.font.SysFont("Arial", font_size)
    explanation_font = pygame.font.SysFont("Arial", font_size)
    font_press_any_key = pygame.font.SysFont("Arial", 35)
    explanation_general = "This game is developed for an experiment. \n" \
                          "In this experiment you will play with a ship \n" \
                          "that shoots aliens. \n" \
                          "Whenever an alien is shot a killcode is asked. \n" \
                          "Solve the multiplications for the correct killcode. \n" \
                          "The entire experiment will take 12 minutes."
    explanation_numpad = "Press the arrow keys to move the ship around"
    explanation_spacebar = "To shoot at an alien press the spacebar"
    explanation_press_any_key = "PRESS ANY KEY TO CONTINUE"
    explanation_numpad_label = explanation_font.render(explanation_numpad, 1, WHITE)
    explanation_spacebar_label = explanation_font.render(explanation_spacebar, 1, WHITE)
    explanation_press_any_key_label = font_press_any_key.render(explanation_press_any_key, 1, DARK_BLUE)
    text_x = WIDTH / 2 - explanation_numpad_label.get_width() / 2
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        back_button.draw(WINDOW, WHITE)

        max_y_general = render_multi_line(explanation_general, text_x, 50, font_size + 5, explanation_font_general)

        explanation_numpad_y = max_y_general + font_size * 3
        numpad_y = explanation_numpad_y + font_size * 2
        explanation_spacebar_y = numpad_y + NUMPAD.get_height() + font_size * 2
        spacebar_y = explanation_spacebar_y + font_size * 2
        press_any_key_y = spacebar_y + + NUMPAD.get_height() + font_size * 2

        WINDOW.blit(explanation_numpad_label, (get_middle_x(explanation_numpad_label), explanation_numpad_y))
        WINDOW.blit(NUMPAD, (get_middle_x(NUMPAD.get_width()), numpad_y))

        WINDOW.blit(explanation_spacebar_label, (get_middle_x(explanation_spacebar_label), explanation_spacebar_y))
        WINDOW.blit(SPACEBAR, (get_middle_x(SPACEBAR.get_width()), spacebar_y))
        WINDOW.blit(explanation_press_any_key_label, (get_middle_x(explanation_press_any_key_label), press_any_key_y))

        events = pygame.event.get()
        pygame.display.update()
        for event in events:
            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.KEYDOWN:
                run = False
                main(ship, chosen_ship, color, group_num)
            position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                back_button.hoverEffect(position)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isHovered(position):
                    choose_color(chosen_ship, group_num)


def choose_fighter(group_num):
    title_font = pygame.font.SysFont("notosansmonocjkkr", 40)
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    # Essentially the screen is split up into 21 parts. Buttons take up 4*4 = 16 parts of space
    button_width = WIDTH * (4 / 21)
    button_height = 500
    button_y = HEIGHT - button_height - 50
    back_button = Button(BACKGROUND_GREY, WIDTH * (1 / 21), button_font.get_height(), 150, 50, button_font, "< Back")
    # Inbetween each of the buttons 1/21 part is left open
    nelson_button = BigButton(BACKGROUND_GREY, WIDTH * (1 / 21), button_y, button_width,
                              button_height, button_font, NELSON, True, "lord_nelson", "Lord Nelson")
    commander_button = BigButton(BACKGROUND_GREY, WIDTH * (6 / 21), button_y, button_width,
                                 button_height, button_font, COMMANDER, True, "commander_cosmonaut",
                                 "Commander Cosmonaut")
    pointy_button = BigButton(BACKGROUND_GREY, WIDTH * (11 / 21), button_y,
                              button_width, button_height, button_font, POINTY_BOY, True, "pointy_boy", "Pointy Boy")
    donut_button = BigButton(BACKGROUND_GREY, WIDTH * (16 / 21), button_y, button_width,
                             button_height, button_font, DONUT, True, "donut_warrior", "Donut Warrior", True,
                             "3 answers correct in a row in a row to unlock")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        back_button.draw(WINDOW, WHITE)
        nelson_button.draw(WINDOW, WHITE)
        commander_button.draw(WINDOW, WHITE)
        pointy_button.draw(WINDOW, WHITE)
        donut_button.draw(WINDOW, WHITE)
        title_label = title_font.render("Choose fighter:", 1, WHITE)
        title_label_drop_shadow = title_font.render("Choose fighter:", 1, BLACK)
        offset = 3
        WINDOW.blit(title_label_drop_shadow, (WIDTH * (1 / 21) + offset, title_label.get_height() + 50 + offset))
        WINDOW.blit(title_label, (WIDTH * (1 / 21), title_label.get_height() + 50))
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                back_button.hoverEffect(position)
                nelson_button.hoverEffect(position)
                commander_button.hoverEffect(position)
                pointy_button.hoverEffect(position)
                donut_button.hoverEffect(position)

            # if button is pressed then ...
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isHovered(position):
                    main_menu(group_num)
                if nelson_button.isHovered(position):
                    choose_color("lord_nelson", group_num)
                if commander_button.isHovered(position):
                    choose_color("commander_cosmonaut", group_num)
                if pointy_button.isHovered(position):
                    choose_color("pointy_boy", group_num)
                if donut_button.isHovered(position):
                    if not donut_button.is_locked:
                        choose_color("donut_warrior", group_num)
    # pygame.quit()
def switch_unlock_texts(chosen_ship):
    switcher = {
        "lord_nelson": "Get to level 3 to unlock",
        "commander_cosmonaut": "Get a score of 5000 to unlock",
        "pointy_boy": "Hit 3 aliens with only 3 lasers in a row to unlock",
        "donut_warrior": "8 answers correct in a row in a row to unlock"
    }
    return switcher.get(chosen_ship, "")


def choose_color(chosen_ship, group_num):
    title_font = pygame.font.SysFont("notosansmonocjkkr", 40)
    subtitle_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    button_width = WIDTH * (4 / 21)
    button_height = 400
    button_y = HEIGHT - button_height - 50

    unlock_text = ""

    back_button = Button(BACKGROUND_GREY, WIDTH * (1 / 21), button_font.get_height(), 150, 50, button_font, "< Back")
    purple_button = BigButton(BACKGROUND_GREY, WIDTH * (1 / 21), button_y, button_width,
                              button_height, button_font, choose_ship(chosen_ship, "purple"), "", False, "Purple")
    green_button = BigButton(BACKGROUND_GREY, WIDTH * (6 / 21), button_y, button_width,
                             button_height, button_font, choose_ship(chosen_ship, "green"), "", False, "Green")
    red_button = BigButton(BACKGROUND_GREY, WIDTH * (11 / 21), button_y,
                           button_width,
                           button_height, button_font, choose_ship(chosen_ship, "red"), "", False, "Red")
    gold_button = BigButton(BACKGROUND_GREY, WIDTH * (16 / 21), button_y, button_width,
                            button_height, button_font, choose_ship(chosen_ship, "gold"), "", False, "Gold", True,
                            switch_unlock_texts(chosen_ship))

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        back_button.draw(WINDOW, WHITE)
        purple_button.draw(WINDOW, WHITE)
        green_button.draw(WINDOW, WHITE)
        red_button.draw(WINDOW, WHITE)
        gold_button.draw(WINDOW, WHITE)
        title_label = title_font.render("Pick a color:", 1, WHITE)
        title_label_drop_shadow = title_font.render("Pick a color:", 1, BLACK)
        # Remove the underscores from the string and capitalize the first letters of each word
        ship_name = chosen_ship.replace("_", " ").title()
        subtitle_label = subtitle_font.render(ship_name, 1, WHITE)
        subtitle_label_drop_shadow = subtitle_font.render(ship_name, 1, BLACK)
        offset = 3
        WINDOW.blit(title_label_drop_shadow, (WIDTH * (1 / 21) + offset, title_label.get_height() + 50 + offset))
        WINDOW.blit(title_label, (WIDTH * (1 / 21), title_label.get_height() + 50))
        WINDOW.blit(subtitle_label_drop_shadow,
                    (WIDTH * (1 / 21) + offset, title_label.get_height() * 2 + 50 + offset))
        WINDOW.blit(subtitle_label, (WIDTH * (1 / 21), title_label.get_height() * 2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                back_button.hoverEffect(position)
                purple_button.hoverEffect(position)
                green_button.hoverEffect(position)
                red_button.hoverEffect(position)
                gold_button.hoverEffect(position)

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isHovered(position):
                    choose_fighter(group_num)
                if purple_button.isHovered(position):
                    show_explanation(choose_ship(chosen_ship, "purple"), chosen_ship, "purple", group_num)
                if green_button.isHovered(position):
                    show_explanation(choose_ship(chosen_ship, "green"), chosen_ship, "green", group_num)
                if red_button.isHovered(position):
                    show_explanation(choose_ship(chosen_ship, "red"), chosen_ship, "red", group_num)
                if gold_button.isHovered(position):
                    if not gold_button.is_locked:
                        show_explanation(choose_ship(chosen_ship, "gold"), chosen_ship, "gold", group_num)
    # pygame.quit()


def save_full_experiment_data():
    if os.path.isfile(PATH):
        experiment_data = pd.read_csv(PATH)
        # if os.path.isfile(FINAL_PATH):
        #     old_experiment_data = pd.read_csv(FINAL_PATH)
        #     experiment_data = old_experiment_data.append(experiment_data, ignore_index=True)
        os.remove(PATH)
        experiment_data.to_csv(FINAL_PATH, index=False)


if os.path.isfile('Save_Data/temp_game_data.csv'):
    os.remove("Save_Data/temp_game_data.csv")
# main_menu()
