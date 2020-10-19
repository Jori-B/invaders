from utilities.main_functions import *
from classes.button import Button
import sys


def break_screen(group_number, questionnaire_code):
    font_size = 25
    break_font = pygame.font.SysFont("Arial", font_size)
    link_font = pygame.font.SysFont("Arial", font_size * 2)
    break_text = "You can take a break right now. During this break,\n" \
                 "we ask you to fill in a questionnaire.\n" \
                 f"Please enter \"{ID_CODE_1}\" under Experiment Code.\n" \
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
                    if group_number == 1:
                        print("main(group_num=group_number)")
                    if group_number == 2:
                        print("default_experiment(group_num=group_number)"
