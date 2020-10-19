from utilities.main_functions import *
from classes.button import Button
import sys


def about_screen():
    font_size = 25
    about_font = pygame.font.SysFont("Arial", font_size)
    about_explanation_text = "This application uses an Adaptive Fact Learning system for \n" \
                             "teaching people multiplication (tables) while playing Space Invaders. \n" \
                             "This gamified learning system should increase the learners motivation \n\n" \
                             "SlimStampen is the Adaptive Fact Learning system used for timing the \n" \
                             "presentation of multiplication questions, based on the learner's memory \n" \
                             "of those facts. The timing of when certain questions are asked should \n" \
                             "optimize the learners memorization of the different multiplications"
    created_by_text = "Created by Jelle Bosch, Francesca Perin and Jori Blankestijn"
    created_by_label = about_font.render(created_by_text, 1, WHITE)

    created_by_y = HEIGHT - 2 * created_by_label.get_height()
    button_font = pygame.font.SysFont("notosansmonocjkkr", 20)
    back_button = Button(BACKGROUND_GREY, WIDTH * (1 / 21), button_font.get_height(), 150, 50, button_font, "< Back")

    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        render_multi_line(about_explanation_text, 150, 70, font_size + 5, about_font)
        WINDOW.blit(created_by_label,
                    (get_middle_x(created_by_label), created_by_y))
        WINDOW.blit(GHOST_BOY, (get_middle_x(GHOST_BOY), HEIGHT / 2))

        back_button.draw(WINDOW, WHITE)

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
                back_button.hoverEffect(position)

            # if back button is pressed go back to main menu
            if event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.isHovered(position):
                    run = False
