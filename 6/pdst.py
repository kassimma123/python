
def validate_user(name, age, email):
    if not name:
        raise ValueError("poadaj imie")

    if type(age) is not int:
        raise ValueError("wiek musi byc liczba calkowita")
    
    if age < 18:
        raise ValueError("osoba musi miec conajmniej 18 lat")
    
    if "@" not in email:
        raise ValueError("adres e-mail musi zawierac @")

    at_index = email.index("@")
    if "." not in email[at_index+1:]:
        raise ValueError("adres e-mail musi zawierać kropke po @")

    return True

    
