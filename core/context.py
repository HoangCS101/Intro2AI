class Context:
    def __init__(self):
        self.player_ai_difficulty = None
        self.player_ai_func = None

        self.white_ai_difficulty = None
        self.white_ai_func = None

        self.black_ai_difficulty = None
        self.black_ai_func = None

        self.current_scene = None

    def set_player_ai(self, difficulty, func):
        self.player_ai_difficulty = difficulty
        self.player_ai_func = func

    def set_ai_vs_ai(self, white_diff, white_func, black_diff, black_func):
        self.white_ai_difficulty = white_diff
        self.white_ai_func = white_func
        self.black_ai_difficulty = black_diff
        self.black_ai_func = black_func