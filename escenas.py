#/usr/bin/env python
# -*- coding: utf-8 -*-

"Tutorial de Pygame/PGU: Creando una variante de Pac-man."

import os
import sys
from random import choice
import pygame as p
from pgu.tilevid import Tilevid, Sprite
from pgu import text
from pgu.high import High
from pyjuego.personajes import CharacterSprite
from pyjuego.g_escenas import Escena
from pyjuego.objetos import Texto, TecladoPantalla
from pyjuego.funciones import cargar_imagen

TW, TH = 32, 32     #Ancho y largo de los tiles.

class EscenaJuego(Escena):
    "Clase que define la escena principal del videojuego."
    def __init__(self):
        "Inicialización de las variables del videojuego."
        Escena.__init__(self)
        self.motor = Tilevid()
        tiles = {
            1: ('todos', self.tile_muro, None),
            4: ('personaje', self.recoge_ruby, None),
        }
        self.motor.tga_load_tiles('media/niveles/tiles_tierra.tga', (TW, TH), tiles)
        self.motor.tga_load_level('media/niveles/laberinto2.tga')
        #Imágenes para los sprites.
        imagenes = [
            #Sprites del jugador.
            ('lp_s1', 'media/sprites/lp_s1.gif', (0, 0, 24, 24) ),
            ('lp_s2', 'media/sprites/lp_s2.gif', (0, 0, 24, 24) ),
            ('lp_o1', 'media/sprites/lp_o1.gif', (0, 0, 24, 24) ),
            ('lp_o2', 'media/sprites/lp_o2.gif', (0, 0, 24, 24) ),
            ('lp_e1', 'media/sprites/lp_e1.gif', (0, 0, 24, 24) ),
            ('lp_e2', 'media/sprites/lp_e2.gif', (0, 0, 24, 24) ),
            ('lp_n1', 'media/sprites/lp_n1.gif', (0, 0, 24, 24) ),
            ('lp_n2', 'media/sprites/lp_n2.gif', (0, 0, 24, 24) ),
            #Sprites de la bruja maldita.
            ('bm_s1', 'media/sprites/bm_s1.gif', (0, 0, 24, 24) ),
            ('bm_s2', 'media/sprites/bm_s2.gif', (0, 0, 24, 24) ),
            ('bm_o1', 'media/sprites/bm_o1.gif', (0, 0, 24, 24) ),
            ('bm_o2', 'media/sprites/bm_o2.gif', (0, 0, 24, 24) ),
            ('bm_e1', 'media/sprites/bm_e1.gif', (0, 0, 24, 24) ),
            ('bm_e2', 'media/sprites/bm_e2.gif', (0, 0, 24, 24) ),
            ('bm_n1', 'media/sprites/bm_n1.gif', (0, 0, 24, 24) ),
            ('bm_n2', 'media/sprites/bm_n2.gif', (0, 0, 24, 24) ),
            #Sprites del paladín del imperio.
            ('pi_s1', 'media/sprites/pi_s1.gif', (0, 0, 24, 24) ),
            ('pi_s2', 'media/sprites/pi_s2.gif', (0, 0, 24, 24) ),
            ('pi_o1', 'media/sprites/pi_o1.gif', (0, 0, 24, 24) ),
            ('pi_o2', 'media/sprites/pi_o2.gif', (0, 0, 24, 24) ),
            ('pi_e1', 'media/sprites/pi_e1.gif', (0, 0, 24, 24) ),
            ('pi_e2', 'media/sprites/pi_e2.gif', (0, 0, 24, 24) ),
            ('pi_n1', 'media/sprites/pi_n1.gif', (0, 0, 24, 24) ),
            ('pi_n2', 'media/sprites/pi_n2.gif', (0, 0, 24, 24) ),
            #Sprites del alter ego.
            ('ae_s1', 'media/sprites/ae_s1.gif', (0, 0, 24, 24) ),
            ('ae_s2', 'media/sprites/ae_s2.gif', (0, 0, 24, 24) ),
            ('ae_o1', 'media/sprites/ae_o1.gif', (0, 0, 24, 24) ),
            ('ae_o2', 'media/sprites/ae_o2.gif', (0, 0, 24, 24) ),
            ('ae_e1', 'media/sprites/ae_e1.gif', (0, 0, 24, 24) ),
            ('ae_e2', 'media/sprites/ae_e2.gif', (0, 0, 24, 24) ),
            ('ae_n1', 'media/sprites/ae_n1.gif', (0, 0, 24, 24) ),
            ('ae_n2', 'media/sprites/ae_n2.gif', (0, 0, 24, 24) ),
            #Sprites de los no-muertos.
            ('nm_s1', 'media/sprites/nm_s1.gif', (0, 0, 24, 24) ),
            ('nm_s2', 'media/sprites/nm_s2.gif', (0, 0, 24, 24) ),
            ('nm_o1', 'media/sprites/nm_o1.gif', (0, 0, 24, 24) ),
            ('nm_o2', 'media/sprites/nm_o2.gif', (0, 0, 24, 24) ),
            ('nm_e1', 'media/sprites/nm_e1.gif', (0, 0, 24, 24) ),
            ('nm_e2', 'media/sprites/nm_e2.gif', (0, 0, 24, 24) ),
            ('nm_n1', 'media/sprites/nm_n1.gif', (0, 0, 24, 24) ),
            ('nm_n2', 'media/sprites/nm_n2.gif', (0, 0, 24, 24) ),
        ]
        self.codigos = {
            1: (self.crear_jugador, None),
            4: (self.bruja_maldita, None),
            5: (self.alter_ego, None),
            6: (self.paladin, None),
            7: (self.no_muerto, None),
        }
        self.motor.load_images(imagenes)
        self.motor.run_codes(self.codigos, (0, 0, 16, 16))
        self.puntos = 0
        self.rubies = 0
        #Conteo inicial de rubíes.
        for linea in self.motor.tlayer:
            for tile in linea:
                if tile == 4:
                    self.rubies += 1
        
    def crear_jugador(self, motor, tile, valor):
        "Función para crear el sprite animado del jugador."
        imagenes = [
            ['lp_s1', 'lp_s2'],   #Abajo
            ['lp_n1', 'lp_n2'],   #Arriba
            ['lp_o1', 'lp_o2'],   #Izquierda
            ['lp_e1', 'lp_e2'],   #Derecha
        ]
        jugador = CharacterSprite(imagenes, (tile.rect.x+4, tile.rect.y+4), motor, 20)
        motor.sprites.append(jugador)
        jugador.loop = self.mover_jugador
        jugador.groups = motor.string2groups('todos,personaje')
        jugador.speed = 2
        
    def bruja_maldita(self, motor, tile, valor):
        "Función para crear a la bruja maldita."
        imagenes = [
            ['bm_s1', 'bm_s2'],   #Abajo
            ['bm_n1', 'bm_n2'],   #Arriba
            ['bm_o1', 'bm_o2'],   #Izquierda
            ['bm_e1', 'bm_e2'],   #Derecha
        ]
        bruja = CharacterSprite(imagenes, (tile.rect.x+4, tile.rect.y+4), motor, 20)
        motor.sprites.append(bruja)
        bruja.groups = motor.string2groups('todos')
        bruja.agroups = motor.string2groups('personaje')
        bruja.loop = self.mover_enemigo
        bruja.hit = self.juego_terminado
        bruja.speed = 2
        bruja.set_movedir(0)
        
    def alter_ego(self, motor, tile, valor):
        "Función para crear el alter ego."
        imagenes = [
            ['ae_s1', 'ae_s2'],   #Abajo
            ['ae_n1', 'ae_n2'],   #Arriba
            ['ae_o1', 'ae_o2'],   #Izquierda
            ['ae_e1', 'ae_e2'],   #Derecha
        ]
        alter = CharacterSprite(imagenes, (tile.rect.x+4, tile.rect.y+4), motor, 20)
        motor.sprites.append(alter)
        alter.groups = motor.string2groups('todos')
        alter.agroups = motor.string2groups('personaje')
        alter.loop = self.mover_enemigo
        alter.hit = self.juego_terminado
        alter.speed = 2
        alter.set_movedir(0)
        
    def paladin(self, motor, tile, valor):
        "Función para crear al paladín del imperio."
        imagenes = [
            ['pi_s1', 'pi_s2'],   #Abajo
            ['pi_n1', 'pi_n2'],   #Arriba
            ['pi_o1', 'pi_o2'],   #Izquierda
            ['pi_e1', 'pi_e2'],   #Derecha
        ]
        paladin = CharacterSprite(imagenes, (tile.rect.x+4, tile.rect.y+4), motor, 20)
        motor.sprites.append(paladin)
        paladin.groups = motor.string2groups('todos')
        paladin.agroups = motor.string2groups('personaje')
        paladin.loop = self.mover_enemigo
        paladin.hit = self.juego_terminado
        paladin.speed = 2
        paladin.set_movedir(2)
        
    def no_muerto(self, motor, tile, valor):
        "Función para crear al paladín del imperio."
        imagenes = [
            ['nm_s1', 'nm_s2'],   #Abajo
            ['nm_n1', 'nm_n2'],   #Arriba
            ['nm_o1', 'nm_o2'],   #Izquierda
            ['nm_e1', 'nm_e2'],   #Derecha
        ]
        no_muerto = CharacterSprite(imagenes, (tile.rect.x+4, tile.rect.y+4), motor, 20)
        motor.sprites.append(no_muerto)
        no_muerto.groups = motor.string2groups('todos')
        no_muerto.agroups = motor.string2groups('personaje')
        no_muerto.loop = self.mover_enemigo
        no_muerto.hit = self.juego_terminado
        no_muerto.speed = 2
        no_muerto.set_movedir(0)
        
    def tile_muro(self, motor, tile, sprite):
        sprite.crashed = True
        if sprite._rect.bottom <= tile._rect.top:
            sprite.rect.bottom = tile.rect.top
        if sprite._rect.right <= tile._rect.left:
            sprite.rect.right = tile.rect.left
        if sprite._rect.left >= tile._rect.right:
            sprite.rect.left = tile.rect.right
        if sprite._rect.top >= tile._rect.bottom:
            sprite.rect.top = tile.rect.bottom
            
    def recoge_ruby(self, motor, tile, sprite):
        self.puntos += 100
        self.rubies -= 1
        motor.set((tile.tx, tile.ty), 0)
        
    def mover_jugador(self, motor, sprite):
        teclas = p.key.get_pressed()
        if teclas[p.K_UP]:
            sprite.set_movedir(1)
        elif teclas[p.K_DOWN]:
            sprite.set_movedir(0)
        elif teclas[p.K_LEFT]:
            sprite.set_movedir(2)
        elif teclas[p.K_RIGHT]:
            sprite.set_movedir(3)
        sprite.update()
        
    def mover_enemigo(self, motor, sprite):
        if sprite.tile_changed():
            caminos = sprite.next_are_free([0, 2, 3, 4])
            if caminos:
                sprite.movedir = choice(caminos)
            else:
                sprite.reverse()
        sprite.update()
        
    def juego_terminado(self, motor, sprite, objeto):
        "Accede aquí en caso de colisión entre sprites."
        puntuaciones = High('media/puntuaciones/normal.dat')
        if puntuaciones.check(self.puntos) == None:
            #Aquí no alcanzo entrar.
            self.cambiar_escena(EscenaJuegoTerminado(self.puntos))
        else:
            self.cambiar_escena(EscenaTeclado(self.puntos))
            
    def actualizar(self):
        "Actualiza los objetos del juego."
        if self.rubies:
            self.motor.loop()
        else:
            self.juego_terminado(None, None, None)
            
    def dibujar(self, pantalla):
        "Dibujar objetos en pantalla."
        self.motor.paint(pantalla)
        fuente = p.font.Font(None, 36)
        puntuacion = fuente.render('%07d' % self.puntos, True, (255,255,255))
        x = pantalla.get_size()[0] - puntuacion.get_width()
        y = pantalla.get_size()[1] - puntuacion.get_height()
        pantalla.blit(puntuacion, (x, y))
        

