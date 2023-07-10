import os
import pygame


SCREEN_WIDTH = 700
#Loading images
BLACK_QUEEN = pygame.image.load(os.path.join("assets", "black_queen.png"))
BLACK_BISHOP = pygame.image.load(os.path.join("assets", "black_bishop.png"))
BLACK_KING = pygame.image.load(os.path.join("assets", "black_king.png"))
BLACK_PAWN = pygame.image.load(os.path.join("assets", "black_pawn.png"))
BLACK_ROOK = pygame.image.load(os.path.join("assets", "black_rook.png"))
BLACK_KNIGHT = pygame.image.load(os.path.join("assets", "black_knight.png"))
WHITE_QUEEN = pygame.image.load(os.path.join("assets", "white_queen.png"))
WHITE_BISHOP = pygame.image.load(os.path.join("assets", "white_bishop.png"))
WHITE_KING = pygame.image.load(os.path.join("assets", "white_king.png"))
WHITE_PAWN = pygame.image.load(os.path.join("assets", "white_pawn.png"))
WHITE_ROOK = pygame.image.load(os.path.join("assets", "white_rook.png"))
WHITE_KNIGHT = pygame.image.load(os.path.join("assets", "white_knight.png"))


BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "board.png")), (SCREEN_WIDTH, SCREEN_WIDTH))
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
WIDTH =  SCREEN_WIDTH/8

number_to_position_map = {}
for i in range(64):
    number_to_position_map[i] = (i//8, i % 8) #(y, x) for list indexing

#State vars
selected_piece = None
piece_possible_moves = []
current_move = None
board = []
white_moves = False