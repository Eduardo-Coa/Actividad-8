"""Repositorio en memoria: implementación para pruebas y demostraciones."""

from __future__ import annotations

from typing import Dict, List

from app.exceptions import CuestionarioNoEncontradoError
from app.interfaces.i_repositorio_cuestionario import IRepositorioCuestionario
from app.models.cuestionario_phq9 import CuestionarioPHQ9


class RepositorioMemoria(IRepositorioCuestionario):
    """Almacena cuestionarios en RAM. No persiste entre ejecuciones."""

    def __init__(self) -> None:
        self._datos: Dict[str, CuestionarioPHQ9] = {}

    def guardar(self, cuestionario: CuestionarioPHQ9) -> None:
        self._datos[cuestionario.id] = cuestionario

    def obtener_por_id(self, id_cuestionario: str) -> CuestionarioPHQ9:
        if id_cuestionario not in self._datos:
            raise CuestionarioNoEncontradoError(id_cuestionario)
        return self._datos[id_cuestionario]

    def obtener_todos(self) -> List[CuestionarioPHQ9]:
        return list(self._datos.values())

    def actualizar(self, cuestionario: CuestionarioPHQ9) -> None:
        if cuestionario.id not in self._datos:
            raise CuestionarioNoEncontradoError(cuestionario.id)
        self._datos[cuestionario.id] = cuestionario

    def eliminar(self, id_cuestionario: str) -> None:
        if id_cuestionario not in self._datos:
            raise CuestionarioNoEncontradoError(id_cuestionario)
        del self._datos[id_cuestionario]

    def obtener_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]:
        return [
            c for c in self._datos.values()
            if c.codigo_estudiante == codigo_estudiante
        ]
