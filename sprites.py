# Clases de Sprite para el juego
import pygame as pg
from settings import *
import random

#Clase para los sprites
class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert() #Carga la imagen de la carpeta recursos

    def get_image(self, x, y, width, height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

#Sprite para el pacman
class Player(pg.sprite.Sprite):
    def __init__(self, game, loc, wallPos, bits, ba):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walls = wallPos
        self.bit_list = bits
        self.bitAmount = ba
        self.load_images()
        self.image = self.right_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.key = pg.key.get_pressed()
        self.bits_collected = 0
        self.queue = []
        self.move = 2
        self.move_x = 0
        self.move_y = 0
        self.key_pressed = []
        self.queue = []
        self.last_update = 0
        self.current_frame = 0

    def load_images(self): #Carga la imagen de Pacman.
            self.left_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 180), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),180), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 180)]
            self.right_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20,20)), pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20,20)),  pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)), pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20,20))]
            self.up_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 90), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),90), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 90)]
            self.down_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 270), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),270), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 270)]
            for image in self.left_frames:
                image.set_colorkey(BLACK)
            for image in self.right_frames:
                image.set_colorkey(BLACK)
            for image in self.up_frames:
                image.set_colorkey(BLACK)
            for image in self.down_frames:
                image.set_colorkey(BLACK) 

    def animate(self, y, x): #Se define el orden de la animación respecto al sprite
        now = pg.time.get_ticks()
        if self.move_x == -self.move:
            self.sprite_frames = self.left_frames
        elif self.move_x == self.move:
            self.sprite_frames = self.right_frames
        elif self.move_y == self.move:
            self.sprite_frames = self.down_frames
        elif self.move_y == -self.move:
            self.sprite_frames = self.up_frames
        else:
            self.sprite_frames = [self.right_frames[0]]
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

    def update(self): #Actualizaciones del sprite de Pacman respecto a las teclas presionadas
        key = pg.key.get_pressed()
        if len(self.queue) < 1:
            if key[pg.K_LEFT]:
                self.queue.append(key)
            elif key[pg.K_RIGHT]:
                self.queue.append(key)
            elif key[pg.K_UP]:
                self.queue.append(key)
            elif key[pg.K_DOWN]:
                self.queue.append(key)
        if self.rect.y % 20 == 0 and self.rect.x % 20 == 0:
            if len(self.queue) > 0:
                if self.queue[-1][pg.K_LEFT]:
                    self.rect.x -= 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.x += 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_x = -self.move
                        self.move_y = 0
                elif self.queue[-1][pg.K_RIGHT]:
                    self.rect.x += 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.x -= 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = 0
                        self.move_x = self.move
                elif self.queue[-1][pg.K_UP]:
                    self.rect.y -= 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.y += 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = -self.move
                        self.move_x = 0
                elif self.queue[-1][pg.K_DOWN]:
                    self.rect.y += 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.y -= 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = self.move
                        self.move_x = 0
        self.animate(self.rect.y, self.rect.x)
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.x == 440:
            self.rect.x = 2
        elif self.rect.x == 0:
            self.rect.x = 438
        if pg.sprite.spritecollide(self, self.walls, False):
            if self.key_pressed[-1][pg.K_LEFT]:
                self.rect.x += 2
                self.move_y = 0
                self.move_x = 0
            elif self.key_pressed[-1][pg.K_RIGHT]:
                self.rect.x -= 2
                self.move_y = 0
                self.move_x = 0
            elif self.key_pressed[-1][pg.K_UP]:
                self.rect.y += 2
                self.move_y = 0
                self.move_x = 0
            else:
                self.rect.y -= 2
                self.move_y = 0
                self.move_x = 0
        
        if pg.sprite.spritecollide(self, self.bit_list, True):
            self.bits_collected += 1
        if self.bits_collected == self.bitAmount:
            pass

#Sprite para los muros
class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, color=BLUE):
        self._layer = 0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 20
        self.image = pg.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

