import pygame
import random
# Definicja wymiarów okna gry
szerokosc_Okna = 480
wysokosc_Okna = 480
# Zdefiniowanie wymiarów poszczegółnych kratek siatki
rozmiar_Kratki = 20
szerokosc_Kratki = szerokosc_Okna / rozmiar_Kratki
wysokosc_Kratki = wysokosc_Okna / rozmiar_Kratki

# zmiana kierunku ruchu
gora = (0, -1)
dol = (0, 1)
lewo = (-1, 0)
prawo = (1, 0)

class Snake():
    def __init__(self):
        self.__dlugosc = 1
        self.__pozycja = [((szerokosc_Okna / 2), (wysokosc_Okna / 2))]
        self.__kierunek_ruchu = gora
        self.punkty = 0
        self.kolor = (0, 255, 0)

    def pozycja_Glowy(self):
        return self.__pozycja[-1]

    def kierunek(self, kierunek_ruchu):
        # Jeśli wąż ma ogon nie może się cofnąć
        if self.__dlugosc > 1 and (kierunek_ruchu[0] * -1, kierunek_ruchu[1] * -1) == self.__kierunek_ruchu:
            return
        else:
            self.__kierunek_ruchu = kierunek_ruchu

    def ruch(self):
        glowa = self.pozycja_Glowy()
        x,y = self.__kierunek_ruchu
        # Nowa pozycja Snake na bazie pozycji jego głowy
        nowa_Pozycja = (((glowa[0] + (x * rozmiar_Kratki)) % szerokosc_Okna), (glowa[1] + (y * rozmiar_Kratki)) % wysokosc_Okna)

        # Jeśli nowa pozycja jest w miejscu ogona, Snake jest restowany
        if len(self.__pozycja) > 2 and nowa_Pozycja in self.__pozycja[2:]:
            self.reset()
        # Jeśli nowa pozycja będzie się równać krawędzi scian wąż zostanie zresetowany
        elif  ((nowa_Pozycja[1]) == 0 and y == 1) or ((nowa_Pozycja[1]) == 460 and y == -1):
            self.reset()
        elif ((nowa_Pozycja[0]) == 0 and x == 1) or ((nowa_Pozycja[0]) == 460 and x == -1):
            self.reset()
        else:
            # Przypisanie nowej pozycji do listy __pozycja
            self.__pozycja.append(nowa_Pozycja)
            # Usuwanie starej pozycji lub ominięcie kroku w wyniku snek się wydłuża
            if len(self.__pozycja) > self.__dlugosc:  del self.__pozycja[0]

    def reset(self):
        self.__dlugosc = 1
        self.__pozycja = [((szerokosc_Okna / 2), (wysokosc_Okna / 2))]
        self.__kierunek_ruchu = random.choice([gora, dol, lewo, prawo])
        self.punkty = 0

    def rysowanie(self, okno_Gry):
        # Odczytywanie listy od końca ponieważ nowa pozycja głowy jest na końcu listy
        # Dalsze współżędne na liście wskazują położenie części ogona węża
        for p in self.__pozycja[::-1]:
            r = pygame.Rect((p[0], p[1]), (rozmiar_Kratki, rozmiar_Kratki))
            pygame.draw.rect(okno_Gry, self.kolor, r)
            pygame.draw.rect(okno_Gry, (128, 128, 128), r, 1)

    def zjedzenie(self):
        self.__dlugosc += 1
        self.punkty += 1


class Jablko():
    def __init__(self):
        self.pozycja = (0, 0)
        self.kolor = (255, 0, 0)
        self.pozycja_Losowa()

    def pozycja_Losowa(self):
        self.pozycja = (random.randint(0, szerokosc_Kratki - 1) * rozmiar_Kratki, random.randint(0, wysokosc_Kratki - 1) * rozmiar_Kratki)

    def rysuj(self, okno_Gry):
        r = pygame.Rect((self.pozycja[0], self.pozycja[1]), (rozmiar_Kratki, rozmiar_Kratki))
        pygame.draw.rect(okno_Gry, self.kolor, r)



def rysowanieSiatki(surface):
    # Linia pozioma
    surface.fill((0, 0, 0))
    for i in range(0, int(szerokosc_Kratki)):
        pygame.draw.line(surface, (128, 128, 128), (0 , i * rozmiar_Kratki), (szerokosc_Okna, i * rozmiar_Kratki))
    # vertical lines
    for j in range(0, int(wysokosc_Kratki)):
        pygame.draw.line(surface, (128, 128, 128), (j * rozmiar_Kratki, 0), (j * rozmiar_Kratki, wysokosc_Okna))

def main():
    pygame.init()
    # Inicjalizacja okna gry
    okno_Gry= pygame.display.set_mode((szerokosc_Okna, wysokosc_Okna), 0, 32)
    pygame.display.set_caption("SNAKE")
    # Wyrasowanie siatki
    rysowanieSiatki(okno_Gry)
    # Inicjalizacja obiektów klas
    snake = Snake()
    jablko = Jablko()
    czcionka = pygame.font.SysFont('comicsans', 30)
    run = True
    while (run):
        pygame.time.delay(100)
        # Wyłączenie gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Sterowanie do Snake'a
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.kierunek(gora)
                elif event.key == pygame.K_DOWN:
                    snake.kierunek(dol)
                elif event.key == pygame.K_LEFT:
                    snake.kierunek(lewo)
                elif event.key == pygame.K_RIGHT:
                    snake.kierunek(prawo)
        snake.ruch()
        if snake.pozycja_Glowy() == jablko.pozycja:
            snake.zjedzenie()
            jablko.pozycja_Losowa()
        rysowanieSiatki(okno_Gry)
        snake.rysowanie(okno_Gry)
        jablko.rysuj(okno_Gry)
        okno_Gry.blit(okno_Gry, (0, 0))
        wynik = czcionka.render("Punkty {0}".format(snake.punkty), 1, (255, 255, 0))
        okno_Gry.blit(wynik, (5, 10))
        pygame.display.update()

main()
