from decimal import Decimal, ROUND_HALF_UP
 
class KontoBankowe:
    def __init__(self, saldo):
        self.__saldo = Decimal(str(saldo)).quantize(Decimal('0.01'), rounding = ROUND_HALF_UP)
    
    def wplac(self, kwota):
        kwota = Decimal(str(kwota)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if kwota > 0: 
            self.__saldo += kwota
            print(f"Wpłacono: {kwota} zł")
        else: print("kwota musi byc wieksza od 0")
    
    def wyplac(self, kwota):
        kwota = Decimal(str(kwota)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if kwota > 0 and kwota <= self.__saldo: 
            self.__saldo -= kwota
            print(f"Wypłacono: {kwota} zł")
        else: print("kwota musi byc wieksza od 0 lub nie mozna wyplacic wiecej niz na koncie")
    
    def pokaz_saldo(self):
        print(f"Aktualne saldo: {self.__saldo} zł")

    #getter
    @property
    def saldo(self):
        return self.__saldo 


# --- Testy ---
if __name__ == "__main__":
    konto = KontoBankowe(100.55)

    # Próbujemy wpłacić kwotę z 3 miejscami po przecinku (50.123 zł). 
    # System bankowy zaokrągli to do 50.12 zł przed dodaniem do konta.
    konto.wplac(50.123) 

    konto.wyplac(30.00)
    konto.pokaz_saldo() # Wynik: 100.55 + 50.12 - 30.00 = 120.67 zł

    # Działanie Walidatora przy wypłacie
    konto.wyplac(500) # Zwróci błąd braku środków