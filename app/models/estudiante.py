"""Entidad Estudiante del proyecto de apoyo psicologico."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import Any

from app.exceptions import EstudianteInvalidoError

EDAD_MINIMA = 14
EDAD_MAXIMA = 100
SEMESTRE_MINIMO = 1
SEMESTRE_MAXIMO = 12
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Estudiante:
    """Representa un estudiante del sistema de apoyo psicologico.

    Args:
        codigo: codigo institucional unico.
        nombre_completo: nombres y apellidos.
        edad: edad del estudiante.
        semestre: semestre academico actual.
        correo: correo valido del estudiante.
        programa: programa academico.
        fecha_registro: fecha de creacion del registro.
    """

    codigo: str
    nombre_completo: str
    edad: int
    semestre: int
    correo: str
    programa: str
    fecha_registro: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "codigo", self.codigo.strip().upper())
        object.__setattr__(
            self,
            "nombre_completo",
            self.nombre_completo.strip(),
        )
        object.__setattr__(self, "correo", self.correo.strip().lower())
        object.__setattr__(self, "programa", self.programa.strip())
        self._validar()

    def _validar(self) -> None:
        if not self.codigo:
            raise EstudianteInvalidoError("El codigo no puede estar vacio.")
        if not self.nombre_completo:
            raise EstudianteInvalidoError("El nombre no puede estar vacio.")
        if not EDAD_MINIMA <= self.edad <= EDAD_MAXIMA:
            raise EstudianteInvalidoError("La edad debe estar entre 14 y 100.")
        if not SEMESTRE_MINIMO <= self.semestre <= SEMESTRE_MAXIMO:
            raise EstudianteInvalidoError(
                "El semestre debe estar entre 1 y 12."
            )
        if not PATRON_CORREO.match(self.correo):
            raise EstudianteInvalidoError("El correo no tiene formato valido.")
        if not self.programa:
            raise EstudianteInvalidoError("El programa no puede estar vacio.")

    def to_dict(self) -> dict[str, Any]:
        """Convierte el estudiante en un diccionario serializable.

        Returns:
            Diccionario con los datos del estudiante.
        """
        return {
            "codigo": self.codigo,
            "nombre_completo": self.nombre_completo,
            "edad": self.edad,
            "semestre": self.semestre,
            "correo": self.correo,
            "programa": self.programa,
            "fecha_registro": self.fecha_registro.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Estudiante":
        """Crea un estudiante desde un diccionario.

        Args:
            data: datos previamente serializados.

        Returns:
            Estudiante validado.
        """
        return cls(
            codigo=str(data["codigo"]),
            nombre_completo=str(data["nombre_completo"]),
            edad=int(data["edad"]),
            semestre=int(data["semestre"]),
            correo=str(data["correo"]),
            programa=str(data["programa"]),
            fecha_registro=datetime.fromisoformat(
                str(data["fecha_registro"])
            ),
        )
