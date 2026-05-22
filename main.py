import time
import os
import subprocess
import json
import random
import turtle

# Odpowiada za przechowywanie parametrów gracza oraz jego pojazdu + powoduje przemieszczenie łazika
class Lazik():
    def __init__(self):
        self.imie = ""
        self.nazwa_pojazdu = ""
        self.x = 0
        self.y = 0
        self.kat = 0
        self.paliwo = 0
        self.energia = 0
        self.znalezione_krysztaly = 0
        self.znalezione_oznaki_zycia = 0
        self.kierunek_geograficzny = ""
        self.liczba_ruchow = 0
        self.nazwa_wyprawy = ""
        self.poziom_radiacji = 0
        self.pole_radiacji = ""
        self.poczatkowy_x = 0
        self.poczatkowy_y = 0
        self.poczatkowy_kat = 0
        self.poczatkowa_energia = 0
        self.poczatkowe_paliwo = 0

    def przemieszczenie_lazika(self, kierunek, obiekt_mapy):
        nowa_pozycja_x = self.x
        nowa_pozycja_y = self.y
        nowy_kierunek = self.kat
        nowy_kierunek_geo = self.kierunek_geograficzny

        if kierunek == "l":
            nowy_kierunek = 270
            nowy_kierunek_geo = "zachód"
            nowa_pozycja_x -= 1
        elif kierunek == "p":
            nowy_kierunek = 90
            nowy_kierunek_geo = "wschód"
            nowa_pozycja_x += 1
        elif kierunek == "g":
            nowy_kierunek = 0
            nowy_kierunek_geo = "północ"
            nowa_pozycja_y += 1
        elif kierunek == "d":
            nowy_kierunek = 180
            nowy_kierunek_geo = "południe"
            nowa_pozycja_y -= 1

        if obiekt_mapy.czy_przeszkoda(nowa_pozycja_x, nowa_pozycja_y):
            return False

        if  nowa_pozycja_x < obiekt_mapy.minimalna_pozycja_x or nowa_pozycja_x > obiekt_mapy.maksymalna_pozycja_x:
            return False

        if  nowa_pozycja_y < obiekt_mapy.minimalna_pozycja_y or nowa_pozycja_y > obiekt_mapy.maksymalna_pozycja_y:
            return False

        self.x = nowa_pozycja_x
        self.y = nowa_pozycja_y
        self.kat = nowy_kierunek
        self.kierunek_geograficzny = nowy_kierunek_geo
        return True

class Mapa():
    def __init__(self):
        self.pozycje_przeszkod = []
        self.pozycje_krysztalow = []
        self.pozycje_oznak_zycia = []
        self.pozycje_promieniowania = []
        self.pozycje_cywilizacji = []
        self.maksymalna_pozycja_x = 50
        self.maksymalna_pozycja_y = 50
        self.minimalna_pozycja_x = 0
        self.minimalna_pozycja_y = 0

    # Sprawdza czy koło gracza jest przeszkoda jeśli tak to gracz musi wpisać inny kierunek ruchu
    def czy_przeszkoda(self, x, y):
        for przeszkoda in self.pozycje_przeszkod:
            if x == przeszkoda[1] and y == przeszkoda[2]:
                print(f"Przeszkoda typu: {przeszkoda[0]} na x = {przeszkoda[1]} i y = {przeszkoda[2]}. W miejscu nowego ruchu!")
                print("Oprogramowanie łazika nie pozwala na taki ruch! Spróbuj ponownie :)")
                time.sleep(2)
                return True
        return False

    # Wczytuje dane mapy i ważnych punktów z pliku mapa.json
    # Później zmienia odczytane dane na bardziej przystępną formę podwójnej listy
    def zaladuj_mape(self):
        try:
            with open('mapa.json', 'r') as plik:
                dane_json = json.load(plik)
        except FileNotFoundError:
            print("Nie znaleziono pliku mapa.json!")
            exit()

        pozycje_promieniowania_nieuporzadkowane = dane_json["strefy_promieniowania"]
        self.pozycje_promieniowania.clear()

        for strefa in pozycje_promieniowania_nieuporzadkowane:
            nazwa_poziomu = strefa["poziom"]
            x_pocz = strefa["x_pocz"]
            y_pocz = strefa["y_pocz"]
            x_konc = strefa["x_konc"]
            y_konc = strefa["y_konc"]
            self.pozycje_promieniowania.append([nazwa_poziomu, x_pocz, y_pocz, x_konc, y_konc])

        pozycje_krysztalow_nieuporzadkowane = dane_json["krysztaly"]
        self.pozycje_krysztalow.clear()

        for krysztal in pozycje_krysztalow_nieuporzadkowane:
            typ = krysztal["typ"]
            komentarz = krysztal["komentarz"]
            x = krysztal["x"]
            y = krysztal["y"]
            self.pozycje_krysztalow.append([typ, komentarz, x, y])

        pozycje_przeszkod_nieuporzadkowane = dane_json["przeszkody"]
        self.pozycje_przeszkod.clear()

        for przeszkoda in pozycje_przeszkod_nieuporzadkowane:
            typ = przeszkoda["typ"]
            x = przeszkoda["x"]
            y = przeszkoda["y"]
            self.pozycje_przeszkod.append([typ, x, y])

        pozycje_oznak_zycia_nieuporzadkowane = dane_json["oznaki_zycia"]
        self.pozycje_oznak_zycia.clear()

        for oznaka_zycia in pozycje_oznak_zycia_nieuporzadkowane:
            typ = oznaka_zycia["typ"]
            komentarz = oznaka_zycia["komentarz"]
            x = oznaka_zycia["x"]
            y = oznaka_zycia["y"]
            self.pozycje_oznak_zycia.append([typ, komentarz, x, y])

        self.pozycja_starozytnej_cywilizacji = [dane_json["stara_cywlizacja"][0], dane_json["stara_cywlizacja"][1]]

