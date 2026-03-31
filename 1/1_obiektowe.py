from math import sin, pi, exp

class KalkulatorFunkcji:
    def __init__(self):
        pass

    def cos(self, x):
        return sin(pi/2 - x)
    
    def tangens(self, x):
        return sin(x) / self.cos(x)
    
    def cotangens(self, x):
        return 1 / self.tangens
    
    def sinh(self, x):
        return (exp(x) - exp(-x))/2
    
    def cosh(self, x):
        return (exp(x) + exp(-x))/2
    
    def secans(self, x):
        return 1 / self.cos(x)
    
    def cosecans(self, x):
        return 1 / self.sin(x)
    
    def oblicz(self, func, x):
        if func == 'cos': return self.cos(x)
        elif func == 'tangens': return self.tangens(x)
        elif func == 'cotangens': return self.cotangens(x)
        elif func == 'sinh': return self.sinh(x)
        elif func == 'cosh': return self.cosh(x)
        elif func == 'secans': return self.secans(x)
        elif func == 'cosecans': return self.cosecans(x)
        return None
    
    def pochodna(self, func, x):
        if func == 'cos':
            return -sin(x)
        elif func == 'tangens':
            return 1 / self.cos(x)**2
        elif func == 'cotangens':
            return -self.cosecans(x)**2
        elif func == 'sinh':
            return self.cosh(x)
        elif func == 'cosh':
            return self.sinh(x)
        elif func == 'secans':
            return self.secans(x) * self.tangens(x)
        elif func == 'cosecans':
            return -self.cosecans(x) * self.cotangens(x)
        return None
    
def main():
    moj_kalkulator = KalkulatorFunkcji()

    x = float(input("Podaj wartość x: "))
    print("Dostępne: cos, tangens, cotangens, sinh, cosh, secans, cosecans")
    functionToSolve = input("Jaką funkcję chcesz użyć? ") 
    derivativeYN = input("Czy chcesz policzyć z tego pochodną pierwszego stopnia? (y/n): ")

    if derivativeYN.lower == "y":
        result = moj_kalkulator.pochodna(functionToSolve, x)
    else:
        result = moj_kalkulator.oblicz(functionToSolve, x)

    if result is not None:
        print(f"Wynik: {result:.3f}")
    else:
        print("Nieprawidłowa nazwa funkcji!")

if __name__ == "__main__":
    main()