import pygame
import random

class Questions:
    def __init__(self, game):

        self.game = game

        # Параметры вопросов и ответов
        self.question_active = False
        self.question_text = ''
        self.answers = []
        self.correct_answer = ''
        self.answered_correctly = False

    def ask_question(self):
        # Создание вопроса и ответов
        self.op1 = random.randint(0, 9)
        self.op2 = random.randint(0, 9)
        self.apt = random.choice(['+', '-'])
        while self.apt == '-' and self.op1 < self.op2:
            self.op1 = random.randint(0, 9)
            self.op2 = random.randint(0, 9)
        self.question_active = True
        self.question_text = f'{self.op1} {self.apt} {self.op2} = ?'
        if self.apt == '+':
            self.correct_answer = str(self.op1 + self.op2)
        elif self.apt == '-':
            self.correct_answer = str(self.op1 - self.op2)
        self.answers = [self.correct_answer]
        while len(self.answers) < 4:
            new_answer = str(random.randint(0, 18))
            if new_answer != self.correct_answer and new_answer not in self.answers:
                self.answers.append(new_answer)
        random.shuffle(self.answers)

    def handle_question(self, keys):
        # Обработка ответа на вопрос
        if keys[pygame.K_1]:
            self.check_answer(self.answers[0])
        elif keys[pygame.K_2]:
            self.check_answer(self.answers[1])
        elif keys[pygame.K_3]:
            self.check_answer(self.answers[2])
        elif keys[pygame.K_4]:
            self.check_answer(self.answers[3])

    def check_answer(self, answer):
        # Проверка правильности ответа
        if answer == self.correct_answer:
            self.answered_correctly = True
            self.question_active = False
            self.game.score += 10
        else:
            self.answered_correctly = False
            self.question_active = False
            self.game.movement_allowed = False

    def render_question(self):
        # Отрисовка вопроса и ответов
        question_label = self.game.font.render(self.question_text, False, 'White')
        self.game.screen.blit(question_label, (320, 60))

        answer_x1 = 160
        answer_x2 = 520
        answer_y = 83

        for idx, answer in enumerate(self.answers):
            if idx % 2 == 0:
                answer_x = answer_x1
            else:
                answer_x = answer_x2

            if idx % 2 == 0:
                answer_y += 46

            answer_label = self.game.minifont.render(f'{idx + 1}. {answer}', False, 'White')
            self.game.screen.blit(answer_label, (answer_x, answer_y))