class Radar():
    def __init__(self):
        self.zasieg = 6

    # Rysuje kluczowe punkty podczas rozrywki
    def narysuj_obiekt(self, x, y, zolwik, przesuniecie, skala, kolor):
            zolwik.penup()
            zolwik.pencolor(kolor)
            zolwik.goto((x + przesuniecie)*skala, (y + przesuniecie)*skala)
            zolwik.pendown()
            zolwik.pensize(5)
            zolwik.goto((x + przesuniecie)*skala, (y + przesuniecie)*skala)
            zolwik.penup()

    # Wyszukuje najbliższe pole radiacji w obrębie gracza
    def najblizsza_radiacja(self, obiekt_mapa, obiekt_lazik):
        for poziom, x_pocz, y_pocz,x_konc, y_konc in obiekt_mapa.pozycje_promieniowania:
            if poziom == obiekt_lazik.pole_radiacji: continue

            warunek_dla_x = (x_pocz - self.zasieg <= obiekt_lazik.x) and (x_konc + self.zasieg >= obiekt_lazik.x)
            warunek_dla_y = (y_pocz - self.zasieg <= obiekt_lazik.y) and (y_konc + self.zasieg >= obiekt_lazik.y)

            if warunek_dla_x and warunek_dla_y:
                print(f"[SYSTEM] Uwaga! W odległości do {self.zasieg} pól wykryto strefę: {poziom} promieniowanie!")
                time.sleep(1.5)
                break

    # Wyszukuje x kryształów najbliższych graczowi
    def najblizsze_krysztaly(self, obiekt_mapa, obiekt_lazik, zolwik, przesuniecie, skala):
        znaleziono = 0
        for typ, komentarz, x, y in obiekt_mapa.pozycje_krysztalow:
            odleglosc_x = abs(x - obiekt_lazik.x)
            odleglosc_y = abs(y - obiekt_lazik.y)
            if odleglosc_x <= self.zasieg and odleglosc_y <= self.zasieg:
                znaleziono = znaleziono + 1
                self.narysuj_obiekt(x, y, zolwik, przesuniecie, skala, "purple")
                print(f"[RADAR] wykrył nieznany minerał x = {x}, y = {y}")
        if znaleziono > 0:
            time.sleep(2)

    # Wyszukuje x oznak życia blisko gracza
    def najblizsze_oznaki_zycia(self, obiekt_mapa, obiekt_lazik, zolwik, przesuniecie, skala):
        for typ, komentarz, x, y in obiekt_mapa.pozycje_oznak_zycia:
            if obiekt_lazik.x == x and obiekt_lazik.y == y:
                continue
            
            warunek_dla_x = (obiekt_lazik.x >= x - self.zasieg) and (obiekt_lazik.x <= x + self.zasieg)
            warunek_dla_y = (obiekt_lazik.y >= y - self.zasieg) and (obiekt_lazik.y <= y + self.zasieg)

            if warunek_dla_x and warunek_dla_y:
                self.narysuj_obiekt(x, y, zolwik, przesuniecie, skala, "green")
                print(f"[RADAR] Wykryto anomalię biologiczną! Znajduje się na x = {x}, y = {y}")
                time.sleep(2)
                break

