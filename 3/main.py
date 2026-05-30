import argparse
import sys
import yaml
from dataclasses import dataclass
from typing import Generator, Any

# Typ pomocniczy dla spłaszczonej konfiguracji
FlatConfig = dict[str, Any]

# --- MODELE DANYCH (KLASY KONFIGURACYJNE) ---
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


# --- KLASY POMOCNICZE / GENERATORY ---
class ConfigSectionIterator:
    def __init__(self, config_dict: dict[str, Any]):
        self._sections = list(config_dict.items())
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self) -> tuple[str, Any]:
        if self._index >= len(self._sections):
            raise StopIteration
        
        section = self._sections[self._index]
        self._index += 1
        return section


def flatten_config(config_dict: dict[str, Any], prefix: str = "") -> Generator[tuple[str, Any], None, None]:
    for key, value in config_dict.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            yield from flatten_config(value, full_key)
        else:
            yield full_key, value 


def validate_fields(flat_config: FlatConfig, required_paths: list[str]) -> Generator[tuple[str, bool], bool, None]:
    for path in required_paths:
        exists = path in flat_config
        should_continue = yield (path, exists)
        
        if should_continue is False:
            print("Walidacja przerwana przez użytkownika.")
            return


# --- FUNKCJE-SEKCJE (PODZIAŁ NA PODZADANIA) ---

def poziom_latwy(config: dict[str, Any]) -> None:
    print("---POZIOM ŁATWY---\n")
    print("--- DEBUG: Zawartość zmiennej config ---")
    print(config)
    print("----------------------------------------\n")
    
    print("sekcje konfiguracji:")
    for idx, section in enumerate(config.keys()):
        print(f"\t[{idx}] {section}")
    
    print("\nsekcja 'serwer':")
    server_config = config['server']
    keys = list(server_config.keys())
    values = list(server_config.values())
    
    for k, v in zip(keys, values):
        print(f"\t{k} -> {v}")
    
    top_level_keys = [key for key in config]
    print("\n--- DEBUG: Pobrane główne klucze ---")
    print(top_level_keys)


def poziom_sredni(config: dict[str, Any]) -> None:
    print("\n---POZIOM ŚREDNI---")
    gen = flatten_config(config)
    
    first = next(gen)
    print(f"Pierwsza wartość: {first[0]} = {first[1]}\n")
    
    print("Pozostałe pola:")
    for path, value in gen:
        print(f"\t{path} = {value}")


def poziom_trudny(config: dict[str, Any]) -> None:
    print("\n---POZIOM TRUDNY---")
    iterator = ConfigSectionIterator(config)
    parsed_sections = {}
    
    for section_name, section_data in iterator:
        print(f"Przetwarzam sekcję: {section_name}")
        
        # Zastąpienie if-elif na match-case
        match section_name:
            case "app":
                parsed_sections["app"] = AppConfig(**section_data)
            case "server":
                parsed_sections["server"] = ServerConfig(**section_data)
            case "database":
                parsed_sections["database"] = DatabaseConfig(**section_data)
    
    final_config = AppConfiguration(**parsed_sections)
    
    print("\nKonfiguracja załadowana:")
    print(f"\t{final_config.app}")
    print(f"\t{final_config.server}")
    print(f"\t{final_config.database}")


def zadanie_dodatkowe(config: dict[str, Any]) -> None:
    print("\n--- ZADANIE DODATKOWE (SEND) ---")
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
        print(f"\t{path}: {status}")
    
        try:
            result = validator.send(True)
        except StopIteration:
            break
            
    print("\nWalidacja zakończona.")


# --- GŁÓWNY PUNKT WEJŚCIA SKRYPTU ---

def main() -> None:
    # Wykorzystanie argparse zamiast zhardkodowanej ścieżki
    parser = argparse.ArgumentParser(description="Wczytywanie i walidacja konfiguracji YAML")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Ścieżka do pliku konfiguracyjnego YAML (domyślnie: config.yaml)"
    )
    
    args = parser.parse_args()
    
    try:
        with open(args.config, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku konfiguracji pod ścieżką: {args.config}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Błąd podczas parsowania pliku YAML: {exc}")
        sys.exit(1)
        
    # Uruchomienie poszczególnych sekcji
    poziom_latwy(config)
    poziom_sredni(config)
    poziom_trudny(config)
    zadanie_dodatkowe(config)


if __name__ == "__main__":
    main()