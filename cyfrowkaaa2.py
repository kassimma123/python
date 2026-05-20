from sympy import symbols
from sympy.simplify.cse_main import cse

def testuj_i_optymalizuj_dekrementator():
    print("=== WERYFIKACJA LOGIKI DEKREMENTATORA ===")
    Q2, Q1, Q0 = symbols('Q2 Q1 Q0')

    # Wzory wyznaczone z tabel Karnaugha
    N2 = (Q2 & Q1) | (Q2 & Q0)
    N1 = (Q2 & ~Q1 & ~Q0) | (Q1 & Q0)
    N0 = (Q2 & ~Q0) | (Q1 & ~Q0)

    print("Q2 Q1 Q0 | N2 N1 N0 (Wyliczone) | Sprawdzenie")
    print("---------------------------------------------")
    wszystko_ok = True
    
    for q2_val in [0, 1]:
        for q1_val in [0, 1]:
            for q0_val in [0, 1]:
                # Wyliczenie z Twoich wzorów
                n2_val = 1 if N2.subs({Q2: q2_val, Q1: q1_val, Q0: q0_val}) else 0
                n1_val = 1 if N1.subs({Q2: q2_val, Q1: q1_val, Q0: q0_val}) else 0
                n0_val = 1 if N0.subs({Q2: q2_val, Q1: q1_val, Q0: q0_val}) else 0
                
                # Zdefiniowanie poprawnego zachowania (dekrementator nasycający)
                wartosc_wejsciowa = q2_val * 4 + q1_val * 2 + q0_val
                oczekiwany_wynik = max(0, wartosc_wejsciowa - 1) # Odejmij 1, ale nie schodź poniżej 0
                
                # Zamiana oczekiwanego wyniku dziesiętnego z powrotem na bity
                oczekiwane_n2 = 1 if (oczekiwany_wynik & 4) else 0
                oczekiwane_n1 = 1 if (oczekiwany_wynik & 2) else 0
                oczekiwane_n0 = 1 if (oczekiwany_wynik & 1) else 0

                # Porównanie
                if n2_val == oczekiwane_n2 and n1_val == oczekiwane_n1 and n0_val == oczekiwane_n0:
                    status = "[OK]"
                else:
                    status = "[BŁĄD]"
                    wszystko_ok = False

                print(f" {q2_val}  {q1_val}  {q0_val} |  {n2_val}  {n1_val}  {n0_val}            | {status}")

    if wszystko_ok:
        print("\n-> WNIOSEK: Wszystko się zgadza! Wzory dekrementatora są poprawne.\n")
    else:
        print("\n-> UWAGA: Znaleziono błędy we wzorach dekrementatora!\n")

    funkcje_wyjsciowe = [N2, N1, N0]
    wspolne_bloki, zoptymalizowane_wyjscia = cse(funkcje_wyjsciowe)

    print("=== DEKREMENTATOR: ZNALEZIONE WSPÓLNE BLOKI ===")
    for nazwa_zmiennej, wzor_bloku in wspolne_bloki:
        print(f"  {nazwa_zmiennej} = {wzor_bloku}")

    print("\n=== DEKREMENTATOR: ZOPTYMALIZOWANE WZORY ===")
    nazwy_wyjsc = ['N2', 'N1', 'N0']
    for nazwa, zopt_wzor in zip(nazwy_wyjsc, zoptymalizowane_wyjscia):
        print(f"  Wyjście {nazwa} = {zopt_wzor}")

def testuj_selektor():
    print("\n=== WERYFIKACJA LOGIKI SELEKTORA ===")
    L, I, N = symbols('L I N')
    
    # Wzór wyznaczony z tabeli Karnaugha
    D = (L & I) | (~L & N)
    
    print("L I N | D (Wyliczone) | Sprawdzenie")
    print("-----------------------------------")
    wszystko_ok = True
    
    for l_val in [0, 1]:
        for i_val in [0, 1]:
            for n_val in [0, 1]:
                wynik_int = 1 if D.subs({L: l_val, I: i_val, N: n_val}) else 0
                
                # Zdefiniowanie poprawnego zachowania (L=0 to puszczamy N, L=1 to puszczamy I)
                oczekiwany_wynik = i_val if l_val == 1 else n_val
                
                # Porównanie
                if wynik_int == oczekiwany_wynik:
                    status = "[OK]"
                else:
                    status = "[BŁĄD]"
                    wszystko_ok = False

                print(f"{l_val} {i_val} {n_val} |  {wynik_int}            | {status}")

    if wszystko_ok:
        print("\n-> WNIOSEK: Wszystko się zgadza! Wzór selektora (MUX) działa idealnie.")
    else:
        print("\n-> UWAGA: Znaleziono błędy we wzorze selektora!")

testuj_i_optymalizuj_dekrementator()
testuj_selektor()