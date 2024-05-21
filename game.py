import pygame

from questions import Questions
from best_score import BestScore
from menu import Menu
from gameplay import Gameplay

class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        # Создание окна игры
        self.screen = pygame.display.set_mode((750, 428))
        pygame.display.set_caption('White pooch')
        pygame.display.set_icon(pygame.image.load('images/player_right/player_right1.png'))

        # Загрузка шрифтов
        self.font = pygame.font.Font('fonts/HanaleiFill-Regular.ttf', 40)
        self.minifont = pygame.font.Font('fonts/HanaleiFill-Regular.ttf', 30)

        # Загрузка и воспроизведение фоновой музыки
        self.bg_sound = pygame.mixer.Sound('sound/bg.mp3')
        self.bg_sound.play()

        # Переменная для хранения счета
        self.score = 0

        # Флаг для основного цикла игры
        self.running = False

        # Флаг для разрешения движения игрока
        self.movement_allowed = True

        # Создание экземпляров классов для управления игрой
        self.b_score = BestScore(self)
        self.questions = Questions(self)
        self.menu = Menu(self)
        self.gameplay = Gameplay(self)


    def handle_events(self):
        # Обработка событий
        self.menu.handle_events()

    def update(self):
        # Обновление состояния игры
        self.gameplay.update()

    def render(self):
        # Отрисовка состояния игры
        self.menu.render()

    def run(self):
        # Основной игровой цикл
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(15)

        pygame.quit()