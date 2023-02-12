import pygame

from entities.board_square import *
import config

from pygame.locals import (
    MOUSEBUTTONUP,   
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()


screen = pygame.display.set_mode((config.screen_width, config.screen_width))

#Making the board
board = []
width = config.screen_width / 8
is_white = False

y_start = 0
for y in range(8):
    x_start = 0
    rank = []
    is_white = not is_white
    for x in range(8):
        bs = BoardSquare(x_start, y_start, width, is_white)
        rank.append(bs)
        is_white = not is_white
        x_start += width
    board.append(rank)
    y_start += width

print(len(board))
print(len(board[7]))
#Rendering the board
for rank in board:
    for square in rank:
        surf = pygame.Surface((square.width_height, square.width_height))

        if square.is_white:
            surf.fill((236,235,214))
        else:
            
            surf.fill((123,147, 92))
        rect = surf.get_rect()
        screen.blit(surf, (square.x_start, square.y_start))
        pygame.display.flip()


#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())