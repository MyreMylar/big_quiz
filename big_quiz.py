import pygame
import os

from game.intro_screen import IntroScreen
from game.main_quiz import MainQuiz
from game.end_screen import EndScreen


window_resolution = (800, 600)
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("Big Quiz")
screen = pygame.display.set_mode(window_resolution)

background = pygame.Surface(screen.get_size())
background = background.convert() 
background.fill((220, 220, 220))

fonts = [pygame.font.Font("data/ShadowsIntoLight.ttf", 24),
         pygame.font.Font("data/ShadowsIntoLight.ttf", 48),
         pygame.font.Font("data/JustAnotherHand.ttf", 100)]
fonts[0].set_bold(False)

all_states = {"intro": IntroScreen(screen, fonts, window_resolution),
              "main_quiz": MainQuiz(screen, fonts, window_resolution),
              "end": EndScreen(screen, fonts, window_resolution)}
current_state = all_states['intro']
current_state.start()

is_running = True
clock = pygame.time.Clock()
while is_running:
    time_delta = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        current_state.process_event(event)

    current_state.run(time_delta)

    if current_state.time_to_transition:
        transition_data = current_state.shutdown()
        current_state = all_states[current_state.transition_target]
        current_state.start(transition_data)

    pygame.display.flip()  # flip all our drawn stuff onto the screen

pygame.quit()  # exited game loop so quit pygame
