"""Repositorios para la entidad Estudiante."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
from pathlib import Path

from app.models.estudiante import Estudiante


class IEstudianteRepository(ABC):
    """Contrato comun para repositorios de estudiantes."""

    @abstractmethod
    def guardar(self, estudiante: Estudiante) -> None:
        """Guarda un estudiante.

        Args:
            estudiante: estudiante validado.
        """

    @abstractmethod
    def listar(self) -> list[Estudiante]:
        """Lista los estudiantes registrados.

        Returns:
            Lista de estudiantes.
        """


class EstudianteMemoryRepository(IEstudianteRepository):
    """Repositorio en memoria para pruebas rapidas."""

    def __init__(self) -> None:
        self._estudiantes: dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> None:
        """Guarda o reemplaza un estudiante por codigo.

        Args:
            estudiante: estudiante validado.
        """
        self._estudiantes[estudiante.codigo] = estudiante

    def listar(self) -> list[Estudiante]:
        """Lista estudiantes en memoria.

        Returns:
            Lista ordenada por codigo.
        """
        return [
            self._estudiantes[codigo]
            for codigo in sorted(self._estudiantes)
        ]


class EstudianteJsonRepository(IEstudianteRepository):
    """Repositorio JSON para persistir estudiantes."""

    def __init__(self, ruta: str = "data/estudiantes.json") -> None:
        self._ruta = Path(ruta)
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        if not self._ruta.exists():
            self._ruta.write_text("[]", encoding="utf-8")

    def guardar(self, estudiante: Estudiante) -> None:
        """Guarda o reemplaza un estudiante en JSON.

        Args:
            estudiante: estudiante validado.
        """
        estudiantes = {item.codigo: item for item in self.listar()}
        estudiantes[estudiante.codigo] = estudiante
        data = [item.to_dict() for item in estudiantes.values()]
        self._ruta.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def listar(self) -> list[Estudiante]:
        """Lista estudiantes guardados en JSON.

        Returns:
            Lista de estudiantes.
        """
        data = json.loads(self._ruta.read_text(encoding="utf-8"))
        return [Estudiante.from_dict(item) for item in data]
