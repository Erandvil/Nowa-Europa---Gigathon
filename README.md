# NOWA EUROPA - GIGATHON 2026

## Generalny opis
Jesteś badaczem kosmicznym. Twoim zadaniem jest odnalezienie 8 minerałów i zebranie z nich próbek.
Możesz równiesz znaleźć 3 oznaki życia albo fragmenty statku starożytnej cywilizacji!

Poruszasz się w dwuwymiarowej przestrzeni wprowadzając kierunek: góra, dół, lewo, prawo.
Później wprowadzony przez ciebie kierunek jest zamieniany na kąt jaki stanowisz względem mapy.

Po wykonaniu ruchu zmieniają się pewne zmienne:
    - Zwiększa się poziom napromieniowania łazika (gdy znajdujesz się w minimum polu średnim promieniowania)
    - Zmniejsz się ilość paliwa i energi
    - Gdy znajdziesz się blisko komina hydrotermalnego zwiększa się paliwo i energia

Gdy znajdziesz się na polu z kryształem czy oznaką życia to zmienia się wartość znalezionych elementów.
Czasem nie możesz się poruszyć w daną stronę bo jest przeszkoda (dodałem tylko 3 ze względu na małą mapę a wydaje mi się ,że przy większej mapie niż 50x50 chociaż w sumie nawet jest mniejsza poprzez pole bardzo wysokiego promieniowania to rozrywka byłaby monotonna)

Po pewnych zmianach radar wykrywa pewne elementy np. kryształy czy anomalie i pokazują dokładną pozycje x i y.
Radar ukazuje też strefy promieniowania.

Gra kończy się tak jak na początku wspominałem na 4 różne sposoby:
1. Wpadnięcie pod lód:
    - Brak paliwa
    - Brak energii
    - Zbyt wysoka dawka promieniowania w strefie bardzo wysokiego promieniowania
2. Zebranie 8 kryształów
3. Znalezienie 3 oznak życia
4. Odkrycie starożytnej cywilizacji w punkcie (40, 40) (znajduje się na końcu mapa.json)

Aby gra działała poprawnie należy umieścić plik mapa.json w tym samym folderze co main.py.

## Funkcje / pomoc w testowaniu
Wprowadziłem prymitywny sposób sprawdzenia na szybko podstawowych cech gry:
1. Po wpisaniu "cheat" jest możliwe wpisanie nowych współrzędnych łazika
2. Po wpisaniu "zak_wsz_krsz", "zak_wsz_zyc", "zak_zn_cyw" otrzymujemy specyficzne zakończenie

## Możliwa modernizacja
1. Dodanie ulepszeń łazika.
2. Automatycznie generowana mapa
3. Wczytywanie/Zapisywanie stanu gry
4. Dodatkowe utrudnienia np. meteoryty
5. Zamiast użyć turtle wykorzystać pygame

## Skąd pomysł?
Zainspirowałem się ostatnio czytaną lekturą, jaką jest "Wyobrażone życie" autorstwa James'a Trefila'a i Micheal'a Summers'a.
Po kilku godzinnym czytaniu pomyślałem sobie ,że struktura Nowej Europy, księżycia Jowisza idealnie nadaje się na
tematykę projektu dla etapu III Gigathon. Sam z powodu zainteresowania fizyką oraz postaciami znanymi z dokonań tej dziedzinie
np. Richard Feynman mój ulubiony naukowiec postanowiłem połączyć tą ciekawość z projektem konkursowym.
