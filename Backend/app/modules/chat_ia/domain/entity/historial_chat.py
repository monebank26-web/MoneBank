from app.shared.exceptions.business_exceptions import ChatInvalido


class HistorialChat:

    ROLES_VALIDOS = {"user", "model"}
    MAX_TURNOS = 12

    def __init__(self, turnos_wire):
        self.turnos_wire = self._validar(turnos_wire)
        self._gemini = [self._wire_a_gemini(t) for t in self.turnos_wire]

    def _validar(self, turnos):
        if not isinstance(turnos, list):
            raise ChatInvalido()
        for turno in turnos:
            if not isinstance(turno, dict):
                raise ChatInvalido()
            if turno.get("rol") not in self.ROLES_VALIDOS:
                raise ChatInvalido()
            if not isinstance(turno.get("texto", ""), str):
                raise ChatInvalido()
        return turnos[-self.MAX_TURNOS:]

    def _wire_a_gemini(self, turno_wire):
        return {
            "role": turno_wire["rol"],
            "parts": [{"text": turno_wire["texto"]}],
        }

    def agregar(self, turno_wire):
        self.turnos_wire = (self.turnos_wire + [turno_wire])[-self.MAX_TURNOS:]
        self._gemini = [self._wire_a_gemini(t) for t in self.turnos_wire]
        return self._gemini

    @property
    def contenido_gemini(self):
        return self._gemini
