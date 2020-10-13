# Based on https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=UnityCoin
import random
import numpy as np
from classes.button import Button
from classes.bigButton import BigButton
from classes.rectangle import Rectangle
from classes.player import Player
from classes.enemy import Enemy
from classes.explosion import Explosion
from classes.disappear import Disappear
from classes.reappear import Reappear
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


def main(ship):
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

    enemies = []
    # Every level a new wave will be created of 5 enemies
    wave_length = 3
    enemy_velocity = 0.5

    # How fast the player can move every time you press the key a max of 5 pixels to move
    player_velocity = 5
    laser_velocity = 4

    # Define a player space ship at location
    player = Player(WIDTH / 2, HEIGHT, ship)
    # Center the ship on screen
    player.x -= (player.get_width() / 2)
    player.y -= (player.get_height() + 50)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    answering_question = False
    enemy_hit = None

    def show_answer(is_correct, answer, x, y):

        if is_correct:
            text = "Correct!"
            correct_img = CORRECT_IMG
            main_font_size = 30
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, main_font, False, text)
            correct_box.draw(WINDOW)
        else:
            text = "Incorrect! Answer was: "
            correct_img = INCORRECT_IMG
            main_font_size = 20
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            answer_font = pygame.font.SysFont("notosansmonocjkkr", 30)

            correct_box = Rectangle(WHITE, x + correct_img.get_width(), y, 250, 100, main_font, answer_font, True, text,
                                    str(answer))
            correct_box.draw(WINDOW)

        WINDOW.blit(correct_img, (
            x, y + 15,
            correct_img.get_width() + 50, correct_img.get_height()))

        pygame.display.update()
        # Show the correct answer for 2 seconds
        time.sleep(3)

    def kill_enemy(enemy):
        enemy_center_loc = (enemy.x + enemy.get_width() / 2, enemy.y + enemy.get_height() / 2)
        explosion = Explosion(enemy_center_loc, 'large')
        all_sprites.add(explosion)
        enemies.remove(enemy)

    def runaway_enemy(enemy, enemies):
        enemy_center_loc = [enemy.x + enemy.get_width() / 2, enemy.y + enemy.get_height() / 2]
        disappear = Disappear(enemy_center_loc, 'large')
        all_sprites.add(disappear)
        enemies.remove(enemy)

        new_enemy_center_loc=[enemy_center_loc[0],enemy_center_loc[1]-100]

        for enemy_check in enemies:
            enemy_check_loc = (enemy_check.x + enemy_check.get_width() / 2, enemy_check.y + enemy_check.get_height() / 2)

            #diff_x = abs(new_enemy_center_loc[1] - enemy_check_loc[1])
            diff_y = abs(new_enemy_center_loc[1] - enemy_check_loc[1])


            if diff_y<= (enemy_check.get_height() + 100) :

                while not diff_y<= (enemy_check.get_height() + 100) :
                    print("Kebabo è intelligente")

                    new_enemy_center_loc[1]-=50

                    diff_y = abs(new_enemy_center_loc[1] - enemy_check_loc[1])


        reappear = Reappear(new_enemy_center_loc, 'large')
        all_sprites.add(reappear)
        reapp_enemy = Enemy( new_enemy_center_loc[0]-enemy.get_width() / 2, new_enemy_center_loc[1]-enemy.get_height() / 2, enemy.color)
        enemies.append(reapp_enemy)

    def redraw_window():
        # Draw the background img at coordinate: 0,0 (which is the top left)

        all_sprites.update()
        all_sprites.draw(WINDOW)

        # Draw text (f strings embed variables)
        lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)
        # Top left hand corner plus a little offset
        WINDOW.blit(lives_label, (10, 10))
        # Top light hand corner (width screen minus width of label minus 10 pixels offset
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # Draw all enemies (before you initialize the player so the player goes over them)
        for enemy in enemies:
            enemy.draw(WINDOW)
        # Draw the player
        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, WHITE)
            WINDOW.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2 - lost_label.get_height() / 2))

    # TODO: When shooting an enemy tell the player the "explosion code" needs to be entered
    while run:
        clock.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0))

        # No more lives or health then you lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            # FPS * 3 = 3 sec
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        # If there are no more enemies on screen then
        if len(enemies) == 0 or len(enemies) == 1:
            level += 1
            wave_length += 3
            spawn_box = random.sample(range(1, 6), 5)

            x_boundaries = np.arange(70, WIDTH -70, (WIDTH -145)/ 3).astype(int)  # range 1,2,3 
            y_boundaries = np.arange(10, HEIGHT -10, (HEIGHT -25)/ 2).astype(int)  # range 4,5,6

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
                # YOU COULD CHANGE THIS TO quit() to press 'x' and quit the program
                run = False

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
                    player.health -= 10
                    kill_enemy(enemy)

                # If the enemy moves off screen lose a life
                if enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)

        redraw_window()

        # Laser velocity needs to be negative since the y value is lower upwards the screen, meaning laser will go up
        # TODO: Extra parameter SlimStampen question
        has_hit_enemy, enemy = player.move_lasers(-laser_velocity, enemies, WINDOW)
        if has_hit_enemy and not answering_question:

            enemy_hit = enemy

            for enemy in enemies[:]:
                enemy.stop_lasers()

            player.stop_lasers()

            enemy_hit.stop_lasers()

            # Record question onset time
            question_onset_time = int(round(time.time() * 1000)) - START_TIME
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
            enemy_velocity = (0.5 + (model.get_count_seen_facts(int(round(time.time() * 1000)) - START_TIME) * 0.1)) / 2

            code_text = str("Enter the kill code below")
            x = WIDTH / 2 - ANSWER_BOX.get_width() / 2
            y = HEIGHT / 2 - ANSWER_BOX.get_height() / 2
            width = 400
            height = 150

            correct_box = Rectangle(WHITE, x, y, width, height, main_font, main_font, True, code_text, str(question),
                                    RED, BLACK_NON_TRANSPARENT)
            correct_box.draw(WINDOW)

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
                        response_time = int(round(time.time() * 1000)) - question_onset_time
                        # Log the response
                        # Stringify answer instead of typecasting string as int (since a string might not
                        # be castable)
                        if str(answer) == string:
                            print("Correct!")
                            resp = Response(new_fact, question_onset_time, response_time, True)
                            model.m.register_response(resp)
                            kill_enemy(enemy_hit)
                        else:
                            print("Wrong! The correct answer was " + str(answer))
                            resp = Response(new_fact, question_onset_time, response_time, False)
                            model.m.register_response(resp)
                            runaway_enemy(enemy_hit, enemies)

                        show_answer(str(answer) == string, answer, x, y + ANSWER_BOX.get_height())

                        # Update enemy velocity according to the amount of facts that have been seen
                        enemy_velocity = 0.5 + (
                                model.get_count_seen_facts(int(round(time.time() * 1000)) - START_TIME) * 0.1)

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
    button_x = WIDTH - 1.3 * button_width
    start_button_y = 130
    start_button = Button(BACKGROUND_GREY, button_x, start_button_y, button_width,
                          button_height, button_font, "Start game!")
    upgrade_button = Button(BACKGROUND_GREY, button_x, start_button_y + 140, button_width,
                            button_height, button_font, "Upgrades")
    settings_button = Button(BACKGROUND_GREY, button_x, start_button_y + 280,
                             button_width,
                             button_height, button_font, "Settings")
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
                run = False
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                if start_button.isHovered(position):
                    start_button.color = GREEN
                else:
                    start_button.color = BACKGROUND_GREY
                if upgrade_button.isHovered(position):
                    upgrade_button.color = GREEN
                else:
                    upgrade_button.color = BACKGROUND_GREY
                if about_button.isHovered(position):
                    about_button.color = GREEN
                else:
                    about_button.color = BACKGROUND_GREY
                if settings_button.isHovered(position):
                    settings_button.color = GREEN
                else:
                    settings_button.color = BACKGROUND_GREY

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isHovered(position):
                    # initi slipsta
                    choose_fighter()
    pygame.quit()


