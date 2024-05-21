class BestScore:

    def __init__(self, game):

        self.game = game

        # Атрибут для хранения лучших результатов
        self.best_scores = []

    def read_best_scores(self):
        # Чтение лучших результатов
        try:
            with open('score.txt', 'r') as file:
                lines = file.readlines()
                self.best_scores = [int(score.strip()) for score in lines]
                return self.best_scores
        except FileNotFoundError:
            self.best_scores = [0] * 5
            return self.best_scores

    def update_best_scores(self):
        # Обновление лучших результатов
        best_scores = self.read_best_scores()
        new_score = self.game.score

        if not best_scores:
            best_scores.append(new_score)
        else:
            for i, score in enumerate(best_scores):
                if new_score > score:
                    best_scores.insert(i, new_score)
                    break
            else:
                best_scores.append(new_score)
            best_scores = best_scores[:5]
        try:
            with open('score.txt', 'w') as file:
                for score in best_scores:
                    file.write(str(score) + '\n')
        except Exception as e:
            print('Ошибка при записи новых лучших счетов:', e)