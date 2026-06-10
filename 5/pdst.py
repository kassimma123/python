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


