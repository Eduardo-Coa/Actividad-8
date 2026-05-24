"""Factory Method aplicado a repositorios de Estudiante."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.exceptions import RepositorioNoSoportadoError
from app.repositories.estudiante_repository import (
    EstudianteJsonRepository,
    EstudianteMemoryRepository,
    IEstudianteRepository,
)


class EstudianteRepositoryCreator(ABC):
    """Creator abstracto para repositorios de estudiantes."""

    @abstractmethod
    def crear_repositorio(self) -> IEstudianteRepository:
        """Crea un repositorio concreto.

        Returns:
            Repositorio de estudiantes.
        """


class MemoryRepositoryCreator(EstudianteRepositoryCreator):
    """Creator concreto para repositorios en memoria."""

    def crear_repositorio(self) -> IEstudianteRepository:
        """Crea un repositorio en memoria.

        Returns:
            Repositorio en memoria.
        """
        return EstudianteMemoryRepository()


class JsonRepositoryCreator(EstudianteRepositoryCreator):
    """Creator concreto para repositorios JSON."""

    def __init__(self, ruta: str = "data/estudiantes.json") -> None:
        self._ruta = ruta

    def crear_repositorio(self) -> IEstudianteRepository:
        """Crea un repositorio JSON.

        Returns:
            Repositorio JSON.
        """
        return EstudianteJsonRepository(self._ruta)


def obtener_creator(
    tipo_repositorio: str,
    ruta: str = "data/estudiantes.json",
) -> EstudianteRepositoryCreator:
    """Selecciona el creator segun el tipo de repositorio.

    Args:
        tipo_repositorio: memoria o json.
        ruta: ruta usada cuando el repositorio es JSON.

    Returns:
        Creator concreto.
    """
    tipo = tipo_repositorio.strip().lower()
    if tipo == "memoria":
        return MemoryRepositoryCreator()
    if tipo == "json":
        return JsonRepositoryCreator(ruta)
    raise RepositorioNoSoportadoError(
        f"Repositorio no soportado: {tipo_repositorio}."
    )
