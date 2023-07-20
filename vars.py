import os
import pygame
from entities.piece import Piece

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

FPS = 60
clock = pygame.time.Clock()

ESCAPE = 0
PVP = 1
PVCPU = 2
DRAW_STALEMATE = 3
DRAW_50_MOVE = 4
DRAW_REPETITION = 5
WHITE_WINS = 6
BLACK_WINS = 7 
CHECKMATE = 8

#State vars
playing = False
selected_piece = None
selected_square = None
piece_possible_moves = []
all_possible_moves_to_play = []
all_possible_moves_just_played = []
current_move = None
board = []
white_moves = True
last_move = None
moves_played = []
check = False
halfmove_counter = 0
fullmove_counter = 0
positions_strings = []
result = None
#Castling

white_king_moved = False 
white_left_rook_moved = False 
white_right_rook_moved = False 
black_king_moved = False 
black_left_rook_moved = False 
black_right_rook_moved = False 

fen_to_piece_map = {
    "P": Piece(True, 1),
    "N": Piece(True, 3),
    "B": Piece(True, 4),
    "R": Piece(True, 5),
    "Q": Piece(True, 9),
    "K": Piece(True, 10),
    "p": Piece(False, 1),
    "n": Piece(False, 3),
    "b": Piece(False, 4),
    "r": Piece(False, 5),
    "q": Piece(False, 9),
    "k": Piece(False, 10),
}

fen_for_initial_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

letter_to_number_map = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e" : 4,
    "f" : 5,
    "g" : 6,
    "h" : 7,
}