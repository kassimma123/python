
import pytest
from srd import ReservationSystem, AlreadyReservedError, ReservationNotFoundError

def test_successful_reservation():
    system = ReservationSystem(5)
    system.reserve("user1")

    assert system.is_reserved("user_1") == True
    assert system.available_seats() == 4

def test_successful_canselation():
    system = ReservationSystem(2)
    system.reserve("user1")
    system.cancel("user_1")

    assert system.is_reserved("user_1") == False
    assert system.available_seats() == 2

def test_reserve_no_seats_available():
    system = ReservationSystem(1)
    system.reserve("user1")

    with pytest.raises(AlreadyReservedError):
        system.reserve("user_2")

def test_reserve_already_reserved():
    system = ReservationSystem(5)
    system.reserve("user_1")

    with pytest.raises(AlreadyReservedError):
        system.reserve("user_1")


def test_cancel_non_existent_reservation():
    system = ReservationSystem(5)

    with pytest.raises(ReservationNotFoundError):
        system.cancel("ghost_user")
    

    
    
