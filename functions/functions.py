import os
import pygame
from entities.board_square import BoardSquare
from entities.move import Move

from entities.piece import Piece
import vars

def make_board():
    is_white = False

    y_start = 0
    number = 0
    for y in range(8):
        x_start = 0
        rank = []
        is_white = not is_white
        for x in range(8):
            bs = BoardSquare(x_start, y_start, vars.WIDTH, is_white, number)
            rank.append(bs)
            is_white = not is_white
            number += 1
            x_start += vars.WIDTH
        vars.board.append(rank)
        y_start += vars.WIDTH

def initial_position():
    #BLACK PIECES
    #King
    piece = Piece(False, 10)
    y,x = vars.number_to_position_map[4]
    vars.board[y][x].piece = piece
    #Queen
    piece = Piece(False, 9)
    y,x = vars.number_to_position_map[3]
    vars.board[y][x].piece = piece
    #Rooks
    piece = Piece(False, 5)
    y,x = vars.number_to_position_map[0]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[7]
    vars.board[y][x].piece = piece
    #Bishops
    piece = Piece(False, 4)
    y,x = vars.number_to_position_map[2]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[5]
    vars.board[y][x].piece = piece
    #Knights
    piece = Piece(False, 3)
    y,x = vars.number_to_position_map[1]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[6]
    vars.board[y][x].piece = piece
    #Pawns
    piece = Piece(False, 1)
    for i in range(8):
        y,x = vars.number_to_position_map[8+i]
        vars.board[y][x].piece = piece
    #WHITE PIECES
    #King
    piece = Piece(True, 10)
    y,x = vars.number_to_position_map[60]
    vars.board[y][x].piece = piece
    #Queen
    piece = Piece(True, 9)
    y,x = vars.number_to_position_map[59]
    vars.board[y][x].piece = piece
    #Rook
    piece = Piece(True, 5)
    y,x = vars.number_to_position_map[63]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[56]
    vars.board[y][x].piece = piece
    #Knight
    piece = Piece(True, 3)
    y,x = vars.number_to_position_map[62]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[57]
    vars.board[y][x].piece = piece
    #Bishop
    piece = Piece(True, 4)
    y,x = vars.number_to_position_map[61]
    vars.board[y][x].piece = piece
    y,x = vars.number_to_position_map[58]
    vars.board[y][x].piece = piece
    #Pawn
    piece = Piece(True, 1)
    for i in range(8):
        y,x = vars.number_to_position_map[48 + i]
        vars.board[y][x].piece = piece
def render_pieces(board, window):
    for rank in board:
        for square in rank:
            if square.piece != None:
                piece = square.piece
                x = square.x_start +square.width_height/2 - piece.img.get_width()/2
                y = square.y_start +square.width_height/2 - piece.img.get_height()/2
                window.blit(piece.img, (x,y))

