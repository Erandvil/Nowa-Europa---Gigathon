# Generalny opis
Jesteś badaczem kosmicznym. Twoim zadaniem jest odnalezienie 6 minerałów i zebranie z nich próbek.
Możesz również znaleźć 3 oznaki życia albo fragmenty statku starożytnej cywilizacji!

Poruszasz się w dwuwymiarowej przestrzeni, wprowadzając kierunek: góra, dół, lewo, prawo.
Później wprowadzony przez Ciebie kierunek jest zamieniany na kąt, jaki stanowisz względem mapy.

Po wykonaniu ruchu zmieniają się pewne zmienne:
    - Zwiększa się poziom napromieniowania łazika (gdy znajdujesz się minimum w polu średniego promieniowania)
    - Zmniejsza się ilość paliwa i energii
    - Gdy znajdziesz się blisko komina hydrotermalnego, zwiększa się paliwo i energia

Gdy znajdziesz się na polu z kryształem czy oznaką życia, to zmienia się wartość znalezionych elementów.
Czasem nie możesz się poruszyć w daną stronę, bo jest przeszkoda (dodałem tylko 3 ze względu na małą mapę, a wydaje mi się, że przy większej mapie niż 50x50 rozrywka byłaby monotonna. Pomimo tego mapa i tak jest mniejsza ze względu na strefę bardzo wysokiego promieniowania).

Po pewnych zmianach radar wykrywa pewne elementy, np. kryształy czy anomalie, i pokazuje dokładną pozycję x i y.
Radar ukazuje też strefy promieniowania.

Gra kończy się, tak jak na początku wspominałem, na 4 różne sposoby:
1. Wpadnięcie pod lód:
    - Brak paliwa
    - Brak energii
    - Zbyt wysoka dawka promieniowania w strefie bardzo wysokiego promieniowania
2. Zebranie 6 kryształów
3. Znalezienie 3 oznak życia
4. Odkrycie starożytnej cywilizacji w punkcie (40, 40) (znajduje się na końcu pliku mapa.json)

**Ważna uwaga dotycząca realizmu rozgrywki:**
W kosmicznych realiach każda chwila postoju w strefie promieniowania kosztuje – łazik zużywa energię na podtrzymanie systemów termicznych i łączności radiowej,
nawet gdy stoi w miejscu i czeka na decyzje nawigatora!

# Funkcje / pomoc w testowaniu
Wprowadziłem prymitywny sposób sprawdzenia na szybko podstawowych cech gry:
1. Po wpisaniu "cheat" jest możliwe wpisanie nowych współrzędnych łazika
2. Po wpisaniu "zak_wsz_krsz", "zak_wsz_zyc", "zak_zn_cyw" otrzymujemy specyficzne zakończenie

# Możliwa modernizacja
1. Dodanie ulepszeń łazika.
2. Automatycznie generowana mapa
3. Wczytywanie/Zapisywanie stanu gry
4. Dodatkowe utrudnienia, np. meteoryty
5. Zamiast użyć turtle, wykorzystać pygame

# Skąd pomysł?
Zainspirowałem się ostatnio czytaną lekturą, jaką jest "Wyobrażone życie" autorstwa Jamesa Trefila i Michaela Summersa.
Po kilkugodzinnym czytaniu pomyślałem sobie, że struktura Nowej Europy, księżyca Jowisza, idealnie nadaje się na
tematykę projektu dla etapu III Gigathon. Sam z powodu zainteresowania fizyką oraz postaciami znanymi z dokonań w tej dziedzinie,
np. Richard Feynman – mój ulubiony naukowiec, postanowiłem połączyć tę ciekawość z projektem konkursowym.
