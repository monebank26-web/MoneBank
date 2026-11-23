from app.shared.exceptions.base import BusinessError


class ChatInvalido(BusinessError):
    message = "El historial del chat contiene turnos inválidos"


class ConsejoIANoDisponible(BusinessError):
    message = "El servicio de consejos de IA no está disponible en este momento"