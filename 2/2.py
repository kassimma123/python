import argparse
import yaml
from pathlib import Path

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

    if not config_path.exists():
        print(f"błąd: plik '{config_path}' nie istnieje")
        return
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)

            print("pomyślnie wczytano do słownika (dict):")
            print(config)

    except yaml.YAMLError as exc:
        print(f"błąd podczas parsowania pliku YAML: {exc}")
    except Exception as e:
        print(f"wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    main()