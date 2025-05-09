import pygame
from core.scene import Scene
import ChessEngine

class GameplayAIAIScene(Scene):
    def __init__(self, screen, context, switch_scene):
        super().__init__(screen, context)
        self.switch_scene = switch_scene
        self.board_width = self.board_height = 680
        self.dimension = 8
        self.sq_size = self.board_height // self.dimension
        self.max_fps = 15
        self.images = {}
        self.colours = [pygame.Color('#EBEBD0'), pygame.Color('#769455')]
        self.move_log_panel_width = 210
        self.move_log_panel_height = self.board_height
        self.move_log_font = pygame.font.SysFont('Arial', 14, False, False)
        self.endgame_font = pygame.font.SysFont('Helvetica', 32, True, False)
        
        # Game state
        self.game_state = ChessEngine.GameState()
        self.valid_moves = self.game_state.get_valid_moves()
        self.move_made = False
        self.animate = False
        self.square_selected = ()  # Tuple rỗng như code gốc
        self.player_clicks = []
        self.game_over = False


        # Clock
        self.clock = pygame.time.Clock()
        
        # Load images
        self.load_images()

    def load_images(self):
        pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP',
                  'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
        for piece in pieces:
            self.images[piece] = pygame.transform.smoothscale(
                pygame.image.load(f'images/{piece}.png'), (self.sq_size, self.sq_size))

    def handle_event(self, event):
        
        
        
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and self.human_turn:
            location = pygame.mouse.get_pos()
            column = location[0] // self.sq_size
            row = location[1] // self.sq_size
            if self.square_selected == (row, column) or column >= self.dimension:
                self.square_selected = ()
                self.player_clicks = []
            else:
                self.square_selected = (row, column)
                self.player_clicks.append(self.square_selected)      
                if len(self.player_clicks) == 2:
                    move = ChessEngine.Move(self.player_clicks[0], self.player_clicks[1], self.game_state.board)
                    for i in range(len(self.valid_moves)):
                        if move == self.valid_moves[i]:
                            self.game_state.make_move(self.valid_moves[i])
                            self.move_made = True
                            self.animate = True
                            self.square_selected = ()
                            self.player_clicks = []
                            break
                    if not self.move_made:
                        self.player_clicks = [self.square_selected]
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:  # Undo move
                self.game_state.undo_move()
                self.move_made = True
                self.animate = False
                self.game_over = False
                self.square_selected = ()  # Tuple rỗng
            elif event.key == pygame.K_r:  # Reset board
                self.game_state = ChessEngine.GameState()
                self.valid_moves = self.game_state.get_valid_moves()
                self.square_selected = ()  # Tuple rỗng
                self.player_clicks = []
                self.move_made = False
                self.animate = False
                self.game_over = False
            elif event.key == pygame.K_ESCAPE:  # Return to main menu
                self.switch_scene("main_menu")

    def update(self):
        if not self.game_over:
            ai_move = self.context.white_ai_func(self.game_state, self.valid_moves, "white")
            print(ai_move)
            if not self.game_state.white_to_move:
                ai_move = self.context.black_ai_func(self.game_state, self.valid_moves, "black")
            if ai_move is None:
                ai_move = self.random_move()
            self.game_state.make_move(ai_move)
            self.move_made = True
            self.animate = True
        
        if self.move_made:
            if self.animate:
                self.animate_move(self.game_state.move_log[-1])
            self.valid_moves = self.game_state.get_valid_moves()
            self.move_made = False
            self.animate = False
        
        self.clock.tick(self.max_fps)
        

    def render(self):
        self.screen.fill(pygame.Color('white'))
        self.draw_game_state()
        if self.game_state.checkmate or self.game_state.stalemate:
            self.game_over = True
            if self.game_state.stalemate:
                text = 'Stalemate'
            else:
                text = 'Black wins by checkmate' if self.game_state.white_to_move else 'White wins by checkmate'
            self.draw_endgame_text(text)
        pygame.display.flip()

    def draw_game_state(self):
        self.draw_board()
        self.highlight_squares()
        self.draw_pieces()
        self.draw_move_log()

    def draw_board(self):
        for row in range(self.dimension):
            for column in range(self.dimension):
                colour = self.colours[((row + column) % 2)]
                pygame.draw.rect(self.screen, colour,
                               pygame.Rect(column * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def highlight_squares(self):
        if self.square_selected != ():
            row, column = self.square_selected
            if self.game_state.board[row][column][0] == ('w' if self.game_state.white_to_move else 'b'):
                s = pygame.Surface((self.sq_size, self.sq_size))
                s.set_alpha(70)
                s.fill(pygame.Color('yellow'))
                self.screen.blit(s, (column * self.sq_size, row * self.sq_size))
        
        if len(self.game_state.move_log) != 0:
            last_move = self.game_state.move_log[-1]
            s = pygame.Surface((self.sq_size, self.sq_size))
            s.set_alpha(70)
            s.fill(pygame.Color('yellow'))
            self.screen.blit(s, (last_move.start_column * self.sq_size, last_move.start_row * self.sq_size))
            self.screen.blit(s, (last_move.end_column * self.sq_size, last_move.end_row * self.sq_size))

    def draw_pieces(self):
        for row in range(self.dimension):
            for column in range(self.dimension):
                piece = self.game_state.board[row][column]
                if piece != '--':
                    self.screen.blit(self.images[piece],
                                   pygame.Rect(column * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def draw_move_log(self):
        move_log_area = pygame.Rect(self.board_width, 0, self.move_log_panel_width, self.move_log_panel_height)
        pygame.draw.rect(self.screen, pygame.Color('#2d2d2e'), move_log_area)
        move_log = self.game_state.move_log
        move_texts = []
        for i in range(0, len(move_log), 2):
            move_string = f'{i // 2 + 1}. {str(move_log[i])} '
            if i + 1 < len(move_log):
                move_string += f'{str(move_log[i + 1])} '
            move_texts.append(move_string)
        
        move_per_row = 2
        padding = 5
        line_spacing = 2
        text_y = padding
        for i in range(0, len(move_texts), move_per_row):
            text = ''
            for j in range(move_per_row):
                if i + j < len(move_texts):
                    text += move_texts[i + j]
            text_object = self.move_log_font.render(text, True, pygame.Color('whitesmoke'))
            text_location = move_log_area.move(padding, text_y)
            self.screen.blit(text_object, text_location)
            text_y += text_object.get_height() + line_spacing

    def animate_move(self, move):
        delta_row = move.end_row - move.start_row
        delta_column = move.end_column - move.start_column
        frames_per_square = 5
        frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square
        
        for frame in range(frame_count + 1):
            row = move.start_row + delta_row * frame / frame_count
            column = move.start_column + delta_column * frame / frame_count
            self.draw_board()
            self.draw_pieces()
            colour = self.colours[(move.end_row + move.end_column) % 2]
            end_square = pygame.Rect(move.end_column * self.sq_size, move.end_row * self.sq_size,
                                  self.sq_size, self.sq_size)
            pygame.draw.rect(self.screen, colour, end_square)
            if move.piece_captured != '--':
                if move.is_en_passant_move:
                    en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                    end_square = pygame.Rect(move.end_column * self.sq_size, en_passant_row * self.sq_size,
                                          self.sq_size, self.sq_size)
                self.screen.blit(self.images[move.piece_captured], end_square)
            self.screen.blit(self.images[move.piece_moved],
                           pygame.Rect(column * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))
            pygame.display.flip()
            self.clock.tick(60)

    def draw_endgame_text(self, text):
        text_object = self.endgame_font.render(text, True, pygame.Color('gray'), pygame.Color('mintcream'))
        text_location = pygame.Rect(0, 0, self.board_width, self.board_height).move(
            self.board_width / 2 - text_object.get_width() / 2,
            self.board_height / 2 - text_object.get_height() / 2)
        self.screen.blit(text_object, text_location)
        text_object = self.endgame_font.render(text, True, pygame.Color('black'))
        self.screen.blit(text_object, text_location.move(2, 2))

    def random_move(self):
        from random import choice
        return choice(self.valid_moves) if self.valid_moves else None