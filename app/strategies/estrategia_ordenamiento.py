"""Patrón Strategy: algoritmos de ordenamiento intercambiables."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.models.cuestionario_phq9 import CuestionarioPHQ9


class IEstrategiaOrdenamiento(ABC):
    """Interfaz común para todas las estrategias de ordenamiento."""

    @abstractmethod
    def ordenar(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> List[CuestionarioPHQ9]:
        """Retorna una nueva lista ordenada sin modificar la original."""


class OrdenarPorFechaDesc(IEstrategiaOrdenamiento):
    """De más reciente a más antiguo."""

    def ordenar(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> List[CuestionarioPHQ9]:
        return sorted(
            cuestionarios, key=lambda c: c.fecha_aplicacion, reverse=True
        )


class OrdenarPorPuntajeDesc(IEstrategiaOrdenamiento):
    """De mayor a menor puntaje (casos más severos primero)."""

    def ordenar(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> List[CuestionarioPHQ9]:
        return sorted(
            cuestionarios, key=lambda c: c.puntaje_total, reverse=True
        )


class OrdenarPorCodigoAsc(IEstrategiaOrdenamiento):
    """Alfabéticamente por código de estudiante."""

    def ordenar(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> List[CuestionarioPHQ9]:
        return sorted(cuestionarios, key=lambda c: c.codigo_estudiante)


class ListadorCuestionarios:
    """Contexto que delega el ordenamiento a una IEstrategiaOrdenamiento.

    Permite cambiar el algoritmo de ordenamiento en tiempo de ejecución
    sin modificar el código del cliente.

    Args:
        estrategia: algoritmo de ordenamiento inicial.
    """

    def __init__(self, estrategia: IEstrategiaOrdenamiento) -> None:
        self._estrategia = estrategia

    def cambiar_estrategia(
        self, estrategia: IEstrategiaOrdenamiento
    ) -> None:
        """Sustituye la estrategia activa en tiempo de ejecución."""
        self._estrategia = estrategia

    def listar(
        self, cuestionarios: List[CuestionarioPHQ9]
    ) -> List[CuestionarioPHQ9]:
        """Aplica la estrategia activa y retorna la lista ordenada."""
        return self._estrategia.ordenar(cuestionarios)
