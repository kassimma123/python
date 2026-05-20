# Iterowanie po różnych rzeczach w Pythonie

## 0. Iterowanie w Pythonie

Z dydaktycznego obowiązku trzeba zaznaczyć, że każde zapętlenie przy pomocy `while` lub `for` będzie jakąś formą iterowania interpretera po tym samym fragmencie kodu.

Szczególnie istotna jest możliwość iterowania po elementach składowych obiektów-kolekcji:

```python
# Przykład iterowania po liście
for x in [1, 2, 3, 4, 5]:
    print(x)
```

Na dzisiejszych laboratoriach będziemy zajmować się zagadnieniem tworzenia własnych iteratorów oraz generatorów (w odróżnieniu od iteratorów, tworzą dane na żądanie) pokroju `range()`:

```python
# Przykład wykorzystania generatora range()
for x in range(0, 5):
    print(x)
```

## 1. Podstawy iteracji

Z pewnymi uproszczeniami, można powiedzieć, że *wszystko* w Pythonie, co obsługuje pętlę `for` (np. `list`, `tuple`, `range`), jest *obiektem iterowalnym*. Z technicznej perspektywy, obiekt iterowalny zachowuje się jak jednokierunkowa lista, w której możemy zapytać o kolejny element i dostać go lub odmowę (koniec listy).  Co to dokładnie oznacza?

* Iterator to metoda `__iter__()`, która pozwa przejść pętlą po pewnym obiekcie i odczytać jego elementy składowe.  
  * Przykładem klas obiektów, które posiadają wbudowaną implementację metody `__iter__()` to kolekcje (np. `list`, `tuple`).
* Metoda `__iter__()` musi zwrócić obiekt, który ma implementację metody `__next__()`.
  * Może to być ten sam obiekt, który posiada iterator (tj. implmenetuje obydwie metody `__iter__` oraz `__next__`).
  * Metoda `__next__()` może zostać skojarzona ze wskaźnikiem na kolejny element jednokierunkowej listy.
  * Wywołanie tej metody odbya się przy pomocy funkcji `iter()`, która zwraca obiekt, na którym można zawołać funkcję `next()`.
* Iterowanie po obiekcie iterowalnym polega na wywoływaniu jego metody `__next__()`.
  * Wywołanie tej metody odbywa się przy pomocy `next()`.
* Zakończenie iteracji jest zgłaszane specjalnym wyjątkiem `StopIteration`.

Obiekty implementujące metody `__iter__` oraz `__next__` spełniają tzw. "*iterator protocol*".

Proszę spojrzeć na poniższy przykład:

```python
class Fibonacci:
    def __init__(self, max_n: int):
        self.max_n = max_n

    def __iter__(self):
        self.n = 0
        self.prev_1 = 1
        self.prev_2 = 0
        return self
    
    def __next__(self):
        if self.n >= self.max_n:
            raise StopIteration

        match self.n:
            case 0:
                self.n = 1
                return 0
            
            case 1:
                self.n = 2
                return 1
            
            case _:
                result = self.prev_1 + self.prev_2
                self.prev_2 = self.prev_1
                self.prev_1 = result
                self.n += 1
                return result

# Tworzymy obiekt implementujący metody `__iter__` oraz `__next__`
numbers = Fibonacci(max_n=5)

# Uzyskujemy z niego iterator
i = iter(numbers)

# Wołamy iterator kilkukrotnie
print(next(i)) # 0
print(next(i)) # 1
print(next(i)) # 1
print(next(i)) # 2
print(next(i)) # 3
print(next(i)) # Exception
```

Dodatkowy przykład z pętla `for`:
```python
print("Start")
for num in Fibonacci(max_n=5):
    print(f"Kolejny wyraz ciągu: {num}")
print("Koniec")
```

## 2. Generatory

Iterowanie po istniejących elementach, może zostać rozwiązane powyższym przykładem. W przypadku gdy elementów może być nieskończenie wiele, nie jesteśmy w stanie ich wcześniej zaalokować - lepiej by było generować je w "locie".

Generatory w Pythonie to specjalne funkcje, które zamiast zwracać wszystkie wartości naraz (jak zwykła funkcja z return), zwracają je "na żądanie" za pomocą słowa kluczowego `yield`. Dzięki temu nie muszą trzymać całej sekwencji w pamięci, co jest bardzo wygodne przy dużych danych lub nieskończonych ciągach. Ta własność nazywa się **leniwą ewaluacją** (ang. *lazy evaluation*).

Generator to funkcja, która przy każdym wywołaniu `next()` zwraca kolejną wartość, a następnie "zapamiętuje swój stan" i czeka aż zostanie znowu wywołany. Po wyczerpaniu wszystkich wartości rzuca wyjątek `StopIteration`.

Przykład:
```python
def zlicz_do_3():
    yield 1
    yield 2
    yield 3

g = zlicz_do_3()
for x in g:
    print(x)
```

## 3. Zaawansowane metody generatorów

Generatory zwracające wartości przy pomocy `yield` mają dodatkowo metody trzy metody: `.send()`, `.close()` oraz `.throw()`. Sprawiają one, że generatory mają "dwukierunkową" komunikację:

* Metoda `send(x)` pozwala przesłać wartość do generatora – ta wartość staje się wynikiem aktualnego wyrażenia `yield`, dzięki czemu generator zachowuje się jak prosta forma korutyny (ang. *corutine*). Jeśli generator nie jest wstrzymany w yield, wywołanie send() zakończy się błędem.
* Metoda `throw(exc)` pozwala rzucić wyjątek w miejscu, w którym generator został wstrzymany (w `yield`); wyjątek może być obsłużony wewnątrz generatora, a generator może przy tym zwrócić kolejną wartość lub zakończyć się. 
* Natomiast `close()` faktycznie zakończy pracę generatora, rzucając wyjątek `StopIteration` w miejscu `yield`, co może pozwolić np. na poprawne zwolnienie zasobów.

Więcej informacji w dodatkowych materiałach [2].

## 4. Użyteczne zastosowania iteracji i generatorów

### List comprehension

Wykorzystując iterowanie po generatorze, można utworzyć długie listy, np:
```python
nums = [x**2 for x in range(10)] # 10 elementów, kwadraty liczb od 0 do 9
```

Gdyby potrzebny był generator o poodobnej funkcji:
```python
nums_gen = (x**2 for x in range(10))
```

### Generator - czytanie plików linijka po linijce

```python
file_name = "techcrunch.csv"
lines = (line for line in open(file_name))
```

### Generator - elementy stringa

```python
list_line = (s.rstrip().split(",") for s in lines)
```

### Iterator `enumerate()`
Zliczanie kolejnych elementów, zwraca tuplę dwóch wartości.

```python
names = ["Ala", "Ewa", "Kamil"]
for cnt, name in enumerate(names):
    print(f"nr: {cnt} imię: {name})
```

### Generator `zip()` - łączenie iterowalnych obiektów

```python
products = ["jabłka", "banany", "gruszki"]
prices = [3.5,  2.0,  4.0]

for prod, price in zip(products, prices):
    print(f"{prod}: {price} zł")
```

## Dodatkowe materiały

1. [RealPython - Iterators and Iterables in Python: Run Efficient Iterations](https://realpython.com/python-iterators-iterables/)
2. [RealPython - How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)