def choose_fighter():
    title_font = pygame.font.SysFont("notosansmonocjkkr", 40)
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    button_width = WIDTH * (4/21)
    button_height = 500
    button_y = 150
    nelson_button = BigButton(BACKGROUND_GREY, WIDTH * (1/21), button_y, button_width,
                           button_height, button_font, NELSON, "Lord Nelson")
    commander_button = BigButton(BACKGROUND_GREY, WIDTH * (6/21), button_y, button_width,
                              button_height, button_font, COMMANDER, "Commander Cosmonaut")
    pointy_button = BigButton(BACKGROUND_GREY, WIDTH * (11/21), button_y,
                           button_width ,
                           button_height, button_font, POINTY_BOY, "Pointy Boy")
    donut_button = BigButton(BACKGROUND_GREY, WIDTH * (16/21), button_y, button_width,
                          button_height, button_font, DONUT, "Donut Warrior")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        nelson_button.draw(WINDOW, WHITE)
        commander_button.draw(WINDOW, WHITE)
        pointy_button.draw(WINDOW, WHITE)
        donut_button.draw(WINDOW, WHITE)
        title_label = title_font.render("Choose fighter:", 1, WHITE)
        title_label_drop_shadow = title_font.render("Choose fighter:", 1, BLACK)
        offset = 3
        WINDOW.blit(title_label_drop_shadow, (WIDTH * (1/21) + offset, title_label.get_height() + offset))
        WINDOW.blit(title_label, (WIDTH * (1/21), title_label.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                run = False
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                if nelson_button.isHovered(position):
                    nelson_button.color = GREEN
                else:
                    nelson_button.color = BACKGROUND_GREY
                if commander_button.isHovered(position):
                    commander_button.color = GREEN
                else:
                    commander_button.color = BACKGROUND_GREY
                if pointy_button.isHovered(position):
                    pointy_button.color = GREEN
                else:
                    pointy_button.color = BACKGROUND_GREY
                if donut_button.isHovered(position):
                    donut_button.color = GREEN
                else:
                    donut_button.color = BACKGROUND_GREY

            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if nelson_button.isHovered(position):
                    main(choose_ship("lord_nelson", "purple"))
                if commander_button.isHovered(position):
                    main(choose_ship("commander", "purple"))
                if pointy_button.isHovered(position):
                    main(choose_ship("pointy_boy", "purple"))
                if donut_button.isHovered(position):
                    main(choose_ship("donut", "purple"))
    pygame.quit()


main_menu()
