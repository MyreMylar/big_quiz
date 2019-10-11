import pygame
from pygame.locals import *

from game.ui_text_button import UITextButton


class EndScreen:
    def __init__(self, screen, fonts, screen_size):
        self.screen_size = screen_size
        self.screen = screen
        self.fonts = fonts

        self.background = None
        self.buttons = []

        self.time_to_transition = False
        self.transition_target = 'intro'
        self.is_running = True

        self.total_len = 0
        self.total_answered = 0
        self.final_score = 0

        self.end_text_render = None
        self.end_text_render_rect = None

        self.score_text_render = None
        self.score_text_render_rect = None

        self.stat_text_render = None
        self.stat_text_render_rect = None

    def start(self, transition_data):
        self.total_len = transition_data['total_len']
        self.total_answered = transition_data['total_answered']
        self.final_score = transition_data['final_score']

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((220, 220, 220))

        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.2), int(self.screen_size[1] * 0.8),
                                          int(self.screen_size[0] * 0.6), 50), "Retry", self.fonts, 0))

        self.end_text_render = self.fonts[1].render("You reached the end of the Big Quiz!", True, pygame.Color(0, 0, 0))
        self.end_text_render_rect = self.end_text_render.get_rect(centerx=int(self.screen_size[0] / 2),
                                                                  centery=int(self.screen_size[1] * 0.3))

        self.score_text_render = self.fonts[0].render("You scored: " + str(self.final_score) + " points!", True,
                                                      pygame.Color(0, 0, 0))
        self.score_text_render_rect = self.score_text_render.get_rect(centerx=int(self.screen_size[0] / 2),
                                                                      centery=int(self.screen_size[1] * 0.5))

        self.stat_text_render = self.fonts[0].render("You correctly answered: "
                                                     "" + str(self.total_answered) + "/" + str(self.total_len),
                                                     True, pygame.Color(0, 0, 0))
        self.stat_text_render_rect = self.stat_text_render.get_rect(centerx=int(self.screen_size[0] / 2),
                                                                    centery=int(self.screen_size[1] * 0.6))

    def shutdown(self):
        transition_data = {}

        self.time_to_transition = False

        self.background = None
        self.buttons = []

        self.end_text_render = None
        self.end_text_render_rect = None

        self.score_text_render = None
        self.score_text_render_rect = None

        self.stat_text_render = None
        self.stat_text_render_rect = None

        return transition_data

    def process_event(self, event):
        for button in self.buttons:
            button.handle_input_event(event)

    def run(self, time_delta):

        if self.buttons[0].was_pressed():
            self.time_to_transition = True

        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.end_text_render, self.end_text_render_rect)
        self.screen.blit(self.score_text_render, self.score_text_render_rect)
        self.screen.blit(self.stat_text_render, self.stat_text_render_rect)

        for button in self.buttons:
            button.update()
            button.draw(self.screen)
