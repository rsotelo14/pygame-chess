import os
import pygame

from entities.board_square import *

from functions.functions import *
from vars import *

pygame.init()


#Making the board
#TODO: PUT NUMBER ON SQUARE
board = []
is_white = False

y_start = 0
for y in range(8):
    x_start = 0
    rank = []
    is_white = not is_white
    for x in range(8):
        bs = BoardSquare(x_start, y_start, WIDTH, is_white)
        rank.append(bs)
        is_white = not is_white
        x_start += WIDTH
    board.append(rank)
    y_start += WIDTH


#Main vars
running = True
FPS = 60
clock = pygame.time.Clock()
#Making pieces
piece = Piece(True)
piece.img = WHITE_KING
board[0][1].piece = piece

piece2 = Piece(False)
piece2.img = BLACK_BISHOP 
board[0][2].piece = piece2
#Main loop
while running:
    clock.tick(FPS)
  #  render_pieces(board, WIN)
    redraw_window(WIN, board)

    if not(vars.selected_piece is None): 
        x,y = pygame.mouse.get_pos()
        render_selected_piece(x,y, WIN)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            select_square(x,y, board, WIDTH, WIN)
            
    pygame.display.update()
