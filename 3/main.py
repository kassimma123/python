import yaml
from dataclasses import dataclass

print("---POZIOM ŁATWY---\n")

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

print("--- DEBUG: Zawartość zmiennej config ---")
print(config)
print("----------------------------------------\n")

print("sekcje konfiguracji:")

for idx, section in enumerate(config.keys()):
    print(f"    [{idx}] {section}")

print("\nsekcja 'serwer':")

server_config = config['server']

keys = list(server_config.keys())
values = list(server_config.values())

for k, v in zip(keys, values):
    print(f" {k} -> {v}")

top_level_keys = [key for key in config]

print("\n--- DEBUG: Pobrane główne klucze ---")
print(top_level_keys)

print("\n---POZIOM ŚREDNI---")

def flatten_config(config_dict, prefix=""):
    for key, value in config_dict.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            yield from flatten_config(value, full_key)
        else:
            yield full_key, value 

gen = flatten_config(config)

first = next(gen)
print(f"Pierwsza wartość: {first[0]} = {first[1]}\n")

print("Pozostałe pola:")
for path, value in gen:
    print(f"    {path} = {value}")

print("/n---POZIOM TRUDNY---")

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
class DatabaseConfig:
    credentials: dict
    settings: dict

@dataclass(slots=True, frozen=True)
class AppConfiguration:
    app: AppConfig
    server: ServerConfig
    database: DatabaseConfig

class ConfigSectionIterator:
    def __init__(self, config_dict: dict):
        self._sections = list(config_dict.items())
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._sections):
            raise StopIteration
        
        section = self._sections[self._index]
        self._index+= 1
        return section
iterator = ConfigSectionIterator(config)

parsed_sections = {}

for section_name, section_data in iterator:
    print(f"Przetwarzam sekcję: {section_name}")
    
    if section_name == "app":
        parsed_sections["app"] = AppConfig(**section_data)
    elif section_name == "server":
        parsed_sections["server"] = ServerConfig(**section_data)
    elif section_name == "database":
        parsed_sections["database"] = DatabaseConfig(**section_data)

final_config = AppConfiguration(**parsed_sections)

print("\nKonfiguracja załadowana:")
print(f"  {final_config.app}")
print(f"  {final_config.server}")
print(f"  {final_config.database}")


print("\n--- ZADANIE DODATKOWE (SEND) ---")

def validate_fields(flat_config: dict, required_paths: list[str]):
    for path in required_paths:
        exists = path in flat_config
        should_continue = yield (path, exists)
        
        if should_continue is False:
            print("Walidacja przerwana przez użytkownika.")
            return

required = [
    "app.name", "app.debug",
    "server.host", "server.port",
    "database.credentials.user", "database.credentials.password"
]

flat = dict(flatten_config(config))

validator = validate_fields(flat, required)

print("Walidacja pól konfiguracji:")
result = next(validator)

while True:
    path, exists = result
    status = "OK" if exists else "BRAK"
    print(f"  {path}: {status}")

    try:
        result = validator.send(True)
    except StopIteration:
        break

print("\nWalidacja zakończona.")