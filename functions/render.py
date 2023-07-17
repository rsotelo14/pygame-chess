import pygame
import vars

def highlight_last_move(window):

    y_1, x_1 = vars.number_to_position_map[vars.last_move.start_square_num]
    square = vars.board[y_1][x_1]
    window.blit(vars.HIGHLIGHT_SQUARE, (square.x_start, square.y_start))
    y_2, x_2 = vars.number_to_position_map[vars.last_move.target_square_num]
    square = vars.board[y_2][x_2]
    window.blit(vars.HIGHLIGHT_SQUARE, (square.x_start, square.y_start))

def highlight_checked_square(window):
    for rank in vars.board:
        for square in rank:
            if square.piece == None:
                continue
            if square.piece.value == 10 and square.piece.is_white == vars.white_moves:
                window.blit(vars.HIGHLIGHT_CHECKED_SQUARE, (square.x_start,square.y_start))

def highlight_possible_squares(board, window):
    for move in vars.piece_possible_moves:
        target_square_num = move.target_square_num
        y,x = vars.number_to_position_map[target_square_num]
        square = vars.board[y][x]            
        if move.start_square_num != move.target_square_num:
            window.blit(vars.HIGHLIGHT_DOT, (square.x_start, square.y_start))
        else:
            window.blit(vars.HIGHLIGHT_SQUARE, (square.x_start, square.y_start)) 

def render_selected_piece(x_start, y_start , window):
    x = x_start - vars.selected_piece.img.get_width()/2
    y = y_start - vars.selected_piece.img.get_height()/2
    window.blit(vars.selected_piece.img, (x,y))

def render_pieces(board, window):
    for rank in board:
        for square in rank:
            if square.piece != None:
                piece = square.piece
                x = square.x_start +square.width_height/2 - piece.img.get_width()/2
                y = square.y_start +square.width_height/2 - piece.img.get_height()/2
                window.blit(piece.img, (x,y))
