import os
import pygame


SCREEN_WIDTH = 800
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


BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "board_new.jpg")), (SCREEN_WIDTH, SCREEN_WIDTH))
HIGHLIGHT_DOT = pygame.transform.scale(pygame.image.load(os.path.join("assets", "highlight_dot.png")), (SCREEN_WIDTH/8, SCREEN_WIDTH/8))
HIGHLIGHT_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "highlight_square.png")), (SCREEN_WIDTH/8, SCREEN_WIDTH/8))
HIGHLIGHT_CHECKED_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "highlight_checked_square.png")), (SCREEN_WIDTH/8, SCREEN_WIDTH/8))
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
white_king_moved = False 
white_left_rook_moved = False 
white_right_rook_moved = False 
black_king_moved = False 
black_left_rook_moved = False 
black_right_rook_moved = False 
last_move = None
check = False