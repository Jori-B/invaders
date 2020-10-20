import sys
from classes.button import Button
from utilities.main_functions import *
from classes.saveData import *


def end_screen(questionnaire_code):
    has_pressed_close = False

    font_size = 25
    end_font = pygame.font.SysFont("Arial", font_size)
    link_font = pygame.font.SysFont("Arial", font_size * 2)
    end_text = "You\'ve finished the second and last block!\n" \
               "As with the first, we ask you to fill out a questionnaire.\n" \
               "Go to the questionnaire using the following link: "
    link_text = "https://forms.gle/" + str(questionnaire_code)
    link_label = link_font.render(link_text, 1, WHITE)
    max_y_text = render_multi_line(end_text, 150, 70, font_size + 5, end_font)
    link_y = max_y_text + link_label.get_height()
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    button_width = 180
    button_height = 60
    img_y = link_y + 100

    close_text = "After filling in the questionnaire, press Finish"
    close_label = end_font.render(close_text, 1, DARK_BLUE)
    close_text_y = img_y + GHOST_BOY.get_height() + close_label.get_height() * 2

    close_btn_y = close_text_y + close_label.get_height() * 3

    close_btn = Button(BACKGROUND_GREY, get_middle_x(button_width), close_btn_y,
                          button_width, button_height, button_font, "Finish")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))

        if not has_pressed_close:
            render_multi_line(end_text, 150, 50, font_size + 5, end_font)
            WINDOW.blit(link_label,
                        (get_middle_x(link_label), link_y))
            WINDOW.blit(GHOST_BOY, (get_middle_x(GHOST_BOY), img_y))
            WINDOW.blit(close_label,
                        (get_middle_x(close_label), close_text_y))
            close_btn.draw(WINDOW, WHITE)
        else:
            time_passed_in_sec = (pygame.time.get_ticks() - start_time) / 1000
            if time_passed_in_sec > 3:
                if os.path.isfile('Save_Data/temp_basic_slimstampen_data.csv'):
                    os.remove("Save_Data/temp_basic_slimstampen_data.csv")
                if os.path.isfile('Save_Data/temp_game_data.csv'):
                    os.remove("Save_Data/temp_game_data.csv")
                save_full_experiment_data()
                run = False
                pygame.quit()
                sys.exit()
                break
            else:
                WINDOW.blit(THANKS_TEXT, (get_middle_x(WELCOME_TEXT), HEIGHT / 4))
                WINDOW.blit(GHOST_BOY_BYE, (get_middle_x(GHOST_BOY_BYE), img_y))

        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                save_full_experiment_data()
                if os.path.isfile('Save_Data/temp_basic_slimstampen_data.csv'):
                    os.remove("Save_Data/temp_basic_slimstampen_data.csv")
                if os.path.isfile('Save_Data/temp_game_data.csv'):
                    os.remove("Save_Data/temp_game_data.csv")
                run = False
                pygame.quit()
                sys.exit()
                break
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                close_btn.hoverEffect(position)

            # if continue button is pressed then start the next phase of the experiment
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Based on the condition bring the user to someplace
                if close_btn.isHovered(position):
                    start_time = pygame.time.get_ticks()
                    picture_cnt = 1
                    cnt_direction = "forward"
                    has_pressed_close = True


