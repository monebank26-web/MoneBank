from datetime import datetime

import pytest

from app.modules.auth.domain.entity import intento_autenticacion


FECHA_FIJA = datetime(2026, 1, 15, 12, 0)


class DatetimeFija(datetime):
    @classmethod
    def now(cls, tz=None):
        if tz is None:
            return FECHA_FIJA
        return FECHA_FIJA.replace(tzinfo=tz)


@pytest.fixture
def reloj_fijo(monkeypatch):
    monkeypatch.setattr(intento_autenticacion, "datetime", DatetimeFija)
    return FECHA_FIJA
