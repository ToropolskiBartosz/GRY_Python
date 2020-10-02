import pygame
import random


pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
# zmienne globalne
s_width = 800
s_height = 700
play_width = 300  # 10 bloków = 30 szerokość jednego
play_height = 600  # 20 bloków wysokości = 30 wysokości jeden blok
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Lista ze skrzałtami kawałków

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
#Definicja kolorów poszczególnych krztałtów
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # rotacja od 0-3


#5#Wypełnia siatkę określonymi kolorami
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c #zmiana koloru w liście o indeksie i j
    return grid

#7# KONWERTOWANIE# Konwertowanie zmiennej z listy shape na kształt
def convert_shape_format(shape):
    positions = []
    #Przyjmujemy obiekt klocka (odczytujemy jego krztałt)
    #                     iolość rotacji  długość listy [ 0%4=0 1%4=3 2%4=2 3%4=1 4%4=o wszystkie elementy T]
    format = shape.shape[shape.rotation % len(shape.shape)]
    #formatowi przypisany jest krztałr
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))#shape.y umożliwia spadanie shape.x poruszanie

    
    for i, pos in enumerate(positions):
        #skorektowanie wylatowania kawałków
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

#9# Określ prawidłową przestrzeń
def valid_space(shape, grid):
    #Wypisuję wolną pozycję
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    #Tworzenie jedno wymiarowej tablicy
    accepted_positions = [j for sub in accepted_positions for j in sub]
    #7# KONWERTOWANIE#
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True

#8#Sprawdzanie, czy przegrywamy
def check_lost(positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

#6# # POBIERANIE_FIGURY # Wyświeta losowo figury
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))

#12# rysowanie na środku ektanu "Przegrałeś"
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

 #3# # FUNKCJA_RYSOWANIA_LINI # Ta funkcja rysuje szare linie siatki, które widzimy
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    # poziome linie
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))
    # pionowe linie
    for j in range(col):
        pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


#11 # ta fukcja czyść wiersze jeśli zapełni się kolorem
def clear_rows(grid, locked):
    # muszę sprawdzić, czy rząd jest czysty, przesuń co drugi rząd powyżej jednego w dół

    inc = 0
    #usuwanie wiersza
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # dodaj pozycje do usunięcia z zablokowanego
            ind = i
            for j in range(len(row)):
                try:
                    bulletSound = pygame.mixer.Sound('laser.wav')
                    bulletSound.play()
                    del locked[(j, i)]
                except:
                    continue
    # Funkcja "przesuniecia" kawałka nad usunientym wierszem
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

#10#Rysowania jaka będzie kolejna figura
def draw_next_shape(shape, surface):
    #Tworzenie nagłówka
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Nastepna figura', 1, (255, 255, 255))
    # Położenie rysowanego bloczka
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    # Tu chyba będzie lepsze zero   #
    format = shape.shape[0]
    #Rysowanie bloczka
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
                # Rysowanie śatki na blocku #
                pygame.draw.rect(surface, (128, 128, 128), (sx + j * 30, sy + i * 30, 30, 30), 1)
    #wypisanie nagłówka
    surface.blit(label, (sx + 10, sy - 30))