class EscenaInicio(Escena):
    "Escena inicial del videojuego."
    def __init__(self):
        "Inicio del juego."
        Escena.__init__(self)
        #Configuración de la escena.
        p.mouse.set_visible(False)
        #Elementos gráficos.
        self.fondo = cargar_imagen("inicio.png", dirs="media/imagenes")
        #Opciones del menú.
        self.opcs = [
            ('Nuevo Juego',),
            ('Puntuaciones',),
            ('Salir',),
        ]
        #Opción seleccionada.
        self.opc = 0
        #Creando el archivo de puntuaciones.
        if not os.path.exists('media/puntuaciones/normal.dat'):
            puntuaciones = High('media/puntuaciones/normal.dat')
            for i in range(1, 11):
                puntuaciones.submit(1000*i**2, 'Computadora')
            puntuaciones.save()
        
    def leer_eventos(self, eventos):
        "Redirecciona a la pantalla adecuada."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_DOWN:
                    self.opc += 1
                    if self.opc >= len(self.opcs):
                        self.opc = 0
                elif evento.key == p.K_UP:
                    self.opc -= 1
                    if self.opc < 0:
                        self.opc = len(self.opcs) - 1
                elif evento.key == p.K_RETURN or evento.key == p.K_KP_ENTER:
                    if self.opc == 0:
                        self.cambiar_escena(EscenaJuego())
                    if self.opc == 1:
                        self.cambiar_escena(EscenaPuntuaciones())
                    elif self.opc == 2:
                        sys.exit(0)

    def dibujar(self, pantalla):
        "Mostrar pantalla inicial."
        pantalla.blit(self.fondo, (0, 0))
        #Dibujando las opciones
        x, y = 16, 400
        for i in range(len(self.opcs)):
            sombra = Texto(self.opcs[i][0], tamano=28, color=(0xFF,0xFF,0xFF))
            if self.opc == i:
                texto  = Texto(self.opcs[i][0], tamano=28, color=(0,0x33,0x99))
            else:
                texto  = Texto(self.opcs[i][0], tamano=28, color=(0,0,0x33))
            pantalla.blit(sombra.mostrar(), (x+1, y+1))
            pantalla.blit(texto.mostrar(), (x, y))
            y += 32
        #Dibujando el nombre del juego.
        texto  = Texto("Atwood", tamano=96, color=(0,0,0))
        pantalla.blit(texto.mostrar(), (264, 256))
            
