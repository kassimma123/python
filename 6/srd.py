
#def własnych wątków
class NoSeatsAvailableError(Exception):
    pass
class AlreadyReservedError(Exception):
    pass
class ReservationNotFoundError(Exception):
    pass

#główna klasa systemu rezerwacji
class ReservationSystem:
    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.reservations = set()
    
    def reserve(self, user_id):
        if user_id in self.reservations:
            raise AlreadyReservedError("ten uzytkownik ma juz rezerwacje")

        if len(self.reservations) >= self.total_seats:
            raise NoSeatsAvailableError("brak wolnych miejsc na wydarzenie")
        
        self.reservations.add(user_id)
        
    def cancel(self, user_id):
        if user_id not in self.reservations:
            raise ReservationNotFoundError("nie znaeziono rezerwacji do anulowania")
        self.reservations.remove(user_id)

    def available_seats(self):
        return self.total_seats - len(self.reservations)

    def is_reserved(self, user_id):
        return user_id in self.reservations