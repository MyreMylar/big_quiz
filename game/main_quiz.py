import pygame
import csv
import random

from game.text_render import render_word_wrapped_text
from game.ui_text_button import UITextButton


class QuizQuestion:
    def __init__(self, idx, question, answer_a, answer_b, answer_c, right_answer):
        self.id = idx
        self.question = question
        self.answer_a = answer_a
        self.answer_b = answer_b
        self.answer_c = answer_c
        self.right_answer = right_answer


class MainQuiz:
    def __init__(self, screen, fonts, screen_size):
        self.screen_size = screen_size
        self.screen = screen
        self.fonts = fonts

        self.background = None

        self.picked_bonus_round = ""

        self.time_to_transition = False
        self.transition_target = 'end'
        self.transition_data = {}
          
        self.autumn_questions = []
        self.spring_questions = []
        self.summer_questions = []
        self.film_questions = []
        self.music_questions = []
        self.minecraft_questions = []
        self.all_normal_questions = []

        self.bonus_questions = {}

        self.bonus_round_len = 5
        self.bonus_question_index = 0

        self.current_multiplier = 1

        self.question_answered = False
        self.new_answer_key = ""

        self.current_quiz_question = None
        self.current_question_index = 0

        self.buttons = []

        self.total_score = 0
        self.bonus_round = False
        self.round_num = 1
        self.questions_asked_in_current_round = 0
        self.total_asked_questions = 1

        self.is_running = True

        self.question_timed_out = False

        self.total_len = 0
        self.total_correct_answers = 0

        self.timer = 15.0
        self.timer_acc = 0.0

        self.questions_per_round = 10

    def start(self, transition_data):
        self.picked_bonus_round = transition_data['picked_bonus_round']

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((220, 220, 220))

        with open("data/autumn_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.autumn_questions.append(QuizQuestion(int(row[0]), row[1], row[2], row[3], row[4], row[5]))

        with open("data/spring_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.spring_questions.append(QuizQuestion(row[0], row[1], row[2], row[3], row[4], row[5]))

        with open("data/summer_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.summer_questions.append(QuizQuestion(row[0], row[1], row[2], row[3], row[4], row[5]))

        with open("data/film_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.film_questions.append(QuizQuestion(row[0], row[1], row[2], row[3], row[4], row[5]))

        with open("data/music_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.music_questions.append(QuizQuestion(row[0], row[1], row[2], row[3], row[4], row[5]))

        with open("data/minecraft_questions.csv") as questions_file:
            read_csv = csv.reader(questions_file, delimiter=',')
            for row in read_csv:
                if len(row) == 6:
                    self.minecraft_questions.append(QuizQuestion(row[0], row[1], row[2], row[3], row[4], row[5]))

        random.shuffle(self.autumn_questions)
        random.shuffle(self.spring_questions)
        random.shuffle(self.summer_questions)
        random.shuffle(self.film_questions)
        random.shuffle(self.music_questions)
        random.shuffle(self.minecraft_questions)

        self.all_normal_questions = self.autumn_questions + self.spring_questions + self.summer_questions
        random.shuffle(self.all_normal_questions)

        self.bonus_questions = {"film": self.film_questions,
                                "music": self.music_questions,
                                "minecraft": self.minecraft_questions}

        self.bonus_round_len = 5
        self.bonus_question_index = 0

        self.current_multiplier = 1

        self.question_answered = False
        self.new_answer_key = ""

        self.current_quiz_question = self.all_normal_questions[0]
        self.current_question_index = 0

        self.total_len = self.bonus_round_len
        self.total_len += len(self.all_normal_questions)

        self.setup_buttons()

    def shutdown(self):
        self.transition_data['total_len'] = self.total_asked_questions
        self.transition_data['total_answered'] = self.total_correct_answers
        self.transition_data['final_score'] = self.total_score

        self.time_to_transition = False

        self.background = None

        self.autumn_questions = []
        self.spring_questions = []
        self.summer_questions = []
        self.film_questions = []
        self.music_questions = []
        self.all_normal_questions = []

        self.bonus_questions = {}

        self.current_quiz_question = None
        self.picked_bonus_round = ""
        self.time_to_transition = False
        self.total_score = 0
        self.bonus_round = False
        self.round_num = 1
        self.questions_asked_in_current_round = 0
        self.total_asked_questions = 1
        self.total_correct_answers = 0
        self.total_len = 0

        self.buttons[:] = []

        return self.transition_data

    def setup_buttons(self):
        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.1),
                                          int(self.screen_size[1] * 0.5),
                                          int(self.screen_size[0] * 0.6),
                                          50),
                                         self.current_quiz_question.answer_a, self.fonts, 0))
        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.1),
                                          int(self.screen_size[1] * 0.5) + 100,
                                          int(self.screen_size[0] * 0.6),
                                          50),
                                         self.current_quiz_question.answer_b, self.fonts, 0))
        self.buttons.append(UITextButton((int(self.screen_size[0] * 0.1),
                                          int(self.screen_size[1] * 0.5) + 200,
                                          int(self.screen_size[0] * 0.6),
                                          50),
                                         self.current_quiz_question.answer_c, self.fonts, 0))

    def process_event(self, event):
        for button in self.buttons:
            button.handle_input_event(event)

    def run(self, time_delta):
        self.timer_acc += time_delta
        if self.timer_acc > self.timer:
            self.timer_acc = 0.0
            self.question_timed_out = True

        if self.buttons[0].was_pressed():
            self.question_answered = True
            self.new_answer_key = "a"

        if self.buttons[1].was_pressed():
            self.question_answered = True
            self.new_answer_key = "b"

        if self.buttons[2].was_pressed():
            self.question_answered = True
            self.new_answer_key = "c"
    
        if self.question_answered:
            if self.new_answer_key.upper() == self.current_quiz_question.right_answer.upper():
                self.total_score += 50 * self.current_multiplier
                self.total_correct_answers += 1
    
        if self.question_timed_out or self.question_answered:
            self.timer_acc = 0.0
            self.question_answered = False
            self.question_timed_out = False
            self.total_asked_questions += 1
            if self.bonus_round:
                self.current_multiplier = 2
                self.bonus_question_index += 1
                if self.bonus_question_index < self.bonus_round_len:
                    self.current_quiz_question = self.bonus_questions[self.picked_bonus_round][
                        self.bonus_question_index]

                    self.buttons[:] = []
                    self.setup_buttons()
                else:
                    self.bonus_round = False

            if not self.bonus_round:
                self.questions_asked_in_current_round += 1
                if self.questions_asked_in_current_round == self.questions_per_round:
                    self.round_num += 1
                    self.questions_asked_in_current_round = 0
                    self.bonus_round = True

                    # start bonus round
                    self.current_multiplier = 2
                    self.current_quiz_question = self.bonus_questions[self.picked_bonus_round][
                        self.bonus_question_index]

                    self.buttons[:] = []
                    self.setup_buttons()

                else:
                    self.current_multiplier = 1

                    self.new_answer_key = ""
                    self.current_question_index += 1

                    if self.current_question_index < len(self.all_normal_questions):
                        self.current_quiz_question = self.all_normal_questions[self.current_question_index]

                        self.buttons[:] = []
                        self.setup_buttons()

                if self.round_num > 2:
                    self.time_to_transition = True

        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.update()
            button.draw(self.screen)

        score_text_render = self.fonts[0].render("Score: " + str(self.total_score), True, pygame.Color(0, 0, 0))
        score_text_render_rect = score_text_render.get_rect(x=self.screen_size[0] * 0.8,
                                                            centery=self.screen_size[1] * 0.05)
        self.screen.blit(score_text_render, score_text_render_rect)

        round_text = "Round: " + str(self.round_num)
        if self.bonus_round:
            round_text = "Round: Bonus Round! x2 Points!"
        round_text_render = self.fonts[0].render(round_text, True, pygame.Color(0, 0, 0))
        round_text_render_rect = round_text_render.get_rect(x=self.screen_size[0] * 0.05,
                                                            centery=self.screen_size[1] * 0.05)
        self.screen.blit(round_text_render, round_text_render_rect)

        question_number_text = "Question: " + str(self.total_asked_questions)
        question_number_text_render = self.fonts[0].render(question_number_text, True, pygame.Color(0, 0, 0))
        question_number_text_render_rect = question_number_text_render.get_rect(centerx=self.screen_size[0] * 0.5,
                                                                                centery=self.screen_size[1] * 0.05)
        self.screen.blit(question_number_text_render, question_number_text_render_rect)

        q_text = self.current_quiz_question.question
        render_word_wrapped_text(self.screen, (int(self.screen_size[0] * 0.1),
                                               int(self.screen_size[1] * 0.3),
                                               int(self.screen_size[0] * 0.8),
                                               int(self.screen_size[1] * 0.3)),
                                 q_text, self.fonts[0], self.fonts[0], time_delta, pygame.Color(0, 0, 0))

        outer_rect = pygame.Rect(int(self.screen_size[0] * 0.8),
                                 int(self.screen_size[1] * 0.5),
                                 int(self.screen_size[0] * 0.075),
                                 int(self.screen_size[1] * 0.35))
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), outer_rect, 3)
        bar_height = int((int(self.screen_size[1] * 0.35) - 2) * (1.0 - self.timer_acc / 15.0))
        bar_start = int(int(self.screen_size[1] * 0.5) + 2 + (int(self.screen_size[1] * 0.35) - 4) * self.timer_acc / 15.0)

        inner_rect = pygame.Rect(int(self.screen_size[0] * 0.8) + 2, bar_start,
                                 int(self.screen_size[0] * 0.075) - 3, bar_height)
        inner_rect.bottom = outer_rect.bottom-2
        pygame.draw.rect(self.screen, pygame.Color(100, 0, 0), inner_rect)

        return self.is_running