#14# Wprowadzanie wyszszego wyniyku do pliku
def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))
#13#
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score
#4##RYSUJ_OKNO#
def draw_window(surface, grid, score=0,last_score=0):
    surface.fill((0, 0, 0))
    # Tworzenie napisu TETRIS
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 0, 0))
    # Wypisanie tytułu
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    # Obecny wynik jaki posiada gracz
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Wynik: ' + str(int(score)), 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # Najwyższy wynik
    label = font.render('Rekord: ' + str(last_score), 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))
    # Tworzenie pól w siatce
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)
    # Rysowanie obramowania obszaru gry
    pygame.draw.rect(surface, (255, 255, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    #3# # FUNKCJA_RYSOWANIA_LINI # narysuj siatke
    draw_grid(surface, 20, 10)


#2##Pętla główna#
def main(win):
    global grid
    last_score = max_score()#13#Pobiera z funkcji
    locked_positions = {}  # (x,y):(255,0,0) # Słownik do określenia koloru danej współżednej
    #5#Wypełnia siatkę określonymi kolorami
    grid = create_grid(locked_positions)
    #Flaga informująca czy wyświetlać kolejny kawałek
    change_piece = False
    #Warunek działania gry
    run = True
    #6# # POBIERANIE_FIGURY #
    current_piece = get_shape()# tworzymy obiekt klocek/kawałek
    #6# # POBIERANIE_FIGURY #
    next_piece = get_shape()
    clock = pygame.time.Clock()
    #zmienne do zwiększenia trudności gry
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    #Wynik
    score = 0


    while run:
        #5#Wypełnia siatkę określonymi kolorami
        grid = create_grid(locked_positions)
        #Czas
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        #Przśpieszenie spadających klocków
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.05:
                fall_speed -= 0.01

        # Kod to upadającego kawałka
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            # 9# Określ prawidłową przestrzeń
            #Jeśli znajdzie się na dni lub dodkcie podłożem koloru, zatrzyma się
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    # 9# Określ prawidłową przestrzeń
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    # 9# Określ prawidłową przestrzeń
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # OBRACANIE FIGURĄ
                    # 9# Określ prawidłową przestrzeń
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                if event.key == pygame.K_DOWN:
                    # Poruszanie figurą w dół szybciej
                    current_piece.y += 1
                    # 9# Określ prawidłową przestrzeń
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        #7# KONWERTOWANIE#
        shape_pos = convert_shape_format(current_piece)

        # dodaj kolor elementu do siatki do rysowania
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # Jeśli nie jesteśmy ponad ekranem
                grid[y][x] = current_piece.color

        # Blokowanie kawałka w danej pozycji oraz wyświetlenie kolejnego kawałka
        if change_piece:
            #zatrzymanie w określonej pozycji
            for pos in shape_pos:
                p = (pos[0], pos[1])
                #{(1,2):(255,0,0)'Kolor'}
                # dla określonej pozycji jest przypisany dany kolor z klassy "Kawałek"
                locked_positions[p] = current_piece.color
            #Losujemy Nowy kawałek u góry
            current_piece = next_piece
            #6# # POBIERANIE_FIGURY #
            next_piece = get_shape()
            change_piece = False
            #11 #  dodawanie wyniku
            #14 # Usuwanie pełnego wiersza
            scorefirst = clear_rows(grid, locked_positions) *10
            #Bonus
            score += ((scorefirst*scorefirst)/10)




        #4#RYSUJ_OKNO#
        draw_window(win, grid, score, last_score)
        # 10#Rysowania jaka będzie kolejna figura
        draw_next_shape(next_piece, win)
        pygame.display.update()
        #8# Sprawdzanie, czy przegrywamy
        if check_lost(locked_positions):
            # 12# rysowanie na środku ektanu "Przegrałeś"
            draw_text_middle(win, "PRZEGRALES!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            #14#
            update_score(score)
#1#
def main_menu(win):
    run = True
    wall=False
    first=170
    secend=370
    val= 70
    while run:
        win.fill((0, 0, 0))
        font_Title=pygame.font.SysFont("comicsans", 110, bold=True)
        label = font_Title.render('TE', 1, (255, 0, 0))
        win.blit(label, (250, 30))
        label = font_Title.render('TR', 1, (0, 255, 0))
        win.blit(label, (370, 30))
        label = font_Title.render('IS', 1, (128, 0, 128))
        win.blit(label, (490, 30))
        font = pygame.font.SysFont("comicsans", 40, bold=True)
        label = font.render('Wyjdz', 1, (255, 255, 255))
        win.blit(label, (200, 385))
        label = font.render('Start', 1, (255, 255, 255))
        win.blit(label, (200, 315))
        pygame.draw.rect(win, (255, 255, 255), (first, secend, 450, 60), 2)
        pygame.display.update()


        #Obsługa menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if (secend == 370):
                secend -=val
                wall=True
        if keys[pygame.K_DOWN]:
            if (secend == 300):
                secend += val
                wall=False
        if keys[pygame.K_SPACE]:
            if(wall):
                main(win)
            else:
                run = False
    pygame.display.quit()
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start gry