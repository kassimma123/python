from datetime import datetime

class Pojazd:
    def __init__(self, marka: str, model: str, rok: int):
        self.marka = marka
        self.model = model
        self.rok = rok

    def opis(self):
        return f"{self.marka} {self.model} (rok produkcji: {self.rok})"

    @classmethod
    def utworz_domyslny(cls):
        return cls("nieznana marka", "nieznany model", 2000)

    @staticmethod
    def czy_poprawny_rok(rok):
        obecny_rok = datetime.now().year
        if 1886 <=rok <= obecny_rok:
            return True
        else:
            return False

class Samochod(Pojazd):
    def __init__(self, marka: str, model: str, rok: int, liczba_drzwi: int):
        super().__init__(marka, model, rok)
        self.liczba_drzwi = liczba_drzwi
    
    def opis(self):
        opis_bazowy = super().opis()
        return f"[SAMOCHÓD] {opis_bazowy}, Liczba drzwi: {self.liczba_drzwi}"

class Motocykl(Pojazd):
    def __init__(self, marka:str, model:str, rok: int, typ_motocykla: str):
        super().__init__(marka, model, rok)
        self.typ_motocykla = typ_motocykla
    
    def opis(self):
        opis_bazowy = super().opis()
        return f"[MOTOCYKL] {opis_bazowy} , Typ motocykla: {self.typ_motocykla}"


if __name__ == "__main__":
    print("--- Dziedziczenie i Polimorfizm ---")
    auto = Samochod("Toyota", "Corolla", 2021, 5)
    motor = Motocykl("Yamaha", "MT-07", 2023, "Naked")
    
    # Wywołujemy nadpisane metody opis()
    print(auto.opis())
    print(motor.opis())

    print("\n--- Metoda Statyczna (@staticmethod) ---")
    # Wywołujemy na samej klasie, bez tworzenia konkretnego auta!
    rok_testowy = 2030
    czy_ok = Pojazd.czy_poprawny_rok(rok_testowy)
    print(f"Czy rok {rok_testowy} jest poprawny? {czy_ok}")

    rok_testowy2 = 2015
    print(f"Czy rok {rok_testowy2} jest poprawny? {Pojazd.czy_poprawny_rok(rok_testowy2)}")

    print("\n--- Metoda Klasowa (@classmethod) ---")
    # Tworzymy domyślny pojazd bez podawania marki i modelu
    domyslny_pojazd = Pojazd.utworz_domyslny()
    print(domyslny_pojazd.opis())

    

    