import os
import pygame

from entities.board_square import *

from functions.functions import *
from functions.menus import *
from vars import *
import vars

pygame.init()


make_board()
initial_position()

#Main vars
running = True


while running:
    option = main_menu()

    if option == vars.PVP:
        result =pvp()
    elif option == vars.PVCPU:
        result = pvpc()
        
    elif option == vars.ESCAPE:
        break
    if result != vars.ESCAPE:
        result_menu(result)

