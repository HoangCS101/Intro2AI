import pygame as p
import ChessEngine

board_width = board_height = 680  
dimension = 8  
sq_size = board_height // dimension
max_fps = 15  
images = {}
colours = [p.Color('#EBEBD0'), p.Color('#769455')]  

move_log_panel_width = 210
move_log_panel_height = board_height

def draw_game_state(screen, game_state, square_selected, font, colours, images, board_width, move_log_panel_width,
                    move_log_panel_height, sq_size, dimension):
    draw_board(screen, colours, board_width, move_log_panel_width, move_log_panel_height, sq_size, dimension)
    draw_pieces(screen, game_state.board, images, sq_size)
    highlight_squares(screen, game_state, square_selected, colours, sq_size)
    draw_move_log(screen, game_state.move_log, font, board_width, move_log_panel_width, move_log_panel_height, sq_size)
    draw_turn_indicator(screen, game_state.white_to_move, colours, board_width, move_log_panel_width)

def draw_board(screen, colours, board_width, move_log_panel_width, move_log_panel_height, sq_size, dimension):
    light_square_color, dark_square_color = colours
    for row in range(dimension):
        for col in range(dimension):
            color = light_square_color if (row + col) % 2 == 0 else dark_square_color
            p.draw.rect(screen, color, p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))

    p.draw.rect(screen, p.Color('black'), p.Rect(board_width, 0, move_log_panel_width, move_log_panel_height))

def draw_pieces(screen, board, images, sq_size):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                screen.blit(images[piece], p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))

def highlight_squares(screen, game_state, square_selected, colours, sq_size):
    if square_selected:
        row, col = square_selected
        highlight = p.Surface((sq_size, sq_size))
        highlight.set_alpha(100)
        highlight.fill(p.Color('yellow'))
        screen.blit(highlight, (col * sq_size, row * sq_size))

    if game_state.checkers:
        for square in game_state.checkers:
            row, col = square
            highlight = p.Surface((sq_size, sq_size))
            highlight.set_alpha(100)
            highlight.fill(p.Color('red'))
            screen.blit(highlight, (col * sq_size, row * sq_size))

def draw_move_log(screen, move_log, font, board_width, move_log_panel_width, move_log_panel_height, sq_size):
    move_log_rect = p.Rect(board_width, 0, move_log_panel_width, move_log_panel_height)
    p.draw.rect(screen, p.Color('lightgray'), move_log_rect)
    current_y = 5
    for move in move_log:
        move_text = font.render(move.get_chess_notation(), True, p.Color('black'))
        screen.blit(move_text, (board_width + 5, current_y))
        current_y += 25

def draw_turn_indicator(screen, white_to_move, colours, board_width, move_log_panel_width):
    turn_text = 'White to move' if white_to_move else 'Black to move'
    font = p.font.SysFont('Arial', 16, False, False)
    turn_text = font.render(turn_text, True, p.Color('black'))
    screen.blit(turn_text, (board_width + 5, move_log_panel_width - 25))

def draw_endgame_text(screen, text, board_width, board_height):
    font = p.font.SysFont('Arial', 32, True, False)
    endgame_text = font.render(text, True, p.Color('black'))
    screen.blit(endgame_text, (board_width / 2 - endgame_text.get_width() / 2, board_height / 2 - endgame_text.get_height() / 2))

def animate_move(move, screen, board, clock, colours, images, sq_size):
    start_square = move.start_square
    end_square = move.end_square
    piece = board[start_square[0]][start_square[1]]
    color = colours[1] if (start_square[0] + start_square[1]) % 2 == 0 else colours[0]
    delta_x = (end_square[1] - start_square[1]) * sq_size
    delta_y = (end_square[0] - start_square[0]) * sq_size
    x, y = start_square[1] * sq_size, start_square[0] * sq_size
    move_duration = 0.2
    clock.tick()
    start_ticks = p.time.get_ticks()
    while p.time.get_ticks() - start_ticks < move_duration * 1000:
        for event in p.event.get():
            if event.type == p.QUIT:
                return
        screen.fill(p.Color('white'))
        draw_board(screen, colours, board_width, move_log_panel_width, move_log_panel_height, sq_size, 8)
        draw_pieces(screen, board, images, sq_size)
        piece_rect = p.Rect(x + delta_x * (p.time.get_ticks() - start_ticks) / (move_duration * 1000),
                            y + delta_y * (p.time.get_ticks() - start_ticks) / (move_duration * 1000), sq_size, sq_size)
        screen.blit(images[piece], piece_rect)
        p.display.flip()
