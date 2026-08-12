import pytest

from app.core.security.password_policy import validate_password


def test_password_valida():
    assert validate_password("Carlos123!") == "Carlos123!"


def test_password_vacia():
    with pytest.raises(ValueError):
        validate_password("")


def test_password_menor_a_8():
    with pytest.raises(ValueError):
        validate_password("Car1!")


def test_password_sin_mayuscula():
    with pytest.raises(ValueError):
        validate_password("carlos123!")


def test_password_sin_minuscula():
    with pytest.raises(ValueError):
        validate_password("CARLOS123!")


def test_password_sin_numero():
    with pytest.raises(ValueError):
        validate_password("CarlosABC!")


def test_password_sin_caracter_especial():
    with pytest.raises(ValueError):
        validate_password("Carlos123")