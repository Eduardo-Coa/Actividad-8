"""Patrón Command: encapsula operaciones CRUD con soporte de undo."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from app.interfaces.i_repositorio_cuestionario import IRepositorioCuestionario
from app.models.cuestionario_phq9 import CuestionarioPHQ9


class IComando(ABC):
    """Interfaz base para todos los comandos del sistema."""

    @abstractmethod
    def ejecutar(self) -> None:
        """Ejecuta la operación encapsulada."""

    @abstractmethod
    def deshacer(self) -> None:
        """Revierte la operación ejecutada."""


class RegistrarCuestionarioComando(IComando):
    """Guarda un cuestionario; su undo lo elimina.

    Args:
        repositorio: repositorio de persistencia.
        cuestionario: cuestionario a guardar.
    """

    def __init__(
        self,
        repositorio: IRepositorioCuestionario,
        cuestionario: CuestionarioPHQ9,
    ) -> None:
        self._repositorio = repositorio
        self._cuestionario = cuestionario

    def ejecutar(self) -> None:
        self._repositorio.guardar(self._cuestionario)

    def deshacer(self) -> None:
        self._repositorio.eliminar(self._cuestionario.id)


class EliminarCuestionarioComando(IComando):
    """Elimina un cuestionario; su undo lo restaura del respaldo.

    Args:
        repositorio: repositorio de persistencia.
        id_cuestionario: ID del registro a eliminar.
    """

    def __init__(
        self,
        repositorio: IRepositorioCuestionario,
        id_cuestionario: str,
    ) -> None:
        self._repositorio = repositorio
        self._id = id_cuestionario
        self._respaldo: Optional[CuestionarioPHQ9] = None

    def ejecutar(self) -> None:
        self._respaldo = self._repositorio.obtener_por_id(self._id)
        self._repositorio.eliminar(self._id)

    def deshacer(self) -> None:
        if self._respaldo is not None:
            self._repositorio.guardar(self._respaldo)


class HistorialComandos:
    """Pila LIFO de comandos ejecutados; permite deshacer en orden inverso.

    Desacopla al cliente de los detalles de cada operación reversible.
    """

    def __init__(self) -> None:
        self._pila: List[IComando] = []

    def ejecutar(self, comando: IComando) -> None:
        """Ejecuta el comando y lo apila para poder deshacerlo."""
        comando.ejecutar()
        self._pila.append(comando)

    def deshacer(self) -> None:
        """Deshace el último comando; no hace nada si el historial está vacío."""
        if self._pila:
            self._pila.pop().deshacer()

    @property
    def hay_comandos(self) -> bool:
        """True si hay al menos un comando en el historial."""
        return bool(self._pila)
