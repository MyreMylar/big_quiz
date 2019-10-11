import pygame
from pygame.locals import *

from game.ui_text_button import UITextButton


class IntroScreen:
    def __init__(self, screen, fonts, screen_size):
        self.screen_size = screen_size
        self.screen = screen
        self.fonts = fonts

        self.background = None
        self.title_text_render = None
        self.pick_category_render = None
        self.buttons = []

        self.time_to_transition = False
        self.transition_target = 'main_quiz'
        self.is_running = True
        self.transition_data = {}

    def start(self, transition_data=None):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((220, 220, 220))

        self.title_text_render = self.fonts[2].render("The Big Quiz", True, pygame.Color(0, 0, 0))

        self.pick_category_render = self.fonts[1].render("Pick a bonus round category:", True, pygame.Color(0, 0, 0))

        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.3), int(self.screen_size[1] * 0.6),
                                          int(self.screen_size[0] * 0.4), 50), "Film", self.fonts, 0))
        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.3), int(self.screen_size[1] * 0.6) + 75,
                                          int(self.screen_size[0] * 0.4), 50), "Music", self.fonts, 0))
        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.3), int(self.screen_size[1] * 0.6) + 150,
                                          int(self.screen_size[0] * 0.4), 50), "Minecraft", self.fonts, 0))

    def shutdown(self):

        self.time_to_transition = False
        self.background = None
        self.title_text_render = None
        self.pick_category_render = None
        self.buttons = []
        return self.transition_data

    def process_event(self, event):
        for button in self.buttons:
            button.handle_input_event(event)

    def run(self, time_delta):

        if self.buttons[0].was_pressed():
            self.time_to_transition = True
            self.transition_data['picked_bonus_round'] = "film"

        if self.buttons[1].was_pressed():
            self.time_to_transition = True
            self.transition_data['picked_bonus_round'] = "music"

        if self.buttons[2].was_pressed():
            self.time_to_transition = True
            self.transition_data['picked_bonus_round'] = "minecraft"
                
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.update()
            button.draw(self.screen)
                       
        self.screen.blit(self.title_text_render, self.title_text_render.get_rect(centerx=int(self.screen_size[0] / 2),
                                                                                 centery=120))

        self.screen.blit(self.pick_category_render,
                         self.pick_category_render.get_rect(centerx=int(self.screen_size[0] / 2),
                                                            centery=int(self.screen_size[1] * 0.5)))
