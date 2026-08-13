import re


def validate_password(password: str) -> str:
    if not password:
        raise ValueError("La contraseña es obligatoria")

    if len(password) < 8:
        raise ValueError(
            "La contraseña debe tener mínimo 8 caracteres"
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "La contraseña debe contener al menos una mayúscula"
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "La contraseña debe contener al menos una minúscula"
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "La contraseña debe contener al menos un número"
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", password):
        raise ValueError(
            "La contraseña debe contener al menos un carácter especial"
        )

    return password