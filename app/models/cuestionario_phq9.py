"""Entidades de dominio para el cuestionario PHQ-9."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.exceptions import FechaInvalidaError, PuntajeInvalidoError
from app.utils.constantes_negocio import (
    NUM_ITEMS_PHQ9,
    PUNTAJE_MAXIMO_ITEM,
    PUNTAJE_MINIMO_ITEM,
    PUNTAJE_RIESGO_LEVE_PHQ9,
    PUNTAJE_RIESGO_MODERADO_PHQ9,
    PUNTAJE_RIESGO_MODSEVERO_PHQ9,
    PUNTAJE_RIESGO_SEVERO_PHQ9,
)

TEXTOS_ITEMS_PHQ9 = [
    "Poco interés o placer en hacer las cosas",
    "Sentirse decaído, deprimido o sin esperanza",
    "Problemas para dormir o permanecer dormido",
    "Cansancio o poca energía",
    "Poco apetito o comer en exceso",
    "Sentirse mal consigo mismo o que es un fracaso",
    "Problemas para concentrarse en actividades",
    "Moverse o hablar tan lento que otras personas lo notan",
    "Pensamientos de hacerse daño o de que estaría mejor muerto",
]

OPCIONES_RESPUESTA = {
    0: "Nunca",
    1: "Varios días",
    2: "Más de la mitad de los días",
    3: "Casi todos los días",
}


@dataclass
class CuestionarioPHQ9:
    """Cuestionario PHQ-9 aplicado a un estudiante."""

    id: str
    codigo_estudiante: str
    fecha_aplicacion: datetime
    respuestas: List[int] = field(default_factory=list)
    puntaje_total: int = 0
    nivel_severidad: str = ""

    def __post_init__(self) -> None:
        self._validar()
        if self.respuestas:
            self.puntaje_total = self._calcular_puntaje()
            self.nivel_severidad = self._clasificar_severidad()

    def _validar(self) -> None:
        if not self.id or not self.id.strip():
            raise FechaInvalidaError("El ID no puede estar vacío.")
        if not self.codigo_estudiante or not self.codigo_estudiante.strip():
            raise FechaInvalidaError("El código del estudiante no puede estar vacío.")
        if not isinstance(self.fecha_aplicacion, datetime):
            raise FechaInvalidaError("La fecha debe ser un datetime.")
        if self.fecha_aplicacion > datetime.now():
            raise FechaInvalidaError("La fecha no puede ser futura.")
        if self.respuestas:
            if len(self.respuestas) != NUM_ITEMS_PHQ9:
                raise PuntajeInvalidoError(
                    len(self.respuestas), (NUM_ITEMS_PHQ9, NUM_ITEMS_PHQ9)
                )
            for valor in self.respuestas:
                if not (PUNTAJE_MINIMO_ITEM <= valor <= PUNTAJE_MAXIMO_ITEM):
                    raise PuntajeInvalidoError(
                        valor, (PUNTAJE_MINIMO_ITEM, PUNTAJE_MAXIMO_ITEM)
                    )

    def _calcular_puntaje(self) -> int:
        return sum(self.respuestas)

    def _clasificar_severidad(self) -> str:
        if self.puntaje_total >= PUNTAJE_RIESGO_SEVERO_PHQ9:
            return "Severo"
        if self.puntaje_total >= PUNTAJE_RIESGO_MODSEVERO_PHQ9:
            return "Moderadamente severo"
        if self.puntaje_total >= PUNTAJE_RIESGO_MODERADO_PHQ9:
            return "Moderado"
        if self.puntaje_total >= PUNTAJE_RIESGO_LEVE_PHQ9:
            return "Leve"
        return "Mínimo"

    @property
    def es_riesgo_severo(self) -> bool:
        return self.puntaje_total >= PUNTAJE_RIESGO_SEVERO_PHQ9

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo_estudiante": self.codigo_estudiante,
            "fecha_aplicacion": self.fecha_aplicacion.isoformat(),
            "respuestas": self.respuestas,
            "puntaje_total": self.puntaje_total,
            "nivel_severidad": self.nivel_severidad,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> CuestionarioPHQ9:
        return cls(
            id=datos["id"],
            codigo_estudiante=datos["codigo_estudiante"],
            fecha_aplicacion=datetime.fromisoformat(datos["fecha_aplicacion"]),
            respuestas=datos.get("respuestas", []),
        )
