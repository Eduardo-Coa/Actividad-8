"""Excepciones de dominio para la practica."""


class ErrorDominio(Exception):
    """Clase base para errores del dominio."""


class EstudianteInvalidoError(ErrorDominio):
    """Error lanzado cuando un estudiante no cumple reglas."""


class RepositorioNoSoportadoError(ErrorDominio):
    """Error lanzado cuando no existe fabrica para el repositorio."""
