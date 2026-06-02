"""Excepciones de validacion usadas por los modelos."""

from __future__ import annotations


class ValidationError(ValueError):
    """Error base para validaciones de dominio."""


class CampoRequeridoError(ValidationError):
    """Indica que un campo obligatorio llego vacio."""

    def __init__(self, campo: str) -> None:
        super().__init__(f"El campo '{campo}' es obligatorio.")


class CorreoInvalidoError(ValidationError):
    """Indica que el correo no cumple el formato esperado."""

    def __init__(self, correo: str) -> None:
        super().__init__(f"El correo '{correo}' no es valido.")


class DuracionInvalidaError(ValidationError):
    """Indica que la duracion de una sesion no cumple el minimo."""

    def __init__(self, duracion: int, minimo: int) -> None:
        super().__init__(
            f"La duracion de {duracion} minutos es invalida; minimo {minimo}."
        )


class FechaInvalidaError(ValidationError):
    """Indica que una fecha o estado temporal no es valido."""