class EscenaJuegoTerminado(Escena):
    "Escena presentada tras perder en el juego."
    def __init__(self, puntos=0):
        "Inicialización de las variables necesarias."
        Escena.__init__(self)
        #Configuración de la escena.
        p.mouse.set_visible(False)
        #Elementos gráficos.
        self.fondo = cargar_imagen("terminado.png", True, "media/imagenes")
        #Opciones del menú.
        self.opcs = [
            ('Reiniciar', 'F5'),
            (u'Menú', 'F6'),
            ('Salir', 'ESC'),
        ]
        #Opción seleccionada.
        self.opc = -1
        #Puntaje.
        self.puntos = puntos
        
    def leer_eventos(self, eventos):
        "Redirecciona a la pantalla adecuada."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_F5:
                    self.cambiar_escena(EscenaJuego())
                elif evento.key == p.K_RIGHT:
                    self.opc += 1
                    if self.opc >= len(self.opcs):
                        self.opc = 0
                elif evento.key == p.K_LEFT:
                    self.opc -= 1
                    if self.opc < 0:
                        self.opc = len(self.opcs) - 1
                elif evento.key == p.K_RETURN or evento.key == p.K_KP_ENTER:
                    if self.opc == 0:
                        self.cambiar_escena(EscenaJuego())
                    elif self.opc == 1:
                        self.cambiar_escena(EscenaInicio())
                    elif self.opc == 2:
                        sys.exit(0)

    def dibujar(self, pantalla):
        "Mostrar pantalla inicial."
        if self.opc == -1:
            pantalla.blit(self.fondo, (0, 0))
            self.opc = 0
        #Dibujando las opciones
        x, y = 0, 400
        for i in range(len(self.opcs)):
            sombra = Texto(self.opcs[i][0], tamano=28, color=(0,0,0x33))
            if self.opc == i:
                texto  = Texto(self.opcs[i][0], tamano=28, color=(255,255,0))
            else:
                texto  = Texto(self.opcs[i][0], tamano=28, color=(255,255,255))
            x = (pantalla.get_size()[0] / (len(self.opcs) + 1))*(i+1)
            x -= texto.rect.centerx
            pantalla.blit(sombra.mostrar(), (x+1, y+1))
            pantalla.blit(texto.mostrar(), (x, y))
        #Dibujando la puntuación final
        texto = Texto(u"Puntuación Final", tamano=32, color=(255,255,255))
        puntos = Texto(str(self.puntos), tamano=72, color=(255,255,255))
        x = pantalla.get_size()[0] / 2 - puntos.rect.centerx
        pantalla.blit(puntos.mostrar(), (x, 100))
        x = pantalla.get_size()[0] / 2 - texto.rect.centerx
        pantalla.blit(texto.mostrar(), (x, 72))
        
