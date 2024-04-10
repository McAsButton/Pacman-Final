# Pacman en Pygame
#
# Descripción: Recreación del juego Pacman realizado en Pygame, se inicia desde el archivo pacman.py
#
#
## Autores   : Miguel Angel Santa Abreu
##             Wisberg Danilo Gallego Chaverra
##             Jonatan Mariano Muñoz Muñoz
##
## $Fecha    : 30-Oct-2020 17:20:03 $
## DEVELOPED : Visual Studio Code 1.51.1
##             Python 3.8.6 64-bit
##             PyGame 1.9.6
##
## Version   : 1.0

import sys
import Game #Carga todas las definiciones de la clase Game
from Game import Game

if __name__ == '__main__':
    g = Game() #Se define la clase Game como g
    g.show_start_screen() #Se llama la función show_start_screen de la clase Game
    g.show_go_screen() #Se llama la función show_go_screen de la clase Game
    sys.exit() #Salir de Python
