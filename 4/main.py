
#podstawowe
class Student:
    def __init__(self, imie: str, nazwisko: str, numer_albumu: int):
        self.imie = imie
        self.nazwisko = nazwisko
        self.numer_albumu = numer_albumu

    def przedstaw_sie(self):
        return f"Cześć, jestem {self.imie} {self.nazwisko}, a mój indeks to {self.numer_albumu}. "

#stworznie dwóch obiektów klasy student
student1 = Student("Kacper","Masło",123456)
student2 = Student("Jola", "Masełko", 654321)

#wywołanie metody przedstaw_sie 
print(student1.przedstaw_sie())
print(student2.przedstaw_sie())



#zad średniozaawansowane obsłuzenie 3 miejsca po przecinku w zł
#zaawaansowane