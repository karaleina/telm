# encoding=utf-8
from __future__ import print_function
import sys

filename = "small_channel_1.txt"

# wczytywanie pliku do listy próbek 'samples'
f = open(filename)
samples = [int(x) for x in f.read().split()]
f.close()


# to całe do f.close() można zakomentować/usunąć.
# produkuje plik .znormalizowane, żeby sygnał był ograniczony z góry przez 1.0
# do celów poglądowych
maks = max(samples)
znormalizowane = [x / maks for x in samples]
f = open(filename + ".normalizowane", "w")
print("\n".join(map(str, znormalizowane)), file=f)
f.close()

# krok 1.
#filtr dolnoprzepustowy
# y(n) = y(n - 1) - y(n - 2) + x(n) - 2x(n - 6) + x(n - 12)
dolny = [0] * len(samples)

for n in xrange(12, len(samples)):  # liczenie sygnału po zastosowaniu filtru dolnego
    dolny[n] = dolny[n-1] - dolny[n-2] + samples[n] - 2 * samples[n-6] + samples[n-12]  # tutaj moja inwencja 1.000

f = open(filename + ".dolny", "w")  # otwiera plik .dolny, żeby zapisać wyniki po zastosowaniu filtru dolnego
print("\n".join(map(str, dolny)), file=f) # można tę trójkę zakomentować, ale fajnie mieć wyniki pośrednie sygnału do sprawdzenia
f.close()

gorny = [0] * len(samples)  # sygnał po filtrze górnym
for n in xrange(32, len(samples)):
    gorny[n] = dolny[n - 16] - (gorny[n-1] + samples[n] - samples[n - 32]) / 32.

f = open(filename + ".gorny", "w")  # to samo co wyżej, do pliku .gorny trafia sygnał dolny po zastosowaniu filtru górnego
print("\n".join(map(str, gorny)), file=f)
f.close()


pochodna_gorny = [0] * len(samples)  # miejsce na sygnał po zastosowaniu pochodnej
for n in xrange(4, len(samples)):
    pochodna_gorny[n] = 0.125 * (2 * samples[n] + samples[n-1] - samples[n-3] - 2 * samples[n-4])
f = open(filename + ".pochodna_gorny", "w")  # to samo co wyżej...
print("\n".join(map(str, pochodna_gorny)), file=f)
f.close()

kwadrat = [0] * len(samples)  # po kwadratowaniu...
for n in xrange(4, len(samples)):
    kwadrat[n] = pochodna_gorny[n] ** 2
f = open(filename + ".kwadrat", "w")  # to samo co wyżej...
print("\n".join(map(str, kwadrat)), file=f)
f.close()

usredniony = [0] * len(samples)  # miejsce na sygnał po przejechaniu się oknem
szerokosc_okna = 20
for n in xrange(szerokosc_okna, len(samples)):
    usredniony[n] = sum(kwadrat[n-i] for i in xrange(szerokosc_okna)) / szerokosc_okna

maks = max(usredniony)
for n in xrange(len(samples)):  # normalizacja sygnału
    usredniony[n] = usredniony[n] / maks

f = open(filename + ".usredniony", "w")  #  zapisywanie ostatecznego sygnału
print("\n".join(map(str, usredniony)), file=f)
f.close()

# rozpoznawanie stromych zboczy w ostatecznym sygnale
zbocza = []
poczatek_zbocza = 0
for n in xrange(1, len(samples)):
    if usredniony[n] - usredniony[n-1] > 0.01:  # zbocze trwa, idziemy dalej w prawo
        continue
    # zbocze się zakończyło, tzn. sygnał spadł w dół lub wzrost jest za mało stromy
    # jeśli długość zbocza jest co najmniej 5, to klasyfikujemy to jako zbocze.
    if n - poczatek_zbocza >= 5:  # jeśli zbocze jest dostatecznie długie
        zbocza.append((poczatek_zbocza, n-1))
        # n - poczatek_zbocza
    poczatek_zbocza = n


# teraz mamy zbocza, które w najbardziej typowym przypadku są jednego z dwóch rodzajów:
# a) zbocze do punktu przegięia (tam gdzie jest załamek R)
# b) zbocze od załamka R do pierwszego piku w sygnale
# żeby się upewnić, że zachodzi ten przypadek, to koniec zbocza a) musi być blisko początku zbocza b)
# jeśli tak jest to, twierdzę, że punkt R jest gdzieś pomiędzy końcem a) a początkiem b) -> więc mniemam na końcu a) bo tak ładniej działa


start, koniec = zbocza[0] # start, koniec oznaczają początek i koniec wcześniejsego zbocza
zalamki_r = []
for i in xrange(1, len(zbocza)):
    nowy_start, nowy_koniec = zbocza[i] # nowy_start, nowy_koniec oznaczają początek i koniec następnego zbocza
    if nowy_start - koniec < 3:  # jeśli koniec a) jest blisko b)
        r = koniec
        zalamki_r.append((r, samples[r]))  # dodaję informację o załamku (czas, napięcie)
    start, koniec = nowy_start, nowy_koniec  # odtworzenie sytuacji wejściowej, następne zbocze staje się poprzednim

f = open(filename + ".punkty_r", "w")
print("\n".join(["%s %s" % zalamek for zalamek in zalamki_r]), file=f)
f.close()

punkty_q = []
punkty_s = []

for czas_r, wysokosc_r in zalamki_r:  # wyszukuje załamki q, s dookoła załamka r
    na_prawo = czas_r + 1
    while samples[czas_r] <= samples[na_prawo]:
        na_prawo += 1

    while na_prawo < len(samples) - 1 and samples[na_prawo] > samples[na_prawo + 1]:
        na_prawo += 1
    punkty_s.append((na_prawo, samples[na_prawo]))

    na_lewo = czas_r - 1
    while samples[czas_r] >= samples[na_lewo]: # znalazł kandydata, najbliższy na lewo mniejszy od załamka r
        na_lewo -= 1

    while na_lewo > 0 and samples[na_lewo] > samples[na_lewo - 1]:  # schodzenie w dół
        na_lewo -= 1
    punkty_q.append((na_lewo, samples[na_lewo]))

f = open(filename + ".punkty_q", "w")
print("\n".join(["%s %s" % zalamek for zalamek in punkty_q]), file=f)
f.close()

f = open(filename + ".punkty_s", "w")
print("\n".join(["%s %s" % zalamek for zalamek in punkty_s]), file=f)
f.close()

odstepy = []
for i in xrange(1, len(zalamki_r)):
    odstepy.append(zalamki_r[i][0] - zalamki_r[i - 1][0])

posortowane = sorted(odstepy)
f = open(filename + ".czestotliwosc", "w")
print("\n".join(["%.2f" % (60. * 250 / odleglosc) for odleglosc in posortowane]), file=f)
f.close()
