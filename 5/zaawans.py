from abc import ABC , abstractmethod
from dataclasses import dataclass, fields
from enum import StrEnum
import yaml
from pathlib import Path


class SectionType(StrEnum):
    APP = "app"
    SERVER = "server"
    DATABASE = "database"

class BaseConfigSection(ABC): #Abstract Base Class

    #klasa abstrakcyjna wymuszająca interfejs dla kazdej sekcji konfiguracji
    @abstractmethod
    def validate(self) -> None:
        """każda sekcja musi implementować walidacje"""
        pass

    @abstractmethod
    def display(self) -> None:
        """każda sekcja musi umieć się wyświetlić"""
        pass

#fabryka
class ConfigFactory:
    @staticmethod
    def create_section(section_name: str, data: dict) -> BaseConfigSection:
        try:
            section = SectionType(section_name.lower())
        except ValueError:
            raise ValueError(f"nieznana sekcja konfiguracji: '{section_name}'")

        match section:
            case SectionType.APP:
                return AppConfig(**data)
            case SectionType.SERVER:
                return ServerConfig(**data)
            case SectionType.DATABASE:
                return DatabaseConfig(**data)
            case _:
                raise NotImplementedError(f"brak implementacji dla sekcji: {section}")


#konfiguracja aplikacji
@dataclass(slots=True, frozen=True)
class AppConfig(BaseConfigSection):
    name: str
    debug: bool

    def validate(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("Pole name musi być typu string")
        if not isinstance(self.debug, bool):
            raise TypeError("Pole debug musi być typu bool")

        if not self.name:
            raise ValueError("Pole name nie może być puste")
        if len(self.name) < 3:
            raise ValueError("Pole name musi mieć co najmniej 3 znaki")
        if not self.name.isalpha():
            raise ValueError("Pole musi sie skladac z samych liter ")

    def __str__(self) -> str:
        return ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )
    
    def display(self) -> None:
        print(f"AppConfig: {str(self)}")

#konfiguracja serwera
@dataclass(slots=True, frozen=True)
class ServerConfig(BaseConfigSection):
    host: str
    port: int
    timeout: int 

    def validate(self) -> None:
        if not isinstance(self.host, str):
            raise TypeError("host musi być string")
        if not isinstance(self.port, int):
            raise TypeError("port musi byc integerem")
        if not isinstance(self.timeout, int):
            raise TypeError("timeout musi byc integerem")

        if not self.host:
            raise ValueError("host nie moze byc pusty")
        if not (1 <= self.port <= 65535):
            raise ValueError("port musi byc pomiedzy 1 a 65535")
        if self.timeout <= 0:
            raise ValueError("timeout musi byc > 0")

    def __str__(self) -> str:
        return ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )
    
    def display(self) -> None:
        print(f"ServerConfig: {str(self)}")

#konfiguracja bazy danych
@dataclass(slots=True, frozen=True)
class DatabaseConfig(BaseConfigSection):
    db_name: str
    user: str

    def validate(self) -> None:
        if not isinstance(self.db_name, str):
            raise TypeError("db_name musi byc stringiem")
        if not isinstance(self.user, str):
            raise TypeError("user musi byc stringiem")

        if not self.db_name:
            raise ValueError("db_name nie moze byc pusty")
        if not self.user:
            raise ValueError("user nie moze byc pusty")

    def __str__(self) -> str:
        return ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )
    
    def display(self) -> None:
        print(f"DatabaseConfig: {str(self)}")
    
#klasa zbiorcza
@dataclass(slots=True, frozen=False)
class ApplicationConfig:
    sections: dict[str, BaseConfigSection]

    def validate_all(self) -> None:
        print("rozpoczynam globalną walidacje...")
        for section in self.sections.values():
            section.validate()
        print("walidacja zakonczona sukcesem")
    
    def display_all(self) -> None:
        print("\n---pełna konfiguracja aplikacji---")
        for name, section in self.sections.items():
            print(f"[{name.upper()}]")
            section.display()


#główny program       
if __name__ == "__main__":
    #plik yaml
    current_dir = Path(__file__).parent
    config_path = current_dir / "config.yaml"

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku config.yaml w ścieżce: {config_path}")
        exit(1)

    #tworzenie obiektów przez fabryke
    parsed_sections = {}
    for section_name, section_data in config_data.items():
        obj = ConfigFactory.create_section(section_name, section_data)
        parsed_sections[section_name] = obj

    #utworzenie głównego obiektu aplikacji
    app_config = ApplicationConfig(sections=parsed_sections)

    #zwalidowanie całości
    app_config.validate_all()

    #wyświetlanie całości
    app_config.display_all()    


