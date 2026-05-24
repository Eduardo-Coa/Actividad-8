"""Contrato abstracto para el repositorio de CuestionarioPHQ9."""

from abc import ABC, abstractmethod
from typing import List

from app.models.cuestionario_phq9 import CuestionarioPHQ9


class IRepositorioCuestionario(ABC):
    """Define las operaciones CRUD para cualquier repositorio de PHQ-9."""

    @abstractmethod
    def guardar(self, cuestionario: CuestionarioPHQ9) -> None: ...

    @abstractmethod
    def obtener_por_id(self, id_cuestionario: str) -> CuestionarioPHQ9: ...

    @abstractmethod
    def obtener_todos(self) -> List[CuestionarioPHQ9]: ...

    @abstractmethod
    def actualizar(self, cuestionario: CuestionarioPHQ9) -> None: ...

    @abstractmethod
    def eliminar(self, id_cuestionario: str) -> None: ...

    @abstractmethod
    def obtener_por_estudiante(
        self, codigo_estudiante: str
    ) -> List[CuestionarioPHQ9]: ...