#Sprite para la tapa que bloquea la entrada al recinto de los fantasmas
class Entrance(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = 0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 20
        self.image = pg.image.load('recursos/Entrada.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

#Sprite para las galletas (dot, bit, etc)
class Bit(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = 0
        self.groups = game.all_sprites, game.bit_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.image = pg.image.load('recursos/Dot.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + self.size / 2
        self.rect.y = pos[1] + self.size / 2

#Sprite para el fantasma rojo
class GhostRED(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]

    def load_images(self): #Se carga la imagen del fantasma rojo
        self.left_frames = [self.game.rgspritesheet.get_image(148, 57.5, 20, 20), self.game.rgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.rgspritesheet.get_image(148, 185, 20, 20), self.game.rgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.rgspritesheet.get_image(20, 185, 20, 20), self.game.rgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.rgspritesheet.get_image(20, 315, 20, 20), self.game.rgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x): #Se define el orden de la animación respecto al sprite
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        
    def update(self): #Actualizaciones del fantasma rojo
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        #ABAJO, ARRIBA, IZQUIERDA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0

        #ABAJO, ARRIBA, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
        
        #ABAJO, ARRIBA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
        
        #ABAJO, IZQUIERDA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]

        #ABAJO, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #ARRIBA, IZQUIERDA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]

        #ARRIBA, DERECHA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #IZQUIERDA, DERECHA
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]

        #ABAJO
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            
        # ARRIBA
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
            
        #IZQUIERDA
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            
        #DERECHA
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0

        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos

#Sprite  para el fantasma naranja
class GhostORANGE(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False

    def load_images(self):#Se carga la imagen del fantasma naranja
        self.left_frames = [self.game.ogspritesheet.get_image(148, 57.5, 20, 20), self.game.ogspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.ogspritesheet.get_image(148, 185, 20, 20), self.game.ogspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.ogspritesheet.get_image(20, 185, 20, 20), self.game.ogspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.ogspritesheet.get_image(20, 315, 20, 20), self.game.ogspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):#Se define el orden de la animación respecto al sprite
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        
    def update(self):#Actualizaciones del fantasma naranja
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True
        
        #ABAJO, ARRIBA IZQUIERDA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0

        #ABAJO, ARRIBA, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
        
        #ABAJO, ARRIBA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
        
        #ABAJO, IZQUIERDA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]

        #ABAJO, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        # ARRIBA, IZQUIERDA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
        
        #ARRIBA, DERECHA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #IZQUIERDA, DERECHA
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]

        #ABAJO
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            
        #ARRIBA
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
           
        #IZQUIERDA
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0

        #DERECHA
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
        self.animate(self.rect.y, self.rect.x)          
        self.rect.y += self.yPos
        self.rect.x += self.xPos

#Sprite para el fantasmas rosa
class GhostPINK(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False

    def load_images(self):#Se carga la imagen del fantasma rosa
        self.left_frames = [self.game.pgspritesheet.get_image(148, 57.5, 20, 20), self.game.pgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.pgspritesheet.get_image(148, 185, 20, 20), self.game.pgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.pgspritesheet.get_image(20, 185, 20, 20), self.game.pgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.pgspritesheet.get_image(20, 315, 20, 20), self.game.pgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):#Se define el orden de la animación respecto al sprite
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        
    def update(self):#Actualizaciones del fantasma rosa
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True

        #ABAJO, ARRIBA, IZQUIERDA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0

        #ABAJO, ARRIBA, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0

        #ABAJO, ARRIBA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
        
        # ABAJO, IZQUIERDA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]

        #ABAJO, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #ARRIBA, IZQUIERDA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
        
        #ARRIBA, DERECHA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #IZQUIERDA, DERECHA
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]

        #ABAJO
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            
        #ARRIBA
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0

        #IZQUIERDA
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0

        #DERECHA
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos

#Sprite para el fantasma azul
class GhostBLUE(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False

    def load_images(self):#Se carga la imagen del fantasma azul
        self.left_frames = [self.game.bgspritesheet.get_image(148, 57.5, 20, 20), self.game.bgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.bgspritesheet.get_image(148, 185, 20, 20), self.game.bgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.bgspritesheet.get_image(20, 185, 20, 20), self.game.bgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.bgspritesheet.get_image(20, 315, 20, 20), self.game.bgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):#Se define el orden de la animación respecto al sprite
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        
    def update(self):#Actualizaciones del fantasma azul
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True

        #ABAJO, ARRIBA, IZQUIERDA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0

        #ABAJO, ARRIBA, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0

        #ABAJO, ARRIBA
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
        
        #ABAJO, IZQUIERDA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]

        #ABAJO, DERECHA
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #ARRIBA, IZQUIERDA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
        
        #ARRIBA, DERECHA
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]

        #IZQUIERDA, DERECHA
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]

        #ABAJO
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            
        #ARRIBA
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0

        #IZQUIERDA
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0

        #DERECHA
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos