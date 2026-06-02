import unittest

class Osoba:
    def __init__(self, imie:str, nazwisko:str):
        self.imie = imie
        self.nazwisko = nazwisko

    def opis(self):
        return f"{self.imie} {self.nazwisko}"

class Uzytkownik(Osoba):
    def __init__(self, imie:str, nazwisko: str):
        super().__init__(imie, nazwisko)
        self.__wypozyczone = []

    def dodaj_ksiazke(self, ksiazka):
        self.__wypozyczone.append(ksiazka)
        print(f"Dodałeś książke {ksiazka.tytul} do wypożyczenia")

    def usun_ksiazke(self, ksiazka):
        if ksiazka in self.__wypozyczone:
            self.__wypozyczone.remove(ksiazka)
            print(f"Usunięto książkę {ksiazka.tytul}")
        else:
            print("Nie posiadasz tej książki.")

    def opis(self):
        return f"Uzytkownik: {super().opis()} \n wypozyczone ksiązki: {len(self.__wypozyczone)}"
    
    @property
    def wypozyczone(self):
        return self.__wypozyczone
    
    
class Ksiazka:
    def __init__(self, tytul:str, autor:str):
        self.tytul = tytul
        self.autor = autor

        self.__dostepnosc = True

    def czy_dostepna(self):
        return self.__dostepnosc
    
    def wypozycz(self):
        self.__dostepnosc = False
        print(f"Ksiazka {self.tytul} - {self.autor} zostala wypozyczona")

    def zwroc(self):
        self.__dostepnosc = True
        print(f"Ksiazka {self.tytul} - {self.autor} zostala zwrocona")

    def opis(self):
        status = "Dostepna" if self.__dostepnosc else "Wypozyczona"
        return f"Ksiazka {self.tytul} - {self.autor} status: [{status}]"
    
    
class Biblioteka:
    def __init__(self):
        self.ksiazki = []
        self.uzytkownicy = []

    def dodaj_ksiazke(self, ksiazka):
        self.ksiazki.append(ksiazka)
        print(f"Ksiazka {ksiazka.tytul} - {ksiazka.autor} zostala dodana do biblioteki.")
    
    def dodaj_uzytkownika(self, uzytkownik):
        self.uzytkownicy.append(uzytkownik)
        print(f"Uzytkownik {uzytkownik.imie} - {uzytkownik.nazwisko} zostal dodany do biblioteki")

    def wypozycz_ksiazke(self, ksiazka, uzytkownik):
        if uzytkownik not in self.uzytkownicy:
            print(f"Uzytkownik {uzytkownik.imie} {uzytkownik.nazwisko} nie jest zarejestrowany. Rejestruję...")
            self.dodaj_uzytkownika(uzytkownik)
        if ksiazka in self.ksiazki and ksiazka.czy_dostepna():
            ksiazka.wypozycz()
            uzytkownik.dodaj_ksiazke(ksiazka)
            print(f"Ksiazka {ksiazka.tytul} zostala wypozyczona przez {uzytkownik.imie}")
        else:
            print(f"Ksiazka {ksiazka.tytul} nie jest dostepna w bibliotece.")

    def zwroc_ksiazke(self, ksiazka, uzytkownik):
        if ksiazka in uzytkownik.wypozyczone and uzytkownik in self.uzytkownicy:
            ksiazka.zwroc()
            uzytkownik.usun_ksiazke(ksiazka)
            print(f"Ksiazka {ksiazka.tytul} - {ksiazka.autor} zostala zwrocona przez {uzytkownik.imie} - {uzytkownik.nazwisko}")

class TestSystemuBibliotecznego(unittest.TestCase):
    def setUp(self):
        self.biblioteka = Biblioteka()
        self.k1 = Ksiazka("Wiedźmin", "Andrzej Sapkowski")
        self.k2 = Ksiazka("Diuna", "Frank Herbert")
        self.u1 = Uzytkownik("Jan", "Kowalski")

    def test_dodawanie_ksiazki(self):
        self.biblioteka.dodaj_ksiazke(self.k1)
        # asercja, czy książka faktycznie jest na liście
        self.assertIn(self.k1, self.biblioteka.ksiazki)

    def test_wypozyczanie_dostepnej_ksiazki(self):
        self.biblioteka.dodaj_ksiazke(self.k1)
        self.biblioteka.dodaj_uzytkownika(self.u1)
        
        self.biblioteka.wypozycz_ksiazke(self.k1, self.u1)
        
        # Sprawdzamy czy status książki zmienił się na niedostępna
        self.assertFalse(self.k1.czy_dostepna())
        # Sprawdzamy czy użytkownik ma książkę na swojej liście
        self.assertIn(self.k1, self.u1.wypozyczone)

    def test_automatyczna_rejestracja_uzytkownika(self):
        self.biblioteka.dodaj_ksiazke(self.k1)
        # NIE dodajemy użytkownika ręcznie, wywołujemy od razu wypożyczenie
        self.biblioteka.wypozycz_ksiazke(self.k1, self.u1)
        
        # Sprawdzamy, czy system sam dodał użytkownika do biblioteki
        self.assertIn(self.u1, self.biblioteka.uzytkownicy)
        self.assertIn(self.k1, self.u1.wypozyczone)

    def test_zwrot_ksiazki(self):
        self.biblioteka.dodaj_ksiazke(self.k1)
        self.biblioteka.wypozycz_ksiazke(self.k1, self.u1)
        
        # Zwracamy książkę
        self.biblioteka.zwroc_ksiazke(self.k1, self.u1)
        
        # Sprawdzamy stan po zwrocie
        self.assertTrue(self.k1.czy_dostepna())
        self.assertNotIn(self.k1, self.u1.wypozyczone)

    def test_brak_dostepnosci_ksiazki(self):
        self.biblioteka.dodaj_ksiazke(self.k1)
        u2 = Uzytkownik("Anna", "Nowak")
        
        # Pierwszy użytkownik wypożycza książkę
        self.biblioteka.wypozycz_ksiazke(self.k1, self.u1)
        
        # Drugi próbuje wypożyczyć tę samą
        self.biblioteka.wypozycz_ksiazke(self.k1, u2)
        
        # Książka nie powinna trafić do u2
        self.assertNotIn(self.k1, u2.wypozyczone)

if __name__ == '__main__':
    unittest.main()