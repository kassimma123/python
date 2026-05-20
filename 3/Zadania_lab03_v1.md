## Laboratorium 3 – Menedżer konfiguracji cz. 2

# Parsowanie konfiguracji z użyciem iteratorów i generatorów

Rozbuduj program z poprzednich laboratoriów tak, aby konfiguracja była podzielona na logiczne sekcje, a dane z pliku YAML parsowane do odpowiednich typów. Celem zadania jest przejście od pracy na zwykłym słowniku do bardziej uporządkowanego modelu opartego na dataclass, przy wykorzystaniu technik iteracji i generatorów.

## **Poziom łatwy – Iterowanie po konfiguracji i ekstrakcja danych**

**Cel**

Naucz się iterować po wczytanej konfiguracji YAML przy użyciu list comprehension, enumerate() oraz zip(), zamiast ręcznego indeksowania i pętli while.

**Założenia**

Program powinien:

* wczytywać plik YAML (tak jak w poprzednich laboratoriach),
* iterować po sekcjach konfiguracji przy użyciu .items() i list comprehension,
* wyświetlić numerowaną listę sekcji przy użyciu enumerate(),
* zestawić klucze i wartości wybranych sekcji płaskich przy użyciu zip(),
* zachować obsługę błędów z poprzednich laboratoriów.

**Wymagania**

Użyj następujących konstrukcji:

```python
# Wylistowanie sekcji z numeracją
for idx, section in enumerate(config.keys()):
    ...

# Zestawienie kluczy i wartości przy użyciu zip()
keys = list(server_config.keys())
values = list(server_config.values())
for k, v in zip(keys, values):
    ...

# Pobranie wszystkich kluczy najwyższego poziomu przy użyciu list comprehension
top_level_keys = [key for key in config]
```

**Efekt końcowy**

```
Sekcje konfiguracji:
  [0] app
  [1] server
  [2] database

Sekcja 'server':
  host  -> 127.0.0.1
  port  -> 8080
```


## **Poziom średni – Ekstrakcja danych z użyciem generatorów**

**Cel**

Wprowadź generatory do przetwarzania konfiguracji: zamiast budować całe listy danych naraz, generuj pary klucz–wartość leniwie, na żądanie.

**Założenia**

Program powinien realizować wszystko z poziomu łatwego, a dodatkowo:

* zawierać generator `flatten_config()`, który przechodzi przez zagnieżdżony słownik konfiguracji i zwraca kolejne pary `(ścieżka, wartość)` w postaci krotek, np. `("server.host", "127.0.0.1")`,
* korzystać z yield wewnątrz generatora,
* używać next() do ręcznego pobrania pierwszej wartości z generatora (przed iterowaniem pętlą),
* wyświetlić wszystkie spłaszczone pary konfiguracji w czytelnej formie.

**Wskazówka – szkielet generatora**

```python
def flatten_config(config: dict, prefix: str = "") -> ...:
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            yield from flatten_config(value, full_key)
        else:
            yield full_key, value
```

Zauważ, że `yield from` deleguje generowanie wartości do rekurencyjnego wywołania — to bardziej elegancki odpowiednik pętli z `yield` wewnątrz.


**Wymagania**

```python
gen = flatten_config(config)

# Pobierz pierwszą parę ręcznie
first = next(gen)
print(f"Pierwsza wartość: {first[0]} = {first[1]}")

# Pozostałe iteruj pętlą
for path, value in gen:
    print(f"  {path} = {value}")
```

**Efekt końcowy**

```
Pierwsza wartość: app.name = MojaAplikacja

Pozostałe pola:
  app.debug = True
  server.host = 127.0.0.1
  server.port = 8080
  server.timeout = 30
  database.credentials.user = admin
  database.credentials.password = secret
  database.settings.pool_size = 5
  database.settings.retry = True
```

## **Poziom trudny – Własny iterator sekcji i budowa obiektu konfiguracji**

**Cel**

