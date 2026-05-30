import argparse
import yaml
from pathlib import Path
import sys

def load_yaml_config(file_path: Path) -> dict:
    if not file_path.exists():
        print(f"błąd: plik nie istnieje {file_path}" )
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file) or {}
    except yaml.YAMLError as exc:
        print(f"błąd podczas parsowania pliku YAML: {exc}")
        sys.exit(1)
    except Exception as e:
        print(f"wystąpił nieoczekiwany błąd podczas odczytu: {e}")
        sys.exit(1)

def print_config(config_dict: dict, indent: int = 0):
    for key, value in config_dict.items():
        prefix = " " * indent
        if isinstance(value, dict):
            print(f"{prefix}{key}: ")
            print_config(value, indent + 1)
        else:
            print(f"{prefix}{key}: {value}")
        

def validate_config(config_dict: dict) -> bool:
    required_keys = [
        "app.name",
        "app.debug",
        "server.host",
        "server.port",
        "database.credentials.user",
        "database.credentials.password"
    ]
    is_valid = True
    for path in required_keys:
        keys = path.split('.')
        current_level = config_dict

        for key in keys:
            if isinstance(current_level, dict) and key in current_level:
                current_level = current_level[key]
            else:
                print(f"> brak klucza: {path}")
                is_valid = False
                break
    if is_valid:
        print("> konfiguracja jest poprawna")
    return is_valid

        

def main():
    parser = argparse.ArgumentParser(description="wczytywanie konfiguracji YAML")

    parser.add_argument(
        "--config", 
        type=Path, 
        required=True,
        help="ściezka do pliku konfiguracyjnego YAML"
    )

    args = parser.parse_args()
    config_path = args.config

    config = load_yaml_config(config_path)
    print_config(config)
    print("--------------------------\n")

    validate_config(config)


if __name__ == "__main__":
    main()