class EscenaPuntuaciones(Escena):
    "Escena para mostrar las puntuaciones más altas."
    def __init__(self, pos = None):
        "Inicializa los objetos necesarios y verifica la existencia de archivo."
        Escena.__init__(self)
        #Configuración de la escena.
        p.mouse.set_visible(False)
        #Elementos gráficos.
        self.fondo = cargar_imagen("inicio.png", dirs="media/imagenes")
        #Creando la lista de puntuaciones.
        self.puntuaciones = []
        if not os.path.exists('media/puntuaciones/normal.dat'):
            pass
        else:
            puntuaciones = High('media/puntuaciones/normal.dat')
            for puntuacion in puntuaciones:
                self.puntuaciones.append((
                    puntuacion.name,
                    str(puntuacion.score).zfill(6)
                ))
        self.pos = pos
        
    def leer_eventos(self, eventos):
        "Redirecciona a la pantalla adecuada."
        for evento in eventos:
            if evento.type == p.KEYDOWN:
                if evento.key == p.K_RETURN or evento.key == p.K_KP_ENTER:
                    self.cambiar_escena(EscenaInicio())

    def dibujar(self, pantalla):
        "Mostrar pantalla inicial."
        pantalla.blit(self.fondo, (0, 0))
        datos = self.puntuaciones   #Alias de puntuaciones para evitar escribir.
        #Dibujando las puntuaciones.
        x, y = 48, 100
        for i in range(len(self.puntuaciones)):
            #Si hay una puntuación nueva, cambiar el tamaño y el color.
            if self.pos == i + 1:
                color = (0x66,0x11,0x11)
                tamano = 30
            else:
                color = (0,0,0x33)
                tamano = 28
            #Imprimiendo el nombre.
            sombra = Texto(datos[i][0], tamano, color=(0xFF,0xFF,0xFF))
            texto  = Texto(datos[i][0], tamano, color=color)
            pantalla.blit(sombra.mostrar(), (x+1, y+1))
            pantalla.blit(texto.mostrar(), (x, y))
            #Imprimiendo la puntuación.
            sombra = Texto(datos[i][1], tamano, color=(0xFF,0xFF,0xFF))
            texto  = Texto(datos[i][1], tamano, color=color)
            pantalla.blit(sombra.mostrar(), (x+301, y+1))
            pantalla.blit(texto.mostrar(), (x+300, y))
            y += 36
        #Impresión de título e instrucciones.
        sombra = Texto(u"Puntuaciones Más Altas", tamano=40, color=(99,99,99))
        texto  = Texto(u"Puntuaciones Más Altas", tamano=40, color=(0,0,0))
        x = pantalla.get_size()[0] / 2 - texto.rect.centerx
        pantalla.blit(sombra.mostrar(), (x+1, 25))
        pantalla.blit(texto.mostrar(), (x, 24))
        sombra = Texto(u"Volver al Menú", tamano=24, color=(0xFF,0xFF,0xFF))
        texto  = Texto(u"Volver al Menú", tamano=24, color=(0,0x33,0x99))
        x = pantalla.get_size()[0] / 2 - texto.rect.centerx
        pantalla.blit(sombra.mostrar(), (x+1, 451))
        pantalla.blit(texto.mostrar(), (x, 450))
        
