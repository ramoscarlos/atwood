Atwood / Tutorial de PGU
===


Datos del desarrollo
---

    Autor:          Carlos Alberto Ramos López
    Correo:         UnboundDarkness@gmail.com
    Desarrollado:   Enero 2012 - Abril 2012
    Licencia:       GPL v3 / Archivo LICENSE


Descripción
---
Atwood es un videojuego simple, en desarrollo, que emula el clásico Pac-man. Es desarrollado con Pygame, Phil's Pygame Utilities, y un poco de Pykitten. Para ejecutar el videojuego: `python atwood.py`


Recursos gráficos
---

* [Last Guardian / Philipp Lenssen](http://blogoscoped.com/archive/2006-08-08-n51.html)
* [Varios conjuntos de Reiner's Tilesets / Reiner “Tiles” Prokein](http://www.reinerstilesets.de/)


Archivos y carpetas
---

    raíz
    -> media            #Directorio de recursos que utiliza el juego.
      -> imagenes       #Directorio donde residen las imágenes.
      -> niveles        #Directorio donde se encuentran los archivos *.tga.
      -> puntuaciones   #Directorio donde residen los archivos de las puntuaciones.
      -> sprites        #Directorio para las imágenes de los sprites.
    -- atwood.py        #Archivo para ejecutar el videojuego.
    -- comun.py         #Incluye funciones comunes para los videojuegos.
    -- escenas.py       #Núcleo del juego. Contiene todas las escenas del juego.
    -- g_escenas.py     #Módulo con las clases Director y Escena.
    -- leeme.txt        #Este archivo.
    -- LICENSE          #Archivo de la licencia.
    -- limpiar.sh       #Script que permite borrar los archivos .pyc.
    -- pykitten_fork.py #Módulo que contiene las clases para personajes animados.


Controles
---

    En cualquier pantalla:
        Esc           - Salir del videojuego.
    Menú Principal:
        Flecha Abajo  - Cambiar de opción.
        Flecha Arriba - Cambiar de opción.
        Enter o Intro - Ejecutar la acción correspondiente a la opción seleccionada.
    En el juego:
        Flechas       - Controlan el movimiento del personaje.
    En Juego Terminado:
        Flecha Der.   - Cambiar de opción.
        Flecha Izq.   - Cambiar de opción.
        Enter o Intro - Ejecutar la acción correspondiente a la opción seleccionada.
    En Puntuaciones:
        Enter o Intro - Volver a la pantalla de menú.
