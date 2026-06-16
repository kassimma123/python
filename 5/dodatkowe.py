from dataclasses import dataclass, fields
from abc import ABC, abstractmethod

#interfejs
class BaseConfigSection(ABC):
    @abstractmethod
    def validate(self) -> None:
        pass

    @abstractmethod
    def display(self) -> None:
        pass

#dynamiczna fabryka
class ConfigFactory:
    _registry = {}

    @classmethod
    def register(cls, section_name: str, section_class):
        """metoda pozwalajaca zapisac nowa klase do rejestru"""
        cls._registry[section_name] = section_class

    @classmethod
    def create_section(cls, section_name: str, data: dict) -> BaseConfigSection:
        """tworzy obiekt szukajac odpowiedniej klasy w rejestrze"""
        if section_name not in cls._registry:
            raise ValueError(f"Nie ma zdefiniowanej konfiguracji dla: {section_name}")
        
        return cls._registry[section_name](**data)


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
    
#nowa sekcja
@dataclass(slots=True, frozen=True)
class LoggingConfig(BaseConfigSection):
    level: str
    file: str

    def validate(self) -> None:
        if self.level not in ["INFO", "DEBUG", "ERROR"]:
            raise ValueError("Niepoprawny poziom logowania")

    def __str__(self) -> str:
        return ", ".join(
            f"{field.name}={getattr(self, field.name)!r}"
            for field in fields(self)
        )
    
    def display(self) -> None:
        print(f"LoggingConfig: {str(self)}")

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
    
    ConfigFactory.register("app", AppConfig)
    ConfigFactory.register("server", ServerConfig)
    ConfigFactory.register("database", DatabaseConfig)
    ConfigFactory.register("logging", LoggingConfig)

    config_data = {
        'app': {'name': 'MojaAplikacja', 'debug': True}, 
        'server': {'host': '127.0.0.1', 'port': 8080, 'timeout': 30}, 
        'database': {'db_name': 'moja_baza', 'user': 'admin'},
        'logging': {'level': 'INFO', 'file': '/var/log/app.log'} #nowe
    }

    parsed_sections = {}
    for section_name, section_data in config_data.items():
        obj =  ConfigFactory.create_section(section_name, section_data)
        parsed_sections[section_name] = obj

    app_config = ApplicationConfig(sections=parsed_sections)
    app_config.validate_all()
    app_config.display_all()
