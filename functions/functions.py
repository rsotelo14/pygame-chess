import os
import pygame
import copy

from entities.board_square import BoardSquare
from entities.move import Move
from entities.piece import Piece
from entities.castle import Castle
from entities.en_passant import EnPassant
from functions.render import *

import vars

def init_variables():
    vars.selected_piece = None
    vars.piece_possible_moves = []
    vars.all_possible_moves_to_play = []
    vars.all_possible_moves_just_played = []
    vars.current_move = None
    vars.white_moves = True
    vars.last_move = None
    vars.check = False
    vars.halfmove_counter = 0
    vars.fullmove_counter = 0
    vars.positions_strings = []
    vars.result = None
    #Castling
    vars.white_king_moved = False 
    vars.white_left_rook_moved = False 
    vars.white_right_rook_moved = False 
    vars.black_king_moved = False 
    vars.black_left_rook_moved = False 
    vars.black_right_rook_moved = False 



def make_board():
    vars.board = []
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
    make_board()
    init_variables()

    setup_fen_string(vars.fen_for_initial_position)
 #   #BLACK PIECES
 #   #King
 #   piece = Piece(False, 10)
 #   vars.black_king_piece = piece
 #   y,x = vars.number_to_position_map[4]
 #   vars.board[y][x].piece = piece
 #   #Queen
 #   piece = Piece(False, 9)
 #   y,x = vars.number_to_position_map[3]
 #   vars.board[y][x].piece = piece
 #   #Rooks
 #   piece = Piece(False, 5)
 #   y,x = vars.number_to_position_map[0]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[7]
 #   vars.board[y][x].piece = piece
 #   #Bishops
 #   piece = Piece(False, 4)
 #   y,x = vars.number_to_position_map[2]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[5]
 #   vars.board[y][x].piece = piece
 #   #Knights
 #   piece = Piece(False, 3)
 #   y,x = vars.number_to_position_map[1]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[6]
 #   vars.board[y][x].piece = piece
 #   #Pawns
 #   piece = Piece(False, 1)
 #   for i in range(8):
 #       y,x = vars.number_to_position_map[8+i]
 #       vars.board[y][x].piece = piece
 #   #WHITE PIECES
 #   #King
 #   piece = Piece(True, 10)
 #   vars.white_king_piece = piece
 #   y,x = vars.number_to_position_map[60]
 #   vars.board[y][x].piece = piece
 #   #Queen
 #   piece = Piece(True, 9)
 #   y,x = vars.number_to_position_map[59]
 #   vars.board[y][x].piece = piece
 #   #Rook
 #   piece = Piece(True, 5)
 #   y,x = vars.number_to_position_map[63]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[56]
 #   vars.board[y][x].piece = piece
 #   #Knight
 #   piece = Piece(True, 3)
 #   y,x = vars.number_to_position_map[62]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[57]
 #   vars.board[y][x].piece = piece
 #   #Bishop
 #   piece = Piece(True, 4)
 #   y,x = vars.number_to_position_map[61]
 #   vars.board[y][x].piece = piece
 #   y,x = vars.number_to_position_map[58]
 #   vars.board[y][x].piece = piece
 #   #Pawn
 #   piece = Piece(True, 1)
 #   for i in range(8):
 #       y,x = vars.number_to_position_map[48 + i]
 #       vars.board[y][x].piece = piece
 #   vars.all_possible_moves_to_play = calculate_all_moves_to_play()



def select_square(x,y, board, width):
    x_index = int(x // width)
    y_index = int(y // width)
    selected_square = board[y_index][x_index]
    distances = calculate_edge_distance(selected_square.number)
    #Selecting a piece
    if selected_square.piece != None and vars.selected_piece == None and selected_square.piece.is_white == vars.white_moves:
        vars.selected_piece = board[y_index][x_index].piece
        vars.piece_possible_moves = remove_ilegal_moves(calculate_piece_moves(selected_square.number, distances, vars.selected_piece))
        board[y_index][x_index].piece = None
    #Dropping a piece
    elif vars.selected_piece != None:
        for move in vars.piece_possible_moves:
            if selected_square.number == move.target_square_num:
                check_move_for_castling_change(move)
                target_square_piece = make_move(move)
                vars.selected_piece = None
                check_move_for_promotion(move)
                vars.piece_possible_moves = []
                if move.start_square_num != move.target_square_num:

                    move_made(move)
                    look_for_checks()
                    check_for_checkmate_or_stalemate()
                    check_for_50_move_rule(target_square_piece)
                    fen_string = generate_fen_string_for_position()
                    check_for_threefold_repetition(fen_string)
                    
                return

def check_for_threefold_repetition(fen_string):
    split = fen_string.split(" ")
    counter = 0
    string_to_check = remove_characters_until_two_spaces(fen_string)
    for string in vars.positions_strings:
        if string == string_to_check:
            counter += 1
    if counter >= 3:
        vars.playing = False
        vars.result = vars.DRAW_REPETITION
    

def check_for_50_move_rule(target_square_piece):
    if vars.last_move.piece.value == 1 or target_square_piece != None:
        vars.halfmove_counter = 0
    else:
        vars.halfmove_counter += 1
        if vars.halfmove_counter ==100:
            vars.playing = False
            vars.result = vars.DRAW_50_MOVE


def check_move_for_promotion(move):
    if move.piece.value != 1:
        return
    y,x = vars.number_to_position_map[move.target_square_num] 
    if (move.piece.is_white and y == 0) or (not move.piece.is_white and y == 7):
        vars.board[y][x].piece = Piece(move.piece.is_white, 9)

def check_for_checkmate_or_stalemate():
    for move in vars.all_possible_moves_to_play:
        if move.piece.is_white != vars.white_moves:
            continue
        if move.start_square_num != move.target_square_num:
            return
    vars.playing = False
    vars.result = vars.CHECKMATE

def look_for_checks():
    checked = False
    for move in vars.all_possible_moves_just_played:
        y,x = vars.number_to_position_map[move.target_square_num]
        try:
            if vars.board[y][x].piece.value == 10 and vars.board[y][x].piece.is_white == (not move.piece.is_white):
                checked = True
                break
        except:
            pass
    vars.check = checked

def castle(move):
    if move.piece.is_white:
        if move.is_short_castle:
            rook = vars.board[7][7].piece
            vars.board[7][7].piece = None
            vars.board[7][5].piece = rook
        else:
            rook = vars.board[7][0].piece
            vars.board[7][0].piece = None
            vars.board[7][3].piece = rook
    else:
        if move.is_short_castle:
            rook = vars.board[0][7].piece
            vars.board[0][7].piece = None
            vars.board[0][5].piece = rook
        else:
            rook = vars.board[0][0].piece
            vars.board[0][0].piece = None
            vars.board[0][3].piece = rook

def en_passant(move):
    if move.piece.is_white:
        y, x = vars.number_to_position_map[move.target_square_num +8]
        vars.board[y][x].piece = None
    else:
        y, x = vars.number_to_position_map[move.target_square_num -8]
        vars.board[y][x].piece = None

def check_move_for_castling_change(move):
    piece = move.piece
    if move.start_square_num == move.target_square_num:
        return
    if piece == Piece(False,10):
        vars.black_king_moved = True
    if piece == Piece(True,10):
        vars.white_king_moved = True
    if piece.value == 5:
        if piece.is_white:
            if move.start_square_num == 56:
                vars.white_left_rook_moved = True
            if move.start_square_num == 63:
                vars.white_right_rook_moved = True
        else:
            if move.start_square_num == 0:
                vars.black_left_rook_moved = True
            if move.start_square_num == 7:
                vars.black_right_rook_moved = True
    y , x = vars.number_to_position_map[move.target_square_num]
    target_piece = vars.board[y][x].piece
    if target_piece != None and target_piece.value == 5:
        if target_piece.is_white and move.target_square_num == 63:
            vars.white_right_rook_moved = True
        if target_piece.is_white and move.target_square_num == 56:
            vars.white_left_rook_moved = True
        if not target_piece.is_white and move.target_square_num == 7:
            vars.black_right_rook_moved = True
        if not target_piece.is_white and move.target_square_num == 0:
            vars.black_left_rook_moved = True
  
def remove_ilegal_moves(moves):
    temp_board = vars.board
    remove_moves=  []
    #For each of the possible moves
    for move in moves:
       #If its to the same square it doesnt matter
       if move.start_square_num == move.target_square_num:
           continue
       #Get the squares
       
       y_start, x_start = vars.number_to_position_map[move.start_square_num]
       y_target, x_target = vars.number_to_position_map[move.target_square_num]
       #Save the piece in target square
       target_square_piece = make_move(move)
       vars.white_moves = not vars.white_moves
       #Calculate moves
       all_moves = calculate_all_moves_to_play()
       for new_move in all_moves:
           #If it's one of my pieces I dont care, and If it's in the same square I don't care
           if new_move.piece.is_white != move.piece.is_white and new_move.start_square_num != new_move.target_square_num:
                #Get target square
                y, x = vars.number_to_position_map[new_move.target_square_num]
                if not move.piece.is_white:
                    if vars.board[y][x].piece == Piece(False,10):
                        remove_moves.append(move)
                else:
                    if vars.board[y][x].piece == Piece(True,10):
                        remove_moves.append(move)
       #Unmake move
       unmake_move(move, target_square_piece)
       vars.white_moves = not vars.white_moves
    for move_to_remove in remove_moves:
        try:
            moves.remove(move_to_remove)
        except:
            pass
    return moves

def make_move(move):
     if type(move) == Castle:
        castle(move)
     if type(move) == EnPassant:
        en_passant(move)
     y_start, x_start = vars.number_to_position_map[move.start_square_num]
     y_target, x_target = vars.number_to_position_map[move.target_square_num]
     target_square_piece = vars.board[y_target][x_target].piece
     vars.board[y_start][x_start].piece = None
     vars.board[y_target][x_target].piece = move.piece
     return target_square_piece

def unmake_move(move, target_square_piece):
     if type(move) == Castle:
        un_castle(move)
     if type(move) == EnPassant:
        un_en_passant(move)
     y_start, x_start = vars.number_to_position_map[move.start_square_num]
     y_target, x_target = vars.number_to_position_map[move.target_square_num]  
     vars.board[y_start][x_start].piece = move.piece
     vars.board[y_target][x_target].piece = target_square_piece

def move_made(move):
    vars.white_moves = not vars.white_moves
    vars.last_move = move
    if not move.piece.is_white:
        vars.fullmove_counter += 1
    vars.all_possible_moves_to_play = remove_ilegal_moves(calculate_all_moves_to_play())
    vars.all_possible_moves_just_played = remove_ilegal_moves(calculate_all_moves_just_played())

def un_castle(move):
    if move.piece.is_white:
        if move.is_short_castle:
            rook = vars.board[7][5].piece
            vars.board[7][7].piece = rook
            vars.board[7][5].piece = None
        else:
            rook = vars.board[7][3].piece
            vars.board[7][0].piece = rook
            vars.board[7][3].piece = None
    else:
        if move.is_short_castle:
            rook = vars.board[0][5].piece
            vars.board[0][7].piece = rook
            vars.board[0][5].piece = None
        else:
            rook = vars.board[0][3].piece
            vars.board[0][0].piece = rook
            vars.board[0][3].piece = None
def un_en_passant(move):
    print("UNDO EN PASSANT;")
    if move.piece.is_white:
        y_target, x_target = vars.number_to_position_map[move.target_square_num +8]
        vars.board[y_target][x_target].piece = Piece(False, 1)
    else:
        y_target, x_target = vars.number_to_position_map[move.target_square_num -8]
        vars.board[y_target][x_target].piece = Piece(True, 1)

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
def calculate_all_moves_to_play():
    moves = []
    for rank in vars.board:
        for square in rank:
            if square.piece != None and square.piece.is_white == vars.white_moves:
                distances = calculate_edge_distance(square.number)
                moves = moves + calculate_piece_moves(square.number, distances, square.piece)
    return moves
def calculate_all_moves_just_played():
    moves = []
    for rank in vars.board:
        for square in rank:
            if square.piece != None and square.piece.is_white == (not vars.white_moves):
                distances = calculate_edge_distance(square.number)
                moves = moves + calculate_piece_moves(square.number, distances, square.piece)
    return moves
def calculate_piece_moves(number, distances, piece):


    if piece.value == 5:
        moves = calculate_rook_moves(number, distances, piece)
    elif piece.value == 4:
        moves = calculate_bishop_moves(number, distances, piece)
    elif piece.value == 3:
        moves = calculate_knight_moves(number, distances, piece)
    elif piece.value == 9:
        moves = calculate_bishop_moves(number, distances, piece) + calculate_rook_moves(number, distances, piece)
    elif piece.value == 10:
        king_distances = {}
        for direction in ["up", "down", "left", "right"]:
            if distances[direction] != 0:
                king_distances[direction] = 1
            else:
                king_distances[direction] = 0
        moves = calculate_bishop_moves(number, king_distances, piece) + calculate_rook_moves(number, king_distances, piece) + check_castling(number, piece)
    elif piece.value == 1:
        moves = calculate_pawn_moves(number, distances, piece)
    return moves

def check_castling(number, piece):
    moves = []
    if vars.check:
        return moves
    if piece.is_white:
        if vars.white_king_moved:
            return moves
        if not vars.white_left_rook_moved:
            can_long_castle = True
            for i in [1,2,3]:
                try:
                    y, x = vars.number_to_position_map[number -i]
                    if vars.board[y][x].piece != None:
                        can_long_castle = False
                    if i != 3:
                        for move in vars.all_possible_moves_to_play:
                            if move.piece != None and move.piece.is_white == (not piece.is_white) and move.target_square_num == number -i:
                                can_long_castle = False
                except: 
                    pass
            if can_long_castle:
                moves.append(Castle(number, number -2, piece, False))
        if not vars.white_right_rook_moved:
            can_short_castle = True
            for i in [1,2]:
                try:
                    y, x = vars.number_to_position_map[number +i]
                    if vars.board[y][x].piece != None:
                        can_short_castle = False
                    for move in vars.all_possible_moves_to_play:
                        if move.piece != None and move.piece.is_white == (not piece.is_white) and move.target_square_num == number +i:
                            can_short_castle = False
                except:
                    pass
            if can_short_castle:
                moves.append(Castle(number, number +2, piece, True))
    if not piece.is_white:
        if vars.black_king_moved:
            return moves
        if not vars.black_left_rook_moved:
            can_long_castle = True
            for i in [1,2,3]:
                try:
                    y, x = vars.number_to_position_map[number -i]
                    if vars.board[y][x].piece != None:
                        can_long_castle = False
                    if i != 3:
                        for move in vars.all_possible_moves_to_play:
                            if move.piece != None and move.piece.is_white == (not piece.is_white) and move.target_square_num == number -i:
                                can_long_castle = False
                except:
                    pass
            if can_long_castle:
                moves.append(Castle(number, number -2, piece, False))
        if not vars.black_right_rook_moved:
            can_short_castle = True
            for i in [1,2]:
                y, x = vars.number_to_position_map[number +i]
                if vars.board[y][x].piece != None:
                    can_short_castle = False
                for move in vars.all_possible_moves_to_play:
                        if move.piece != None and move.piece.is_white == (not piece.is_white) and move.target_square_num == number +i:
                            can_short_castle = False
            if can_short_castle:
                moves.append(Castle(number, number +2, piece, True))
    return moves


def calculate_rook_moves(number, distances, piece):
    moves = []
    for i in range(1,distances["left"]+1):
        move = Move(number, number -1*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["right"]+1):
        move = Move(number, number +1*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["up"]+1):
        move = Move(number, number -8*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break
    for i in range(1,distances["down"]+1):
        move = Move(number, number +8*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    move = Move(number, number, piece)
    moves.append(move)
    return moves

def calculate_bishop_moves(number, distances, piece):
    moves = []
    #Up left
    for i in range(1,min(distances["left"],distances["up"])+1):
        move = Move(number, number -9*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Up right
    for i in range(1,min(distances["right"], distances["up"])+1):
        move = Move(number, number -7*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Down left
    for i in range(1,min(distances["left"],distances["down"])+1):
        move = Move(number, number +7*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    #Down right
    for i in range(1,min(distances["down"], distances["right"])+1):
        move = Move(number, number +9*i, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
        if not keep_going:
            break

    move = Move(number, number, piece)
    moves.append(move)
    return moves
def calculate_knight_moves(number, distances, piece):
    moves = []
    # U U L
    if not(distances["up"] < 2 or distances["left"] < 1):
        move = Move(number, number -17, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # U L L
    if not(distances["up"]<1 or distances["left"] < 2):
        move = Move(number, number -10, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # U U R
    if not(distances["up"]<2 or distances["right"] < 1):
        move = Move(number, number -15, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # U R R
    if not(distances["up"]<1 or distances["right"] < 2):
        move = Move(number, number -6, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # D D L
    if not(distances["down"]<2 or distances["left"] < 1):
        move = Move(number, number +15, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # D L L
    if not(distances["down"]<1 or distances["left"] < 2): 
        move = Move(number, number +6, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # D D R
    if not(distances["down"]<2 or distances["right"] < 1):
        move = Move(number, number +17, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)
    # D R R
    if not(distances["down"]<1 or distances["right"] < 2):
        move = Move(number, number +10, piece)
        possible , keep_going = check_target_piece(move, piece)
        if possible:
            moves.append(move)

    move = Move(number, number, piece)
    moves.append(move)

    return moves

def calculate_pawn_moves(number,distances, piece):
    moves = []
    if piece.is_white:
        move = Move(number, number -8, piece)
        possible , keep_going = check_target_piece(move, piece)
        if keep_going:
            moves.append(move)
        y,x = vars.number_to_position_map[number]
        if y == 6:
            if possible:
                move = Move(number, number -16, piece)
                possible , keep_going = check_target_piece(move, piece)
                if keep_going:
                    moves.append(move)
        #Taking
        if x != 0:
            move = Move(number, number-9, piece)
            possible , keep_going = check_target_piece(move, piece)
            if possible and not keep_going:
                moves.append(move)
        if x != 7:        
            move = Move(number, number-7, piece)
            possible , keep_going = check_target_piece(move, piece)
            if possible and not keep_going:
                moves.append(move)
        #En passant
        last_move= vars.last_move
        if last_move != None:
            if y == 3 and not last_move.piece.is_white and last_move.piece.value == 1 and last_move.start_square_num == last_move.target_square_num -16:
                y_last_move, x_last_move = vars.number_to_position_map[vars.last_move.target_square_num]
                if x_last_move == x +1 or x_last_move == x -1:
                    moves.append(EnPassant(number, last_move.target_square_num - 8, piece ))

            
    else:
        move = Move(number, number +8, piece)
        possible , keep_going = check_target_piece(move, piece)
        if keep_going:
            moves.append(move)
        y,x = vars.number_to_position_map[number]
        if y == 1:
            if possible:
                move = Move(number, number +16, piece)
                possible , keep_going = check_target_piece(move, piece)
                if keep_going:
                    moves.append(move)
        #Taking
        if x != 7:
            move = Move(number, number+9, piece)
            possible , keep_going = check_target_piece(move, piece)
            if possible and not keep_going:
                moves.append(move)
        if x != 0:
            move = Move(number, number+7, piece)
            possible , keep_going = check_target_piece(move, piece)
            if possible and not keep_going:
                moves.append(move)
        #En passant
        last_move= vars.last_move
        if y == 4 and last_move.piece.is_white and last_move.piece.value == 1 and last_move.start_square_num == last_move.target_square_num +16:
            y_last_move, x_last_move = vars.number_to_position_map[vars.last_move.target_square_num]
            if x_last_move == x +1 or x_last_move == x -1:
                moves.append(EnPassant(number, last_move.target_square_num + 8, piece ))
        
    move = Move(number, number, piece)
    moves.append(move)
    return moves


def check_target_piece(move, piece):
    if move.target_square_num < 0 or move.target_square_num > 63:
        return False, False 
    y , x = vars.number_to_position_map[move.target_square_num]
    target_square = vars.board[y][x]
    keep_going = True
    possible = True
    if target_square.piece != None:
        keep_going = False
        if target_square.piece.is_white == piece.is_white:
            possible = False
    return possible, keep_going

def setup_fen_string(fen_string):
    pieces = fen_string.split(" ")
    
    #Parse piece positions
    ranks = pieces[0].split("/")
    y = 0
    for rank in ranks:
        x = 0
        for char in rank:
            if char.isnumeric():
                x += int(char)
            else:
                vars.board[y][x].piece = vars.fen_to_piece_map[char]
                x+= 1
        y += 1
    
    #Parse active color
    vars.white_moves = True if pieces[1] == "w" else False

    #Parse castling rights
    vars.white_king_moved = False
    vars.black_king_moved = False
    vars.white_right_rook_moved = False if "K" in pieces[2] else True
    vars.white_left_rook_moved = False if "Q" in pieces[2] else True
    vars.black_left_rook_moved = False if "k" in pieces[2] else True
    vars.black_right_rook_moved = False if "q" in pieces[2] else True

    #Parse en passant square
    vars.last_move = None
    en_passant_square = pieces[3]
    if en_passant_square != "-":
        x = vars.letter_to_number_map(en_passant_square[0])
        y = 8 - int(en_passant_square[1])
        square_num = get_keys_from_value(vars.number_to_position_map, (y,x))[0]
        if vars.white_moves:
            vars.last_move = Move(square_num-8, square_num +8, Piece(False,1))
        else:
            vars.last_move = Move(square_num+8, square_num -8, Piece(True,1))

    #Parse halfmove clock
    vars.halfmove_counter = int(pieces[4])
    #Parse fullmove number
    vars.fullmove_counter = int(pieces[5])
    #Look for checks
    vars.all_possible_moves_to_play = remove_ilegal_moves(calculate_all_moves_to_play())
    vars.all_possible_moves_just_played = remove_ilegal_moves(calculate_all_moves_just_played())
    look_for_checks()

def generate_fen_string_for_position():
    fen_string = ""
    #Generate piece placement section
    y = 0
    for rank in vars.board:
        empty_square_count = 0
        for square in rank:
            piece = square.piece
            if piece == None:
                empty_square_count += 1
            else:
                if empty_square_count >0:
                    fen_string += str(empty_square_count)
                    empty_square_count = 0
                fen_string += get_keys_from_value(vars.fen_to_piece_map,piece)[0]
        
        if empty_square_count >0:
            fen_string += str(empty_square_count)
        if y != 7:
            fen_string += "/"
        y +=1

    #Generate active color section
    fen_string += " " + ("w" if vars.white_moves else "b")

    #Generate castling rights section
    castling_string = ""
    if not vars.white_king_moved and not vars.white_right_rook_moved:
        castling_string += "K"        
    if not vars.white_king_moved and not vars.white_left_rook_moved:
        castling_string += "Q"
    if not vars.black_king_moved and not vars.black_right_rook_moved:
        castling_string += "k"
    if not vars.black_king_moved and not vars.black_left_rook_moved:
        castling_string += "q"
    
    fen_string += " " + (castling_string if castling_string != "" else "-")

    #Generate en passant target square section
    if vars.last_move.piece.value == 1 and abs(vars.last_move.start_square_num - vars.last_move.target_square_num) == 16:
        y,x = vars.number_to_position_map[vars.last_move.target_square_num]
        letter = get_keys_from_value(vars.letter_to_number_map, x)[0]
        number = 8 - y + (-1 if vars.last_move.piece.is_white else 1)
        fen_string += " " + letter+ str(number)
    else:
        fen_string += " -" 
    #Generate halfmove clock section
    fen_string += " " + str(vars.halfmove_counter)
    #Generate fullmove number section
    fen_string += " " + str(vars.fullmove_counter)

    vars.positions_strings.append(remove_characters_until_two_spaces(fen_string))
    print(fen_string)
    return fen_string

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

def remove_characters_until_two_spaces(string):
    count = 0
    index = len(string) - 1

    while index >= 0 and count < 2:
        if string[index] == ' ':
            count += 1
        index -= 1

    if count == 2:
        return string[:index + 1]
    else:
        return string
