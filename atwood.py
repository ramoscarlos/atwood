#/usr/bin/env python
# -*- coding: utf-8 -*-

"Script para ejecutar el juego."

from pyjuego.g_escenas import Director
from escenas import EscenaInicio, EscenaTeclado

def main():
    "Ejecutar el juego."
    director = Director("Atwood: Tutorial de PGU", (512, 512))
    director.ejecutar(EscenaInicio())

if __name__ == "__main__":
    main()
