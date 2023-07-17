import pygame
import vars
from functions.render import *
from functions.functions import *

def main_menu():
    title_font = pygame.font.SysFont('trebuchetms', 40,True)
    text_font = pygame.font.SysFont('trebuchetms', 30,True)
    main_menu_text = title_font.render("PYCHESS",True, (0,0,0))
    main_menu_rect = main_menu_text.get_rect(center= (400,300))
    pvp_text = text_font.render("P1 VS P2 (Press A)", True, (0,0,0))
    pvp_rect = pvp_text.get_rect(center=(400,375))
    pvcpu_text = text_font.render("P1 VS PC (Press B)", True, (0,0,0))
    pvcpu_rect = pvcpu_text.get_rect(center=(400,425))

    main_menu = True
    WIN = vars.WIN

    menu_rect = pygame.Rect(250,250,300,300)

    while main_menu:
        vars.clock.tick(vars.FPS)
        WIN.blit(vars.BG, (0,0))
        pygame.draw.rect(WIN, (234, 235, 209),menu_rect)
        pygame.draw.rect(WIN, (0,50,0),menu_rect, 10)
        WIN.blit(main_menu_text, main_menu_rect)
        WIN.blit(pvp_text, pvp_rect)
        WIN.blit(pvcpu_text, pvcpu_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                   return vars.PVP
                if event.key == pygame.K_b:
                   return vars.PVCPU
                if event.key == pygame.K_ESCAPE:
                   return vars.ESCAPE
        pygame.display.update()


def result_menu(result):
    title_font = pygame.font.SysFont('trebuchetms', 40,True)
    text_font = pygame.font.SysFont('trebuchetms', 30,True)
    if result == vars.WHITE_WINS:
        main_menu_text = title_font.render("WHITE WINS",True, (0,0,0))
        subtitle_text = text_font.render("by Checkmate", True, (0,0,0))
    elif result == vars.BLACK_WINS:
        main_menu_text = title_font.render("BLACK WINS",True, (0,0,0))
        subtitle_text = text_font.render("by Checkmate", True, (0,0,0))
    elif result == vars.DRAW_STALEMATE:
        main_menu_text = title_font.render("DRAW",True, (0,0,0))
        subtitle_text = text_font.render("by Stalemate", True, (0,0,0))
    elif result == vars.DRAW_REPETITION:
        main_menu_text = title_font.render("DRAW",True, (0,0,0))
        subtitle_text = text_font.render("by Repetition", True, (0,0,0))
    else:
        main_menu_text = title_font.render("DRAW",True, (0,0,0))
        subtitle_text = text_font.render("by 50-move-rule", True, (0,0,0))


    main_menu_rect = main_menu_text.get_rect(center= (400,300))
    subtitle_rect = subtitle_text.get_rect(center= (400,350))
    message = text_font.render("Press SPACE", True, (0,0,0))
    message_rect = message.get_rect(center=(400,450))

    result_menu = True
    WIN = vars.WIN

    menu_rect = pygame.Rect(250,250,300,300)

    while result_menu:
        vars.clock.tick(vars.FPS)
        WIN.blit(vars.BG, (0,0))
        pygame.draw.rect(WIN, (234, 235, 209),menu_rect)
        pygame.draw.rect(WIN, (0,50,0),menu_rect, 10)
        WIN.blit(main_menu_text, main_menu_rect)
        WIN.blit(subtitle_text,subtitle_rect)
        WIN.blit(message, message_rect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   return 
        pygame.display.update()

def pvp():
    initial_position()
    vars.playing = True
    WIN = vars.WIN
    board = vars.board
    WIDTH = vars.WIDTH
    while vars.playing:
        vars.clock.tick(vars.FPS)
        WIN.blit(vars.BG, (0,0))
        if not(vars.last_move is None): 
            highlight_last_move(WIN)
        if vars.check:
            highlight_checked_square(WIN)
        render_pieces(board, WIN)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    vars.playing = False
                    return vars.ESCAPE
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                select_square(x,y, vars.board, WIDTH)
        if vars.piece_possible_moves != []:
            highlight_possible_squares(vars.board, WIN)
        if not(vars.selected_piece is None): 
            x,y = pygame.mouse.get_pos()
            render_selected_piece(x,y, WIN)
                
        pygame.display.update()
    if not vars.check:
        if vars.result == vars.DRAW_REPETITION:
            return vars.DRAW_REPETITION
        elif vars.result == vars.DRAW_STALEMATE:
            return vars.DRAW_STALEMATE
        else:
            return vars.DRAW_50_MOVE
    if vars.check and not vars.white_moves:
        return vars.WHITE_WINS
    if vars.check and vars.white_moves:
        return vars.BLACK_WINS

