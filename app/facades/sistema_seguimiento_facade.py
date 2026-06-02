"""Patron Facade aplicado a psicologos y sesiones de seguimiento."""

from __future__ import annotations

from datetime import datetime

from app.models.psicologo import Psicologo
from app.models.sesion_seguimiento import SesionSeguimiento


class SistemaSeguimientoFacade:
    """Interfaz simple para programar sesiones con psicologos.

    Definicion formal GoF: "Proporciona una interfaz unificada para un
    conjunto de interfaces en un subsistema. Facade define una interfaz de
    mayor nivel que hace que el subsistema sea mas facil de usar"
    (Gamma et al., Design Patterns, 1994).

    Esta fachada oculta al cliente la creacion de modelos, validaciones
    internas y almacenamiento en memoria usados para la practica.
    """

    def __init__(self) -> None:
        self._psicologos: dict[str, Psicologo] = {}
        self._sesiones: dict[str, SesionSeguimiento] = {}

    def registrar_psicologo(
        self,
        id_psicologo: str,
        nombre: str,
        correo: str,
        especialidad: str,
    ) -> Psicologo:
        """Crea y almacena un psicologo validado."""
        psicologo = Psicologo(
            id=id_psicologo,
            nombre=nombre,
            correo=correo,
            especialidad=especialidad,
        )
        self._psicologos[psicologo.id] = psicologo
        return psicologo

    def agendar_sesion(
        self,
        codigo_estudiante: str,
        id_psicologo: str,
        fecha_hora: datetime,
        duracion_minutos: int,
        motivo: str,
    ) -> SesionSeguimiento:
        """Crea una sesion si el psicologo existe y guarda el resultado."""
        if id_psicologo not in self._psicologos:
            raise ValueError(f"No existe un psicologo con id '{id_psicologo}'.")

        sesion = SesionSeguimiento(
            codigo_estudiante=codigo_estudiante,
            id_psicologo=id_psicologo,
            fecha_hora=fecha_hora,
            duracion_minutos=duracion_minutos,
            motivo=motivo,
        )
        self._sesiones[sesion.id] = sesion
        return sesion

    def sesiones_por_estudiante(self, codigo_estudiante: str) -> list[SesionSeguimiento]:
        """Retorna las sesiones asociadas a un estudiante."""
        return [
            sesion
            for sesion in self._sesiones.values()
            if sesion.codigo_estudiante == codigo_estudiante
        ]

    def resumen(self) -> dict[str, int]:
        """Entrega un resumen general del subsistema de seguimiento."""
        return {
            "psicologos": len(self._psicologos),
            "sesiones": len(self._sesiones),
        }