class Gra():
    def __init__(self):
        self.uruchomiona = False
        self.mapa_swiata = None
        self.aktywny_lazik = None
        self.radar = None
        self.zolwik = turtle.Turtle()
        self.skala = 10
        self.przesuniecie = -25
        self.mozliwe_kierunki = ["l", "p", "g", "d"]
        self.uruchomiony = True
        self.poczatek = True
        self.pozycja_x_przed =  0
        self.pozycja_y_przed = 0
        self.energia_przed = 0
        self.paliwo_przed = 0
        self.energia_min = 100
        self.paliwo_min = 100
        self.energia_max = 200
        self.paliwo_max = 200
        self.odejmowane_paliwo = 1
        self.wspolczynnik_odejmowania_energi = 0.1

    def powitanie(self):
        print("|----------------------------|")
        print("|        WITAJ W GRZE        |")
        print("|        NOWA EUROPA         |")
        print("|----------------------------|")
        print("|    Autor Eryk Goraj ^-^    |")
        time.sleep(3)
        self.wyczysc_konsole()
    
    # Usuwa wcześniejsze komunikaty w konsoli by zachować przejrzystość
    def wyczysc_konsole(self):
        cmd = ""
        if os.name == "nt":
            cmd = "cls"
        else:
            cmd = "clear"
        subprocess.call(cmd, shell=True)

    # Funkcja pomocniczas do narysuj mape odpowiada za narysowanie obramówki mapy i pól radiacji
    def narysuj_pole(self, kolor, x_min, y_min, x_max, y_max, wypelnienie):
        if wypelnienie:
            self.zolwik.fillcolor(kolor)
            self.zolwik.begin_fill()

        self.zolwik.pencolor(kolor)
        self.zolwik.penup()
        self.zolwik.goto((x_min + self.przesuniecie) * self.skala, (y_min + self.przesuniecie) * self.skala)
        self.zolwik.pendown()
        self.zolwik.goto((x_max + self.przesuniecie) * self.skala, (y_min + self.przesuniecie) * self.skala)
        self.zolwik.goto((x_max + self.przesuniecie) * self.skala, (y_max + self.przesuniecie) * self.skala)
        self.zolwik.goto((x_min + self.przesuniecie) * self.skala, (y_max + self.przesuniecie) * self.skala)
        self.zolwik.goto((x_min + self.przesuniecie) * self.skala, (y_min + self.przesuniecie) * self.skala)
        if wypelnienie:
            self.zolwik.end_fill()

    # Rysuje mapę
    def narysuj_mape(self):
        self.przesuniecie = -25
        self.zolwik.pensize(1)
        self.narysuj_pole("red", 0, 0, 50, 50, True)
        self.narysuj_pole("pink", 5, 5, 45, 45, True)
        self.narysuj_pole("yellow", 15, 15, 35, 35, True)
        self.narysuj_pole("blue", 20, 20, 30, 30, True)
        self.zolwik.pensize(5)
        self.narysuj_pole("black", 0, 0, 50, 50, False)
        self.zolwik.pensize(3)

    # Startowe wprowadzenie danych przez gracza
    def wprowadz_dane(self, obiekt_lazik):
        obiekt_lazik.x = 0
        obiekt_lazik.y = 0

        self.zolwik.hideturtle()
        self.narysuj_mape()

        print("[SYSTEM] Nierozpoznano profilu kierowcy i pojazdu...")
        time.sleep(2)
        self.wyczysc_konsole()
        print("[SYSTEM] Uzupełnij dane kierowcy")
        print("[SYSTEM] Podaj swoje imię:")
        gracz_imie = input("> ")
        obiekt_lazik.imie = gracz_imie
        print(f"[SYSTEM] Witaj {gracz_imie}!")
        time.sleep(2)
        print("[SYSTEM] Nazwa wyprawy #ERROR404\n")
        print("[SYSTEM] Podaj nazwę wyprawy:")
        nazwa_wyprawy = input("> ")
        obiekt_lazik.nazwa_wyprawy = nazwa_wyprawy
        print(f"[SYSTEM] Wyprawa o nazwie {nazwa_wyprawy} uznaję za rozpoczętą!")
        input("[NACIŚNIJ ENTER BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()
        print("[SYSTEM] Wykryto problem z odczytu parametrów zasobów łazika XXXX\n")
        time.sleep(2)
        print("[SYSTEM] Brak nazwy pojazdu")
        time.sleep(2)
        self.wyczysc_konsole()
        print("[SYSTEM] Uzupełnij dane pojazdu\n")
        print("[SYSTEM] Podaj nazwę pojazdu:")
        pojazd_nazwa = input("> ")
        obiekt_lazik.nazwa_pojazdu = pojazd_nazwa
        print("[SYSTEM] Wprowadź parametry zasobów pojazdu (łazika), kontrolki znajdują się przy panelu sterowania pojazdu.\n")

        print(f"[SYSTEM] Podaj ilość energi w przedziale ({self.energia_min}, {self.energia_max}):")
        while True:
            try:
                dane_energia = int(input("> "))
                if self.energia_min < dane_energia < self.energia_max:
                    obiekt_lazik.energia = dane_energia
                    obiekt_lazik.poczatkowa_energia = dane_energia
                    break
                else:
                    print(f"Liczba spoza przedziału! Podaj wartość między {self.energia_min} a {self.energia_max}.")
            except ValueError:
                print("Niepoprawny typ wproawdzonych danych")
                time.sleep(1)

        print(f"[SYSTEM] Podaj ilość paliwa w przedziale ({self.paliwo_min}, {self.paliwo_max}):")
        while True:
            try:
                dane_paliwo = int(input("> "))
                if self.paliwo_min < dane_paliwo < self.paliwo_max:
                    obiekt_lazik.paliwo = dane_paliwo
                    obiekt_lazik.poczatkowe_paliwo = dane_paliwo
                    break
                else:
                    print(f"Liczba spoza przedziału! Podaj wartość między {self.paliwo_min} a {self.paliwo_max}.")
            except ValueError:
                print("Niepoprawny typ wproawdzonych danych")
                time.sleep(1)
        
        self.wyczysc_konsole()
        print(f"[SYSTEM] Profil pojazdu: \nNazwa pojazdu - {obiekt_lazik.nazwa_pojazdu}\nZawartość energi w akumulatorach - {obiekt_lazik.energia}kAh\nZawartość paliwa - {obiekt_lazik.paliwo}L")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()
        print("[SYSTEM] Po dokonaniu analizy podłoża, możliwy zakres ruchu w planszy 50x50. Jednak końcowa sfera ma bardzo wysokie promieniowanie.\n")
        print(f"[SYSTEM] Wybierz miejsce zrzutu! Teren nadający się do lądowania w przedziałach x(20, 30) y(20, 30)")

        while True:
            try:
                dane_x = int(input("[x]> "))
                if 20 < dane_x < 30:
                    obiekt_lazik.poczatkowy_x = dane_x
                    obiekt_lazik.x = obiekt_lazik.poczatkowy_x
                    break
                else:
                    print("Liczba powinna mieścić się w przedziale (20, 30)")
            except ValueError:
                print("Niepoprawny typ wproawdzonych danych")
                time.sleep(1)

        while True:
            try:
                dane_y = int(input("[y]> "))
                if 20 < dane_y < 30:
                    obiekt_lazik.poczatkowy_y = dane_y
                    obiekt_lazik.y = obiekt_lazik.poczatkowy_y
                    break
                else:
                    print("Liczba powinna mieścić się w przedziale (20, 30)")
            except ValueError:
                print("Niepoprawny typ wproawdzonych danych")
                time.sleep(1)

        self.wyczysc_konsole()
        print(f"[SYSTEM] Wybierz początkowy kierunek ruchu! (G - północ, D - południe, L - zachód, P - wschód)")
        self.zolwik.penup()
        self.zolwik.goto((obiekt_lazik.x + self.przesuniecie)*self.skala, (obiekt_lazik.y+self.przesuniecie)*self.skala)
        self.zolwik.pendown()
        self.zolwik.pencolor("black")

        print("[SYSTEM] Wprowadź kierunek:")
        while True:
            poczatkowy_kierunek_ruchu = input("> ")
            poczatkowy_kierunek_ruchu = poczatkowy_kierunek_ruchu.lower()
            if poczatkowy_kierunek_ruchu in self.mozliwe_kierunki:
                break

        if poczatkowy_kierunek_ruchu == "l":
            obiekt_lazik.kierunek_geograficzny = "zachód"
            obiekt_lazik.kat = 270
        elif poczatkowy_kierunek_ruchu == "p":
            obiekt_lazik.kierunek_geograficzny = "wschód"
            obiekt_lazik.kat = 90
        elif poczatkowy_kierunek_ruchu == "g":
            obiekt_lazik.kierunek_geograficzny = "północ"
            obiekt_lazik.kat = 0
        elif poczatkowy_kierunek_ruchu == "d":
            obiekt_lazik.kierunek_geograficzny = "południe"
            obiekt_lazik.kat = 180

        obiekt_lazik.poczatkowy_kat = obiekt_lazik.kat

        print(f"[SYSTEM] Wybrano {obiekt_lazik.kierunek_geograficzny}!")
        self.zolwik.dot(10, "slateblue")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()
        
        print(f"|==================== WPROWADZONA KONFIGURACJA ====================|")
        print(f" - Granice świata: X od 0 do 50, Y od 0 do 50")
        print(f" - Warunki do zaliczenia misji:")
        print(f"        Zebranie 6 minerałów")
        print(f"        Odkrycie 3 oznak życia")
        print(f"        Znalezienie pozostałości starożytnej cywilizacji")
        print(f" - Imię kierowcy: {obiekt_lazik.imie}")
        print(f" - Nazwa wyprawy: {obiekt_lazik.nazwa_wyprawy}")
        print(f" - Początkowa orientacja:")
        print(f"        Pozycja: X[{obiekt_lazik.poczatkowy_x}] Y[{obiekt_lazik.poczatkowy_y}] ")
        print(f"        Kąt: {obiekt_lazik.poczatkowy_kat} stopni")
        print(f" - Początkowe zasoby:")
        print(f"        Paliwo: {obiekt_lazik.poczatkowe_paliwo} [L]")
        print(f"        Energia: {obiekt_lazik.poczatkowa_energia} [kAh]")
        print(f"|========================= -------------- =========================|") 
        
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()

        print("[SYSTEM] Ktoś próbuje nawiązać z tobą połączenie na kanale 13...")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()
    
    # Tajne zakończenie
    def znalezienie_starozytnej_cywilizacji(self, obiekt_lazik):
        print("(ty) Hmmm co to może być...")
        time.sleep(2)
        print("(ty) Spróbuje oczyścić ten kawałek metalu sprężonym powietrzem.")
        time.sleep(2)
        print("*Używasz dmuchawki sprężonego powietrza")
        time.sleep(2)
        print("(ty) To wygląda jak wejście... Wejście do statku kosmicznego!")
        time.sleep(2)
        print("*Przykładasz magnes do stalowego panelu. Drzwi się otwierają")
        time.sleep(2)
        print("Po zwiedzeniu całego statku możesz być pewny że to pradawny statek, który miał na celu kolonizacje tych terenow.")
        time.sleep(2)
        print("Zapewne poprzez silne pole grawitacyjne Jowisza oraz pasma asteroid uszkodził im się tylni kadłub.")
        time.sleep(2)
        print("Znajdujesz dziwne szkielety chitynowe postaci")
        time.sleep(2)
        print("Zawiadamiasz dowodctwo, ktore przysyla ci wsparcie...")
        time.sleep(2)
        print("Teraz wszyscy doceniaja twoje zaslugi...")
        time.sleep(2)
        print("OTO POCZĄTEK NOWEJ ERY LUDZKOSCI - PODRÓŻE MIĘDZY GALAKTYKAMI")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.wyczysc_konsole()
        self.podsumowanie(obiekt_lazik, "Znalazłeś starożytną cywilizacje!")
    
    # Wydarzenia losow czyli w kodzie burza słoneczna i wyciek paliwa
    def wydarzenie_losowe(self, nazwa, opis):
        wylosowana = random.randint(1, 12)
        if wylosowana == 1:
            utracony_zasob = random.randint(0, 10)
            print(f"Tracisz {utracony_zasob} {nazwa}! Przez {opis}...")
            time.sleep(2)
            return utracony_zasob
        return 0

    # Sprawdza czy gracz znajduje się na polu z jakimś kryształem/oznaką życia/polem pozostałości starożytnej cywilizacji
    def gracz_znalazl(self, obiekt_mapa, obiekt_lazik):

        for krysztal in obiekt_mapa.pozycje_krysztalow[:]:
            typ, komentarz, x, y = krysztal
            if obiekt_lazik.x == x and obiekt_lazik.y == y:
                obiekt_mapa.pozycje_krysztalow.remove(krysztal)
                obiekt_lazik.znalezione_krysztaly += 1
                print(f"Wow znalazłeś {typ}!")
                print(f"- {komentarz}")
                input("[NACIŚNIJ ENTER BY KONTYNUOWAĆ]> ")

        for oznaka_zycia in obiekt_mapa.pozycje_oznak_zycia[:]:
            typ, komentarz, x, y = oznaka_zycia

            if obiekt_lazik.x == x and obiekt_lazik.y == y:
                obiekt_mapa.pozycje_oznak_zycia.remove(oznaka_zycia)
                obiekt_lazik.znalezione_oznaki_zycia += 1
                print(f"Wow znalazłeś {typ}!")
                print(f"- {komentarz}")
                print("ZNAJDUJESZ SIĘ BLISKO KOMINA HYDROTERMALNEGO I OTRZYMUJESZ +20 PALIWA i +10 ENERGII!")
                print("Energię otrzymujesz z przemiany ciepła a paliwo z poboru i przetworzenia metanu zawartego w lodzie!")
                obiekt_lazik.energia += 10
                obiekt_lazik.paliwo += 20
                input("[NACIŚNIJ ENTER BY KONTYNUOWAĆ]> ")

        if obiekt_lazik.znalezione_krysztaly == 6:
            self.podsumowanie(obiekt_lazik, "Znalazłeś wszystkie kryształy!")
            return True
        elif obiekt_lazik.znalezione_oznaki_zycia == 3:
            self.podsumowanie(obiekt_lazik, "Znalazłeś wszystkie oznaki życia!")
            return True

        if obiekt_mapa.pozycja_starozytnej_cywilizacji and obiekt_lazik.x == obiekt_mapa.pozycja_starozytnej_cywilizacji[0] and obiekt_lazik.y == obiekt_mapa.pozycja_starozytnej_cywilizacji[1]:
            self.znalezienie_starozytnej_cywilizacji(obiekt_lazik)
            return True
        return False

    # Podsumowuje całą grę, czyli co udało się graczowi osiągnąć
    def podsumowanie(self, obiekt_lazik, wiadomosc):
            self.wyczysc_konsole()
            self.zolwik.dot(12, "moccasin")
            print(f"|============= STATYSTYKI GRY =============|")
            print(f" - Ukończono grę w {obiekt_lazik.liczba_ruchow} ruchach!")
            print(f" - Nazwa wyprawy: {obiekt_lazik.nazwa_wyprawy}")
            print(f" - Początkowa orientacja:")
            print(f"        Pozycja: X[{obiekt_lazik.poczatkowy_x}] Y[{obiekt_lazik.poczatkowy_y}] ")
            print(f"        Kąt: {obiekt_lazik.poczatkowy_kat} stopni")
            print(f" - Początkowe zasoby:")
            print(f"        Paliwo: {obiekt_lazik.poczatkowe_paliwo} [L]")
            print(f"        Energia: {obiekt_lazik.poczatkowa_energia} [kAh]")
            print(f" - Końcowa orientacja:")
            print(f"        Pozycja: X[{obiekt_lazik.x}] Y[{obiekt_lazik.y}] ")
            print(f"        Kąt: {obiekt_lazik.kat} stopni")
            print(f" - Końcowe zasoby:")
            print(f"        Paliwo: {obiekt_lazik.paliwo} [L]")
            print(f"        Energia: {obiekt_lazik.energia} [kAh]")
            print(f" - Typ zakończenia:")
            print(f"        {wiadomosc}")
            print(f"|============= -------------- =============|")

            decyzja = input("T - by zagrać ponownie | Inny klawisz by skończyć: ")
            if decyzja.lower() == "t":
                self.poczatek = True
                return
            self.uruchomiony = False

    # Odczytuje radiacje z miejsca w którym znajduje się gracz i zwiększa jego poziom radiacji
    def odczyt_radiacji(self, obiekt_mapa, obiekt_lazik):
        radiacja = self.sprawdz_pole(obiekt_mapa, obiekt_lazik)

        if radiacja == "średnie":
            obiekt_lazik.poziom_radiacji = 20
        elif radiacja == "wysokie":
            obiekt_lazik.poziom_radiacji = 50
        elif radiacja == "bardzo wysokie":
            self.wpadniecie_pod_lod(obiekt_lazik, "Wjechałeś na teren, cienkiego lodu! PRZEGYRWASZ")
        else:
            obiekt_lazik.poziom_radiacji = 0

    # Zakończenie w którym gracz wpada pod lód
    def wpadniecie_pod_lod(self, obiekt_lazik, wiadomosc):
        print("(ty) Mejdej, mejdej! Łazik wpadł pod pokrywę lodową, schodzę na dno zbiornika.")
        time.sleep(2)
        print("(ty) Halo! Słyszy mnie ktoś?")
        time.sleep(2)
        print("(???) U###- Br**# Sygna#")
        time.sleep(2)
        print("(ty) Ahh! Pokrywa lodowa blokuje fale elektromagnetyczne!\n")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")
        self.poczatek = True
        self.podsumowanie(obiekt_lazik, wiadomosc)

    # Wstawka fabularna
    def poczatek_gry(self):
        print("(???) Halo... tu Tomasz Głaz. Słyszysz mnie?")
        time.sleep(2)
        print("(Ty) Tak głośno i wyraźnie!")
        time.sleep(2)
        print("(Tomasz Głaz) Ahh całe sczęście, obawialiśmy się, że będzie problem z łącznością\nprzez promieniowanie jowisza!")
        time.sleep(2)
        print("(Tomasz Głaz) Na twoim pulpicie powinny się pojawić zadania.")
        time.sleep(2)
        print("(Tomasz Głaz) Twoim głównym celem jest odnalezienie 6 rzadkich minerałów lub 3 oznak życia.")
        time.sleep(2)
        print("(Tomasz Głaz) Powodzenia, jakby coś się działo zgłoś to!")
        time.sleep(2)
        print("(Ty) Trzymaj się!")
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")

    # Wyświetla statystyki na początku tury
    def statystyki_gracza(self, obiekt_lazik):
        print("|===========| OGÓLNE INFORMACJE |===========|")
        print(f"| Aktualny ruch = {obiekt_lazik.liczba_ruchow + 1}")
        print(f"| Aktualna pozycja = x[{obiekt_lazik.x}] y[{obiekt_lazik.y}]")
        print(f"| Aktualny kierunek = {obiekt_lazik.kierunek_geograficzny}")
        print("|")
        print(f"| Stan paliwa = {obiekt_lazik.paliwo}L")
        print(f"| Stan energi = {obiekt_lazik.energia}kAh")
        print("|")
        print(f"| Znalezione kryształy = {obiekt_lazik.znalezione_krysztaly}/6")
        print(f"| Znalezione oznaki życia = {obiekt_lazik.znalezione_oznaki_zycia}/3")
        print("|===========================================|")

    # Wyświetla statystyki końcowe tury
    def podsumowanie_tury(self, obiekt_lazik):
        print("|===========| PODSUMOWANIE TURY |===========|")
        print(f"| Pozycja: przed -> [{self.pozycja_x_przed},{self.pozycja_y_przed}] po -> [{obiekt_lazik.x},{obiekt_lazik.y}]")
        print(f"| Stan paliwa: przed -> {self.paliwo_przed} po -> {obiekt_lazik.paliwo} [L]")
        print(f"| Stan energi: przed -> {self.energia_przed} po -> {obiekt_lazik.energia} [kAh]")
        print("|===========================================|")

    # Odpowiada za najważniejszą część gry
    # Przemieszczenie, wyszukiwanie obiektów, nakładanie na gracza kar lub zysków
    def kolejny_ruch(self, obiekt_mapa, obiekt_lazik, obiekt_radar):
        if self.poczatek == True:
            return 
        self.odczyt_radiacji(obiekt_mapa, obiekt_lazik)

        self.pozycja_x_przed = obiekt_lazik.x
        self.pozycja_y_przed = obiekt_lazik.y
        self.energia_przed = obiekt_lazik.energia
        self.paliwo_przed = obiekt_lazik.paliwo

        obiekt_lazik.energia -= int((obiekt_lazik.poziom_radiacji * self.wspolczynnik_odejmowania_energi) // 2)
        obiekt_lazik.poziom_radiacji -= 0.5
        if obiekt_lazik.poziom_radiacji < 0:
            obiekt_lazik.poziom_radiacji = 0


        if obiekt_lazik.energia <= 0:
            print("[SYSTEM] Cała energia przepadła na znegowanie efektu promieniowania!")
            self.wpadniecie_pod_lod(obiekt_lazik, "Łazik stracił całą energię przez promieniowanie! PRZEGRYWASZ")
            return
        
        self.statystyki_gracza(obiekt_lazik)
        
        print("Wpisz L aby poruszyć się o jedno pole w lewo, P o jedno w prawo, G o jedno w górę i D o jedno w dół")
        kierunek_ruchu = input("> ")
        kierunek_ruchu = kierunek_ruchu.lower()
        print("|===========| AKCJA UŻYTKOWNIKA |===========|")
        print(f"> ~Wybrany kierunek ruchu: {kierunek_ruchu}")

        if kierunek_ruchu not in self.mozliwe_kierunki and kierunek_ruchu not in ["cheat", "zak_wsz_krsz", "zak_wsz_zyc", "zak_zn_cyw"]:
            print("Złe dane!")
            time.sleep(2)
            return
        elif kierunek_ruchu == "cheat":
            obiekt_lazik.x = 0
            obiekt_lazik.y =0 

            print(f"[SYSTEM/CHEAT] Wybierz miejsce pojazdu... x,y[0, 50]")
            while True:
                try:
                    dane_x = int(input("[x]> "))
                    if 0 <= dane_x <= 50:
                        obiekt_lazik.x = dane_x
                        obiekt_lazik.poczatkowy_x = dane_x
                        break
                    else:
                        print("Liczba powinna mieścić się w przedziale [0, 50]")
                except ValueError:
                    print("Niepoprawny typ wproawdzonych danych")
                    time.sleep(1)

            while True:
                try:
                    dane_y = int(input("[y]> "))
                    if 0 <= dane_y <= 50:
                        obiekt_lazik.y = dane_y
                        obiekt_lazik.poczatkowy_y = dane_y
                        break
                    else:
                        print("Liczba powinna mieścić się w przedziale [0, 50]")
                except ValueError:
                    print("Niepoprawny typ wproawdzonych danych")
                    time.sleep(1)

            self.zolwik.penup()
            self.zolwik.goto((obiekt_lazik.x + self.przesuniecie)*self.skala, (obiekt_lazik.y + self.przesuniecie)*self.skala)
            return


        elif kierunek_ruchu == "zak_wsz_krsz":
            obiekt_lazik.znalezione_krysztaly = 6
            self.podsumowanie(obiekt_lazik, "Znalazłeś wszystkie kryształy!")
            self.poczatek = True
            return
        elif kierunek_ruchu == "zak_wsz_zyc":
            obiekt_lazik.znalezione_oznaki_zycia = 3
            self.podsumowanie(obiekt_lazik, "Znalazłeś wszystkie oznaki życia!")
            self.poczatek = True
            return
        elif kierunek_ruchu == "zak_zn_cyw":
            self.znalezienie_starozytnej_cywilizacji(obiekt_lazik)
            self.poczatek = True
            return

        if not obiekt_lazik.przemieszczenie_lazika(kierunek_ruchu, obiekt_mapa):
            return
            
        time.sleep(1)

        print("")
        print(f"> ~Nowa pozycja = x:{obiekt_lazik.x} y:{obiekt_lazik.y}")
        print("|===========================================|")
        time.sleep(2)
        self.wyczysc_konsole()

        if (self.gracz_znalazl(obiekt_mapa, obiekt_lazik)):
            return

        time.sleep(2)
        self.wyczysc_konsole()
        obiekt_radar.najblizsza_radiacja(obiekt_mapa, obiekt_lazik)
        obiekt_radar.najblizsze_krysztaly(obiekt_mapa, obiekt_lazik, self.zolwik, self.przesuniecie, self.skala)
        obiekt_radar.najblizsze_oznaki_zycia(obiekt_mapa, obiekt_lazik, self.zolwik, self.przesuniecie, self.skala)
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")

        obiekt_lazik.liczba_ruchow += 1
        obiekt_lazik.paliwo -= self.odejmowane_paliwo
        obiekt_lazik.energia -= self.wydarzenie_losowe("energii", "burzą słoneczną")
        obiekt_lazik.paliwo -= self.wydarzenie_losowe("paliwa", "wyciekiem ze zbiornika paliwa")

        if obiekt_lazik.paliwo <= 0:
            print("[SYSTEM] Oj! Skończyło Ci się paliwo!")
            self.wpadniecie_pod_lod(obiekt_lazik, "Straciłeś paliwo, zbyt długo stoisz w jednym miejscu! PRZEGYRWASZ")
            return

        if obiekt_lazik.energia <= 0:
            print("[SYSTEM] Cała energia przepadła na znegowanie efektu promieniowania!")
            self.wpadniecie_pod_lod(obiekt_lazik, "Łazik stracił całą energię przez promieniowanie! PRZEGRYWASZ")
            return

        self.zolwik.penup()
        self.zolwik.goto((self.pozycja_x_przed + self.przesuniecie)*self.skala, (self.pozycja_y_przed + self.przesuniecie)*self.skala)
        self.narysuj_lazik(obiekt_lazik.x, obiekt_lazik.y)
        time.sleep(2)
        self.wyczysc_konsole()
        self.podsumowanie_tury(obiekt_lazik)
        input("[NACIŚNIJ DOWOLNY KLAWISZ BY KONTYNUOWAĆ]> ")

    def narysuj_lazik(self, x, y):
        self.zolwik.pendown()
        self.zolwik.color("black")
        self.zolwik.goto((x + self.przesuniecie)*self.skala, (y+self.przesuniecie)*self.skala)
        self.zolwik.penup()

    # Funkcja pomocnicza do odczyt_radiacji()
    def sprawdz_pole(self, obiekt_mapa, obiekt_lazik):
        obiekt_lazik.pole_radiacji = "niskie"
        for poziom, x_pocz, y_pocz, x_konc, y_konc in reversed(obiekt_mapa.pozycje_promieniowania):
            if (obiekt_lazik.x >= x_pocz and obiekt_lazik.y >= y_pocz) and (obiekt_lazik.x <= x_konc and obiekt_lazik.y <= y_konc):
                obiekt_lazik.pole_radiacji = poziom
                return(poziom)
        return "niskie"

gra = Gra()
mapa = Mapa()
lazik = Lazik()
radar = Radar()

while gra.uruchomiony:
    if gra.poczatek == True:
        gra.zolwik.clear()
        gra.mapa_swiata = Mapa()
        gra.aktywny_lazik = Lazik()
        gra.radar = Radar()

        gra.zolwik.clear()
        gra.wyczysc_konsole()
        gra.powitanie()
        gra.mapa_swiata.zaladuj_mape()
        gra.wprowadz_dane(gra.aktywny_lazik)
        gra.poczatek_gry()
        gra.poczatek = False
    
    gra.wyczysc_konsole()
    gra.kolejny_ruch(gra.mapa_swiata, gra.aktywny_lazik, gra.radar)