class EscenaTeclado(Escena):
    "Escena para introducir el nombre del jugador."
    def __init__(self, puntos = 0):
        "Inicializa los objetos necesarios."
        Escena.__init__(self)
        #Configuración de la escena.
        p.mouse.set_visible(False)
        #Elementos gráficos.
        self.fondo = cargar_imagen("inicio.png", dirs="media/imagenes")
        self.trans = cargar_imagen("terminado.png", True, "media/imagenes")
        #Propiedades
        self.teclado = TecladoPantalla()
        self.puntos = puntos
        
    def leer_eventos(self, eventos):
        "Registra el movimiento con las flechas."
        self.teclado.leer_eventos(eventos)
        
    def actualizar(self):
        "Guarda la puntuación en el archivo cuando se selecciona OK."
        if self.teclado.completado == True:
            if len(self.teclado.cadena) > 0:
                #Guardar puntuación en archivo.
                puntuaciones = High('media/puntuaciones/normal.dat')
                puntuaciones.submit(self.puntos, self.teclado.cadena)
                puntuaciones.save()
                posicion = puntuaciones.check(self.puntos)
                self.cambiar_escena(EscenaPuntuaciones(posicion))
            else:
                self.teclado.completado = False

    def dibujar(self, pantalla):
        "Mostrar teclado en pantalla."
        pantalla.blit(self.fondo, (0, 0))
        pantalla.blit(self.trans, (0, 0))
        self.teclado.dibujar_teclado(pantalla, 24, pos_y=172, inc_y=36)
        self.teclado.dibujar_display(pantalla, 32, pos_y=64)
        self.teclado.dibujar_comandos(pantalla, 24)
        texto = Texto(u"¡Nueva puntuación alta!", tamano=36, color=(255,255,99))
        x = pantalla.get_size()[0] / 2 - texto.rect.centerx
        pantalla.blit(texto.mostrar(), (x, 10))
