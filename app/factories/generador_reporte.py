"""Patrón Factory Method: crea distintos tipos de reporte PHQ-9."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.utils.constantes_negocio import FORMATO_FECHA_DISPLAY


# ── Productos ─────────────────────────────────────────────────────────────


class Reporte(ABC):
    """Producto abstracto: interfaz común de todos los formatos de reporte."""

    @abstractmethod
    def formatear(self, cuestionarios: List[CuestionarioPHQ9]) -> str:
        """Genera la representación textual del reporte."""


class ReporteTexto(Reporte):
    """Producto concreto: tabla de texto plano alineada en columnas."""

    def formatear(self, cuestionarios: List[CuestionarioPHQ9]) -> str:
        encabezado = (
            f"{'CÓDIGO':<16} {'FECHA':<18} {'PUNTAJE':>8}  SEVERIDAD"
        )
        separador = "-" * 60
        filas = [encabezado, separador]
        for c in cuestionarios:
            fecha = c.fecha_aplicacion.strftime(FORMATO_FECHA_DISPLAY)
            filas.append(
                f"{c.codigo_estudiante:<16} {fecha:<18}"
                f" {c.puntaje_total:>8}  {c.nivel_severidad}"
            )
        return "\n".join(filas)


class ReporteCSV(Reporte):
    """Producto concreto: valores separados por comas (CSV)."""

    def formatear(self, cuestionarios: List[CuestionarioPHQ9]) -> str:
        lineas = [
            "id,codigo_estudiante,fecha_aplicacion,"
            "puntaje_total,nivel_severidad"
        ]
        for c in cuestionarios:
            lineas.append(
                f"{c.id},{c.codigo_estudiante},"
                f"{c.fecha_aplicacion.isoformat()},"
                f"{c.puntaje_total},{c.nivel_severidad}"
            )
        return "\n".join(lineas)


# ── Creadores ─────────────────────────────────────────────────────────────


class GeneradorReporte(ABC):
    """Creador abstracto con el Factory Method crear_reporte().

    El método generar() usa el producto devuelto por crear_reporte(),
    que cada subclase concreta decide qué tipo instanciar.
    """

    def generar(self, cuestionarios: List[CuestionarioPHQ9]) -> str:
        """Genera el reporte usando el producto de la subclase.

        Args:
            cuestionarios: lista de cuestionarios a incluir.

        Returns:
            Cadena con el reporte formateado.
        """
        return self.crear_reporte().formatear(cuestionarios)

    @abstractmethod
    def crear_reporte(self) -> Reporte:
        """Factory Method: la subclase decide qué Reporte crear."""


class GeneradorReporteTexto(GeneradorReporte):
    """Creador concreto que produce reportes en texto plano."""

    def crear_reporte(self) -> Reporte:
        return ReporteTexto()


class GeneradorReporteCSV(GeneradorReporte):
    """Creador concreto que produce reportes en formato CSV."""

    def crear_reporte(self) -> Reporte:
        return ReporteCSV()
