import pygame

class Gameplay:
    def __init__(self, game):

        self.game = game
        self.screen = game.screen

        # Загрузка изображений
        self.bg = pygame.image.load('images/bg.png').convert()
        self.ghost = pygame.image.load('images/ghost.png').convert_alpha()
        self.answ = pygame.image.load('images/answers.png').convert_alpha()
        self.crate = pygame.image.load('images/crate.png').convert_alpha()
        self.heart = pygame.image.load('images/heart.png').convert_alpha()

        # Загрузка спрайтов для анимации движения игрока
        self.walk_right = [
            pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
            pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
            pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
            pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
            pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
            pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
            pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
        ]

        # Параметры игрока
        self.player_speed = 5
        self.player_x = 50
        self.player_y = 345
        self.is_jump = False
        self.jump_count = 9
        self.player_anim_count = 0

        # Параметры фона
        self.bg_x = 0

        # Список призраков и таймер появления призраков
        self.ghost_list_in_game = []
        self.ghost_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ghost_timer, 8000)

        # Количество жизней и время последнего столкновения с призраком
        self.lives = 3
        self.last_collision_time = pygame.time.get_ticks()

        # Флаг для управления игровым процессом
        self.gameplay = True

    def update(self):
        # Обновление состояния игры
        keys = pygame.key.get_pressed()
        if self.game.movement_allowed:
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.player_x > 50:
                self.player_x -= self.player_speed
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.player_x < 200:
                self.player_x += self.player_speed

        if self.game.questions.question_active:
            self.game.questions.handle_question(keys)
        else:
            self.handle_jump(keys)

        if self.player_anim_count == 3:
            self.player_anim_count = 0
        else:
            self.player_anim_count += 1

        if self.game.movement_allowed:
            self.bg_x -= 2
            if self.bg_x == -750:
                self.bg_x = 0

    def handle_jump(self, keys):
        # Обработка прыжка игрока
        if self.game.movement_allowed:
            if not self.is_jump:
                if keys[pygame.K_SPACE]:
                    self.is_jump = True
            else:
                if self.jump_count >= -9:
                    self.player_y -= (self.jump_count * abs(self.jump_count)) / 2
                    self.jump_count -= 1
                else:
                    self.is_jump = False
                    self.jump_count = 9

    def spawn_ghost(self):
        # Создание призрака
        self.ghost_list_in_game.append(self.ghost.get_rect(topleft=(755, 355)))

        if len(self.ghost_list_in_game) == 1:
            self.game.questions.ask_question()

    def handle_ghost_collision(self):
        # Обработка столкновения с призраком
        self.lives -= 1
        if self.lives == 0:
            self.game.b_score.read_best_scores()
            self.game.b_score.update_best_scores()
            self.game.menu.in_score_menu = True
        else:
            self.last_collision_time = pygame.time.get_ticks()
        self.game.movement_allowed = True

    def render_gameplay(self):
        # Отрисовка процесса игры
        player_rect = self.walk_left[0].get_rect(topleft=(self.player_x, self.player_y))
        current_time = pygame.time.get_ticks()

        for (i, el) in enumerate(self.ghost_list_in_game):
            self.screen.blit(self.ghost, el)
            el.x -= 10

            if el.x < -10:
                self.ghost_list_in_game.pop(i)

            if player_rect.colliderect(el) and current_time - self.last_collision_time > 1000:
                self.handle_ghost_collision()

        keys = pygame.key.get_pressed()
        if self.game.movement_allowed:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.screen.blit(self.walk_left[self.player_anim_count], (self.player_x, self.player_y))
            else:
                self.screen.blit(self.walk_right[self.player_anim_count], (self.player_x, self.player_y))
        else:
            self.screen.blit(self.walk_right[0], (self.player_x, self.player_y))
            self.screen.blit(self.crate, (self.player_x - 5, self.player_y - 10))

        if self.game.questions.question_active:
            self.game.questions.render_question()

    def render_lives(self):
        # Отрисовка количества жизней
        lives_label = self.game.minifont.render(f'x{self.lives}', False, (181, 228, 249))
        self.screen.blit(self.heart, (10, 10))
        self.screen.blit(lives_label, (50, 5))

    def render_score(self):
        # Отрисовка текущего счета
        score_label = self.game.minifont.render(f'{self.game.score}', False, (181, 228, 249))
        self.screen.blit(score_label, (700, 5))

    def reset_game(self):
        # Сброс игры
        self.gameplay = True
        self.player_x = 50
        self.ghost_list_in_game.clear()
        self.lives = 3
        self.game.score = 0
