
#podstawowe
class Student:
    #konstruktor
    def __init__(self, imie: str, nazwisko: str, indeks: int):
        self.imie = imie
        self.nazwisko = nazwisko
        self.indeks = indeks


    #metoda wypisująca dane
    def przedstaw_sie(self):
        return f"Cześć, jestem {self.imie} {self.nazwisko}, a mój indeks to {self.indeks}. "

    #metoda specjalna 
    def __str__(self):
        return self.przedstaw_sie()

#test
student1 = Student("Kacper","Masło",123456)
student2 = Student("Jola", "Masełko", 654321)

print(student1)
print(student2)

#zad średniozaawansowane obsłuzenie 3 miejsca po przecinku w zł -- biblioteka decimal
#getter setter, walidator 
class KontoBankowe:
    def __init__(self, saldo):
        self.__saldo = round(saldo, 2) # prywatny atrybut __saldo
    
    def wplac(self, kwota):
        if kwota > 0: self.saldo += kwota
        else: print("kwota musi byc wieksza od 0")
    
    def wyplac(self, kwota):
        if kwota > 0 and kwota <= self.saldo: self.saldo -= kwota
        else: print("kwota musi byc wieksza od 0 lub nie mozna wyplacic wiecej niz na koncie")
    
    def pokaz_saldo(self):
        print(f"Aktualne saldo: {round(self.__saldo, 2)} zł")

    @property
    def saldo(self):
        return self.__saldo # bezpieczny odczyt przez property


# Test
konto = KontoBankowe(100)
konto.wplac(50)
konto.wyplac(30)
konto.pokaz_saldo() # Wypisze aktualne saldo
print(konto.saldo)  # Odczyt salda bez nawiasów dzięki @property