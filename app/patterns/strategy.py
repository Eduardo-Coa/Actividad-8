"""Patrón Strategy aplicado a GAD-7.

Problema: el sistema necesita exportar los resultados del cuestionario GAD-7
en distintos formatos (JSON, texto plano, CSV) sin modificar la clase que
genera el reporte. Cada formato es una estrategia intercambiable.

Definición formal: Strategy define una familia de algoritmos, los encapsula
en clases separadas y los hace intercambiables. El cliente elige la estrategia
en tiempo de ejecución sin cambiar el código del contexto.
(Gamma et al., Design Patterns, 1994)
"""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import StringIO
from typing import List


# ── Modelo simplificado GAD-7 ─────────────────────────────────────────────────

@dataclass
class ResultadoGAD7:
    codigo_estudiante: str
    respuestas: List[int]        # 7 valores de 0-3
    puntaje_total: int
    nivel_severidad: str


# ── Interfaz Strategy ─────────────────────────────────────────────────────────

class EstrategiaExportacion(ABC):
    """Contrato para todas las estrategias de exportación."""

    @abstractmethod
    def exportar(self, resultados: List[ResultadoGAD7]) -> str:
        """Convierte la lista de resultados al formato objetivo."""


# ── Estrategias concretas ─────────────────────────────────────────────────────

class EstrategiaJSON(EstrategiaExportacion):
    """Exporta los resultados como JSON con sangría de 2 espacios."""

    def exportar(self, resultados: List[ResultadoGAD7]) -> str:
        datos = [
            {
                "codigo_estudiante": r.codigo_estudiante,
                "respuestas": r.respuestas,
                "puntaje_total": r.puntaje_total,
                "nivel_severidad": r.nivel_severidad,
            }
            for r in resultados
        ]
        return json.dumps(datos, ensure_ascii=False, indent=2)


class EstrategiaTextoPlano(EstrategiaExportacion):
    """Exporta los resultados como texto legible para el usuario."""

    def exportar(self, resultados: List[ResultadoGAD7]) -> str:
        lineas = ["=== Resultados GAD-7 ==="]
        for r in resultados:
            lineas.append(
                f"Estudiante: {r.codigo_estudiante} | "
                f"Puntaje: {r.puntaje_total} | "
                f"Nivel: {r.nivel_severidad}"
            )
        return "\n".join(lineas)


class EstrategiaCSV(EstrategiaExportacion):
    """Exporta los resultados en formato CSV."""

    def exportar(self, resultados: List[ResultadoGAD7]) -> str:
        buffer = StringIO(newline="")
        escritor = csv.writer(buffer)
        escritor.writerow(["codigo_estudiante", "puntaje_total", "nivel_severidad"])
        for r in resultados:
            escritor.writerow([r.codigo_estudiante, r.puntaje_total, r.nivel_severidad])
        return buffer.getvalue().strip()


# ── Contexto ──────────────────────────────────────────────────────────────────

class ReporteGAD7:
    """Contexto que delega la exportación a la estrategia configurada.

    El contexto no sabe cómo se exporta; solo sabe que tiene una estrategia.
    """

    def __init__(self, estrategia: EstrategiaExportacion) -> None:
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaExportacion) -> None:
        """Permite cambiar la estrategia en tiempo de ejecución."""
        self._estrategia = estrategia

    def generar(self, resultados: List[ResultadoGAD7]) -> str:
        """Genera el reporte usando la estrategia activa."""
        return self._estrategia.exportar(resultados)
