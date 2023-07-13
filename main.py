import os
import pygame

from entities.board_square import *

from functions.functions import *
from vars import *
import vars

pygame.init()


make_board()
initial_position()

#Main vars
running = True
FPS = 60
clock = pygame.time.Clock()
#Main loop
while vars.running:
    clock.tick(FPS)
    WIN.blit(vars.BG, (0,0))
    if not(vars.last_move is None): 
        highlight_last_move(WIN)
    if vars.check:
        highlight_checked_square(WIN)
    render_pieces(board, WIN)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               vars.running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            select_square(x,y, vars.board, WIDTH)
    if vars.piece_possible_moves != []:
        highlight_possible_squares(vars.board, WIN)
    if not(vars.selected_piece is None): 
        x,y = pygame.mouse.get_pos()
        render_selected_piece(x,y, WIN)
            
    pygame.display.update()
