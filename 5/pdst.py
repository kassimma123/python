from dataclasses import dataclass, fields

class BaseConfigSection: #pusta klasa bazowa
    pass

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
            
if __name__ == "__main__":
    app = AppConfig(name="MojaAplikacja", debug = True)
    app.validate()
    app.display()

    server = ServerConfig(host="127.0.0.1", port = 8000, timeout=30)
    server.validate()
    server.display()

    db = DatabaseConfig(db_name="produkcja_db", user = "admin")
    db.validate()
    db.display()
    
    