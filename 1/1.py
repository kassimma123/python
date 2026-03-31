from math import sin, pi, sqrt, exp

# Zadanie:
"""
Przy pomocy w.w. symboli i funkcji zdefiniować:
- cos
- tangens
- funkcje hiperboliczne
- secans i cosenas
- wszystkie pochodne (pierwszego stopnia) w.w. funkcji
*Opcjonalnie*: użyć biblioteki sympy

Zaproponuj architekturę (ew. obiektową) i logikę wybierania funkcji przez użytkownika w terminalu

Całe rozwiązanie powinno się mieścić w jednym pliku.
Wyświetlać 3 miejsca po przecinku przy pomocy print. (wynik {x})
"""
# zakładamy poprawność danych

def cos(x):
    return sin(pi/2 - x)

def tangens(x):
    return sin(x) / cos(x)

def sinh(x):
    return (exp(x) - exp(-x)) / 2

def cosh(x):
    return (exp(x) + exp(-x)) / 2

def secans(x):
    return 1 / cos(x)

def cosecans(x):
    return 1 / sin(x)

def cotangens(x):
    return 1 / tangens(x)

def Calculations(func, x): 
    if func == 'cos': return cos(x)
    elif func == 'tangens': return tangens(x)
    elif func == 'cotangens': return cotangens(x)
    elif func == 'sinh': return sinh(x)
    elif func == 'cosh': return cosh(x)
    elif func == 'secans': return secans(x)
    elif func == 'cosecans': return cosecans(x)
    return None

def derivative(function, x): 
    if function == 'cos':
        return -sin(x)
    elif function == 'tangens':
        return 1/cos(x)**2
    elif function == 'sinh':
        return cosh(x)
    elif function == 'cosh':
        return sinh(x)
    elif function == 'secans':
        return secans(x) * tangens(x)
    elif function == 'cosecans':
        return -cosecans(x) * cotangens(x) 

def main():
    x = float(input("podaj wartość x: "))
    print("Dostępne: cos, tangens, cotangens, sinh, cosh, secans, cosecans")
    functionToSolve = input("Jaką funkcję chcesz użyć? ") 
    derivativeYN = input("Czy chcesz policzyć z tego pochodną pierwszego stopnia? (y/n): ")

    if derivativeYN.lower() == "y":
        result = derivative(functionToSolve, x)
    else:
        result = Calculations(functionToSolve, x)

    if result is not None:
        print(f"Wynik: {result:.3f}")
    else:
        print("Nieprawidłowa nazwa funkcji!")

if __name__ == "__main__":
    main()
