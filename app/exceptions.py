"""Jerarquía de excepciones de dominio del sistema PHQ-9."""


class AppError(Exception):
    """Base de todas las excepciones de dominio."""

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)

    def __str__(self) -> str:
        return self.mensaje


class FechaInvalidaError(AppError):
    def __init__(self, detalle: str) -> None:
        super().__init__(f"Fecha inválida: {detalle}")


class PuntajeInvalidoError(AppError):
    def __init__(self, valor: int, rango_permitido: tuple[int, int]) -> None:
        minimo, maximo = rango_permitido
        super().__init__(
            f"Valor {valor} fuera del rango permitido [{minimo}, {maximo}]."
        )


class CuestionarioNoEncontradoError(AppError):
    def __init__(self, id_cuestionario: str) -> None:
        super().__init__(
            f"No se encontró el cuestionario con ID '{id_cuestionario}'."
        )
