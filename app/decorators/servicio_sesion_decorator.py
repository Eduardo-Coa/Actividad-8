"""Patron Decorator aplicado a sesiones y psicologos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from app.models.psicologo import Psicologo
from app.models.sesion_seguimiento import SesionSeguimiento


class ServicioSesionBase(ABC):
    """Componente base del Decorator para presentar sesiones.

    Definicion formal GoF: "Adjunta responsabilidades adicionales a un
    objeto dinamicamente. Los decoradores proporcionan una alternativa flexible
    a la subclasificacion para extender funcionalidad"
    (Gamma et al., Design Patterns, 1994).
    """

    @abstractmethod
    def describir(self, sesion: SesionSeguimiento, psicologo: Psicologo) -> str:
        """Retorna una descripcion de la sesion."""


class ServicioSesionConcreto(ServicioSesionBase):
    """Servicio concreto que formatea una sesion de seguimiento."""

    def describir(self, sesion: SesionSeguimiento, psicologo: Psicologo) -> str:
        return (
            f"Sesion {sesion.estado.value} para {sesion.codigo_estudiante} "
            f"con {psicologo.nombre} ({psicologo.especialidad}) "
            f"el {sesion.fecha_hora.strftime('%Y-%m-%d %H:%M')} "
            f"por {sesion.duracion_minutos} minutos."
        )


class DecoradorServicioSesion(ServicioSesionBase):
    """Clase base para decoradores de servicios de sesion."""

    def __init__(self, servicio: ServicioSesionBase) -> None:
        self._servicio = servicio

    def describir(self, sesion: SesionSeguimiento, psicologo: Psicologo) -> str:
        return self._servicio.describir(sesion, psicologo)


class DecoradorLog(DecoradorServicioSesion):
    """Agrega una marca de tiempo al resultado del servicio."""

    def describir(self, sesion: SesionSeguimiento, psicologo: Psicologo) -> str:
        resultado = super().describir(sesion, psicologo)
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{resultado}\nLog: descripcion generada en {marca}."


class DecoradorValidacion(DecoradorServicioSesion):
    """Valida consistencia entre la sesion y el psicologo antes de delegar."""

    def describir(self, sesion: SesionSeguimiento, psicologo: Psicologo) -> str:
        if sesion.id_psicologo != psicologo.id:
            raise ValueError("La sesion no pertenece al psicologo indicado.")
        return super().describir(sesion, psicologo)
