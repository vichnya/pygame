import pygame

class Menu:
    def __init__(self, game):

        self.game = game
        self.screen = game.screen

        # Загрузка изображений
        self.bg = pygame.image.load('images/bg.png').convert()
        self.bg_start = pygame.image.load('images/bg1.png').convert()
        self.bg_score = pygame.image.load('images/bg2.png').convert()
        self.bg_education1 = pygame.image.load('images/bg_education1.png').convert()
        self.bg_education2 = pygame.image.load('images/bg_education2.png').convert()
        self.bg_education3 = pygame.image.load('images/bg_education3.png').convert()

        # Флаг для отображения меню игры при старте
        self.in_start_menu = True

        # Флаг для отображения меню счета
        self.in_score_menu = False

        # Флаг для отображения меню обучения
        self.in_education_menu = False
        self.education_page = 1

    def handle_events(self):
        # Обработка событий в меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.in_start_menu = True
                    self.in_education_menu = False
                    self.in_score_menu = False
                    self.game.gameplay.reset_game()

            if self.in_start_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_start_menu_click(event.pos)
            elif self.in_score_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_score_menu_click(event.pos)
            elif self.in_education_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_education_menu_click(event.pos)

            if event.type == self.game.gameplay.ghost_timer:
                self.game.gameplay.spawn_ghost()

    def handle_start_menu_click(self, pos):
        # Обработка нажатий в меню старта
        if 50 < pos[0] < 360 and 205 < pos[1] < 255:
            self.in_start_menu = False
            self.game.gameplay.reset_game()
        elif 50 < pos[0] < 360 and 265 < pos[1] < 313:
            self.in_score_menu = True
            self.in_start_menu = False
        elif 388 < pos[0] < 698 and 265 < pos[1] < 315:
            self.game.running = False
        elif 388 < pos[0] < 698 and 208 < pos[1] < 253:
            self.in_education_menu = True
            self.in_start_menu = False
            self.education_page = 1

    def handle_education_menu_click(self, pos):
        # Обработка нажатий в меню обучения
        if self.education_page == 1 and 573 < pos[0] < 638 and 305 < pos[1] < 370:
            self.education_page = 2
        elif self.education_page == 2 and 573 < pos[0] < 638 and 305 < pos[1] < 370:
            self.education_page = 3

        if 29 < pos[0] < 73 and 29 < pos[1] < 73:
            self.in_start_menu = True
            self.in_education_menu = False

    def handle_score_menu_click(self, pos):
        # Обработка нажатий в меню счета
        if 29 < pos[0] < 73 and 29 < pos[1] < 73:
            self.in_start_menu = True
            self.in_score_menu = False

    def render_start_menu(self):
        # Отрисовка меню старта
        self.screen.blit(self.bg_start, (0, 0))

    def render_score_menu(self):
        # Отрисовка меню счета
        self.screen.blit(self.bg_score, (0, 0))
        self.game.b_score.read_best_scores()
        y_offset = 120
        for i, score in enumerate(self.game.b_score.best_scores):
            score_label = self.game.font.render(f'{score}', True, (38, 56, 64))
            self.screen.blit(score_label, (350, y_offset))
            y_offset += 56

    def render_education_menu(self):
        # Отрисовка меню обучения
        if self.education_page == 1:
            self.screen.blit(self.bg_education1, (0, 0))
        elif self.education_page == 2:
            self.screen.blit(self.bg_education2, (0, 0))
        elif self.education_page == 3:
            self.screen.blit(self.bg_education3, (0, 0))

    def render(self):
        # Отрисовка игрового фона
        if self.in_start_menu:
            self.render_start_menu()
        elif self.in_score_menu:
            self.render_score_menu()
        elif self.in_education_menu:
            self.render_education_menu()
        else:
            self.screen.blit(self.bg, (self.game.gameplay.bg_x, 0))
            self.screen.blit(self.bg, (self.game.gameplay.bg_x + 750, 0))
            self.screen.blit(self.game.gameplay.answ, (0, 50))
            if self.game.gameplay.gameplay:
                self.game.gameplay.render_gameplay()
            self.game.gameplay.render_lives()
            self.game.gameplay.render_score()