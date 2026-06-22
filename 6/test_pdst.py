import pytest
from pdst import validate_user


def test_valid_user():
    assert validate_user("Arron", 20, "aronekMASEŁKO@gmail.com") == True

def test_empty_name():
    with pytest.raises(ValueError):
        validate_user("", 20, "aronekMASEŁKO@gmail.com")

def test_too_low_age():
    with pytest.raises(ValueError):
        validate_user("Arron", 17, "aronekMASEŁKO@gmail.com")

def test_invalid_age_type():
    with pytest.raises(ValueError):
        validate_user("Arron", "20", "aronekMASEŁKO@gmail.com")

def test_email_without_at():
    with pytest.raises(ValueError):
        validate_user("Arron", 20, "aronekMASEŁKOgmail.com")

def test_email_without_dot():
    with pytest.raises(ValueError):
        validate_user("Arron", 20, "aronek.M.A.S.E.Ł.K.O@gmailcom")



