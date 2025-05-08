import ChessAI

def get_ai_function(difficulty):
    if difficulty == "easy":
        return ChessAI.find_easy_move
    elif difficulty == "medium":
        return ChessAI.find_medium_move
    elif difficulty == "hard":
        return ChessAI.find_hard_move
    else:
        return ChessAI.find_rand_move

