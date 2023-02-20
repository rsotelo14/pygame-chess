import os
import pygame

from entities.piece import Piece
import vars


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
    if board[y_index][x_index].piece != None and vars.selected_piece == None:
        vars.selected_piece = board[y_index][x_index].piece
        print(vars.selected_piece)
        board[y_index][x_index].piece = None
    elif vars.selected_piece != None:
        board[y_index][x_index].piece = vars.selected_piece
        vars.selected_piece = None
    

def render_selected_piece(x_start, y_start , window):
    x = x_start - vars.selected_piece.img.get_width()/2
    y = y_start - vars.selected_piece.img.get_height()/2
    window.blit(vars.selected_piece.img, (x,y))



def redraw_window(window, board):
    window.blit(vars.BG, (0,0))
    render_pieces(board, window)

