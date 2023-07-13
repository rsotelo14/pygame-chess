import os
import pygame

from entities.board_square import *

from functions.functions import *
from vars import *
import vars

pygame.init()

#TODO: MAKE FINAL MESSAGE AND RETURN TO MAIN MENU

make_board()
initial_position()

#Main vars
running = True


while running:
    option = main_menu()

    if option == 1:
        pvp()
    elif option == 2:
        #pvpc()
        pvp()

