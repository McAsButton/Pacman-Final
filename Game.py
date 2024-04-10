import pygame as pg
from settings import *
from sprites import *
from time import sleep

class Game:
    #Inicializamos el juego
    def __init__(self):
        pg.init() #Inicializar PyGame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #Definir las medidas de la pantalla del juego
        pg.display.set_caption(TITLE) #Definir el titulo de la pantalla del juego
        self.clock = pg.time.Clock() #Definir un reloj
        self.running = True
        self.spawn_block = 0
        self.show_logo = True

    # Empieza un juego nuevo
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        ######### Se crea el mapa ###########
        Level_1 = [
        'WWWWWWWWWWWWWWWWWWWWWWW',
        'W          W          W',
        'W WWW WWWW W WWWW WWW W',
        'W WWW WWWW W WWWW WWW W',
        'W     R               W',
        'W WWW W WWWWWWW W WWW W',
        'W     W    W    W     W',
        'WWWWW WWWWSWSWWWW WWWWW',
        'WWWWW WSSSSSSSSSW WWWWW',
        'WWWWW WSWWWSWWWSW WWWWW',
        'SSSSS SSWSOPBSWSS SSSSS',
        'WWWWW WSWWWWWWWSW WWWWW',
        'WWWWW WSSSS1SSSSW WWWWW',
        'WWWWW WSWWWWWWWSW WWWWW',
        'W          W          W',
        'W WWW WWWW W WWWW WWW W',
        'WE  W             W  EW',
        'WW  W W WWWWWWW W W  WW',
        'W     W    W    W     W',
        'W WWWWWWWW W WWWWWWWW W',
        'W                     W',
        'WWWWWWWWWWWWWWWWWWWWWWW'
        ]
        x = y = 0
        bitAmount = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bit_list = pg.sprite.Group()
        self.ghost_list = pg.sprite.Group()
        wt = [] #Muros arriba
        wb = [] #Muros abajo
        wl = [] #Muros izquierda
        wr = [] #muros derecha

        for row in Level_1:
            for col in row:
                if col == 'W': #Se define la posición de los muros
                    wall = Wall(self, (x, y))
                    wt.append([wall.rect.top, wall.rect.x])
                    wb.append([wall.rect.bottom, wall.rect.x])
                    wl.append([wall.rect.left, wall.rect.y])
                    wr.append([wall.rect.right, wall.rect.y])

                elif col == ' ': #Se define las posiciones de los pacdots
                    bit1 = Bit(self, (x,y))
                    bitAmount += 1

                elif col == 'R': #Se define la posición inicial del fantasma rojo
                    self.spawnr = GhostRED((x, y), self)
                    bit1 = Bit(self, (x,y))
                    bitAmount += 1

                elif col == 'O': #Se define la posición inicial del fantasma naranja
                    self.spawno = GhostORANGE((x, y), self)

                elif col == 'P': #Se define la posición inicial del fantasma rosa
                    self.spawnp = GhostPINK((x, y), self)

                elif col == 'B': #Se define la posición inicial del fantasma azul
                    self.spawnb = GhostBLUE((x, y), self)
                    
                elif col == '1': #Se define la posición inicial del pacman
                    playerx = x
                    playery = y
                x += 20
            y += 20
            x = 0
        #Agregamos dos muros invisibles para los fantasmas (camino lateral)
        wall = Wall(self, (-20, 200), BLACK)
        wr.append([wall.rect.right, wall.rect.y])

        wall = Wall(self, (460, 200), BLACK)
        wl.append([wall.rect.left, wall.rect.y])
        
        self.spawnr.wt = wt
        self.spawnr.wb = wb
        self.spawnr.wl = wl
        self.spawnr.wr = wr
        self.spawno.wt = wt
        self.spawno.wb = wb
        self.spawno.wl = wl
        self.spawno.wr = wr
        self.spawnp.wt = wt
        self.spawnp.wb = wb
        self.spawnp.wl = wl
        self.spawnp.wr = wr
        self.spawnb.wt = wt
        self.spawnb.wb = wb
        self.spawnb.wl = wl
        self.spawnb.wr = wr
        self.player = Player(self, (playerx, playery), self.walls, self.bit_list, bitAmount) #Se dibuja el pacman
        ########## Finaliza la creación del mapa ##########
        self.run()

    # Bucle del juego
    def run(self):
        self.playing = True
        while self.playing == True:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    #Bucle del juego - actualizaciones
    def update(self):
        self.all_sprites.update()
        if self.spawno.not_spawn and self.spawnp.not_spawn and self.spawnb.not_spawn and self.spawn_block == 0:
            wall = Entrance(self, (220, 180))
            self.spawnr.wt.append([wall.rect.top, wall.rect.x])
            self.spawnr.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnr.wl.append([wall.rect.left, wall.rect.y])
            self.spawnr.wr.append([wall.rect.right, wall.rect.y])
            self.spawno.wt.append([wall.rect.top, wall.rect.x])
            self.spawno.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawno.wl.append([wall.rect.left, wall.rect.y])
            self.spawno.wr.append([wall.rect.right, wall.rect.y])
            self.spawnp.wt.append([wall.rect.top, wall.rect.x])
            self.spawnp.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnp.wl.append([wall.rect.left, wall.rect.y])
            self.spawnp.wr.append([wall.rect.right, wall.rect.y])
            self.spawnb.wt.append([wall.rect.top, wall.rect.x])
            self.spawnb.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnb.wl.append([wall.rect.left, wall.rect.y])
            self.spawnb.wr.append([wall.rect.right, wall.rect.y])
            
    # Bucle del juego - eventos
    def events(self):
        for event in pg.event.get():
            # Verifica si se quiere cerrar la pantalla
            if event.type == pg.QUIT:
                self.show_go_screen()
        #Condición para cuando el pacman muere
        if pg.sprite.spritecollide(self.player, self.ghost_list, False) or self.spawnr.lpos[-1] == (self.player.rect.x, self.player.rect.y):
            count = 0
            times = 0
            done = False
            self.highscores = []
            with open('recursos/high.txt', 'r') as f:
                for line in f:
                    if times == 10:
                        break
                    #Se guarda el puntaje en los puntajes maximos
                    if int(line[line.find(',')+1:]) < self.player.bits_collected and not done:
                        highscore = self.get_name()+', '+str(self.player.bits_collected)
                        self.highscores.append(highscore)
                        times += 1
                        done = True
                    self.highscores.append(line)
                    times += 1
                    count += 1           
            #Condición si los puntajes maximos están en blanco
            if count < 9 and not done:
                self.highscores.append(self.get_name()+', '+str(self.player.bits_collected))
            #Escribe en el archivo txt
            with open('recursos/high.txt', 'w') as f:
                couuut = 0
                for highscore in self.highscores:
                    if couuut == len(self.highscores)-1:
                        f.write(highscore.strip())
                    else:
                        f.write(highscore.strip() +'\n')
                    couuut += 1
            self.show_start_screen()

    #Bucle para obtener el nombre del jugador (Puntuación alta)
    def get_name(self):
        name = []
        waiting = True
        while waiting:
            self.screen.fill(LIGHTBLUE)
            self.draw_text('Obtuviste un puntaje alto, ', 20, YELLOW, WIDTH/2, 50)
            self.draw_text('escribe tu nombre(minusculas y espacios)', 20, YELLOW, WIDTH/2, 70)
            self.draw_text('máximo 10 letras (escribe algo)!', 20, YELLOW, WIDTH/2, 90)
            self.draw_text(''.join(name), 30, YELLOW, WIDTH/2, HEIGHT/2)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                elif event.type == pg.KEYDOWN:
                    if len(name) <= 10:
                        if event.key == pg.K_a:
                            name.append('a')
                        elif event.key == pg.K_b:
                            name.append('b')
                        elif event.key == pg.K_c:
                            name.append('c')
                        elif event.key == pg.K_d:
                            name.append('d')
                        elif event.key == pg.K_e:
                            name.append('e')
                        elif event.key == pg.K_f:
                            name.append('f')
                        elif event.key == pg.K_g:
                            name.append('g')
                        elif event.key == pg.K_h:
                            name.append('h')
                        elif event.key == pg.K_i:
                            name.append('i')
                        elif event.key == pg.K_j:
                            name.append('j')
                        elif event.key == pg.K_k:
                            name.append('k')
                        elif event.key == pg.K_l:
                            name.append('l')
                        elif event.key == pg.K_m:
                            name.append('m')
                        elif event.key == pg.K_n:
                            name.append('n')
                        elif event.key == pg.K_o:
                            name.append('o')
                        elif event.key == pg.K_p:
                            name.append('p')
                        elif event.key == pg.K_q:
                            name.append('q')
                        elif event.key == pg.K_r:
                            name.append('r')    
                        elif event.key == pg.K_s:
                            name.append('s')
                        elif event.key == pg.K_t:
                            name.append('t')
                        elif event.key == pg.K_u:
                            name.append('u')
                        elif event.key == pg.K_v:
                            name.append('v')
                        elif event.key == pg.K_w:
                            name.append('w')
                        elif event.key == pg.K_x:
                            name.append('x')
                        elif event.key == pg.K_y:
                            name.append('y')
                        elif event.key == pg.K_z:
                            name.append('z')
                        elif event.key == pg.K_SPACE:
                            name.append(' ')
                    if event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pg.K_RETURN and len(name) > 0:
                        waiting = False
        return ''.join(name)

    #Bucle del juego - Dibujado
    def draw(self):
        game_screen = pg.image.load('recursos/fondo_juego.png').convert()
        self.screen.blit(game_screen, (0,0))
        self.all_sprites.draw(self.screen)
        self.draw_text('Puntuación máxima:', 30, YELLOW, 100, HEIGHT-150)
        count = 0
        firstHigh = 0
        with open('recursos/high.txt', 'r') as f:
            for line in f:
                count += 1
                pos = line.find(',')
                firstHigh = int(line[pos+1:].strip())
                highscoreDisp = line[pos+1:].strip()
                break
        if count == 0 or self.player.bits_collected > firstHigh:
            highscoreDisp = self.player.bits_collected
        self.draw_text(str(highscoreDisp), 30, YELLOW, 100, HEIGHT-100)
            
        self.draw_text('Su puntuación:', 30, YELLOW, 350, HEIGHT-150)
        self.draw_text(str(self.player.bits_collected), 30, YELLOW, 350, HEIGHT-100)
        # *despues* de dibujar todo, voltea la pantalla
        pg.display.flip()

    #Escribir texto
    def draw_text(self, text, size, color , x, y, font_name = 'Arial Rounded'):
        font = pg.font.Font(pg.font.match_font(font_name), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    #Mostrar la pantalla de inicio
    def show_start_screen(self):
        if self.show_logo:
            self.name = pg.image.load('recursos/PyGame.png').convert()
            self.name_rect = self.name.get_rect()
            self.name = pg.transform.scale(self.name, (284, 300))
            self.screen.fill(BLACK)
            self.screen.blit(self.name, (85, 150))
            pg.display.flip()
            self.show_logo = False
            sleep(2)
        key_press = False
        self.waiting_start = True
        full_list = ['P','r','e','s','i','o','n','a',' u','n','a',' t','e','c','l','a',' p','a','r','a',' e','m','p','e','z','a','r',' .', '.','.']
        show_list = []
        index = 0
        count = 0
        while not key_press:
            count += 1
            sleep(0.2)
            try:
                show_list.append(full_list[index])
                index += 1
            except:
                show_list = []
                index = 0
            self.screen.fill(BLACK)
            pac_image = pg.image.load('recursos/Pacman_Intro.png').convert()
            self.screen.blit(pac_image, (0,0))
            self.draw_text(''.join(show_list), 20, ORANGE, WIDTH / 2, HEIGHT-100)
            pg.display.flip()
            if count > 5: #Comprueba si se presiono una tecla o no
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.show_go_screen()
                    elif event.type == pg.KEYDOWN:
                        key_press = True

        self.screen.fill(BLACK)
        arrowPos = 0
        arrowDict = {0:[WIDTH/2 -200, HEIGHT*1/5], 1:[WIDTH*1/2 -200, HEIGHT*2/5], 2:[WIDTH*1/2 -200, HEIGHT*3/5], 3:[WIDTH*1/2 -200, HEIGHT*4/5]} #Ubicación de la flecha
        self.draw_text('>', 30, YELLOW, WIDTH*1/2 -100, HEIGHT*1/5)
        while self.waiting_start:
            rect_list = []
            menu_image = pg.image.load('recursos/Menu.png').convert()
            self.screen.blit(menu_image, (0,0))
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        arrowPos = (arrowPos+1)%4
                    elif event.key == pg.K_UP:
                        arrowPos = (arrowPos-1)%4
                    elif event.key == pg.K_RETURN:
                        if arrowPos == 0:
                            self.new()
                        elif arrowPos == 1:
                            self.show_credits()
                            self.screen.fill(BLACK)
                        elif arrowPos == 2:
                            self.show_settings()
                            self.screen.fill(BLACK)
                        else:
                            self.show_high()
                            self.screen.fill(BLACK)
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 250, HEIGHT*1/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 250, HEIGHT*2/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 250, HEIGHT*3/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 250, HEIGHT*4/5, 50,50))
            self.draw_text('>', 30, YELLOW, arrowDict[arrowPos][0], arrowDict[arrowPos][1])
            pg.display.flip()
            self.bgspritesheet = Spritesheet('recursos/Fantasma_Azul.png')
            self.rgspritesheet = Spritesheet('recursos/Fantasma_Rojo.png')
            self.pgspritesheet = Spritesheet('recursos/Fantasma_Rosa.png')
            self.ogspritesheet = Spritesheet('recursos/Fantasma_Naranja.png')
            self.pspritesheet = Spritesheet('recursos/Pacman.png')

    #Mostrar las instrucciones
    def show_settings(self):
        instruc_image = pg.image.load('recursos/instrucciones.png').convert()
        self.screen.blit(instruc_image, (0,0))
        pg.display.flip()
        self.wait_for_key()

    #Mostrar puntajes altos
    def show_high(self):        
        count = 0
        high_image = pg.image.load('recursos/puntajes_maximos.png').convert()
        self.screen.blit(high_image, (0,0))
        pg.display.flip()
        highPos = [60,80,100,120,140,160,180,200,220,240]
        with open('recursos/high.txt', 'r') as f:
            for line in f:
                count += 1
                if count > 10:
                    break
                self.draw_text(str(count)+'. '+line.strip(), 25, YELLOW, WIDTH/2, highPos[count-1])
        if count == 0:
            self.draw_text('Aun no hay puntajes altos!', 15, YELLOW, WIDTH/2, 60)
        pg.display.flip()
        self.wait_for_key()

    #Mostrar los créditos
    def show_credits(self):
        credit_image = pg.image.load('recursos/agradecimientos.png').convert()
        self.screen.blit(credit_image, (0,0))
        pg.display.flip()
        self.wait_for_key()
    
    #Mostrar la pantalla de salida
    def show_go_screen(self):
        quit_image = pg.image.load('recursos/Salir.png').convert()
        self.screen.blit(quit_image, (0,0))
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:             
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    waiting = False

    #Esperar pulsación de una tecla
    def wait_for_key(self):
        self.waiting_for_key = True
        while self.waiting_for_key:
            self.clock.tick(FPS)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                    self.waiting_for_key = False
                elif event.type == pg.KEYDOWN:
                    self.waiting_for_key = False