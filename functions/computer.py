import pygame
import vars
import random
import functions.functions as f

def computer_make_move():
    move = random.choice(vars.all_possible_moves_to_play)
    target_square_piece = f.make_move(move, True)
    vars.selected_piece = None
    vars.selected_square = None
    vars.piece_possible_moves = []
    vars.all_possible_moves_to_play = f.remove_ilegal_moves(f.calculate_all_moves_to_play())
    vars.all_possible_moves_just_played = f.remove_ilegal_moves(f.calculate_all_moves_just_played())
    f.look_for_checks()
    f.check_for_checkmate_or_stalemate()
    f.check_for_50_move_rule(target_square_piece)
    fen_string = f.generate_fen_string_for_position()
    f.check_for_threefold_repetition(fen_string)
                        