def select_square(x,y, board, width, window):
    x_index = int(x // width)
    y_index = int(y // width)
    selected_square = board[y_index][x_index]
    distances = calculate_edge_distance(selected_square.number)
    #Selecting a piece
    if selected_square.piece != None and vars.selected_piece == None and selected_square.piece.is_white == vars.white_moves:
        vars.selected_piece = board[y_index][x_index].piece
        board[y_index][x_index].piece = None
        vars.possible_moves = calculate_piece_moves(selected_square.number, distances)
        vars.current_move = Move(selected_square.number)
    #Dropping a piece
    elif vars.selected_piece != None:
        for move in vars.possible_moves:
            if selected_square.number == move.target_square_num:
                board[y_index][x_index].piece = vars.selected_piece
                vars.selected_piece = None
                vars.possible_moves = []
                if move.start_square_num != move.target_square_num:
                    vars.white_moves = not vars.white_moves

                return


def render_selected_piece(x_start, y_start , window):
    x = x_start - vars.selected_piece.img.get_width()/2
    y = y_start - vars.selected_piece.img.get_height()/2
    window.blit(vars.selected_piece.img, (x,y))



def redraw_window(window, board):
    window.blit(vars.BG, (0,0))
    render_pieces(board, window)

def calculate_edge_distance(number):
    left = number % 8
    right = 8 - left - 1
    up = number // 8
    down = 8 - up - 1
    return {
        "left": left,
        "right": right,
        "up": up,
        "down": down,
    }

def calculate_piece_moves(number, distances):
    if vars.selected_piece.value == 5:
        moves = calculate_rook_moves(number, distances)
    elif vars.selected_piece.value == 4:
        moves = calculate_bishop_moves(number, distances)
    elif vars.selected_piece.value == 3:
        moves = calculate_knight_moves(number, distances)
    elif vars.selected_piece.value == 9:
        moves = calculate_bishop_moves(number, distances) + calculate_rook_moves(number, distances)
    elif vars.selected_piece.value == 10:
        king_distances = {}
        for direction in ["up", "down", "left", "right"]:
            if distances[direction] != 0:
                king_distances[direction] = 1
            else:
                king_distances[direction] = 0
        moves = calculate_bishop_moves(number, king_distances) + calculate_rook_moves(number, king_distances)
    elif vars.selected_piece.value == 1:
        moves = calculate_pawn_moves(number, distances)
    return moves

def calculate_rook_moves(number, distances):
    moves = []
    for i in range(1,distances["left"]+1):
        move = Move(number, number -1*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["right"]+1):
        move = Move(number, number +1*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["up"]+1):
        move = Move(number, number -8*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["down"]+1):
        move = Move(number, number +8*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    move = Move(number, number)
    moves.append(move)
    return moves

def calculate_bishop_moves(number, distances):
    moves = []
    #Up left
    for i in range(1,min(distances["left"],distances["up"])+1):
        move = Move(number, number -9*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Up right
    for i in range(1,min(distances["right"], distances["up"])+1):
        move = Move(number, number -7*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Down left
    for i in range(1,min(distances["left"],distances["down"])+1):
        move = Move(number, number +7*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Down right
    for i in range(1,min(distances["down"], distances["right"])+1):
        move = Move(number, number +9*i)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    move = Move(number, number)
    moves.append(move)
    return moves
def calculate_knight_moves(number, distances):
    #TODO CONSIDERAR DISTANCIAS
    moves = []
    # U U L
    if not(distances["up"] < 2 or distances["left"] < 1):
        move = Move(number, number -17)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # U L L
    if not(distances["up"]<1 or distances["left"] < 2):
        move = Move(number, number -10)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # U U R
    if not(distances["up"]<2 or distances["right"] < 1):
        move = Move(number, number -15)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # U R R
    if not(distances["up"]<1 or distances["right"] < 2):
        move = Move(number, number -6)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # D D L
    if not(distances["down"]<2 or distances["left"] < 1):
        move = Move(number, number +15)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # D L L
    if not(distances["down"]<1 or distances["left"] < 2): 
        move = Move(number, number +6)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # D D R
    if not(distances["down"]<2 or distances["right"] < 1):
        move = Move(number, number +17)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)
    # D R R
    if not(distances["down"]<1 or distances["right"] < 2):
        move = Move(number, number +10)
        possible , keep_going = check_target_piece(move)
        if possible:
            moves.append(move)

    move = Move(number, number)
    moves.append(move)

    return moves

def calculate_pawn_moves(number,distances):
    #TODO: DOUBLE STEP AT FIRST AND EN PASSANT 
    #TODO: PROMOTION
    moves = []
    if vars.selected_piece.is_white:
        move = Move(number, number -8)
        possible , keep_going = check_target_piece(move)
        if keep_going:
            moves.append(move)
        y,x = vars.number_to_position_map[number]
        if y == 6:
            move = Move(number, number -16)
            possible , keep_going = check_target_piece(move)
            if keep_going:
                moves.append(move)
        #Taking
        move = Move(number, number-9)
        possible , keep_going = check_target_piece(move)
        if possible and not keep_going:
            moves.append(move)
        move = Move(number, number-7)
        possible , keep_going = check_target_piece(move)
        if possible and not keep_going:
            moves.append(move)
    else:
        move = Move(number, number +8)
        possible , keep_going = check_target_piece(move)
        if keep_going:
            moves.append(move)
        y,x = vars.number_to_position_map[number]
        if y == 1:
            move = Move(number, number +16)
            possible , keep_going = check_target_piece(move)
            if keep_going:
                moves.append(move)
        #Taking
        move = Move(number, number+9)
        possible , keep_going = check_target_piece(move)
        if possible and not keep_going:
            moves.append(move)
        move = Move(number, number+7)
        possible , keep_going = check_target_piece(move)
        if possible and not keep_going:
            moves.append(move)
        
    move = Move(number, number)
    moves.append(move)
    return moves

def highlight_possible_squares(board, window):
    for move in vars.possible_moves:
        target_square_num = move.target_square_num
        for rank in board:
            for square in rank:
                if square.number == target_square_num:
                    rect = pygame.Surface((vars.WIDTH,vars.WIDTH))
                    rect.fill((255,0,0))
                    window.blit(rect, (square.x_start, square.y_start))
    
def check_target_piece(move):
    if move.target_square_num < 0 or move.target_square_num > 63:
        return False, False 
    y , x = vars.number_to_position_map[move.target_square_num]
    target_square = vars.board[y][x]
    keep_going = True
    possible = True
    if target_square.piece != None:
        keep_going = False
        if target_square.piece.is_white == vars.selected_piece.is_white:
            possible = False
    return possible, keep_going

