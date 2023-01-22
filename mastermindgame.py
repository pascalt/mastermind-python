import random

NB_COLORS = 6
NB_DIGITS = 4
MAX_ROUND = 10


class MasterMindGame:
    def __init__(self, max_round=MAX_ROUND, nb_colors=NB_COLORS, nb_digits=NB_DIGITS):
        self.nb_wrong_places = 0
        self.nb_right_places = 0
        self.max_round = max_round
        self.nb_colors = nb_colors
        self.nb_digits = nb_digits
        self._set_secret_code()
        self.code_played = [[-1, -1, -1, -1]]
        self.round = 0
        self.found = False
        self.loose = False

    def _set_secret_code(self):
        self.secret_code = []
        for i in range(self.nb_digits):
            self.secret_code.append(random.randint(0, self.nb_colors - 1))


    def evaluate(self):
        """Counting the backs (good color in the right place) and the whites (good color in the wrong place"""

        # working list _tmp to tag value when mathing
        code_played_tmp = self.code_played[self.round].copy()
        secret_code_tmp = self.secret_code.copy()

        self.nb_right_places = 0
        self.nb_wrong_places = 0

        # the blacks : same value, same place, tag at -1 if they match
        for i in range(self.nb_digits):
            if code_played_tmp[i] == secret_code_tmp[i]:
                self.nb_right_places += 1
                code_played_tmp[i] = -1
                secret_code_tmp[i] = -1

        # the whites : same value, tag at -1 if they match
        for i in range(self.nb_digits):
            if secret_code_tmp[i] >= 0:
                for j in range(self.nb_digits):
                    if 0 <= secret_code_tmp[i] == code_played_tmp[j] >= 0:
                        self.nb_wrong_places += 1
                        code_played_tmp[j] = -1
                        secret_code_tmp[i] = -1

        self.found = self.nb_right_places == self.nb_digits

        self.round += 1
        self.loose = self.round == self.max_round
        self.code_played.append([-1, -1, -1, -1])

    def play_a_color(self, col, value):
        self.code_played[self.round][col] = value

    def reset_game(self):
        self.nb_wrong_places = 0
        self.nb_right_places = 0
        self._set_secret_code()
        self.code_played = [[-1, -1, -1, -1]]
        self.round = 0
        self.found = False
        self.loose = False
