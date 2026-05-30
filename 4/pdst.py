
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