Zbuduj własny iterator zgodny z protokołem iteratora Pythona (`__iter__` + `__next__`), który przechodzi po sekcjach konfiguracji. Następnie użyj go razem z generatorem `flatten_config()` do zbudowania niemutowalnego obiektu konfiguracji opartego na dataclass.

**Założenia**

Program powinien realizować wszystko z poprzednich poziomów, a dodatkowo:

* zawierać klasę `ConfigSectionIterator`, która implementuje protokół iteratora (`__iter__` i `__next__`),
* iterator powinien przechodzić po sekcjach konfiguracji (klucze najwyższego poziomu) i zwracać krotki `(nazwa_sekcji, dict)`,
* rzucać StopIteration po wyczerpaniu sekcji,
* używać dataclass do reprezentowania sekcji konfiguracji,
* końcowy obiekt konfiguracji powinien być niemutowalny `(frozen=True)`.

**Szkielet klasy iteratora**

```python
class ConfigSectionIterator:
    def __init__(self, config: dict):
        self._sections = list(config.items())
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._sections):
            raise StopIteration
        section = self._sections[self._index]
        self._index += 1
        return section
```

**Wymagania dotyczące dataclass**

```python
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class AppConfig:
    name: str
    debug: bool

@dataclass(slots=True, frozen=True)
class ServerConfig:
    host: str
    port: int
    timeout: int

@dataclass(slots=True, frozen=True)
class AppConfiguration:
    app: AppConfig
    server: ServerConfig
    # ...
```

**Wymagania dotyczące użycia iteratora**

```python
iterator = ConfigSectionIterator(config)

for section_name, section_data in iterator:
    print(f"Przetwarzam sekcję: {section_name}")
    # parsuj section_data do odpowiedniego dataclass
```

**Efekt końcowy**

```
Przetwarzam sekcję: app
Przetwarzam sekcję: server
Przetwarzam sekcję: database

Konfiguracja załadowana:
  AppConfig(name='MojaAplikacja', debug=True)
  ServerConfig(host='127.0.0.1', port=8080, timeout=30)

Konfiguracja jest niemutowalna — próba modyfikacji zakończy się błędem.
```

## **Zadanie dodatkowe – Generator walidujący z protokołem `send()`**

**Cel**

Zbuduj generator, który waliduje kolejne pola konfiguracji i umożliwia dwukierunkową komunikację przy użyciu `.send()`.

**Założenia**

Generator validate_fields() powinien:

* przyjmować listę wymaganych ścieżek (np. `"server.host"`, `"database.credentials.password"`),
* dla każdej ścieżki sprawdzać, czy istnieje w spłaszczonej konfiguracji,
* używać `yield` do zwracania wyniku walidacji kolejnego pola (np. `True/False`),
* przyjmować przez `.send()` informację, czy kontynuować walidację czy ją przerwać.

**Szkielet generatora**

```python
def validate_fields(flat_config: dict, required_paths: list[str]):
    for path in required_paths:
        exists = path in flat_config
        should_continue = yield (path, exists)
        if should_continue is False:
            print("Walidacja przerwana przez użytkownika.")
            return
```

**Wymagania dotyczące użycia**

```python
required = [
    "app.name", "app.debug",
    "server.host", "server.port",
    "database.credentials.user", "database.credentials.password"
]

# Spłaszczona konfiguracja ze wszystkimi ścieżkami jako klucze
flat = dict(flatten_config(config))

validator = validate_fields(flat, required)

# Pierwsze wywołanie - inicjalizacja generatora
result = next(validator)

while True:
    path, exists = result
    status = "OK" if exists else "BRAK"
    print(f"  {path}: {status}")

    try:
        # Zdecyduj czy kontynuować (możesz wysłać False aby przerwać)
        result = validator.send(True)
    except StopIteration:
        break

print("Walidacja zakończona.")
```

**Efekt końcowy**

```
Walidacja pól konfiguracji:
  app.name: OK
  app.debug: OK
  server.host: OK
  server.port: OK
  database.credentials.user: OK
  database.credentials.password: OK

Walidacja zakończona.
```
W przypadku brakującego pola:
```
  database.credentials.password: BRAK
```