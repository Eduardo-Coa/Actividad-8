"""Patrón Decorator: agrega logging transparente al repositorio."""

from __future__ import annotations

from datetime import datetime
from typing import List

from app.interfaces.i_repositorio_cuestionario import IRepositorioCuestionario
from app.models.cuestionario_phq9 import CuestionarioPHQ9


class RepositorioConLog(IRepositorioCuestionario):
    """Envuelve cualquier repositorio y registra cada operación en un log.

    No modifica la lógica del repositorio base; solo añade observabilidad.
    El cliente usa RepositorioConLog exactamente igual que el original.

    Args:
        repositorio: repositorio concreto a envolver.
    """

    def __init__(self, repositorio: IRepositorioCuestionario) -> None:
        self._repo = repositorio
        self._log: List[str] = []

    @property
    def log(self) -> List[str]:
        """Copia del registro de operaciones ejecutadas."""
        return list(self._log)

    def _registrar(self, operacion: str) -> None:
        marca = datetime.now().strftime("%H:%M:%S")
        self._log.append(f"[{marca}] {operacion}")

    def guardar(self, cuestionario: CuestionarioPHQ9) -> None:
        self._registrar(f"guardar -> {cuestionario.codigo_estudiante}")
        self._repo.guardar(cuestionario)

    def obtener_por_id(self, id_cuestionario: str) -> CuestionarioPHQ9:
        self._registrar(f"obtener_por_id -> {id_cuestionario[:8]}…")
        return self._repo.obtener_por_id(id_cuestionario)

    def obtener_todos(self) -> List[CuestionarioPHQ9]:
        self._registrar("obtener_todos")
        return self._repo.obtener_todos()

    def actualizar(self, cuestionario: CuestionarioPHQ9) -> None:
        self._registrar(f"actualizar -> {cuestionario.codigo_estudiante}")
        self._repo.actualizar(cuestionario)

    def eliminar(self, id_cuestionario: str) -> None:
        self._registrar(f"eliminar -> {id_cuestionario[:8]}…")
        self._repo.eliminar(id_cuestionario)

    def obtener_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]:
        self._registrar(f"obtener_por_estudiante -> {codigo_estudiante}")
        return self._repo.obtener_por_estudiante(codigo_estudiante)
